# Changelog

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
