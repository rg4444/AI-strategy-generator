"""One-time bootstrap: convert the data section of pppa.lv sg-app.js
(exported as JSON: {AX, C, T, W}) into the YAML source of truth.

Kept in the repo for provenance. After bootstrap the JSON is not needed;
data/*.yaml is edited directly and dist/ is rebuilt with tools/build.py.

Usage: python3 tools/bootstrap_from_js.py sg-data.json
"""
import json, os, sys
from common import DATA, dump_yaml

GROUPS = {
    "A": {"kind": "par", "scored": True,
          "name": {"lv": "Stratēģiskie lēmumi", "en": "Strategic decisions"},
          "description": {"lv": "Ko valsts (vai organizācija) apņemas darīt.",
                          "en": "What the country (or organisation) commits to."}},
    "B": {"kind": "ex", "scored": False,
          "name": {"lv": "Forma un pārvaldība", "en": "Form and governance"},
          "description": {"lv": "Kāda veida dokuments tas ir.",
                          "en": "What kind of artefact the document is."}},
}


def check_keys(obj, allowed, where):
    extra = set(obj) - set(allowed)
    if extra:
        sys.exit(f"unexpected keys {extra} in {where}")


def conv_axis(a):
    check_keys(a, {"grp", "t", "id", "n", "m", "o"}, f"axis {a['id']}")
    assert GROUPS[a["grp"]]["kind"] == a["t"], a["id"]
    opts = []
    for o in a["o"]:
        check_keys(o, {"k", "v", "l", "who", "g", "f"}, f"option {a['id']}.{o['k']}")
        item = {"key": o["k"]}
        if "v" in o:
            item["value"] = o["v"]
        # an option without a value scores 0 (the `reg` axis is descriptive only)
        item.update({"label": o["l"], "chosen_by": o.get("who", ""), "gives": o["g"], "forecloses": o["f"]})
        opts.append(item)
    return {"id": a["id"], "group": a["grp"], "name": a["n"], "method": a["m"], "options": opts}


def conv_strategy(c):
    check_keys(c, {"id", "lv", "n", "d", "note", "t", "c", "s", "q"}, f"strategy {c['id']}")
    t = c["t"]
    check_keys(t, {"i", "v", "o", "p"}, f"{c['id']}.t")
    check_keys(t["i"], {"s", "x", "src"}, f"{c['id']}.t.i")
    check_keys(t["v"], {"q", "nt"}, f"{c['id']}.t.v")
    out = {"id": c["id"], "name": c["n"]}
    if c.get("lv"):
        out["latvian"] = True
    out["documents"] = c["d"]
    if "note" in c:
        out["note"] = c["note"]
    interest = {"status": t["i"]["s"], "text": t["i"]["x"]}
    if t["i"].get("src"):
        interest["source"] = t["i"]["src"]
    vision = {"quote": t["v"].get("q", "") or ""}
    if t["v"].get("nt"):
        vision["note"] = t["v"]["nt"]
    objs = []
    for o in t["o"]:
        check_keys(o, {"n", "lv", "en"}, f"{c['id']}.t.o")
        item = {"lv": o["lv"], "en": o["en"]}
        if o.get("n"):
            item["numbered"] = True
        objs.append(item)
    out["text"] = {"interest": interest, "vision": vision, "objectives": objs, "position": t["p"]}
    # every axis is present in coding; null = the document decides nothing there
    out["coding"] = {a["id"]: c["c"].get(a["id"]) for a in AXES}
    if c.get("s"):
        out["partial"] = c["s"]
    if c.get("q"):
        axis_order = list(c["c"].keys())
        out["low_confidence"] = sorted(c["q"].keys(), key=axis_order.index)
    return out


AXES = []


def main(src):
    d = json.load(open(src, encoding="utf-8"))
    AXES[:] = d["AX"]
    axes = {"version": 1, "groups": GROUPS, "axes": [conv_axis(a) for a in d["AX"]]}
    dump_yaml(axes, os.path.join(DATA, "axes.yaml"))
    dump_yaml({"version": 1,
               "note": "Default weights for group-A axes (percent points; they need not sum to 100). "
                       "Group-B axes are never weighted.",
               "default": d["W"]}, os.path.join(DATA, "weights.yaml"))
    dump_yaml({"version": 1, "strings": d["T"]}, os.path.join(DATA, "ui-strings.yaml"))
    order = []
    for c in d["C"]:
        s = conv_strategy(c)
        order.append(s["id"])
        dump_yaml(s, os.path.join(DATA, "strategies", f"{s['id']}.yaml"))
    dump_yaml({"note": "Display order of strategies in the generator (a divider is drawn after the 17th entry).",
               "order": order}, os.path.join(DATA, "strategies", "_order.yaml"))
    print("axes", len(axes["axes"]), "strategies", len(order))


if __name__ == "__main__":
    main(sys.argv[1])
