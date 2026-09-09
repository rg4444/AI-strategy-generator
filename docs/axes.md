# Decision axes — reference

Generated from `data/axes.yaml` by `tools/build.py`. Do not edit by hand.

## Group A — Strategic decisions (scored, weighted)

What the country (or organisation) commits to.

### `frame` — How the state frames AI / Kā valsts redz MI · default weight 5

Scores how clearly the document takes a position on AI. Neutral tool 0; economic opportunity 2; falling-behind or risk framing 3; transformative force or dependency threat 4. Higher means clearer, not more correct.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `tool` | 0 | neutral tool | LV draft · LV 2020 · DK | No position to defend; nobody objects. | Nothing follows from it. A technology with no stance attracts no priority and no budget. |
| `econ` | 2 | economic opportunity | FI · IE · NL · SI · CZ · PT · PPPA | Familiar, safe, fits any growth agenda. | Competes with every other growth policy on equal terms. No claim to urgency. |
| `trans` | 4 | transformative force | EE · SG · AE | Justifies restructuring institutions, not just funding projects. | Raises expectations you must then meet. Invites disruption anxiety. |
| `dep` | 4 | threat of dependency | LT · KR · CA · EU | Makes sovereignty spending politically defensible. | Implies you will build something. Rhetoric without capacity is quickly exposed. |
| `behind` | 3 | threat of falling behind | UK · JP | Creates urgency with a measurable gap. | Casts the country as a follower and sets a race it may not win. |
| `risk` | 3 | source of risk | NO · EU (MI akts) | Puts rights and safety first; builds public trust before deployment. | Slows adoption. Reads as defensive if it is the only frame. |

### `diff` — Competitive differentiator / Konkurences priekšrocība · default weight 8

Whether the country names something it is distinctively good at. None 0; trust (a crowded claim) 2; language or research 3; deployment speed, compute or capital 4; standard-setting 5, as it buys the most reach per euro.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none stated | LV draft · FI · CZ · PT · JP · LT | No hostage to fortune. | Nothing to export, nothing to be cited for. Interchangeable with every peer. |
| `trust` | 2 | trust and rights | NO · IE | Turns a regulatory constraint into a selling point. | Crowded claim — every European state says it. Hard to measure. |
| `speed` | 4 | speed of public deployment | EE · SG · DK | Demonstrable, visible, and compounds with each deployment. | Requires delivery capacity, not documents. Fails publicly if slow. |
| `lang` | 3 | language and culture | SI · NL · TW | Uncontested for a small language. Nobody can take it from you. | Small market. Needs an economic claim beside it to justify spending. |
| `compute` | 4 | compute capacity | DK · CA · UK | Physical, verifiable, attracts research and industry. | Capital-intensive and depreciating. Latvia cannot win this race. |
| `std` | 5 | standards and trust infrastructure | SG (AI Verify) · EE (agent IDs) · EU (MI akts) | How small states set terms for larger ones. Cheap relative to its reach. | Requires being first and being right in public. Estonia is already moving. |
| `res` | 3 | talent and research | SI | Durable; builds on an existing base rather than a new one. | Slow to show results; competes globally for the same people. |
| `cap` | 4 | scale of capital | KR · AE | Buys position quickly. | Unavailable to most states. Not a strategy Latvia can copy. |
| `mkt` | 3 | market access and investment | IE · NL | Hosts others' capability without building your own. | Dependent on tax and regulatory arbitrage that can change. |

### `interest` — National interest / Nacionālā interese · default weight 10

