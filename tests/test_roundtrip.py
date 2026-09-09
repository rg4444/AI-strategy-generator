"""Consistency tests.

    python3 tests/test_roundtrip.py [original-sg-data.json]

1. dist/sg-data.js evaluates in node and its scores, computed with the exact
   formula used by pppa.lv sg-app.js, equal tools/score.py.
2. If the original JSON export of sg-app.js is given, the rebuilt data is
   semantically identical to it (flag keys normalised).
"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from common import load_all  # noqa: E402
import score as S  # noqa: E402

JS_CHECK = r"""
const fs=require("fs"),vm=require("vm");
const ctx={};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2],"utf8")+"\nthis.__d={AX,C,T,W};",ctx);
const {AX,C,W}=ctx.__d;
const ax=i=>AX.find(a=>a.id===i);
const SC=(d,aid,k)=>d.c[aid]===k?5:((d.s&&d.s[aid]&&d.s[aid][k])||0);
const axScore=(d,aid)=>Math.max(0,...ax(aid).o.map(o=>(o.v||0)*SC(d,aid,o.k)/5));
const A2=AX.filter(a=>a.grp==="A");
const rows=C.map(d=>{let x=0,w=0;A2.forEach(a=>{x+=(W[a.id]||0)*axScore(d,a.id);w+=(W[a.id]||0)});
 return {id:d.id,axes:Object.fromEntries(AX.map(a=>[a.id,+axScore(d,a.id).toFixed(2)])),overall:+(x/w).toFixed(2)}});
console.log(JSON.stringify({rows,data:ctx.__d}));
"""


def normalise(o):
    """Drop flag keys whose value is falsy so `n:0` and missing `n` compare equal."""
    if isinstance(o, dict):
        return {k: normalise(v) for k, v in o.items()
                if v is not None and not (k in ("n", "lv", "src", "nt", "note", "s", "q", "who", "v") and not v)}
    if isinstance(o, list):
        return [normalise(x) for x in o]
    return o


def main():
    axes, weights, ui, strategies = load_all()
    S.validate(axes, weights, strategies)
    js_path = os.path.join(ROOT, "dist", "sg-data.js")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(JS_CHECK)
    out = subprocess.run(["node", f.name, js_path], capture_output=True, text=True, check=True).stdout
    res = json.loads(out)
    # 1. JS scores == python scores
    py = {s["id"]: {"axes": {a["id"]: round(S.axis_score(s, a), 2) for a in axes["axes"]},
                    "overall": round(S.overall(s, axes, weights["default"]), 2)} for s in strategies}
    for r in res["rows"]:
        assert r["axes"] == py[r["id"]]["axes"], (r["id"], r["axes"], py[r["id"]]["axes"])
        assert abs(r["overall"] - py[r["id"]]["overall"]) < 0.011, (r["id"], r["overall"], py[r["id"]]["overall"])
    print("ok: JS scoring == score.py for", len(res["rows"]), "strategies")
    # 2. optional roundtrip against original export
    if len(sys.argv) > 1:
        orig = json.load(open(sys.argv[1], encoding="utf-8"))
        a, b = normalise(orig), normalise(res["data"])
        for key in ("AX", "C", "T", "W"):
            if a[key] != b[key]:
                # find first difference
                ja, jb = json.dumps(a[key], ensure_ascii=False, sort_keys=True), json.dumps(b[key], ensure_ascii=False, sort_keys=True)
                i = next(i for i in range(min(len(ja), len(jb))) if ja[i] != jb[i])
                sys.exit(f"roundtrip mismatch in {key} near: {ja[max(0,i-80):i+80]!r}\n vs {jb[max(0,i-80):i+80]!r}")
        print("ok: rebuilt data is semantically identical to the original export")


if __name__ == "__main__":
    main()
