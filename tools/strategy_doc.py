"""AI strategy document core — the algorithm half of the method, in one file.

This module is the single implementation of:
  * scoring (option / axis / overall)      — see METHOD.md §4, decision/scoring.dmn
  * the JSON form of a strategy document   — schema/ai-strategy.schema.json
  * its XML form                            — schema/ai-strategy.xsd (urn:pppa:ai-strategy:1.0)
  * structural validation against an axes bundle (dist/axes-bundle.json)
  * conversion from the repo's YAML strategy files (data/strategies/*.yaml)

It has no dependencies beyond the standard library so that consumers
(pppa.lv tooling, AI Register) can vendor it verbatim. Consumers must not
fork the scoring: if the method changes, this file changes here first.

SCORING_VERSION is written into every computed <score scoringVersion=".."/>.
"""
from __future__ import annotations
import datetime as _dt
import json
import re
import uuid
import xml.etree.ElementTree as ET

SCORING_VERSION = "1.0"
SCHEMA_VERSION = "1.1"
SCHEMA_VERSIONS = ("1.0", "1.1")
XSD_URL = "https://raw.githubusercontent.com/rg4444/AI-strategy-generator/main/schema/ai-strategy.xsd"
XMLNS = "urn:pppa:ai-strategy:1.0"
AXES_SOURCE = "https://github.com/rg4444/AI-strategy-generator"


# ------------------------------------------------------------------ bundle --
def axes_index(bundle: dict) -> dict:
    return {a["id"]: a for a in bundle["axes"]}


def option_index(axis: dict) -> dict:
    return {o["key"]: o for o in axis["options"]}


def scored_axes(bundle: dict) -> list:
    return [a for a in bundle["axes"] if bundle["groups"][a["group"]]["scored"]]


def axes_for_kind(bundle: dict, kind: str) -> list:
    """Axes with the wording for `kind` applied (organisation -> org overrides).
    Scoring never depends on this; only rendering does."""
    if kind != "organisation":
        return bundle["axes"]
    out = []
    for a in bundle["axes"]:
        o = a.get("org") or {}
        a2 = dict(a)
        a2["name"] = o.get("name", a["name"]); a2["method"] = o.get("method", a["method"])
        a2["options"] = [{**op, **({k: v for k, v in (o.get("options", {}).get(op["key"]) or {}).items()}), "chosen_by": ""}
                         for op in a["options"]]
        out.append(a2)
    return out


def groups_for_kind(bundle: dict, kind: str) -> dict:
    if kind != "organisation":
        return bundle["groups"]
    return {gid: {**g, **(g.get("org") or {})} for gid, g in bundle["groups"].items()}


# ----------------------------------------------------------------- scoring --
def coding_map(doc: dict) -> dict:
    """{axis: {"option": key|None, "partials": {key: score}}} from the document form."""
    out = {}
    for c in doc.get("coding", []):
        out[c["axis"]] = {"option": c.get("option"),
                          "partials": {p["option"]: p["score"] for p in c.get("partials", [])}}
    return out


def option_score(cm: dict, axis_id: str, key: str) -> float:
    c = cm.get(axis_id) or {}
    if c.get("option") == key:
        return 5
    return c.get("partials", {}).get(key, 0)


def axis_score(cm: dict, axis: dict) -> float:
    return max([0] + [o.get("value", 0) * option_score(cm, axis["id"], o["key"]) / 5 for o in axis["options"]])


def weights_map(doc: dict, bundle: dict) -> dict:
    w = dict(bundle.get("default_weights", {}))
    for e in doc.get("weights", []) or []:
        w[e["axis"]] = e["weight"]
    return w


def compute_score(doc: dict, bundle: dict) -> dict:
    cm = coding_map(doc)
    W = weights_map(doc, bundle)
    axes = [{"axis": a["id"], "value": round(axis_score(cm, a), 2)} for a in bundle["axes"]]
    A = scored_axes(bundle)
    tw = sum(W.get(a["id"], 0) for a in A)
    overall = None if tw == 0 else round(sum(W.get(a["id"], 0) * axis_score(cm, a) for a in A) / tw, 2)
    out = {"axes": axes, "scoringVersion": SCORING_VERSION}
    if overall is not None:
        out["overall"] = overall
    return out


