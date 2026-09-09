"""Build all generated artefacts from the YAML source of truth.

    python3 tools/build.py            # writes dist/sg-data.js, decision/scoring.dmn, docs/axes.md
    python3 tools/build.py --check    # build into a temp dir and diff against committed files

dist/sg-data.js is the data half of the pppa.lv generator: it declares the
same four top-level constants (AX, C, T, W) that sg-app.js used to embed.
"""
import argparse, json, os, re, sys, tempfile, filecmp
from xml.sax.saxutils import escape
from common import ROOT, load_all, axis_index

sys.path.insert(0, os.path.dirname(__file__))
from score import validate  # noqa: E402
import strategy_doc as SD  # noqa: E402
import xsd_to_jsonschema as X2J  # noqa: E402
import xml.etree.ElementTree as ET  # noqa: E402
import datetime as _dt  # noqa: E402
import subprocess  # noqa: E402


# ---------------------------------------------------------------- JS data ---
def to_js_axis(a):
    kind = "par" if a["group"] == "A" else "ex"
    return {"grp": a["group"], "t": kind, "id": a["id"], "n": a["name"], "m": a["method"],
            "o": [{"k": o["key"], **({"v": o["value"]} if "value" in o else {}), "l": o["label"],
                   "who": o.get("chosen_by", ""), "g": o["gives"], "f": o["forecloses"]} for o in a["options"]]}


def to_js_strategy(s):
    t = s["text"]
    i = {"s": t["interest"]["status"], "x": t["interest"]["text"]}
    if t["interest"].get("source"):
        i["src"] = t["interest"]["source"]
    v = {"q": t["vision"].get("quote", "")}
    if t["vision"].get("note"):
        v["nt"] = t["vision"]["note"]
    o = []
    for ob in t["objectives"]:
        item = {"n": 1 if ob.get("numbered") else 0, "lv": ob["lv"], "en": ob["en"]}
        o.append(item)
    out = {"id": s["id"]}
    if s.get("latvian"):
        out["lv"] = 1
    out["n"] = s["name"]
    out["d"] = s["documents"]
    if s.get("note"):
        out["note"] = s["note"]
    out["t"] = {"i": i, "v": v, "o": o, "p": t["position"]}
    out["c"] = s["coding"]
    if s.get("partial"):
        out["s"] = s["partial"]
    if s.get("low_confidence"):
        out["q"] = {k: 1 for k in s["low_confidence"]}
    return out


def build_js(axes, weights, ui, strategies):
    js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    lines = [
        '"use strict";',
        "/* GENERATED FILE — do not edit. Source: data/*.yaml in",
        "   https://github.com/rg4444/AI-strategy-generator (tools/build.py).",
        "   Load this script before sg-app.js. */",
        "const AX=" + js([to_js_axis(a) for a in axes["axes"]]) + ";",
        "const C=" + js([to_js_strategy(s) for s in strategies]) + ";",
        "const T=" + js(ui["strings"]) + ";",
        "const W=" + js(weights["default"]) + ";",
        "",
    ]
    return "\n".join(lines)


# -------------------------------------------------------------------- DMN ---
DMN_NS = ('xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" '
          'xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/" '
          'xmlns:dc="http://www.omg.org/spec/DMN/20180521/DC/" '
          'xmlns:feel="https://www.omg.org/spec/DMN/20191111/FEEL/"')