Whether a country-specific reason is stated. Not stated 0; generic competitiveness 2; falling behind or trust 3; independence, service sustainability, diversification or language 4.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | not stated | EE · DK · LV draft | Nothing to defend or disprove. | No answer to “why should the country care”. Weakest possible opening. |
| `demo` | 4 | demographic decline | PPPA — neviena valsts to nav pieteikusi | Ties AI to a problem the state already feels and cannot defer. No comparator country has claimed it. | Requires showing AI actually replaces missing labour rather than merely supplementing it. |
| `comp` | 2 | competitiveness | FI · IE · NL · SI · PT · LV 2020 | Uncontroversial; fits any government. | Generic — could be any country. Persuades nobody in particular. |
| `indep` | 4 | technological independence | LT · CZ · KR · CA · EU | Concrete, current, and survives a change of government. | Invites the question of what you will actually build. |
| `behind` | 3 | risk of falling behind | UK · JP | Creates urgency with a measurable gap. | Frames the country as a follower from the first sentence. |
| `svc` | 4 | public service sustainability | SG | Ties AI to a problem voters already feel. | Reads as cost-cutting unless carefully worded. |
| `div` | 4 | economic diversification | AE | Clear economic logic; justifies large sums. | Only credible if there is a concentration to diversify from. |
| `trust` | 3 | trust as advantage | NO | Turns a regulatory constraint into a selling point. | Hard to measure; easy for others to claim too. |
| `lang` | 4 | language and cultural survival | — | Nobody has claimed it. Uniquely defensible for a small language. | Narrow on its own; needs an economic clause beside it. |

### `ambition` — Ambition type / Ambīcijas veids · default weight 8

The form the end state takes. Reputation 1; capability 3; a number with a year 5. This measures testability, not ambition level.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `reput` | 1 | reputational | LV draft | Unfalsifiable, so nobody can say you failed. | Also unfalsifiable, so nobody can say you succeeded. No budget case. |
| `cap` | 3 | capability | EE · NO · CZ · JP · SG | Names something the country will be able to do. | Still no threshold; success stays a matter of opinion. |
| `quant` | 5 | material / quantified | IE · LT · UK · AE · PT · CA · KR | Justifies budget, enables audit, forces prioritisation. | Public failure becomes possible. Needs a baseline you may not have. |

### `fund` — Funding model / Finansējuma modelis · default weight 12

Whether money is attached. Unfunded 0; budget line 3; PPP vehicle 4; dedicated multi-year fund 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `un` | 0 | unfunded | IE · NO · LV draft | Passes cabinet without a fight. | Every action becomes a bid. Classified as symbolic in comparative work. |
| `line` | 3 | earmarked budget line | FI · SI · CZ · NL · JP | Real money without a new vehicle. | Annual exposure to reallocation. |
| `fund` | 5 | dedicated fund | SG · KR · UK · CA · AE · EU · LT | Multi-year certainty; can commit to infrastructure. | Requires a scale you may not reach alone. |
| `ppp` | 4 | PPP vehicle | DK (Gefion, 85% private) | Private capital carries most of the cost. | Governance shared with a funder whose priorities are not yours. |

### `sourcing` — Model sourcing / Modeļu iegāde · default weight 10

How decidedly the document says where models come from. Decentralised by default 1; bloc co-funding 3; broker or self-hosting 4; national model 5. Measures decidedness, not feasibility.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `dec` | 1 | decentralised procurement | most states, by default | Nothing to build. Institutions move at their own pace. | Seventeen data-handling regimes. This is what fragmentation means. |
| `brok` | 4 | central broker | SG (Pair) · UK · LV draft (undefined) | One gateway: identity, DLP, routing, audit, cost attribution. | You must build and run it. A bottleneck if under-resourced. |
| `self` | 4 | self-hosted open-weight | FR (Albert) · NL · CA · LT | Data never leaves national infrastructure. | Capability gap against frontier models; ongoing operations burden. |
| `natl` | 5 | national frontier model | KR · AE | Full control of the stack. | Costs more than most national AI budgets. Unavailable below a certain scale. |
| `hybrid` | 5 | hybrid: external models + own fallback | PPPA — de facto ceļš mazai valstij | Uses the best available capability day to day and accumulates knowledge from it, while building a fallback that cannot be switched off. | Two things to maintain at once — a gateway to external models and your own. Costlier than picking one. |
| `bloc` | 3 | bloc co-funding | EU (OpenEuroLLM) | A stake in something larger than you could build alone. | You do not set the roadmap. Slower than buying. |

### `compute` — Compute / Skaitļošanas jauda · default weight 5

