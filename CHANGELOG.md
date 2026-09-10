# Changelog

## 1.4.1 — 2026-09-10 (axes 1.1.1)

- Default weights are now a percentage distribution (sum 100). Scores are unchanged
  (the formula normalises); consumers rebalance the other group-A weights proportionally
  when one is edited.
- Reference "PPPA priekšlikums" renamed "Latvija — PPPA projekts" / "Latvia — PPPA draft".
- UI strings: tab "Nacionālās stratēģijas", per-view explanatory hints, matrix note, name
  field labels, weights legend.

## 1.4.0 — 2026-09-09 (axes 1.1.0)

- New group-A axis `access` — *Iedzīvotāju piekļuve MI / Citizen access to AI* — at
  position 12: who gets general-purpose AI and who pays (market 1 · skills 2 · AI inside
  public services 3 · free access for target groups 4 · universal free access 5). Prompted
  by South Korea's "AI for All" (MSIT, Aug 2026): free, unlimited AI for every citizen,
  ≥50 % on domestic models, state-funded compute and operating costs.
- Organisational reading of the axis (employee access: bring-your-own → licences for
  everyone); default weight 8.
- All 20 references coded on `access` (KR and EE, FI, EU, LV 2020, PPPA at full
  confidence; the rest flagged low-confidence pending a re-read). KR profile updated:
  documents, objective, position; partial leans adopt→plat 4, compute→ppp 3, diff→speed 3.
- PPPA proposal: `services` with a partial lean to `universal` (3).
- axesVersion 1.0.0 → 1.1.0. Documents coded against 1.0.0 remain valid; the new axis
  reads as undecided (0) until coded, so overall scores shift slightly.

## 1.3.0 — 2026-09-09

- Schema 1.1: optional `<narrative lang>` element (title, summary, sections with
  paragraphs, assumptions, open questions; generatedAt/model/docVersion) so the
  readable strategy text generated from a configuration travels with the document
  and survives XML/JSON export and import. Namespace unchanged; `schemaVersion`
  is now `1.0 | 1.1`; 1.0 documents still validate.
- Generated XML carries `xsi:schemaLocation` pointing at the raw GitHub XSD; the
  JSON Schema `$id` is the raw GitHub URL, so both resolve.
- `strategy_doc.py`: narratives in `to_xml`/`from_xml`, `XSD_URL`, `SCHEMA_VERSIONS`.

## 1.2.1 — 2026-09-09

- pppa.lv consumer: one bilingual page `/ai-strategy-generator` (old URLs 301, share links carried over); storage v2 keeps every strategy as a schema document with versions, XML/JSON export and import; PHP scoring verified equal to `strategy_doc.py`. `tools/deploy_pppa.py` now also installs the bundle, reference and schema files.

## 1.2.0 — 2026-09-09

- `data/org-reading.yaml`: the organisational reading of every axis (names,
  methods, option labels, gives/forecloses) as SSOT data; English primary,
  Latvian native. Merged into `dist/axes-bundle.json` as `org` on each axis
  and group. Consumers render by the document's `kind`.
- `strategy_doc.axes_for_kind()` / `groups_for_kind()` helpers.

## 1.1.0 — 2026-09-09

- Canonical strategy document schema `schema/ai-strategy.xsd`
  (`urn:pppa:ai-strategy:1.0`) for national and organisational strategies;
  JSON Schema generated from it.
- `tools/strategy_doc.py`: scoring, JSON⇄XML, validation in one dependency-free
  module for consumers to vendor (AI Register, pppa.lv).
- `dist/axes-bundle.json` and `dist/reference-strategies.json` for consumers.
- `data/axes.yaml` version is now a semver string (1.0.0).

## 1.0.0 — 2026-09-09

- First public release. Data imported from the pppa.lv generator (`sg-app.js`)
  as of 2026-09-04: 20 axes (15 scored + 5 form/governance), 95 options,
  20 coded strategies.
- Axis `return` (how return on AI investment is evaluated) present since
  2026-09-04; coded for the PPPA proposal only.
- YAML in `data/` becomes the source of truth; `dist/sg-data.js` is generated
  and deployed to pppa.lv.
- DMN 1.3 scoring tables and BPMN 2.0 coding process added.