def build_dmn(axes, weights):
    """One COLLECT/MAX decision table per axis, plus the weighted overall.

    Inputs per axis: `primary` (the coded option key or null) and one
    `partial_<key>` number (0–5) per option. A row fires either because the
    option is the primary choice (full value) or because it carries a partial
    score (value scaled by partial/5). MAX aggregation picks the best.
    """
    A = [a for a in axes["axes"] if axes["groups"][a["group"]]["scored"]]
    out = [f'<?xml version="1.0" encoding="UTF-8"?>',
           f'<definitions {DMN_NS} id="aiStrategyScoring" name="AI strategy decision-axis scoring" '
           f'namespace="https://github.com/rg4444/AI-strategy-generator">',
           '  <!-- GENERATED from data/axes.yaml and data/weights.yaml by tools/build.py. -->',
           '  <inputData id="in_primary" name="primary"><variable id="v_primary" name="primary" typeRef="string"/></inputData>']
    for a in axes["axes"]:
        aid = a["id"]
        for o in a["options"]:
            k = o["key"]
            out.append(f'  <inputData id="in_partial_{aid}_{k}" name="partial_{aid}_{k}">'
                       f'<variable id="v_partial_{aid}_{k}" name="partial_{aid}_{k}" typeRef="number"/></inputData>')
    for a in axes["axes"]:
        aid = a["id"]
        name = escape(a["name"]["en"])
        out.append(f'  <decision id="score_{aid}" name="Axis score: {name}">')
        out.append(f'    <description>{escape(a["method"]["en"])}</description>')
        out.append(f'    <informationRequirement id="ir_{aid}_p"><requiredInput href="#in_primary"/></informationRequirement>')
        for o in a["options"]:
            out.append(f'    <informationRequirement id="ir_{aid}_{o["key"]}"><requiredInput href="#in_partial_{aid}_{o["key"]}"/></informationRequirement>')
        out.append(f'    <decisionTable id="dt_{aid}" hitPolicy="COLLECT" aggregation="MAX">')
        out.append(f'      <input id="i_{aid}_primary" label="primary option (coding.{aid})"><inputExpression id="ie_{aid}_p" typeRef="string"><text>primary</text></inputExpression></input>')
        for o in a["options"]:
            out.append(f'      <input id="i_{aid}_{o["key"]}" label="partial score for {escape(o["key"])} (0-5)">'
                       f'<inputExpression id="ie_{aid}_{o["key"]}" typeRef="number"><text>partial_{aid}_{o["key"]}</text></inputExpression></input>')
        out.append(f'      <output id="o_{aid}" label="axis score (0-5)" name="score" typeRef="number"/>')
        n = len(a["options"])
        for idx, o in enumerate(a["options"]):
            k, v = o["key"], o.get("value", 0)
            lab = escape(o["label"]["en"])
            # rule 1: primary choice -> full option value
            cells = [f'<inputEntry id="r{aid}_{k}_p_0"><text>"{k}"</text></inputEntry>']
            cells += [f'<inputEntry id="r{aid}_{k}_p_{j+1}"><text>-</text></inputEntry>' for j in range(n)]
            out.append(f'      <rule id="rule_{aid}_{k}_primary"><description>{lab}: primary</description>' +
                       "".join(cells) + f'<outputEntry id="oe_{aid}_{k}_p"><text>{v}</text></outputEntry></rule>')
            # rule 2: partial score -> value scaled by partial/5
            cells = [f'<inputEntry id="r{aid}_{k}_s_0"><text>-</text></inputEntry>']
            for j, oo in enumerate(a["options"]):
                cond = "&gt; 0" if oo["key"] == k else "-"
                cells.append(f'<inputEntry id="r{aid}_{k}_s_{j+1}"><text>{cond}</text></inputEntry>')
            out.append(f'      <rule id="rule_{aid}_{k}_partial"><description>{lab}: partial</description>' +
                       "".join(cells) + f'<outputEntry id="oe_{aid}_{k}_s"><text>{v} * partial_{aid}_{k} / 5</text></outputEntry></rule>')
        # rule 0: nothing coded -> 0
        cells = [f'<inputEntry id="r{aid}_none_0"><text>-</text></inputEntry>'] + \
                [f'<inputEntry id="r{aid}_none_{j+1}"><text>-</text></inputEntry>' for j in range(n)]
        out.append(f'      <rule id="rule_{aid}_undecided"><description>undecided / no partials</description>' +
                   "".join(cells) + f'<outputEntry id="oe_{aid}_none"><text>0</text></outputEntry></rule>')
        out.append('    </decisionTable>')
        out.append('  </decision>')
    # overall
    W = weights["default"]
    out.append('  <decision id="overall" name="Weighted overall score (group A only)">')
    out.append('    <description>Weighted mean of the group-A axis scores. Weights are percent points and need not sum to 100; '
               'group-B axes (form and governance) are displayed but never enter the total.</description>')
    for a in A:
        out.append(f'    <informationRequirement id="ir_overall_{a["id"]}"><requiredDecision href="#score_{a["id"]}"/></informationRequirement>')
    terms = " + ".join(f"({W[a['id']]} * score_{a['id']})" for a in A)
    denom = " + ".join(str(W[a["id"]]) for a in A)
    out.append(f'    <literalExpression id="le_overall"><text>if ({denom}) = 0 then null else ({terms}) / ({denom})</text></literalExpression>')
    out.append('  </decision>')
    out.append('</definitions>')
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------- docs ---
def build_docs(axes, weights, strategies):
    W = weights["default"]
    L = ["# Decision axes — reference", "",
         "Generated from `data/axes.yaml` by `tools/build.py`. Do not edit by hand.", ""]
    for gid, g in axes["groups"].items():
        L += [f"## Group {gid} — {g['name']['en']} ({'scored, weighted' if g['scored'] else 'shown, not weighted'})", "",
              g["description"]["en"], ""]
        for a in axes["axes"]:
            if a["group"] != gid:
                continue
            w = f" · default weight {W[a['id']]}" if a["id"] in W else ""
            L += [f"### `{a['id']}` — {a['name']['en']} / {a['name']['lv']}{w}", "", a["method"]["en"], "",
                  "| key | value | option | chosen by | gives | forecloses |", "|---|---|---|---|---|---|"]
            for o in a["options"]:
                L.append(f"| `{o['key']}` | {o.get('value', '–')} | {o['label']['en']} | {o.get('chosen_by','')} | "
                         f"{o['gives']['en']} | {o['forecloses']['en']} |")
            L.append("")
    L += ["## Coded strategies", "", "| id | name | documents |", "|---|---|---|"]
    for s in strategies:
        L.append(f"| `{s['id']}` | {s['name']['en']} | {s['documents']} |")
    L.append("")
    return "\n".join(L)


