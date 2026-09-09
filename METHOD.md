# AI Strategy Decision Axes — method

Version 1.0 · September 2026 · Rihards Gailums, for the PPPA AI LV Exchange programme

This document defines the comparison and scoring method behind the PPPA
**AI Strategy Generator** ([pppa.lv/mi-strategijas-generators](https://pppa.lv/mi-strategijas-generators),
[English](https://pppa.lv/en/strategy-generator)). The generator is one
implementation; the method is meant to be applied by anyone, to a national
strategy or to an organisation's, with or without the tool. The data that the
tool displays is the YAML in `data/` of this repository. Nothing in the tool
is not in the data.

## 1. What is being compared

Not what a strategy *says*, but what it *decides*.

Most AI strategies are organised by theme (talent, data, infrastructure,
ethics, adoption). Two documents with identical themes can commit their
authors to entirely different things, and a document can cover every theme
while deciding nothing. The unit of comparison here is therefore the
**decision**: a question every strategy answers, explicitly or by omission,
and where each possible answer excludes the others.

A decision is represented as an **axis** with a closed list of **options**.
A strategy is **coded** by selecting, for every axis, the option the document
commits to. The set of codings is the strategy's *configuration*; two
strategies are compared configuration against configuration.

## 2. The axes

Twenty axes, in two groups. The full list with every option, its value, the
countries that chose it, and what each option gives and forecloses is
generated in [`docs/axes.md`](docs/axes.md) from `data/axes.yaml`.

**Group A — strategic decisions** (15 axes; scored and weighted). What the
country or organisation commits to.

| id | axis | the options |
|---|---|---|
| `frame` | How the state frames AI | Neutral tool · economic opportunity · transformative force · threat of dependency · threat of falling behind · source of risk |
| `diff` | Competitive differentiator | None stated · trust and rights · speed of public deployment · language and culture · compute capacity · standards and trust infrastructure · talent and research · scale of capital · market access |
| `interest` | National interest | Not stated · demographic decline · competitiveness · technological independence · risk of falling behind · public-service sustainability · economic diversification · trust as advantage · language and cultural survival |
| `ambition` | Ambition type | Reputational · capability · material/quantified |
| `fund` | Funding model | Unfunded · earmarked budget line · dedicated fund · PPP vehicle |
| `sourcing` | Model sourcing | Decentralised procurement · central broker · self-hosted open-weight · national frontier model · hybrid (external + own fallback) · bloc co-funding |
| `compute` | Compute | None · national HPC · EuroHPC antenna · sovereign PPP · commercial cloud only |
| `lang` | Language strategy | None · data contribution only · fine-tune · national model · regional consortium |
| `identity` | AI identity provision | None · policy discussion only · person e-identity, nothing for agents · agent identity pilot · national AI agent identity · cross-border verification gateway |
| `knowledge` | Knowledge accumulation | None · document digitisation · machine-readable records and data catalogue · reusable shared components · organisational knowledge base · federated knowledge exchange |
| `adopt` | Adoption mechanism | Voluntary · vouchers · mandates · procurement-led · central platform |
| `meas` | Measurement | None · activity KPIs · outcome KPIs · public delivery tracker |
| `eval` | Evaluation & memory | None · solution catalogue · evaluation function · what-works centre |
| `return` | How return is evaluated | None stated · single ROI · ROAI at 90 days · EVC before signature · three instruments by horizon (EVC → ROAI → ROI) |
| `intl` | International posture | EU follower · bilateral · bloc co-funder · standard-setter |

**Group B — form and governance** (5 axes; displayed, never weighted). What
kind of artefact the document is.

| id | axis | the options |
|---|---|---|
| `doctype` | Document type | Vision · plan with actions · statute · rolling action-plan portfolio |
| `horizon` | Horizon & refresh | None · 10-year · 5-year · 3-year rolling · statutory cycle |
| `decomp` | Decomposition | Enablers only · sectors only · enabler × sector matrix · missions |
| `gov` | Governance locus | Line ministry · central digital agency · head-of-government council · statutory body |
| `reg` | Regulatory posture | EU transposition only · soft law · sandbox-first · statutory framework (descriptive; no values) |

Group B is kept out of the total on purpose: a well-governed vision and a
badly governed plan are both possible, and folding form into substance would
let one hide the other.

### How an axis is written

Every axis has a **method note** stating what is scored and ending with the
same caveat: *a higher value means a clearer decision, not a better one.*
Every option has four fields:

- **value** (0–5): how much of a decision this option represents. "None
  stated" is always 0. An option with no value at all scores 0 as well; the
  `reg` axis is descriptive only and carries no values. The remaining values order the options by how much
  they commit the author, not by how desirable they are. Where two options
  commit equally (e.g. `return`: ROAI and EVC are both 3), they share a value.
- **chosen by**: the coded strategies that took this option, so the reader
  can check the coding against the source.
- **gives**: what the author gains by choosing it.
- **forecloses**: what the author gives up. This is the field that turns a
  list of priorities into a strategy. If an option forecloses nothing, it is
  not a decision and does not belong on an axis.

## 3. Coding a strategy

Coding is a reading exercise with rules (the process is drawn in
[`process/strategy-coding.bpmn`](process/strategy-coding.bpmn)).

1. **Sources.** Only published, citable documents: the strategy, its action
   plan, the statute if there is one, official updates. Speeches and
   interviews may be recorded as the source of a quote but do not on their
   own code an axis.
2. **Text layer first.** Before any axis is coded, record what the document
   itself says: whether it states a national (or organisational) interest
   (`yes` / `part` / `no`, with the passage), its vision sentence verbatim,
   its own list of objectives, and a one-paragraph reading of its position.
   This keeps the coding honest — every option chosen must be traceable to
   this layer or to a cited passage.
3. **One primary option per axis.** The option the document commits to. If
   the document takes no position, the coding is `null`. Null is not a
   criticism; it records that the axis is empty.
4. **Partials.** Where a document leans to a second option without committing
   (Estonia on identity: national-ID anchor as primary, gateway and PID as
   partials), the analyst may give the secondary option a partial score of
   1–4. Partials never outrank the primary.
5. **Low confidence.** Any axis where the coding rests on inference rather
   than text is flagged. Flags are shown in the tool as "?" and travel with
   the data. A flag is not a hedge for a clear coding; it is a request for a
   better source.
6. **Review.** A second reader challenges each primary coding against the
   cited passage. Disagreements are resolved by the text, not by the
   analysts' view of what the country ought to have decided.

## 4. Scoring

The formulas are implemented three times and tested for agreement:
[`tools/score.py`](tools/score.py) (reference), [`decision/scoring.dmn`](decision/scoring.dmn)
(DMN 1.3 decision tables, generated), and the generator's JavaScript.

**Option score.** For strategy *s*, axis *a*, option *k*:

    SC(s, a, k) = 5                     if coding[s][a] == k
                = partial[s][a][k]      if a partial score is recorded
                = 0                     otherwise

**Axis score** (0–5):

    axis(s, a) = max over options k of  value(a, k) × SC(s, a, k) / 5

So a primary coding yields the option's full value; a partial of 3 on an
option worth 4 yields 2.4; an axis coded `null` with no partials yields 0.

**Overall score** (0–5), group A only:

    overall(s) = Σ_a w(a) × axis(s, a)  /  Σ_a w(a)

Default weights are in `data/weights.yaml` (funding 12, national interest 10,
model sourcing 10, differentiator/ambition/adoption/measurement 8, return 6,
identity 6, the rest 5). They are percent points and do not have to sum to
100. The generator lets the reader change them; the method does not claim
these are the right weights, only that they are stated.

**Reading a score.** 0 on an axis means the document does not decide there.
A low overall means a document that leaves most questions open, which is
sometimes deliberate (a vision statement) and sometimes not (a plan without
a funding model). The matrix view in the generator marks zeros in red for
this reason: the pattern of empty cells is usually more informative than
the total.

## 5. Views the method supports

- **Browse** — one strategy, text layer and configuration side by side.
- **Compare** — up to three configurations, axis by axis, with the "gives /
  forecloses" text for each chosen option.
- **Matrix** — all strategies × all axes, axis scores and weighted overall.
- **Configure** — an empty configuration for the reader's own strategy;
  choosing an option is the act of deciding, and the export is the record.

## 6. Applying the method to an organisation

The axes were written for national strategies, but only three need a change
of reading; the rest apply verbatim.

| axis | national reading | organisational reading |
|---|---|---|
| `interest` | national interest | the organisational reason: cost, capacity, regulatory pressure, market position, workforce |
| `intl` | international posture | posture toward standards and the wider ecosystem: follower, bilateral partner, co-funder, standard-setter |
| `reg` | regulatory posture | compliance posture toward the AI Act and sector rules: transposition only, soft internal rules, sandbox-first, binding internal framework |

Everything else already is an organisational question. Who owns the models
you depend on (`sourcing`). Whether you rent, share or own compute
(`compute`). Whether your processes are documented in a form a machine can
execute or live in people's heads (`knowledge`). Whether AI agents acting
for you have an identity anyone can verify (`identity`). How adoption is
driven — mandate, platform, budget (`adopt`). How you will know it worked,
and when (`meas`, `eval`, `return`).

The procedure is the same: text layer, one option per axis, null where you
have not decided, partials where you lean, flags where you are guessing.
The output is a configuration, a score, and — the useful part — an explicit
list of what you have foreclosed. A strategy whose "forecloses" column is
empty has not been written yet.

## 7. Document schema and consumers

A coded strategy is a document conforming to
[`schema/ai-strategy.xsd`](schema/ai-strategy.xsd) (namespace
`urn:pppa:ai-strategy:1.0`); the JSON form is defined by the generated
[`schema/ai-strategy.schema.json`](schema/ai-strategy.schema.json). The same
schema holds national and organisational strategies — `@kind` is the only
difference. A document records the `@axesVersion` it was coded against, so
a strategy stays interpretable after the axes change.

Consumers (the pppa.lv generator, AI Register) take two things from this
repository: the data bundle `dist/axes-bundle.json`, which they may update
at runtime, and the algorithm module `tools/strategy_doc.py`, which they
vendor at build time. Scoring is never re-implemented downstream.

## 8. Limits

- Coding is a reading, and readings can be wrong. The `chosen_by` field and
  the low-confidence flags exist so that codings can be challenged against
  the source. Corrections are welcome as pull requests to `data/strategies/`.
- The option values encode *decisiveness*, not merit. Two countries scoring 5
  on `frame` may have chosen opposite frames.
- Twenty strategies is a sample, weighted toward small and mid-sized
  European states plus a few reference points (Singapore, Korea, Japan, UAE,
  UK, Canada, EU). It is not a ranking of the world's AI strategies.
- The `return` axis (added September 2026) is coded only for the PPPA
  proposal; the comparators show `null` until each has been read for it.
- Values and weights are v1 and will change. The version of `data/` a
  comparison was made with is part of that comparison; cite the commit.

## 9. Provenance and citation

The axes and the first 17 codings were produced in August 2026 while
benchmarking Latvia's draft national AI strategy (VARAM, approval deadline
5 September 2026) against comparators, for the PPPA proposal at
[pppa.lv/mi-strategija](https://pppa.lv/mi-strategija). The `return` axis
follows the argument in *Three AI Initiatives, No AI Budget. Here's the
Arithmetic* (R. Gailums, LinkedIn, 24 August 2026).

Cite as: Gailums, R. (2026). *AI Strategy Decision Axes*, v1.0.
https://github.com/rg4444/AI-strategy-generator. Licence CC BY 4.0.

---

## Kopsavilkums latviski

Metode salīdzina MI stratēģijas nevis pēc tā, ko tās *saka*, bet pēc tā, ko
tās *izlemj*. Katrs lēmums ir **ass** ar slēgtu izvēļu sarakstu; katrai
izvēlei ir vērtība (0–5, kur augstāka nozīmē skaidrāku lēmumu, ne labāku),
saraksts, kuras valstis to izvēlējušās, un divi lauki — **ko dod** un **ko
liedz**. Divdesmit asis divās grupās: 15 stratēģisko lēmumu asis (vērtētas
un svērtas) un 5 formas un pārvaldības asis (rādītas, bet nesvērtas).

Stratēģiju **kodē**, katrai asij norādot vienu primāro izvēli (vai `null`, ja
dokuments neko neizlemj), pēc vajadzības daļējus vērtējumus otrai izvēlei un
zemas pārliecības atzīmi tur, kur kodējums balstās secinājumā, ne tekstā.
Ass vērtējums ir labākās izvēles vērtība, mērogota pēc tā, vai izvēle ir
primāra (5/5) vai daļēja; kopvērtējums ir A grupas asu svērtais vidējais.
Nulle asī nozīmē: dokuments šeit neko neizlemj.

Metode der jebkurai organizācijai — trīs asīm mainās tikai lasījums
(`interest`, `intl`, `reg`), pārējās jau ir organizācijas jautājumi.
Stratēģija, kurā aile „ko liedz” ir tukša, vēl nav uzrakstīta.
