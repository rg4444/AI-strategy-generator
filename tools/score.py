"""Reference implementation of the scoring rules (see METHOD.md §5).

    python3 tools/score.py                # matrix of axis scores + weighted overall
    python3 tools/score.py --json         # same as JSON
    python3 tools/score.py --weights my.yaml

This is the executable definition the DMN table and the site JavaScript
must agree with (tests/test_roundtrip.py checks both).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import load_all, load_yaml, axis_index, option_index  # noqa: E402


def option_score(strategy, axis_id, key):
    """5 if `key` is the primary coding on this axis, else the partial score (0–5) or 0."""
    if strategy["coding"].get(axis_id) == key:
        return 5
    return (strategy.get("partial") or {}).get(axis_id, {}).get(key, 0)


def axis_score(strategy, axis):
    """Best option, scaled: max over options of value * option_score / 5."""
    return max([0] + [o.get("value", 0) * option_score(strategy, axis["id"], o["key"]) / 5 for o in axis["options"]])


def overall(strategy, axes, weights):
    A = [a for a in axes["axes"] if axes["groups"][a["group"]]["scored"]]
    tw = sum(weights.get(a["id"], 0) for a in A)
    if tw == 0:
        return None
    return sum(weights.get(a["id"], 0) * axis_score(strategy, a) for a in A) / tw


def validate(axes, weights, strategies):
    ai = axis_index(axes)
    errors, warnings = [], []
    for a in axes["axes"]:
        keys = [o["key"] for o in a["options"]]
        if len(keys) != len(set(keys)):
            errors.append(f"axis {a['id']}: duplicate option keys")
        for o in a["options"]:
            if not (0 <= o.get("value", 0) <= 5):
                errors.append(f"axis {a['id']}.{o['key']}: value out of range")
    for aid in weights["default"]:
        if aid not in ai or not axes["groups"][ai[aid]["group"]]["scored"]:
            errors.append(f"weights: {aid} is not a scored axis")
    for s in strategies:
        for aid, key in s["coding"].items():
            if aid not in ai:
                errors.append(f"{s['id']}: unknown axis {aid}")
            elif key is not None and key not in option_index(ai[aid]):
                errors.append(f"{s['id']}: axis {aid} has unknown option {key}")
        for aid in ai:
            if aid not in s["coding"]:
                errors.append(f"{s['id']}: axis {aid} not coded (use null for undecided)")
        for aid, parts in (s.get("partial") or {}).items():
            for key, v in parts.items():
                if key not in option_index(ai[aid]):
                    # has no effect on the score (only real options are scored); flagged for cleanup
                    warnings.append(f"{s['id']}: partial {aid}.{key} is not an option of {aid} (ignored)")
                if not (0 <= v <= 5):
                    errors.append(f"{s['id']}: partial {aid}.{key} out of range")
        for aid in s.get("low_confidence") or []:
            if aid not in ai:
                errors.append(f"{s['id']}: low_confidence on unknown axis {aid}")
        if s["text"]["interest"]["status"] not in ("yes", "no", "part"):
            errors.append(f"{s['id']}: interest.status must be yes/no/part")
    for w in warnings:
        print("warning:", w, file=sys.stderr)
    if errors:
        sys.exit("validation failed:\n  " + "\n  ".join(errors))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--weights")
    args = ap.parse_args()
    axes, weights, ui, strategies = load_all()
    validate(axes, weights, strategies)
    W = load_yaml(args.weights)["default"] if args.weights else weights["default"]
    rows = []
    for s in strategies:
        rows.append({"id": s["id"], "name": s["name"]["en"],
                     "axes": {a["id"]: round(axis_score(s, a), 2) for a in axes["axes"]},
                     "overall": None if overall(s, axes, W) is None else round(overall(s, axes, W), 2)})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    ids = [a["id"] for a in axes["axes"]]
    print("strategy".ljust(8) + "".join(i[:6].rjust(7) for i in ids) + "  overall")
    for r in rows:
        print(r["id"].ljust(8) + "".join(f"{r['axes'][i]:7.1f}" for i in ids) + f"  {r['overall']:.2f}")


if __name__ == "__main__":
    main()