# ----------------------------------------------------------------- bundle ---
def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return ""


def build_bundle(axes, weights):
    """dist/axes-bundle.json — everything a consumer needs to render, code and score."""
    return {
        "bundle": "ai-strategy-axes",
        "version": str(axes["version"]),
        "scoring_version": SD.SCORING_VERSION,
        "schema_version": SD.SCHEMA_VERSION,
        "source": SD.AXES_SOURCE + ("@" + git_commit() if git_commit() else ""),
        "generated_at": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0, tzinfo=None).isoformat() + "Z",
        "groups": axes["groups"],
        "axes": axes["axes"],
        "default_weights": weights["default"],
    }


def build_reference(bundle, strategies):
    docs = [SD.from_yaml_strategy(s, bundle, kind="national") for s in strategies]
    for d in docs:
        errs = SD.validate(d, bundle)
        if errs:
            sys.exit(f"reference strategy {d['id']} invalid: {errs}")
        # XML round trip must be lossless for the fields the XSD carries
        back = SD.from_xml(SD.to_xml(d))
        for k in ("id", "kind", "axesVersion", "coding", "weights"):
            if back.get(k) != d.get(k):
                sys.exit(f"XML round-trip mismatch for {d['id']} on {k}")
    return docs


def build_json_schema():
    xsd = os.path.join(ROOT, "schema", "ai-strategy.xsd")
    return json.dumps(X2J.Conv(ET.parse(xsd).getroot()).run(), ensure_ascii=False, indent=2) + "\n"


# ------------------------------------------------------------------- main ---
def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", default=ROOT)
    args = ap.parse_args()
    axes, weights, ui, strategies = load_all()
    validate(axes, weights, strategies)
    bundle = build_bundle(axes, weights)
    reference = build_reference(bundle, strategies)
    bundle_json = json.dumps(bundle, ensure_ascii=False, indent=1) + "\n"
    targets = {
        "dist/sg-data.js": build_js(axes, weights, ui, strategies),
        "dist/axes-bundle.json": bundle_json,
        "dist/reference-strategies.json": json.dumps(reference, ensure_ascii=False, indent=1) + "\n",
        "schema/ai-strategy.schema.json": build_json_schema(),
        "decision/scoring.dmn": build_dmn(axes, weights),
        "docs/axes.md": build_docs(axes, weights, strategies),
    }
    if args.check:
        tmp = tempfile.mkdtemp()
        bad = []
        for rel, text in targets.items():
            write(os.path.join(tmp, rel), text)
            if rel in ("dist/axes-bundle.json", "dist/reference-strategies.json"):
                strip = lambda p: re.sub(r'"(generated_at|source|createdAt|updatedAt|axesSource)": "[^"]*"', "", open(p, encoding="utf-8").read())
                if strip(os.path.join(tmp, rel)) != strip(os.path.join(ROOT, rel)):
                    bad.append(rel)
            elif not filecmp.cmp(os.path.join(tmp, rel), os.path.join(ROOT, rel), shallow=False):
                bad.append(rel)
        if bad:
            sys.exit("out of date: " + ", ".join(bad) + "  (run tools/build.py)")
        print("generated files are up to date")
        return
    for rel, text in targets.items():
        write(os.path.join(args.out, rel), text)
        print("wrote", rel)


if __name__ == "__main__":
    main()