# -------------------------------------------------------------- validation --
def validate(doc: dict, bundle: dict) -> list:
    """Structural checks the JSON Schema cannot express (keys must exist in the bundle).
    Returns a list of error strings; empty means valid."""
    errs = []
    ai = axes_index(bundle)
    if doc.get("schemaVersion") not in SCHEMA_VERSIONS:
        errs.append(f"schemaVersion must be one of {SCHEMA_VERSIONS}")
    for n in doc.get("narratives", []) or []:
        if not re.fullmatch(r"[a-z]{2}", n.get("lang", "")):
            errs.append("narrative.lang must be a two-letter code")
    if doc.get("kind") not in ("national", "organisation"):
        errs.append("kind must be national|organisation")
    seen = set()
    for c in doc.get("coding", []):
        aid = c.get("axis")
        if aid not in ai:
            errs.append(f"unknown axis {aid}"); continue
        if aid in seen:
            errs.append(f"axis {aid} coded twice")
        seen.add(aid)
        oi = option_index(ai[aid])
        if c.get("option") is not None and c["option"] not in oi:
            errs.append(f"axis {aid}: unknown option {c['option']}")
        for p in c.get("partials", []) or []:
            if p.get("option") not in oi:
                errs.append(f"axis {aid}: partial on unknown option {p.get('option')}")
            elif p["option"] == c.get("option"):
                errs.append(f"axis {aid}: partial duplicates the primary option")
            if not (1 <= int(p.get("score", 0)) <= 4):
                errs.append(f"axis {aid}: partial score must be 1–4")
    # An axis missing from the document reads as undecided. It is an error only when the
    # document claims the bundle's own axes version (a fresh document must list every axis);
    # documents coded against an older axes version stay valid after an axis is added.
    if str(doc.get("axesVersion", "")) == str(bundle.get("version", "")):
        for aid in ai:
            if aid not in seen:
                errs.append(f"axis {aid} not coded (use no option for undecided)")
    for e in doc.get("weights", []) or []:
        if e.get("axis") not in ai or not bundle["groups"][ai[e["axis"]]["group"]]["scored"]:
            errs.append(f"weight on non-scored axis {e.get('axis')}")
    t = doc.get("text") or {}
    if (t.get("interest") or {}).get("status") not in ("yes", "part", "no"):
        errs.append("text.interest.status must be yes|part|no")
    return errs


# -------------------------------------------------------------- documents --
def new_document(bundle: dict, kind: str = "organisation", title: str = "", subject_name=None,
                 identifier=None, country: str = "", sector: str = "", doc_id: str | None = None) -> dict:
    now = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0, tzinfo=None).isoformat() + "Z"
    d = {
        "id": doc_id or str(uuid.uuid4()),
        "schemaVersion": SCHEMA_VERSION,
        "kind": kind,
        "status": "draft",
        "version": 1,
        "axesVersion": bundle["version"],
        "axesSource": bundle.get("source", AXES_SOURCE),
        "createdAt": now, "updatedAt": now,
        "title": title,
        "subject": {"name": subject_name or {"lv": "", "en": ""}},
        "sources": [],
        "text": {"interest": {"status": "no", "text": {"lv": "", "en": ""}},
                 "vision": {"quote": ""},
                 "objectives": [],
                 "position": {"lv": "", "en": ""}},
        "coding": [{"axis": a["id"], "lowConfidence": False} for a in bundle["axes"]],
        "weights": [],
    }
    if identifier:
        d["subject"]["identifier"] = identifier
    if country:
        d["subject"]["country"] = country
    if sector:
        d["subject"]["sector"] = sector
    return d


def from_yaml_strategy(s: dict, bundle: dict, kind: str = "national") -> dict:
    """Repo data/strategies/<ID>.yaml -> document form."""
    d = new_document(bundle, kind=kind, title=s["name"].get("en", ""), subject_name=s["name"],
                     identifier={"kind": "country" if len(s["id"]) == 2 else "other", "value": s["id"]},
                     doc_id="urn:pppa:ai-strategy:ref:" + s["id"].lower())
    d["status"] = "final"
    d["sources"] = [{"title": s.get("documents", "")}]
    t = s["text"]
    d["text"] = {
        "interest": {"status": t["interest"]["status"], "text": t["interest"]["text"],
                     **({"source": t["interest"]["source"]} if t["interest"].get("source") else {})},
        "vision": {"quote": t["vision"].get("quote", "") or "",
                   **({"note": t["vision"]["note"]} if t["vision"].get("note") else {})},
        "objectives": [{"lv": o["lv"], "en": o["en"], "numbered": bool(o.get("numbered"))} for o in t["objectives"]],
        "position": t["position"],
    }
    lc = set(s.get("low_confidence") or [])
    partial = s.get("partial") or {}
    d["coding"] = []
    for a in bundle["axes"]:
        aid = a["id"]
        c = {"axis": aid, "lowConfidence": aid in lc}
        if s["coding"].get(aid) is not None:
            c["option"] = s["coding"][aid]
        ps = [{"option": k, "score": int(v)} for k, v in (partial.get(aid) or {}).items()
              if k in option_index(a) and k != c.get("option") and 1 <= int(v) <= 4]
        if ps:
            c["partials"] = ps
        d["coding"].append(c)
    d["score"] = compute_score(d, bundle)
    return d