What compute is secured. None 0; commercial cloud only 1; EuroHPC antenna 3; sovereign PPP 4; own national HPC 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | LV 2020 | — | No basis for any sovereignty claim. |
| `nat` | 5 | national HPC | KR · UK · CA · SG · JP · LT | Own capacity and own scheduling priorities. | Capital and power costs; obsolescence in four to five years. |
| `euro` | 3 | EuroHPC antenna | LV (AIFA-LAT) · FI · CZ · IE · SI · PT | Access at a fraction of the cost — €8.4m buys a seat. | Shared queue. An antenna is not a supercomputer; check real capacity. |
| `ppp` | 4 | sovereign PPP | DK · AE | Sovereign-scale capacity on mostly private money. | Founder priorities shape access. |
| `cloud` | 1 | commercial cloud only | NL · IE in practice | Elastic, no capital cost, current hardware. | Dependency is total. No answer if terms or export rules change. |

### `lang` — Language strategy / Valodas stratēģija · default weight 5

How far the national-language provision goes. None 0; data contribution 2; fine-tuning 3; regional consortium 4; national model 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | IE · DK · CZ · PT · UK · CA | — | Fine in English. Not fine in Latvian. |
| `data` | 2 | data contribution only | FI · NO · LT | Cheap; improves commercial models in your language. | You get better service, not capability or leverage. |
| `ft` | 3 | fine-tune | — | Domain and terminology control at modest cost. | Still dependent on someone else's base model. |
| `natl` | 5 | national model | NL · SI · TW · JP · KR · LV draft | A capability that cannot be withdrawn. A real sovereignty asset. | Will not beat frontier models on general reasoning. Say what it is for. |
| `reg` | 4 | regional consortium | EU · Nordic-Baltic potential | Shares cost across languages with the same problem. | Slower; your language competes for attention inside the consortium. |

### `identity` — AI identity provision / MI identitātes nodrošinājums · default weight 6

How far the state has got with identity for AI agents — who the agent is, who owns it, what it may do. None 0; policy talk only 1; person e-identity exists but nothing for agents 2; agent identity pilot 3; national agent identity 4; cross-border verification gateway 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | lielākā daļa valstu | — | When agents start acting for people there will be no way to say who is answerable for what. |
| `policy` | 1 | policy discussion only | UK · CA | At least the question has been asked. | Discussion without infrastructure. Someone else will set the standard. |
| `pid` | 2 | person e-identity, nothing for agents | lielākā daļa ES · SG · KR · JP · AE | The trust anchor already exists — agent identity can be built on it. | Solves nothing by itself. The agent still acts without a mandate. |
| `pilot` | 3 | agent identity pilot | LV — VARAM projekts (6. pakete) | Tests the idea against a real case before locking it in. | A pilot with no scaling plan stays a demo. |
| `natid` | 4 | national AI agent identity | EE (2026. g. jūnijs) | The agent acts within granted authority, fully traceable. | Works only inside your own jurisdiction without an interoperability layer. |
| `gw` | 5 | cross-border verification gateway | PPPA (uzticamības vārteja) — vēl neviena valsts | Verifies agents issued elsewhere too. This is the exportable layer, not the identity itself. | Only valuable if others recognise it — needs standards work, not just code. |

### `knowledge` — Knowledge accumulation / Zināšanu uzkrāšana · default weight 5

Whether the state accumulates and reuses what institutions know and learn, instead of starting from zero each time. None 0; document digitisation 1; machine-readable records and a data catalogue 2; reusable shared components 3; organisational knowledge base 4; federated knowledge exchange between institutions 5. Distinct from “Evaluation & memory”: that axis is what worked, this one is the corpus itself.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | LV 2020 | — | Every institution learns the same thing again, and knowledge leaves with the people. |
| `docs` | 1 | document digitisation | CZ · PT · IE · JP · CA | Paper is no longer the obstacle. | A scanned PDF is not machine-readable. AI still cannot use it. |
| `mrec` | 2 | machine-readable records and data catalogue | LV — VARAM projekts · FI · NL · LT · EU · AE · KR | Data becomes an asset that can be found and reused. | A catalogue is not knowledge — it says what exists, not what the institution learned. |
| `reuse` | 3 | reusable shared components | EE (kratid) | Built once, used many times. Saves money at every institution after the first. | Components transfer, context does not. Each institution still has to adapt them. |
| `orgkb` | 4 | organisational knowledge base | SG (AIBots, 115 iestādes) · UK (AI Knowledge Hub) | Institutional knowledge becomes a system that outlives staff turnover. | Each institution in its own silo — nationally the knowledge still does not talk. |
| `fed` | 5 | federated knowledge exchange | PPPA — vēl neviena valsts | Institutions keep their own but exchange on a shared standard: one learns from another without pooling the data. | Needs a standard and governance before it pays off. The hardest step of the set. |

