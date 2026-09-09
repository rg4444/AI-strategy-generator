# Changelog

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
