# Project Helios → Grifols — Conversion Plan (for your sign-off)

You asked to eliminate Project Helios and make Grifols the worked example throughout.
Helios runs deeper than the deck. Here is the full map, the honest complications, and a
recommended plan. **Nothing is edited yet.**

---

## 1. Where Project Helios lives

| # | Location | What it is |
|---|---|---|
| 1 | Treatise **§15.1** "A Typical European Cov-Lite TLB" (¶486–495 + Table 3) | A hand-built **17-line** option decomposition of a fictitious €600m TLB |
| 2 | Playbook **§4.3** "Worked example — Project Helios from the sponsor's side" (¶181–200) | Efficiency-frontier illustration |
| 3 | Playbook **Chapter 6** "Worked Example — Project Helios from the Sponsor Side" (¶256–285 + Tables 4–6) | Full sponsor efficiency-frontier worked example |
| 4 | **Credit_Optionality_Deck.pptx** Slide 8 | "Worked Example — Project Helios" |
| 5 | **Sponsor_Negotiation_Deck.pptx** Slides 6 & 9 | "Efficiency Frontier — Project Helios" / "The Prize — Project Helios" |
| 6 | **LevFin_Options_Valuation_Model.xlsx** | Entire workbook — a parametric template, default inputs = Helios |
| 7 | **Sponsor_Efficiency_Frontier_Model.xlsx** | Playbook Inputs / Feature Library / Efficiency Frontier — parameterised to Helios |

---

## 2. The complication you need to know about

The deliverables run **two different analyses**, and only one of them is driven by the Grifols model:

- **Analysis A — the option decomposition.** Six embedded options priced on 500 Monte Carlo paths; the yield decomposition. **This is what the Grifols model produces.** It already exists as Treatise Ch 18 and Playbook Ch 9. Every figure ties to the model.

- **Analysis B — the covenant-negotiation efficiency frontier.** V_lender, V_strategic, P(use), η ratios, tier rankings, the distress overlay. **These numbers are playbook *framework parameters* — they are not Grifols-model outputs and never were.** Project Helios is the worked example for Analysis B.

So "convert Helios to Grifols" for Analysis B cannot mean "pull figures from the model" — there are none to pull. It means re-skinning the *deal setup* (enterprise value, EBITDA, leverage, equity cheque) with Grifols numbers from the model's **LBO sheet**, while the per-feature η table stays illustrative.

**Three further frictions:**

1. **Treatise §15.1 vs Ch 18.** If §15.1's 17-line decomposition is "made Grifols," the treatise then carries *two different* Grifols decompositions with different numbers — directly contradicting the goal that every Grifols figure ties to the model.
2. **§15.2 and §15.3 cannot be Grifols.** Chapter 15 also holds "A US HY Bond with Disguised Portability" (§15.2) and "A Stressed Credit Facing an Uptier-Exchange Decision" (§15.3). Grifols has no disguised-portability problem and **never distresses** in the model (probability of covenant breach = 0). These two illustrate scenarios Grifols structurally does not present, so they must stay as labelled hypotheticals.
3. **LevFin_Options_Valuation_Model.xlsx will not tie to the penny.** It is a *parametric* model (closed-form Merton, binomial trees). The Grifols model is *500-path Monte Carlo*. Re-pointing the template at Grifols inputs gives directionally-Grifols values that will **not equal** the Grifols model's option values.

---

## 3. Recommended plan

### Part 1 — Re-anchor every Grifols figure (the original task)
Apply the reconciliation list already approved: Treatise Ch 18, Playbook Ch 9, Sponsor xlsx Grifols tab, Sponsor deck Slide 10. One decimal in tables, integers in prose. Filenames → v2.

### Part 2 — Eliminate Project Helios

| Location | Recommended action |
|---|---|
| **Treatise §15.1 + Table 3** | **Delete** the Project Helios subsection; renumber §15.2→15.1, §15.3→15.2. Ch 18 becomes the treatise's single Grifols worked example. (Avoids a conflicting second decomposition.) |
| **Treatise §15.2 / §15.3** | **Keep as labelled hypotheticals** — they cannot be Grifols (see friction 2). The named "Project Helios" still disappears. |
| **Credit deck Slide 8** | **Replace** with a Grifols worked-example slide — the six-option decomposition + yield decomposition from Ch 18 (model-driven, ties exactly). |
| **Playbook §4.3 + Chapter 6** | **Re-skin to a Grifols LBO**: deal setup taken from the model's LBO sheet (entry EBITDA €1,728m, entry EV €17,279m, total leverage 6.0x, sponsor equity €7,516m, ~4.75y hold, MOIC 2.9x, IRR 25%). The efficiency-frontier feature table (η, V_lender, V_strategic) stays illustrative — it is framework material, not model output. |
| **Sponsor deck Slides 6 & 9** | Re-skin to the Grifols LBO setup, consistent with the Playbook. |
| **Sponsor_Efficiency_Frontier_Model.xlsx** | Re-point the Playbook-Inputs deal cells to the Grifols LBO parameters; Feature Library η values stay illustrative. |
| **LevFin_Options_Valuation_Model.xlsx** | Re-point default Inputs to Grifols deal parameters; relabel Cover text from "Project Helios" to Grifols. Add one line noting it is a parametric companion — close to, not identical with, the Monte Carlo model. |

### What ties exactly vs. what is a re-skin
- **Ties exactly to the model:** all of Analysis A — Treatise Ch 18, Playbook Ch 9, Credit deck Grifols slide, Sponsor deck Slide 10, Sponsor xlsx Grifols tab.
- **Re-skin (Grifols deal parameters from the model; framework η values stay illustrative):** Playbook §4.3 & Ch 6, both Sponsor deck efficiency slides, both Excel template models.

---

## 4. Two decisions I need from you

**Decision 1 — Treatise §15.1.** Delete the Project Helios subsection (recommended — it would otherwise be a second, conflicting Grifols decomposition), or keep it converted into a short Grifols lead-in that points forward to Chapter 18?

**Decision 2 — The efficiency-frontier worked example** (Playbook §4.3 & Ch 6, Sponsor deck Slides 6 & 9, Sponsor xlsx). Project Helios is a €600m mid-cap LBO; a Grifols LBO is a €17bn-EV, €7.5bn-equity mega-deal — a workable but unusual "playbook" example. Options:
- **(a)** Re-skin it to the Grifols LBO (full "everything is Grifols").
- **(b)** Strip the "Project Helios" name and keep it as "a representative European LBO" — the fake project name disappears, the illustration stays generic and correctly-sized.