### `adopt` — Adoption mechanism / Ieviešanas mehānisms · default weight 8

How far the adoption mechanism reaches into institutions. Voluntary 1; vouchers 2; mandates 3; procurement 4; central platform 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `vol` | 1 | voluntary | NO · IE · CZ · CA · JP | No resistance. | Adoption tracks enthusiasm, not need. Uneven by institution. |
| `vou` | 2 | vouchers | LV draft · CZ | Reaches SMEs and small institutions directly. | Funds pilots, not scaling. This is how pilot graveyards form. |
| `mand` | 3 | mandates | AE · KR | Fastest route to uniform adoption. | Produces compliance theatre if capability is not there first. |
| `proc` | 4 | procurement-led | EU (buy European) | The strongest lever a state has. Sets terms once, everywhere. | Slow to change; needs procurement expertise you must build. |
| `plat` | 5 | central platform | SG (Pair) · UK (Humphrey) · EE (Bürokratt) | Adoption becomes a login. Singapore: ~80% of 150,000 officers. | Single point of failure; you own support and trust permanently. |

### `meas` — Measurement / Mērīšana · default weight 8

Whether the strategy can be tested. None 0; activity KPIs 2; outcome KPIs 4; public delivery tracker 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | LV draft · LV 2020 | Nothing to explain in year three. | Cannot defend the budget or claim success. Comparatives are not measures. |
| `act` | 2 | activity KPIs | FI · CZ · JP · EU · CA | Easy to collect from existing reporting. | Counts pilots, not outcomes. Rewards motion. |
| `out` | 4 | outcome KPIs | IE (75% by 2030) · NO · SI · AE · SG · KR | One number and one year makes the strategy testable. | Needs a baseline. You may not like the first reading. |
| `trk` | 5 | public delivery tracker | UK (delivery.ai.gov.uk) | External pressure does the enforcement for you. | Failures are visible in real time. |

### `eval` — Evaluation & memory / Novērtēšana un atmiņa · default weight 5

Whether learning accumulates. None 0; solution catalogue 2; evaluation function 4; what-works centre 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none | almost everyone | — | Every institution relearns the same lesson. Knowledge leaves with staff. |
| `cat` | 2 | solution catalogue | LV draft · SG | Prevents the same thing being built twice. | A list is not a lesson. Records what exists, not what worked. |
| `fn` | 4 | evaluation function | UK (Evaluation Task Force) | Pilots produce evidence instead of anecdotes. | Needs method and staff, and the answers are sometimes unwelcome. |
| `ww` | 5 | what-works centre | UK (What Works Network) | Institutional memory outliving ministers. Nobody has this for AI. | Only pays off across years, past the political horizon. |

### `return` — How return is evaluated / Kā vērtē atdevi · default weight 6