# -------------------------------------------------------------------- XML --
def _text_el(parent, tag, text):
    el = ET.SubElement(parent, tag)
    for lang, val in (text or {}).items():
        if val:
            t = ET.SubElement(el, "t", lang=lang)
            t.text = val
    return el


def to_xml(doc: dict) -> bytes:
    ET.register_namespace("", XMLNS)
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root = ET.Element(f"{{{XMLNS}}}aiStrategy")
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", XMLNS + " " + XSD_URL)
    for k in ("id", "schemaVersion", "kind", "status", "version", "axesVersion", "axesSource",
              "createdAt", "updatedAt", "title"):
        if doc.get(k) not in (None, ""):
            root.set(k, str(doc[k]))
    subj = ET.SubElement(root, "subject")
    _text_el(subj, "name", doc["subject"].get("name"))
    if doc["subject"].get("identifier"):
        idn = ET.SubElement(subj, "identifier", kind=doc["subject"]["identifier"]["kind"])
        idn.text = doc["subject"]["identifier"]["value"]
    for k in ("country", "sector"):
        if doc["subject"].get(k):
            ET.SubElement(subj, k).text = doc["subject"][k]
    if doc.get("sources"):
        srcs = ET.SubElement(root, "sources")
        for s in doc["sources"]:
            se = ET.SubElement(srcs, "source")
            ET.SubElement(se, "title").text = s.get("title", "")
            for k in ("year", "url"):
                if s.get(k):
                    ET.SubElement(se, k).text = s[k]
    t = doc["text"]
    te = ET.SubElement(root, "text")
    ie = ET.SubElement(te, "interest", status=t["interest"]["status"])
    _text_el(ie, "text", t["interest"].get("text"))
    if t["interest"].get("source"):
        ET.SubElement(ie, "source").text = t["interest"]["source"]
    ve = ET.SubElement(te, "vision")
    if t["vision"].get("quote"):
        ET.SubElement(ve, "quote").text = t["vision"]["quote"]
    if t["vision"].get("note"):
        _text_el(ve, "note", t["vision"]["note"])
    oe = ET.SubElement(te, "objectives")
    for o in t.get("objectives", []):
        ob = _text_el(oe, "objective", {k: v for k, v in o.items() if k != "numbered"})
        if o.get("numbered"):
            ob.set("numbered", "true")
    _text_el(te, "position", t.get("position"))
    ce = ET.SubElement(root, "coding")
    for c in doc["coding"]:
        ax = ET.SubElement(ce, "axis", axis=c["axis"])
        if c.get("option"):
            ax.set("option", c["option"])
        if c.get("lowConfidence"):
            ax.set("lowConfidence", "true")
        for p in c.get("partials", []) or []:
            ET.SubElement(ax, "partial", option=p["option"], score=str(p["score"]))
        if c.get("rationale"):
            _text_el(ax, "rationale", c["rationale"])
    if doc.get("weights"):
        we = ET.SubElement(root, "weights")
        for w in doc["weights"]:
            ET.SubElement(we, "axis", axis=w["axis"], weight=str(w["weight"]))
    if doc.get("score"):
        sc = ET.SubElement(root, "score")
        if doc["score"].get("overall") is not None:
            sc.set("overall", str(doc["score"]["overall"]))
        if doc["score"].get("scoringVersion"):
            sc.set("scoringVersion", doc["score"]["scoringVersion"])
        for a in doc["score"].get("axes", []):
            ET.SubElement(sc, "axis", axis=a["axis"], value=str(a["value"]))
    for n in doc.get("narratives", []) or []:
        ne = ET.SubElement(root, "narrative", lang=n["lang"])
        for k in ("generatedAt", "model", "docVersion"):
            if n.get(k) not in (None, ""):
                ne.set(k, str(n[k]))
        if n.get("title"):
            ET.SubElement(ne, "title").text = n["title"]
        if n.get("summary"):
            ET.SubElement(ne, "summary").text = n["summary"]
        for sec in n.get("sections", []) or []:
            se = ET.SubElement(ne, "section")
            ET.SubElement(se, "heading").text = sec.get("heading", "")
            for p in sec.get("paragraphs", []) or []:
                ET.SubElement(se, "paragraph").text = p
        for a in n.get("assumptions", []) or []:
            ET.SubElement(ne, "assumption").text = a
        for q in n.get("openQuestions", []) or []:
            ET.SubElement(ne, "openQuestion").text = q
    ET.indent(root, space="  ")
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="utf-8")


