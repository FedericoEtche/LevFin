# Grifols Re-Anchoring — Reconciliation List

**Source of truth:** `Grifols_Model_v2.xlsx` (the re-saved, intact copy of the re-anchored model).
**Prepared:** 23 May 2026 · **Status:** for your review — NO edits applied yet.

This list covers every stale Grifols figure, ratio and claim across the six deliverables.
Review it, flag anything, answer the three questions at the end, and I will apply the edits and run verification.

---

## A. Two findings before the detail

1. **Two of the six deliverables contain no Grifols figures at all.**
   - `LevFin_Options_Valuation_Model.xlsx` is the stylised **"Project Helios"** template (EUR 600m TLB, EV 1,500, EBITDA 150). Its only Grifols touchpoint is a companion-file *name* in the Cover sheet.
   - `Credit_Optionality_Deck.pptx` — its worked example (Slide 8) is **Project Helios**, not Grifols. There is no Grifols slide. Its only Grifols touchpoint is a companion-file *name* reference on Slide 12.
   These Project Helios numbers are a separate, intentional example — **not stale Grifols figures** — so I will not touch them. See Question 3.

2. **The re-anchored model changes the *direction* of several claims, not just the numbers.** The Merton credit-risk put, the equity cure, and the ECF sweep now all price to **zero**; portability *rises*; and the spread no longer equals the optionality (a 140 bp residual opens up). Several narrative paragraphs therefore need rewriting, not just a number swap. Proposed new wording is shown in full below.

---

## B. Canonical model values (pulled from `Grifols_Model_v2.xlsx`)

| Metric | Value | Source cell |
|---|---|---|
| Revenue 2024 / 2025 | €7,215m / €7,526m | Dashboard B55 / C55 |
| EBITDA 2024 / 2025 | €1,598m / €1,687m | Dashboard B57 / C57 |
| EBITDA margin (2025, ~flat across forecast) | 22.4% | Dashboard C58 |
| EBIT 2024 / 2025 | €1,215m / €1,250m | Dashboard B59 / C59 |
| Cash (2025 onward) | €825m | Dashboard C65 |
| Gross debt — base model, at 2026 launch | ~€9.1bn | Covenants K21 |
| Gross debt face — used for option pricing / Merton strike | €8,175m | Option_Pricing B5 / B18 |
| Total net leverage — 2026 forecast launch (2026Q1) | 4.78x | Covenants K26 / Option_Pricing B48 |
| Total net leverage — forecast range (2026Q1→2030Q4) | 4.78x → 3.03x | Covenants K26:AD26 |
| Covenant headroom — 2026 launch | 3.22 turns | Covenants K30 |
| Total net leverage covenant | 8.0x | Covenants B10 |
| Monte Carlo paths | 500 | Option_Pricing B12 |
| Asset / revenue volatility | 8% | Option_Pricing B17 |
| P(8.0x covenant breached, any quarter) | 0% | MC_Summary B24 |
| Peak leverage over horizon (MC mean) | 4.83x | MC_Summary B21 |
| Enterprise value at horizon — P5 / mean / P95 | €13,704m / €18,194m / €23,830m | MC_Summary C20 / B20 / E20 |
| Cumulative net income to Q28 (MC mean) | €2,573m | MC_Summary B19 |
| **Merton credit-risk put** | €0m / 0.0 bps | Option_Pricing B20 / B21 |
| **Builder basket** | €1,032m / 252.6 bps | Option_Pricing B27 / B28 |
| **Equity cure** | €0m / 0.0 bps | Option_Pricing B35 / B36 |
| **ECF cash sweep** (E[PV swept] €469m) | benefit €0m / 0.0 bps | Option_Pricing B42 / B43 / B44 |
| **Make-whole call (net)** | €122m / 29.8 bps | Option_Pricing B53 / B54 |
| **Portability** | €37m / 9.0 bps | Option_Pricing B62 / B63 |
| **Net embedded optionality** | 291.4 bps | Option_Pricing B72 / Yield_Decomposition B21 |
| Risk-free base rate | 450 bps | Yield_Decomposition B5 |
| Fair all-in yield | 741.4 bps | Yield_Decomposition B12 |
| Quoted all-in yield | 881.7 bps | Yield_Decomposition B14 |
| Quoted spread over risk-free | 431.7 bps | Yield_Decomposition B22 |
| Residual / mispricing (quoted − fair) | 140.3 bps | Yield_Decomposition B15 |

