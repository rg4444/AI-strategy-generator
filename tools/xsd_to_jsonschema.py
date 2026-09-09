"""Generate schema/ai-strategy.schema.json from schema/ai-strategy.xsd.

The XSD is canonical. This converter covers the XSD subset the strategy
schema uses and defines the JSON form of a strategy document:

  * an element with a complexType becomes an object; attributes and child
    elements both become properties (attribute names keep their camelCase);
  * maxOccurs="unbounded" becomes an array of the item type, under the
    PLURAL property name (axis -> axes, source -> sources, objective ->
    objectives, partial -> partials);
  * a wrapper element whose whole content is one unbounded child and no
    attributes (sources, coding, weights, objectives) collapses to that array;
  * TextType (a sequence of <t lang=".."/>) becomes an object keyed by
    language code: {"lv": "...", "en": "..."};
  * simpleContent with attributes becomes {"value": <text>, <attr>: ...};
  * xs:boolean/integer/decimal/dateTime/anyURI map to JSON types/formats;
  * enumerations, patterns and min/max facets are carried over.

Usage: python3 tools/xsd_to_jsonschema.py  [in.xsd] [out.json]
"""
import json, os, sys
import xml.etree.ElementTree as ET

XS = "{http://www.w3.org/2001/XMLSchema}"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLURAL = {"axis": "axes", "source": "sources", "objective": "objectives", "partial": "partials",
          "narrative": "narratives", "section": "sections", "paragraph": "paragraphs",
          "assumption": "assumptions", "openQuestion": "openQuestions"}
BUILTIN = {
    "xs:string": {"type": "string"}, "xs:anyURI": {"type": "string", "format": "uri"},
    "xs:boolean": {"type": "boolean"}, "xs:integer": {"type": "integer"},
    "xs:positiveInteger": {"type": "integer", "minimum": 1}, "xs:decimal": {"type": "number"},
    "xs:dateTime": {"type": "string", "format": "date-time"},
}


