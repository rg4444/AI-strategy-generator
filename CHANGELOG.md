# Changelog

## 1.0.0 — 2026-09-09

- First public release. Data imported from the pppa.lv generator (`sg-app.js`)
  as of 2026-09-04: 20 axes (15 scored + 5 form/governance), 95 options,
  20 coded strategies.
- Axis `return` (how return on AI investment is evaluated) present since
  2026-09-04; coded for the PPPA proposal only.
- YAML in `data/` becomes the source of truth; `dist/sg-data.js` is generated
  and deployed to pppa.lv.
- DMN 1.3 scoring tables and BPMN 2.0 coding process added.