---

## C. Deliverable 1 — `Credit_Optionality_Treatise.docx` (Chapter 18)

### C1. Table 4 — "The six options" (after para 617)

| Row | Field | OLD | NEW |
|---|---|---|---|
| Merton credit-risk put | PV (€m) / bps | 410 / 79 | 0 / 0.0 |
| Builder basket | PV (€m) / bps | 177 / 34 | 1,032 / 252.6 |
| Equity cure | PV (€m) / bps | 122 / 24 | 0 / 0.0 |
| ECF cash sweep | PV (€m) / bps | 65 / (13) | 0 / 0.0 |
| Make-whole call | PV (€m) / bps | 18 / 3 | 122 / 29.8 |
| Portability | PV (€m) / bps | 5 / 1 | 37 / 9.0 |
| Net embedded optionality | bps | 128 | 291.4 |

### C2. Table 5 — "Yield decomposition" (after para 620)

| Component | OLD bps / running | NEW bps / running |
|---|---|---|
| Risk-free base rate | 450 / 450 | 450.0 / 450.0 |
| + Merton credit-risk put | 79 / 529 | 0.0 / 450.0 |
| + Builder basket | 34 / 563 | 252.6 / 702.6 |
| + Equity cure | 24 / 587 | 0.0 / 702.6 |
| + Make-whole call (net) | 3 / 590 | 29.8 / 732.4 |
| + Portability | 1 / 591 | 9.0 / 741.4 |
| − ECF cash sweep (lender holds) | (13) / 578 | 0.0 / 741.4 |
| Fair all-in yield | 578 | 741.4 |
| Quoted all-in yield (model-implied) | 579 | 881.7 |
| Residual / mispricing | 1 | 140.3 |

### C3. Narrative paragraphs (full proposed rewrites)

**Para 595 — base model.** Changes: EBITDA margin 17.8%→22.4%; gross debt 10.4bn→9bn; leverage "between 5.9 and 6.9 times"→"opens at 4.8 times and delevers toward 3.1 times". (Revenue 7.2→9.2bn and 8.0x covenant unchanged.)
> *New:* "…In the base case revenue grows from roughly 7.2 billion euros to 9.2 billion, the EBITDA margin holds near 22.4 percent, gross debt sits around 9 billion, and total net leverage opens at 4.8 times and delevers toward 3.1 times. The governing maintenance covenant is a total net leverage test at 8.0 times."

**Para 602 — simulation outputs.** Changes: breach probability 14.4%→0; peak leverage 7.3x→4.8x; EV mean 10.7bn→18.2bn, P5 8.1bn→13.7bn, P95 14.1bn→23.8bn; cumulative NI 344m→2.6bn.
> *New:* "…The headline figures: the probability that the 8.0-times covenant is breached at some point over the life is zero; peak leverage averages 4.8 times across paths; enterprise value at the horizon averages 18.2 billion euros, with a fifth percentile of 13.7 billion and a ninety-fifth of 23.8 billion; cumulative net income over the forecast averages 2.6 billion. These are not decorative outputs…"

**Para 608 — Merton credit-risk put (rewrite: now zero, claim reverses).**
> *New:* "The lender's first short position is, in principle, the default put: the right, in effect, handed to the equity to walk away if enterprise value falls below the debt. Priced as a European put on enterprise value struck at the 8.2-billion-euro debt face, it is worth nothing in this calibration — zero in present-value terms, and zero basis points a year. The figure is negligible because the model's enterprise value sits well above the debt: a mean enterprise value of 18.2 billion euros against an 8.2-billion debt face leaves the put deeply out-of-the-money on essentially every path. This remains the most calibration-sensitive number in the chapter: the put is a convex function of the enterprise-value multiple and asset volatility, and a materially lower valuation or a higher volatility assumption would bring it back into play. The sensitivity is exposed as an input rather than buried."

