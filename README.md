# AI Strategy Decision Axes

A method for comparing AI strategies by the **decisions they take**, not the
themes they cover — 20 decision axes, each with a closed set of options that
state what the option *gives* and what it *forecloses*, a coding procedure,
and a transparent 0–5 scoring with adjustable weights.

Built for benchmarking Latvia's national AI strategy against 19 comparators
(PPPA AI LV Exchange programme, August–September 2026). The method applies
unchanged to any organisation's AI strategy — see [METHOD.md §6](METHOD.md#6-applying-the-method-to-an-organisation).

Live tool (bilingual): [pppa.lv/ai-strategy-generator](https://pppa.lv/ai-strategy-generator) · stores strategies as `urn:pppa:ai-strategy:1.0` documents with versions, XML/JSON export and import

## What is here

| path | what | edit? |
|---|---|---|
| [`METHOD.md`](METHOD.md) | the method: axes, coding rules, scoring, limits, organisational reading | yes |
| `data/axes.yaml` | the 20 axes and their options (bilingual LV/EN) — **source of truth** | yes |
| `data/weights.yaml` | default weights for the 15 scored axes | yes |
| `data/strategies/*.yaml` | one coded strategy per file (17 countries + EU, Latvia 2020, VARAM draft 2026, PPPA proposal) | yes |
| `data/ui-strings.yaml` | interface strings of the generator | yes |
| `data/org-reading.yaml` | organisational reading of the axes (EN primary, LV native); merged into the bundle as `org` | yes |
| [`docs/axes.md`](docs/axes.md) | human-readable reference of every axis and option | generated |
| [`decision/scoring.dmn`](decision/scoring.dmn) | DMN 1.3 decision tables: one per axis (COLLECT/MAX) + weighted overall | generated |
| [`process/strategy-coding.bpmn`](process/strategy-coding.bpmn) | BPMN 2.0 process for coding and reviewing a strategy | yes |
| `dist/sg-data.js` | the data half of the pppa.lv generator (declares `AX`, `C`, `T`, `W`) | generated |
| `dist/axes-bundle.json` | axes + groups + default weights + versions, for any consumer (AI Register fetches this) | generated |
| `dist/reference-strategies.json` | the 20 coded strategies in document form (JSON form of the XSD) | generated |
| [`schema/ai-strategy.xsd`](schema/ai-strategy.xsd) | **canonical strategy document schema** (`urn:pppa:ai-strategy:1.0`), national and organisational alike | yes |
| `schema/ai-strategy.schema.json` | JSON Schema of the same document | generated |
| `tools/strategy_doc.py` | the algorithm module: scoring, JSON⇄XML, validation — vendored verbatim by consumers | yes |
| `tools/xsd_to_jsonschema.py` | XSD → JSON Schema generator | — |
| `tools/build.py` | rebuild everything generated from `data/` | — |
| `tools/score.py` | reference scorer; prints the matrix | — |
| `tools/bootstrap_from_js.py` | one-time import from the original sg-app.js (provenance only) | — |
| `tests/test_roundtrip.py` | JS scoring == Python scoring; optional roundtrip vs original export | — |
| `ci/github-workflow-check.yml` | GitHub Actions workflow (build --check + tests); copy to `.github/workflows/` to enable | — |

## Use

```sh
pip install pyyaml            # the only dependency; node is needed for the tests
python3 tools/score.py        # axis scores and weighted overall for every coded strategy
python3 tools/build.py        # regenerate dist/, decision/, docs/ after editing data/
python3 tests/test_roundtrip.py
```

### Code your own strategy

Copy `data/strategies/_template.yaml` to `data/strategies/<ID>.yaml`, fill the
text layer, set one option key per axis (`null` where nothing is decided),
add it to `data/strategies/_order.yaml`, run `tools/score.py`. Or use the
generator's *Configure* view, which does the same interactively and exports
DOCX.

### Correct a coding

Every `chosen_by` line and every low-confidence flag is an invitation to
check the coding against the source document. Open a pull request against
the strategy file with the passage that supports the change.

## Versioning

`data/axes.yaml` carries `version`. Option keys are stable identifiers; a
change in an option's *value* or the addition of an axis is a minor version
and is noted in [CHANGELOG.md](CHANGELOG.md). Cite the commit you compared with.

## Licence

CC BY 4.0 — Rihards Gailums, PPPA AI LV Exchange programme. See [LICENSE](LICENSE).
