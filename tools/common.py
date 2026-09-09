"""Shared loaders for the AI Strategy Decision Axes package.

YAML under data/ is the single source of truth. Everything else
(dist/sg-data.js, decision/scoring.dmn, docs/axes.md) is generated.
"""
from __future__ import annotations
import os, sys
try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml is required: pip install pyyaml")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(obj, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(obj, f, allow_unicode=True, sort_keys=False, width=1000,
                       default_flow_style=False)


def load_all():
    axes = load_yaml(os.path.join(DATA, "axes.yaml"))
    weights = load_yaml(os.path.join(DATA, "weights.yaml"))
    ui = load_yaml(os.path.join(DATA, "ui-strings.yaml"))
    order = load_yaml(os.path.join(DATA, "strategies", "_order.yaml"))["order"]
    strategies = [load_yaml(os.path.join(DATA, "strategies", f"{sid}.yaml")) for sid in order]
    return axes, weights, ui, strategies


def axis_index(axes):
    return {a["id"]: a for a in axes["axes"]}


def option_index(axis):
    return {o["key"]: o for o in axis["options"]}