def _text_from(el):
    return {t.get("lang"): (t.text or "") for t in el.findall(f"{{{XMLNS}}}t")} if el is not None else {}


def from_xml(data: bytes) -> dict:
    root = ET.fromstring(data)
    N = f"{{{XMLNS}}}"
    d = {k: root.get(k) for k in ("id", "schemaVersion", "kind", "status", "axesVersion", "axesSource",
                                  "createdAt", "updatedAt", "title") if root.get(k) is not None}
    d["version"] = int(root.get("version", "1"))
    subj = root.find(N + "subject")
    d["subject"] = {"name": _text_from(subj.find(N + "name"))}
    idn = subj.find(N + "identifier")
    if idn is not None:
        d["subject"]["identifier"] = {"kind": idn.get("kind"), "value": idn.text or ""}
    for k in ("country", "sector"):
        e = subj.find(N + k)
        if e is not None:
            d["subject"][k] = e.text or ""
    d["sources"] = [{"title": s.findtext(N + "title", ""), **{k: s.findtext(N + k) for k in ("year", "url") if s.find(N + k) is not None}}
                    for s in root.findall(N + "sources/" + N + "source")]
    te = root.find(N + "text")
    ie, ve = te.find(N + "interest"), te.find(N + "vision")
    d["text"] = {
        "interest": {"status": ie.get("status"), "text": _text_from(ie.find(N + "text")),
                     **({"source": ie.findtext(N + "source")} if ie.find(N + "source") is not None else {})},
        "vision": {"quote": ve.findtext(N + "quote", "") or "",
                   **({"note": _text_from(ve.find(N + "note"))} if ve.find(N + "note") is not None else {})},
        "objectives": [{**_text_from(o), "numbered": o.get("numbered") == "true"} for o in te.findall(N + "objectives/" + N + "objective")],
        "position": _text_from(te.find(N + "position")),
    }
    d["coding"] = []
    for ax in root.findall(N + "coding/" + N + "axis"):
        c = {"axis": ax.get("axis"), "lowConfidence": ax.get("lowConfidence") == "true"}
        if ax.get("option"):
            c["option"] = ax.get("option")
        ps = [{"option": p.get("option"), "score": int(p.get("score"))} for p in ax.findall(N + "partial")]
        if ps:
            c["partials"] = ps
        r = ax.find(N + "rationale")
        if r is not None:
            c["rationale"] = _text_from(r)
        d["coding"].append(c)
    d["weights"] = [{"axis": w.get("axis"), "weight": int(w.get("weight"))} for w in root.findall(N + "weights/" + N + "axis")]
    sc = root.find(N + "score")
    if sc is not None:
        d["score"] = {"axes": [{"axis": a.get("axis"), "value": float(a.get("value"))} for a in sc.findall(N + "axis")],
                      **({"overall": float(sc.get("overall"))} if sc.get("overall") else {}),
                      **({"scoringVersion": sc.get("scoringVersion")} if sc.get("scoringVersion") else {})}
    nars = []
    for ne in root.findall(N + "narrative"):
        n = {"lang": ne.get("lang")}
        for k in ("generatedAt", "model"):
            if ne.get(k):
                n[k] = ne.get(k)
        if ne.get("docVersion"):
            n["docVersion"] = int(ne.get("docVersion"))
        if ne.find(N + "title") is not None:
            n["title"] = ne.findtext(N + "title") or ""
        if ne.find(N + "summary") is not None:
            n["summary"] = ne.findtext(N + "summary") or ""
        n["sections"] = [{"heading": se.findtext(N + "heading") or "", "paragraphs": [p.text or "" for p in se.findall(N + "paragraph")]}
                         for se in ne.findall(N + "section")]
        n["assumptions"] = [a.text or "" for a in ne.findall(N + "assumption")]
        n["openQuestions"] = [q.text or "" for q in ne.findall(N + "openQuestion")]
        nars.append(n)
    if nars:
        d["narratives"] = nars
    return d


def to_json(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, indent=2)