**Para 610 — builder basket.** 177m/34bps → 1,032m/253bps.
> *New:* "…Averaged over the five hundred cumulative-income paths, the leakage capacity is worth 1,032 million euros, or 253 basis points."

**Para 612 — equity cure (rewrite: now zero — no breach in any path).**
> *New:* "…It is priced on the myopic rule — cure when a breach is imminent — and this is not an approximation of convenience. A cure is a forced decision at a fixed test date; there is no value in waiting, so the myopic rule is the optimal rule. Here the lost-remedy cost to the lender is zero: across the five hundred paths the 8.0-times covenant is never breached, so the cure is never triggered and the lender never surrenders its remedy. The right carries real value only in a weaker or more volatile credit."

**Para 614 — ECF cash sweep (rewrite: swept cash 1.65bn→469m; benefit now zero).**
> *New:* "The excess-cash-flow sweep is the one structure in the bundle that the lender holds rather than writes. Above a leverage trigger it forces a share of free cash flow back as principal, deleveraging the credit. Over the paths it returns an expected 469 million euros of cash. Because the credit-risk put it would otherwise offset is itself worth nothing here, the deleveraging it buys scores zero basis points — the one line that runs in the lender's favour, but immaterial in this calibration."

**Para 616 — make-whole and portability (rewrite: make-whole 3→30 bps; portability 1→9 bps, claim reverses).**
> *New:* "Two smaller features close the set. The make-whole call is the borrower's right to refinance early; the make-whole premium compensates the lender for most — but not all — of the spread it forgoes, leaving a net cost of 30 basis points. Portability — the knock-out that lets the debt survive a change of control if leverage is low enough — is worth 9 basis points: Grifols delevers below the portability threshold on every path, so the knock-out reliably fires and erodes the lender's change-of-control put."

**Para 624 — yield decomposition (rewrite: "near-identity" is gone; 140 bp residual).**
> *New:* "The embedded optionality sums to 291 basis points — the fair spread the lender should charge over the risk-free rate. The credit's quoted spread is 432 basis points. The fair all-in yield is therefore 741 basis points against a quoted all-in yield of 882, leaving a residual of 140 basis points."

**Para 625 — reading the residual (rewrite).**
> *New:* "That 140-basis-point residual should be read for what it is, and not for more. It is not a precision result. Several of the components rest on judgment inputs — the value of a lost covenant remedy, the probability of a change of control — and the credit-risk put, as noted, is sensitive to a discounted-cash-flow valuation that runs light. Move any of those inputs and the residual moves with them. A positive residual of this size says the quoted spread more than covers the embedded optionality the model can identify — on these inputs, the loan looks cheap to the lender. What the decomposition delivers is not a verdict to the basis point. It is a structure: the spread is no longer a single opaque number but a sum of named, individually-valued parts, every one of which can be interrogated, stressed and argued."

**Para 628 — what the decomposition is for (rewrite).**
> *New:* "Return to the thesis of Chapter 1: the yield is the residual, not the price. This chapter has made the claim literal. The 432 basis points of quoted spread on this credit is not a measure of 'the risk.' The model can name 291 of it: zero basis points of pure default exposure, 253 of value the sponsor may extract through the builder basket, 30 from the make-whole call and 9 from portability — with the equity cure and the cash sweep both negligible on these paths. The remaining 140 basis points is residual — spread the quoted yield carries that the decomposition cannot attribute to a priced option."

---

## D. Deliverable 2 — `LevFin_Options_Valuation_Model.xlsx`

**No stale Grifols figures.** This is the stylised Project Helios template; its numbers are intentional and stay as-is.

| Cell | OLD | NEW | Note |
|---|---|---|---|
| Cover B36 | "…companion integrated model, **Grifols_Model_v1.xlsx**…" | "…Grifols_Model_v2.xlsx…" | Filename pointer only — see Question 2 |

