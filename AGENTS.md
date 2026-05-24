# LevFin Book — Project Memory

## What this is

A two-book leveraged-finance project, each closing with a fully worked **Grifols, S.A.** example
(the Spanish plasma-derivatives group):

- **The Optionality of Credit Agreements** — lender-side treatise — `Credit_Optionality_Treatise.docx`
- **The Sponsor's Negotiation Playbook** — sponsor-side — `Sponsor_Negotiation_Playbook.docx`

The worked example is a 31-sheet integrated credit model whose option-pricing layer decomposes the
credit's quoted spread into named, individually-priced embedded options. This folder is the active
deliverable set; it also contains older book-manuscript material (`chapter_*.txt`,
`LevFin_Book_Compiled_Manuscript*.docx`, etc.) that is **not** part of the active Grifols work.

## The deliverable set — keep all six + the model mutually consistent

| File | Role |
|---|---|
| `Grifols_Model_v8.xlsx` | The integrated model — **source of record for every figure** |
| `Credit_Optionality_Treatise.docx` | Lender treatise; Ch 18 = Grifols worked example |
| `Sponsor_Negotiation_Playbook.docx` | Sponsor playbook; Ch 9 = Grifols decomposition |
| `Credit_Optionality_Deck.pptx` | Lender deck; Slide 8 = Grifols |
| `Sponsor_Negotiation_Deck.pptx` | Sponsor deck; Slide 10 = Grifols |
| `LevFin_Options_Valuation_Model.xlsx` | Parametric option-pricing companion (directional only) |
| `Sponsor_Efficiency_Frontier_Model.xlsx` | Efficiency-frontier model; "Grifols Worked Example" tab |

Supporting analysis: `Grifols_Actuals_Reference.xlsx` (8-quarter audited-actuals backbone),
`Grifols_Option_Layer_CrossCheck.docx`, `Grifols_Model_v6_Assessment.docx` (v6-vintage).
Superseded models: `Grifols_Model_v6.xlsx`, `v7.xlsx`; v1–v5 are in `Archive/`.

**RULE: any change to the model's figures must be re-anchored across all six deliverables.**
They currently all cite v8. The six chapters/slides quote the same numbers — do not let them drift.

## The model — Grifols_Model_v8.xlsx

- 31 sheets, ~89,000 formulas, 28 quarters (2024Q1–2030Q4), IFRS basis, 12 charts.
- Historical periods (2024–2025) are **hardcoded to Grifols' reported actuals**; the forecast engine
  drives 2026Q1–2030Q4, rolling from the 2025 year-end.
- Scenario selector at `Control!B5` (Base / Upside / Downside).
- Monte Carlo engine: `MC_Engine` (~64,000 formulas, 500 paths) → `MC_Summary`.
- `FX` sheet — currency-translation engine across balance sheet, P&L and cash flow; base case is
  flat-rate (zero impact). Flex `FX!` row 10 (EUR/USD) to run a currency scenario.
- Option layer: `Option_Pricing` → `Yield_Decomposition`.
- Statement sheets: `IS`, `BS`, `CF`, `Debt`, `Covenants`, `LBO`.

## Canonical v8 figures — every deliverable ties to these

- **Audited tie-out:** 2024YE total assets €21,405m / equity €8,606m; 2025YE €19,712m / €7,603m.
  FY2024 revenue €7,212m, EBITDA €1,629m, net income €213m; FY2025 €7,524m / €1,693m / €500m.
- **Leverage:** 2025 net leverage 4.57x; 2026 forecast launch 4.0x; delevers toward ~2.4x by 2030.
- **Option decomposition (annualised bps):** Merton credit-risk put 0 · builder basket 395 ·
  equity cure 0 · ECF cash sweep 0 · make-whole call 14 · portability 9 → **net optionality 418**.
- **Yield:** fair all-in yield 868 · quoted all-in yield 698 · quoted spread over RF 248 ·
  fair spread 418 · **residual / mispricing −170**.
- **LBO (efficiency-frontier setup):** entry EBITDA €1,728m, entry EV €17,279m, 6.0x leverage,
  sponsor equity €7,516m, ~4.75y hold, MOIC ~2.9x, IRR ~25%.

## How the model reached v8 — do not undo these

Rebuilt in stages: cost-of-debt rates corrected → FX-translation correction so the balance sheet
ties to the audited accounts → FY2024 tax one-off → **historical periods re-architected to reported
actuals** → **FX section** added (balance sheet, then extended to P&L + cash flow) → projection
revenue **recalibrated to a seasonal ~3.5% constant-currency path** (replacing a flat 0.8%/qtr that
lost seasonality) → **make-whole call re-priced** as an American call on loan value via a Haug CRR
binomial lattice (replacing a crude expected-cost calc). v1–v7 are superseded.

## Conventions

- **Rounding:** one decimal place in tables; integers in prose.
- **Editing the model:** it carries 12 charts and the ~64k-formula MC engine. Edit cell values with
  `openpyxl` (or XML surgery), then **recalculate with LibreOffice** (the `xlsx` skill's `recalc.py`)
  — openpyxl writes formulas but does not compute them.
- Debt is carried on the Credit-Agreement (ex-IFRS-16) basis for the leverage covenant.

## Known open items / limitations

- **Builder-basket discounting** — the dominant option (≈94% of optionality). The model discounts
  capacity from the 5-year horizon (395 bps); an accrual-date basis gives ~436 bps. Open judgment call.
- **Make-whole** loan-value volatility is set to 6% (≈ modified duration 4.1 × ~135 bp yield vol);
  sensitivity band 9–21 bps.
- A €238m retained-earnings bridge (`Equity!J41`) holds the projection balanced against the 2025Q4
  model-level asset composition — documented, affects no deliverable figure.
- The projection growth assumption was optimistic pre-recalibration; keep it aligned with Grifols'
  constant-currency guidance.

## Source material

Grifols audited consolidated annual accounts (2023, 2024, 2025) and quarterly reports are in this
folder. The Haug option-pricing library (33 workbooks) used to cross-check the option layer is in a
separate `Options` folder on the desktop.