Whether the strategy says how and when to measure the return on AI investment. None 0; one measure (ROI) for everything 2; operational return at 90 days (ROAI) 3; price before signature (EVC) 3; three instruments by horizon — EVC before signature, ROAI at 90 days, ROI at 12 months — 5. Higher means a clearer method, not a larger return. Below the axis: the three questions that pick the instrument.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `none` | 0 | none stated | most strategies | Nothing to measure, so nothing can fail. | Every proposal arrives with its sponsor's number. The decision goes to the most confident presenter, not the arithmetic. |
| `roi` | 2 | single measure — ROI | typical CFO practice | Finance recognises it. Tools with a cash line get approved. | Infrastructure never passes. Two years on: many licences, no capability. |
| `roai` | 3 | operational return at 90 days (ROAI) | PPPA — early-warning instrument | Early signal that the work is faster, cleaner and more consistent: baseline measured before the start, trend subtracted. | No cash line — it cannot justify a budget. A baseline cannot be reconstructed afterwards; from memory it is a negotiation. |
| `evc` | 3 | price before signature (EVC) | procurement practice | A ceiling on what to pay — compared with hiring or outsourcing, not with doing nothing. | Says nothing about return. Presenting EVC as a return case is the commonest category error in AI procurement. |
| `layered` | 5 | three instruments by horizon: EVC → ROAI → ROI | PPPA — no country yet | Each question gets its own instrument at its own moment: price before signature, operational signal at 90 days, cash movement at 12 months. Infrastructure travels inside another project's scope, not on a business case of its own. | Needs baselines before the start and a capture route named in advance — a discipline most institutions do not have. |

### `intl` — International posture / Starptautiskā nostāja · default weight 5

How active the international role is. EU follower 1; bilateral or bloc co-funding 3; standard-setter 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `fol` | 1 | EU follower | most member states · LV draft | Safe, cheap, aligned with funding. | No distinctive asset. Nobody cites you. |
| `std` | 5 | standard-setter | EE (agent IDs) · SG (AI Verify) · SI (IRCAI) | How small states punch above weight. Estonia has done it three times. | Requires being first, and being wrong in public if you are. |
| `bil` | 3 | bilateral | UK · CA · AE | Access to partners' compute and talent. | Asymmetric — the larger party sets the terms. |
| `bloc` | 3 | bloc co-funder | EU members in OpenEuroLLM | Buys a seat at a table you could not build. | Shared credit; slower than acting alone. |

## Group B — Form and governance (shown, not weighted)

What kind of artefact the document is.

### `doctype` — Document type / Dokumenta tips

How binding the document is. Vision 2; plan or rolling portfolio 4; statute 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `vision` | 2 | vision | FI · IE · AE · NO | Fast to write, survives elections, hard to attack. | Nothing is owed. No delivery obligation follows. |
| `plan` | 4 | plan with actions | LT · DK · SG · UK · CZ · PT · LV draft | Actions can be tracked and audited. | Ties you to a list that ages; needs a refresh mechanism. |
| `statute` | 5 | statute | KR · JP | Binding, survives ministers, creates real institutions. | Slow, amendment-heavy, hard to steer once passed. |
| `rolling` | 4 | rolling action-plan portfolio | EE | Adapts every two to three years without reopening the strategy. | No single quotable document; a weaker external signal. |

### `horizon` — Horizon & refresh / Termiņš un atjaunošana

Whether revision is guaranteed. None 0; 10yr 3; 5yr 4; 3yr rolling or statutory cycle 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `r3` | 5 | 3yr rolling | EE · SG · UK | Stays current as the technology moves. | Constant reopening; hard to make long infrastructure commitments. |
| `y5` | 4 | 5yr | DK · CZ · PT · CA · EU · LV draft | Matches budget and EU programming cycles. | Two generations of models will pass inside one cycle. |
| `y10` | 3 | 10yr | LT · AE | Room for compute and skills to actually mature. | Content ages badly; needs mid-term revision built in. |
| `stat` | 5 | statutory cycle | KR · JP | Revision happens whether or not anyone champions it. | Rigid timing; may force a rewrite at the wrong moment. |
| `none` | 0 | none | FI · IE · NO · NL · LV 2020 | No overhead. | The document quietly expires. Nobody is obliged to look again. |

### `decomp` — Decomposition / Struktūra