---

## E. Deliverable 3 — `Credit_Optionality_Deck.pptx`

**No stale Grifols figures.** Worked example (Slide 8) is Project Helios — intentional, stays as-is. Slide 12 carries a generic companion reference ("the integrated Grifols worked-example model") with no number. See Question 3 (add a Grifols slide?).

---

## F. Deliverable 4 — `Sponsor_Negotiation_Playbook.docx` (Chapter 9)

### F1. Table 8 — "The six options … from the sponsor's side" (after para 368)

| Row | OLD bps | NEW bps |
|---|---|---|
| Limited-liability put (Merton) | 79 | 0.0 |
| Builder basket | 34 | 252.6 |
| Equity cure | 24 | 0.0 |
| Make-whole call | 3 | 29.8 |
| Portability | 1 | 9.0 |
| ECF cash sweep | (13) | 0.0 |
| Net optionality held by the sponsor | 128 | 291.4 |

### F2. Table 9 — "The sponsor's scorecard" (after para 371)

| Row | OLD bps | NEW bps |
|---|---|---|
| Spread paid (quoted, over the risk-free rate) | 129 | 431.7 |
| Optionality the sponsor holds (net) | 128 | 291.4 |
| — of which: limited-liability put (not negotiated) | 79 | 0.0 |
| — of which: the negotiated bundle | 49 | 291.4 |

### F3. Section headings (carry numbers)

| Para | OLD | NEW |
|---|---|---|
| 358 | The limited-liability put — 79 basis points | The limited-liability put — zero basis points |
| 360 | The builder basket — 34 basis points | The builder basket — 253 basis points |
| 362 | The equity cure — 24 basis points | The equity cure — zero basis points |
| 364 | The make-whole and portability — 4 basis points together | The make-whole and portability — 39 basis points together |
| 366 | The ECF cash sweep — minus 13 basis points | The ECF cash sweep — zero basis points |

### F4. Narrative paragraphs (full proposed rewrites)

**Para 355 — "the largest single line is the credit-risk put" is now false.**
> *New:* "One option deserves a note before the walk-through. The credit-risk put — in Merton's framing, the right of the equity to hand the keys to the lender if enterprise value falls below the debt — is, on many capital structures, the largest single line in the decomposition. On this one it is not: as the walk-through shows, the model's enterprise value sits well above the debt and the put prices to zero. The lender treatise prices it as default exposure. From the sponsor's chair it is something the sponsor owns outright: the limited-liability put that comes free with the corporate form, and the one piece of optionality in the structure that is never negotiated, because it is never on the table."

**Para 359 — limited-liability put (rewrite: now zero).**
> *New:* "Priced as a European put on enterprise value struck at the 8.2-billion-euro debt face, the limited-liability put is worth nothing in this calibration — zero euros, zero basis points a year. It is still the option the sponsor spends no negotiating capital on, because it comes free with the corporate form; here it simply happens to be far out of the money. The figure is negligible because the model's enterprise value — a mean of 18.2 billion euros at the horizon — sits well above the 8.2-billion debt face, leaving a thick equity cushion. The lesson for a sponsor is the sensitivity, not the decimal: the more leveraged the structure, the more of the equity's worth collapses back into this single option."

**Para 361 — builder basket.**
> *New:* "The builder basket — capacity to distribute value up to fifty percent of cumulative net income — is worth 1,032 million euros, or 253 basis points. In the playbook's terms it is a Tier 1 feature, and the worked example confirms why: it is by far the largest negotiated line in the bundle, and it converts directly into the dividend-recap and distribution optionality at the centre of most sponsor theses."

**Para 363 — equity cure (rewrite: now zero).**
> *New:* "The equity cure — the right to inject equity and cure a covenant breach rather than surrender a remedy to the lender — is worth nothing in this calibration: zero euros, zero basis points. It is the price of staying in control through a stumble, but the model shows no covenant breach on any of the five hundred paths — a zero percent probability that the 8.0-times covenant is ever tested in anger — so on these projections the right is never exercised. It is a Tier 1 feature whose value here is purely contingent: real in a weaker or more volatile credit, latent in this one."