class Conv:
    def __init__(self, root):
        self.root = root
        self.simple = {n.get("name"): n for n in root.findall(f"{XS}simpleType")}
        self.complex = {n.get("name"): n for n in root.findall(f"{XS}complexType")}
        self.defs = {}

    def doc(self, node):
        d = node.find(f"{XS}annotation/{XS}documentation")
        return d.text.strip() if d is not None and d.text else None

    # ---------------------------------------------------------------- simple
    def simple_schema(self, node):
        r = node.find(f"{XS}restriction")
        s = dict(BUILTIN.get(r.get("base"), {"type": "string"}))
        enums = [e.get("value") for e in r.findall(f"{XS}enumeration")]
        if enums:
            s["enum"] = enums
        for f in r:
            tag = f.tag.replace(XS, "")
            v = f.get("value")
            if tag == "pattern":
                s["pattern"] = "^" + v + "$"
            elif tag == "minInclusive":
                s["minimum"] = float(v) if s["type"] == "number" else int(v)
            elif tag == "maxInclusive":
                s["maximum"] = float(v) if s["type"] == "number" else int(v)
        d = self.doc(node)
        if d:
            s["description"] = d
        return s

    def ref_type(self, tname):
        if tname in BUILTIN:
            return dict(BUILTIN[tname])
        if tname in self.simple:
            self.ensure_def(tname, lambda: self.simple_schema(self.simple[tname]))
        elif tname in self.complex:
            self.ensure_def(tname, lambda: self.complex_schema(self.complex[tname]))
        else:
            raise SystemExit(f"unknown type {tname}")
        return {"$ref": f"#/$defs/{tname}"}

    def ensure_def(self, name, build):
        if name not in self.defs:
            self.defs[name] = None  # cycle guard
            self.defs[name] = build()

    # --------------------------------------------------------------- complex
    def complex_schema(self, node, name=None):
        name = name or node.get("name")
        if name == "TextType":
            s = {"type": "object", "patternProperties": {"^[a-z]{2}$": {"type": "string"}}, "additionalProperties": False}
            d = self.doc(node)
            if d:
                s["description"] = d
            return s
        sc = node.find(f"{XS}simpleContent")
        if sc is not None:
            ext = sc.find(f"{XS}extension")
            props = {"value": self.ref_type(ext.get("base"))}
            req = ["value"]
            self.attrs(ext, props, req)
            return {"type": "object", "properties": props, "required": req, "additionalProperties": False}
        cc = node.find(f"{XS}complexContent")
        if cc is not None:
            ext = cc.find(f"{XS}extension")
            props, req = {}, []
            self.attrs(ext, props, req)
            self.seq(ext, props, req)
            if ext.get("base") == "TextType":
                # language map plus the extension's attributes, in one object
                out = {"type": "object", "properties": props,
                       "patternProperties": {"^[a-z]{2}$": {"type": "string"}}, "additionalProperties": False}
                if req:
                    out["required"] = req
                return out
            base = self.ref_type(ext.get("base"))
            out = {"allOf": [base, {"type": "object", "properties": props}]}
            if req:
                out["allOf"][1]["required"] = req
            return out
        props, req = {}, []
        self.seq(node, props, req)
        self.attrs(node, props, req)
        s = {"type": "object", "properties": props, "additionalProperties": False}
        if req:
            s["required"] = req
        d = self.doc(node)
        if d:
            s["description"] = d
        return s

    def attrs(self, node, props, req):
        for a in node.findall(f"{XS}attribute"):
            s = self.ref_type(a.get("type"))
            if a.get("fixed") is not None:
                s = {"const": a.get("fixed")}
            if a.get("default") is not None:
                s = dict(s)
                dv = a.get("default")
                t = self.resolved_type(a.get("type"))
                s["default"] = {"boolean": dv == "true", "integer": int(dv) if dv.isdigit() else dv}.get(t, dv)
            props[a.get("name")] = s
            if a.get("use") == "required":
                req.append(a.get("name"))

    def resolved_type(self, tname):
        if tname in BUILTIN:
            return BUILTIN[tname]["type"]
        if tname in self.simple:
            return self.simple_schema(self.simple[tname])["type"]
        return "string"

    def seq(self, node, props, req):
        sq = node.find(f"{XS}sequence")
        if sq is None:
            return
        for e in sq.findall(f"{XS}element"):
            nm = e.get("name")
            if e.get("type"):
                item = self.ref_type(e.get("type"))
            else:
                ct = e.find(f"{XS}complexType")
                inner = ct.find(f"{XS}sequence")
                kids = inner.findall(f"{XS}element") if inner is not None else []
                if (len(kids) == 1 and kids[0].get("maxOccurs") == "unbounded"
                        and not ct.findall(f"{XS}attribute")):
                    # wrapper collapses to the array of its single child
                    k = kids[0]
                    kitem = self.ref_type(k.get("type")) if k.get("type") else self.complex_schema(k.find(f"{XS}complexType"), name=k.get("name"))
                    item = {"type": "array", "items": kitem}
                    if k.get("minOccurs", "1") != "0":
                        item["minItems"] = int(k.get("minOccurs", "1"))
                    props[nm] = item
                    if e.get("minOccurs", "1") != "0":
                        req.append(nm)
                    continue
                item = self.complex_schema(ct, name=nm)
            d = self.doc(e)
            if d:
                item = dict(item)
                item["description"] = d
            if e.get("maxOccurs") == "unbounded":
                item = {"type": "array", "items": item}
                if e.get("minOccurs", "1") != "0":
                    item["minItems"] = int(e.get("minOccurs", "1"))
                nm = PLURAL.get(nm, nm)
            props[nm] = item
            if e.get("minOccurs", "1") != "0":
                req.append(nm)

    def run(self):
        root_el = self.root.find(f"{XS}element")
        top = self.ref_type(root_el.get("type"))
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/rg4444/AI-strategy-generator/main/schema/ai-strategy.schema.json",
            "title": "AI strategy document (JSON form of urn:pppa:ai-strategy:1.0)",
            "description": "GENERATED from schema/ai-strategy.xsd by tools/xsd_to_jsonschema.py — do not edit.",
            **top,
            "$defs": self.defs,
        }


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "schema", "ai-strategy.xsd")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "schema", "ai-strategy.schema.json")
    schema = Conv(ET.parse(src).getroot()).run()
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", os.path.relpath(dst, ROOT))


if __name__ == "__main__":
    main()