How concentrated the structure is. Enablers only or sectors only 3; matrix 4; missions 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `enab` | 3 | enablers only | most EU states | Clean, comparable, matches EU reporting. | No sector owns anything; ministries can nod without committing. |
| `sect` | 3 | sectors only | AE | Every sector has a name against it. | Shared foundations get built five times or not at all. |
| `matrix` | 4 | enabler × sector matrix | LV draft · NO | Shows how foundations feed sectors. Complete on paper. | Cells with no owner become decoration. Needs a lead per column. |
| `miss` | 5 | missions | SG | Concentrates money on a few outcomes. | Politically hard — choosing missions means refusing others. |

### `gov` — Governance locus / Pārvaldības centrs

How much power there is to direct other institutions. Line ministry 2; central agency 4; head-of-government council or statutory body 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `min` | 2 | line ministry | LV · LT · CZ · SI · NL · CA · AE | Uses an existing mandate; no new institution needed. | Cannot compel other ministries. Coordination stays voluntary. |
| `agy` | 4 | central digital agency | DK · UK · PT · EU | Can build and run shared services, not only write policy. | Needs delivery capacity you must actually staff. |
| `coun` | 5 | head-of-government council | SG (NAIC) · EE (Eesti.ai) | Convening power over ministries. Attention at the top. | Depends on one person's interest; evaporates on a reshuffle. |
| `stat` | 5 | statutory body | KR · JP | Permanent, funded, cannot be quietly dropped. | Legislation first, which you do not have time for. |

### `reg` — Regulatory posture / Regulatīvā nostāja

How settled the regulatory stance is. EU transposition only 1; soft law 2; sandbox 4; statutory framework 5.

| key | value | option | chosen by | gives | forecloses |
|---|---|---|---|---|---|
| `stat` | – | statutory framework | KR · EU | Enforceable; creates authorities with real powers. | Slow; can chill deployment while rules settle. |
| `sand` | – | sandbox-first | DK · LV draft | Learn from real cases before writing rules. | Sandboxes need staff and cases, or they sit empty. |
| `soft` | – | soft law | UK · JP · NO · CA | Fast, flexible, low compliance burden. | No teeth. Depends on goodwill. |
| `eu` | – | EU transposition only | most member states | Minimum viable compliance; no divergence risk. | Purely reactive. No national position to export. |

## Coded strategies

| id | name | documents |
|---|---|---|
| `EE` | Estonia | Kratt 2024–2026 · Data & AI White Paper 2024–2030 · Eesti.ai |
| `LT` | Lithuania | National AI Strategic Guidelines 2026–2035 |
| `FI` | Finland | Finland's Age of AI (2017) · AI 4.0 · Digital Compass 2030 |
| `DK` | Denmark | Digitalisation strategy 2024–2027 · Strategic Approach to AI (2024) |
| `IE` | Ireland | AI — Here for Good (2021, atjaunināta 2024) |
| `NL` | Netherlands | SAPAI (2019) · Generative AI vision (2024) |
| `SI` | Slovenia | NpUI — National Programme for AI to 2025 |
| `NO` | Norway | National Strategy for Artificial Intelligence (2020) |
| `CZ` | Czechia | National AI Strategy 2030 (NAIS, 2024) |
| `PT` | Portugal | AI Portugal 2030 · National AI Agenda 2026–2030 |
| `SG` | Singapore | National AI Strategy 2.0 (2023) · NAIS Update (2026) |
| `KR` | South Korea | AI Basic Act (2024/26) · sovereign AI programme |
| `UK` | United Kingdom | AI Opportunities Action Plan (2025) |
| `CA` | Canada | Canadian Sovereign AI Compute Strategy (2024) |
| `JP` | Japan | AI Promotion Act (2025) · Basic AI Plan (2025) |
| `AE` | UAE | National Strategy for Artificial Intelligence 2031 |
| `EU` | EU | AI Continent Action Plan · Apply AI Strategy (2025) |
| `LV20` | Latvia 2020 | Informatīvais ziņojums “Par mākslīgā intelekta risinājumu attīstību” (MK, 04.02.2020.) |
| `LV26` | Latvia — VARAM draft | MI plāna stratēģiskais kartējums (2026) |
| `PPPA` | PPPA proposal | pppa.lv/mi-strategija-2 · darba versija v2 · 3 pīlāri, 4 mērķi, 12 rīcības |