**Para 365 — make-whole and portability (rewrite).**
> *New:* "The remaining two features round out the bundle. The make-whole call — the right to refinance early — is worth 30 basis points; the make-whole premium compensates the lender for most of the spread it forgoes, but not all, so a modest net value accrues to the sponsor. Portability — the knock-out that lets the debt survive a change of control — is worth 9 basis points: Grifols delevers below the portability threshold on every path, so the knock-out reliably fires. Both are dwarfed by the builder basket: a sponsor who spent a hard-fought concession to widen portability on this credit would have bought 9 basis points of value against the 253 sitting in the builder basket. That is a Tier 4 lesson with a number attached."

**Para 367 — ECF cash sweep (rewrite: 1.65bn→469m, now zero bps).**
> *New:* "One option in the structure runs the other way. The excess-cash-flow sweep is held by the lender, not the sponsor: above a leverage trigger it forces a share of free cash flow back as debt repayment. To the sponsor it is constraint rather than value — it routes roughly 469 million euros of cash to debt repayment over the life. In this calibration it prices at zero basis points: it is the one line in the decomposition that runs the lender's way, but on these paths it nets to nothing."

**Para 371 — the scorecard (rewrite: spread and optionality no longer coincide).**
> *New:* "The lender treatise assembles these lines into a yield: a risk-free base plus every option, netting to a fair all-in yield of 741 basis points against a quoted all-in yield of 882. For the sponsor the same arithmetic is a scorecard. Stripped of the risk-free base, the credit carries 432 basis points of quoted spread, while the priced optionality the sponsor holds nets to 291 basis points. The sponsor pays 432, and the model can account for 291 of it as optionality — leaving a 140-basis-point residual the decomposition does not attribute to any single named option."

**Para 374 — composition (rewrite).**
> *New:* "The 140-basis-point residual is not the interesting part — and, as the lender treatise is careful to say, none of this is a precision result; several components rest on judgment inputs. The interesting part is the composition. Of the 291 basis points of optionality, none sits in the limited-liability put — on this calibration the equity cushion is thick enough that the put the sponsor never negotiates is worthless. The whole 291 is the negotiated bundle — the builder basket, the equity cure, the two smaller features, net of the sweep. That is the number the playbook has been about all along: the second-order optionality, the part a sponsor actually wins or loses at the table."

**Para 375 — the tier split (rewrite).**
> *New:* "And within that 291, the split is what the tier system predicts. The builder basket — 253 basis points on its own — is the Tier 1 feature, and it is where almost the entire value sits. The equity cure is the other Tier 1 feature; it prices at zero here only because the simulation shows no covenant breach, and would carry real value in a weaker credit. Portability — 9 basis points — is the Tier 4 feature, and the worked example shows, with a real number, why a disciplined sponsor concedes it without a fight."

**Para 379 — second lesson (rewrite: the old "limited liability is 79 of 128" claim is now false).**
> *New:* "Second, the value of the limited-liability put — the one option the sponsor never negotiates — depends entirely on how close the structure runs to the debt. On a deeply distressed credit it can dominate the bundle; on Grifols, where the model's enterprise value sits well above the debt, it prices to zero, and the full 291 basis points of priced optionality sits in the negotiated bundle. Either way the proportion is the point: know how much of your optionality is the free limited-liability put before deciding how hard to fight for the rest."

---

## G. Deliverable 5 — `Sponsor_Efficiency_Frontier_Model.xlsx` ("Grifols Worked Example" tab)

| Cell | Field | OLD | NEW |
|---|---|---|---|
| B2 | Source-file name | "…Grifols_Model_**v1**.xlsx…" | "…Grifols_Model_v2.xlsx…" (Question 2) |
| C6 | Gross debt (EUR m) | 10,371 | 8,175 |
| C8 | Quoted all-in spread over risk-free | 129 | 431.7 |
| C11 | Limited-liability put (Merton) | 79 | 0 |
| C12 | Builder basket | 34 | 252.6 |
| C13 | Equity cure | 24 | 0 |
| C14 | Make-whole call | 3 | 29.8 |
| C15 | Portability | 1 | 9.0 |
| C16 | ECF cash sweep | −13 | 0 |
| C17 | Net optionality (=SUM C11:C16) | 128 | 291.4 *(formula auto-updates)* |
| C20 | Spread paid (quoted, over RF) | 129 | 431.7 |
| C22 | of which: limited-liability put | 79 | 0 |
| C21, C23 | formulas (=C17, =C17−C22) | — | auto-update to 291.4 / 291.4 |
| B26–B31 | Interpretation text | see below | full rewrite |

**Interpretation block (B26–B31) — proposed new lines:**
> B26: "The sponsor pays 432 bps of spread and holds 291 bps of priced optionality. The two no"
> B27: "longer coincide — a 140 bp residual is spread the model cannot attribute to a named option."
> B28: "Of the 291 bps, none is the limited-liability put — the equity cushion is thick enough that"
> B29: "it prices to zero here, so the whole 291 bps is the negotiated bundle. The builder basket"
> B30: "(253 bps) carries almost all of it; the equity cure, also Tier 1, prices to zero with no"
> B31: "breach in the simulation; portability (9 bps) is the Tier 4 concede-without-a-fight lesson."

Cover B6 also references "Grifols_Model_v1.xlsx" — see Question 2.

---

## H. Deliverable 6 — `Sponsor_Negotiation_Deck.pptx` (Slide 10)

| Element | OLD | NEW |
|---|---|---|
| Limited-liability put (Merton) | 79 bps | 0 bps |
| Builder basket | 34 bps | 253 bps |
| Equity cure | 24 bps | 0 bps |
| Make-whole call | 3 bps | 30 bps |
| Portability | 1 bps | 9 bps |
| ECF cash sweep (lender holds — a constraint) | (13) bps | 0 bps |
| Net optionality held by the sponsor | 128 bps | 291 bps |
| Scorecard — spread paid, over the risk-free rate | 129 bps | 432 bps |
| Scorecard — optionality the sponsor holds | 128 bps | 291 bps |
| Scorecard — limited-liability put, never negotiated | 79 bps | 0 bps |
| Scorecard — the negotiated bundle | 49 bps | 291 bps |

**"THE LESSON" box — proposed new text:**
> "The decomposition is a negotiation tool, not just the lender's pricing tool. Of the 291 bps the sponsor holds, none is limited liability — the equity cushion is thick enough that it prices to zero here. The negotiated bundle is the full 291 bps: spend the capital where the value is — the builder basket, 253 bps — not on portability, worth 9 bps on this credit."

(Slide subtitle "…500 simulated paths" is correct — unchanged.)

---

## I. Three questions before I edit

**Q1 — Rounding convention.** Builder 252.58 + make-whole 29.79 + portability 9.00 = 291.37. Rounded to whole numbers the parts (253 + 30 + 9) sum to 292, not 291 — integers cannot both round correctly *and* tie. Proposed: **one decimal place in the four summing tables** (Treatise Tables 4–5, Playbook Tables 8–9) and the Sponsor xlsx, so every column ties exactly to the model; **whole numbers in narrative prose** (e.g. "253 basis points"). Alternative: whole numbers everywhere, accepting components that sum ±1 off the stated total.

**Q2 — Model filename.** Three cells point to `Grifols_Model_v1.xlsx` (LevFin xlsx Cover B36; Sponsor xlsx Cover B6 and Grifols tab B2). The intact file is currently `Grifols_Model_v2.xlsx`. Update the pointers to v2, or leave them as v1 (e.g. if you intend to re-save v2 back over v1)?

**Q3 — Lender deck scope.** `Credit_Optionality_Deck.pptx` has no Grifols slide — its worked example is Project Helios. The sponsor deck *does* have one (Slide 10). Leave the lender deck unchanged, or add a Grifols worked-example slide mirroring Treatise Tables 4–5? (Adding a slide is new content beyond a figure refresh.)
