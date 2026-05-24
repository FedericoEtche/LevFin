# Grifols v8 Deliverable Consistency Audit

Prepared: 2026-05-24  
Repository path: `C:\Users\Federico\Code\LevFin-Book`  
Source of record: `Grifols_Model_v8.xlsx`  
Scenario extracted: `Base`

## Method

- Read `Grifols_Model_v8.xlsx` with `openpyxl` in read-only, data-only mode.
- Parsed DOCX and PPTX text directly from OOXML package XML.
- Parsed companion XLSX files in read-only, data-only mode.
- No Office files were opened, recalculated, or modified.
- Extraction was run twice. Both runs returned the same source-value hash:
  `65d154252781de14b446369d88f80d822cab1d39df1d8fd8b40465bd5bd26b4b`.

Classification:

| Status | Meaning |
|---|---|
| PASS | Matches v8 within project rounding convention. |
| WARN | Directional, stylized, historical, or support-only item that should not be treated as current source-of-record text. |
| FAIL | Active deliverable figure or reference conflicts with v8, or creates control risk. |

## Source Values Pulled From v8

### Audited Actuals

| Metric | v8 value | Source |
|---|---:|---|
| FY2024 revenue | EUR 7,212.4m | `Dashboard!B55` |
| FY2025 revenue | EUR 7,524.0m | `Dashboard!C55` |
| FY2024 EBITDA | EUR 1,629.0m | `Dashboard!B57` |
| FY2025 EBITDA | EUR 1,693.1m | `Dashboard!C57` |
| FY2024 net income | EUR 212.8m | `Dashboard!B60` |
| FY2025 net income | EUR 500.2m | `Dashboard!C60` |
| 2024YE total assets | EUR 21,405.2m | `BS!F27` |
| 2025YE total assets | EUR 19,712.0m | `BS!J27` |
| 2024YE total equity | EUR 8,607.0m | `BS!F36` |
| 2025YE total equity | EUR 7,603.0m | `BS!J36` |

### Leverage

| Metric | v8 value | Source |
|---|---:|---|
| 2025Q4 covenant net leverage | 4.57x | `Covenants!J26` |
| 2026Q1 forecast launch net leverage | 4.05x | `Covenants!K26` |
| 2030Q4 net leverage | 2.35x | `Covenants!AD26` |

### Option Decomposition

| Component | v8 value | Source |
|---|---:|---|
| Merton credit-risk put | 0.0 bps | `Option_Pricing!B21` |
| Builder basket PV | EUR 1,321.4m | `Option_Pricing!B27` |
| Builder basket | 394.9 bps | `Option_Pricing!B28` |
| Equity cure | 0.0 bps | `Option_Pricing!B36` |
| ECF cash sweep | 0.0 bps | `Option_Pricing!B44` |
| Make-whole call | 13.8 bps | `Option_Pricing!B54` |
| Portability | 9.0 bps | `Option_Pricing!B63` |
| Net embedded optionality / fair spread | 417.6 bps | `Yield_Decomposition!B21` |

### Yield Bridge

| Metric | v8 value | Source |
|---|---:|---|
| Fair all-in yield | 867.6 bps | `Yield_Decomposition!B12` |
| Quoted all-in yield | 698.3 bps | `Yield_Decomposition!B14` |
| Quoted spread over risk-free | 248.3 bps | `Yield_Decomposition!B22` |
| Fair spread over risk-free | 417.6 bps | `Yield_Decomposition!B21` |
| Residual / mispricing | -169.4 bps | `Yield_Decomposition!B15` |

### LBO Outputs

| Metric | v8 value | Source |
|---|---:|---|
| Entry EBITDA | EUR 1,740.1m | `LBO!B13` |
| Entry enterprise value | EUR 17,400.7m | `LBO!B15` |
| Opening leverage | 6.0x | `LBO!B30` |
| Sponsor equity | EUR 7,569.3m | `LBO!B39` |
| Hold period | 4.75 years | `LBO!B69` |
| MOIC | 2.77x | `LBO!B119` |
| Annualized IRR | 23.9% | `LBO!B121` |

## Known First Findings

1. `PASS` - The option/yield bridge is aligned across the active books, decks, and the Sponsor Efficiency Frontier worked-example tab. The recurring rounded figures are 395 bps builder basket, 418 bps net optionality, 868 bps fair all-in yield, 698 bps quoted all-in yield, 248 bps quoted spread, and -170 bps residual.
2. `FAIL` - The LBO figures appear to drift. `Grifols_Model_v8.xlsx` now shows entry EBITDA of EUR 1,740.1m, entry EV of EUR 17,400.7m, sponsor equity of EUR 7,569.3m, MOIC of 2.77x, and IRR of 23.9%. Project memory and the efficiency-frontier LBO setup cite about EUR 1,728m, EUR 17,279m, EUR 7,516m, about 2.9x MOIC, and about 25% IRR.
3. `WARN` - `Grifols_ReAnchoring_Reconciliation.md` is a pre-v8/v2 workpaper. It should be treated as historical context, not as the current v8 control file.

## Active Deliverable Audit

| Deliverable | Status | Findings |
|---|---|---|
| `Credit_Optionality_Treatise.docx` | PASS / FAIL | Chapter 18 option/yield figures match v8. Paragraphs 663 and 752 describe the model as a "thirty-sheet" model, while v8 has 31 sheets. |
| `Sponsor_Negotiation_Playbook.docx` | PASS / FAIL | Chapter 9 option/yield figures match v8. Earlier LBO discussion cites EUR 1,728m EBITDA, EUR 17.3bn EV, about 2.9x MOIC, and 25% IRR, which conflict with current v8 LBO outputs. |
| `Credit_Optionality_Deck.pptx` | PASS | Slide 8 matches v8 on debt face, launch leverage, 500 paths, option decomposition, yield bridge, and residual. |
| `Sponsor_Negotiation_Deck.pptx` | PASS / WARN | Slide 10 matches v8 option/yield figures. Slides 6 and 9 are efficiency-frontier strategy summaries and should be refreshed if the LBO setup is changed. |
| `LevFin_Options_Valuation_Model.xlsx` | WARN | Cover states that `Grifols_Model_v8.xlsx` is the source of record and that this model is directional. Inputs include Grifols-labelled assumptions that do not need to equal v8, but should not be presented as source-of-record figures. |
| `Sponsor_Efficiency_Frontier_Model.xlsx` | PASS / FAIL | `Grifols Worked Example` tab matches v8 option/yield figures. `Playbook Inputs` carries the older LBO setup: EV EUR 17,279m, EBITDA EUR 1,728m, funded debt EUR 10,368m, sponsor equity EUR 7,516m. |

## Detailed Mismatch Checklist

### Priority 1 - LBO Re-Anchor Decision

| Status | Item | Current v8 | Conflicting reference | Action |
|---|---|---:|---|---|
| FAIL | Entry EBITDA | EUR 1,740.1m | `Sponsor_Negotiation_Playbook.docx` para 632 and `Sponsor_Efficiency_Frontier_Model.xlsx` `Playbook Inputs!C8` cite EUR 1,728m. | Decide whether v8 LBO should be changed back to the canonical setup or whether the deliverables should move to the v8 output. |
| FAIL | Entry EV | EUR 17,400.7m | Playbook para 632 and `Playbook Inputs!C5` cite about EUR 17.3bn / EUR 17,279m. | Same decision as above. |
| FAIL | Sponsor equity | EUR 7,569.3m | `Playbook Inputs!C10` cites EUR 7,516m; deck slide 9 references a EUR 7.5bn check. | Refresh after LBO source decision. |
| FAIL | MOIC | 2.77x | Playbook para 637 cites about 2.9x. | Refresh after LBO source decision. |
| FAIL | Annualized IRR | 23.9% | Playbook para 637 cites 25%. | Refresh after LBO source decision. |

### Priority 2 - Active Text Control Fixes

| Status | Location | Extracted text / issue | Action |
|---|---|---|---|
| FAIL | `Credit_Optionality_Treatise.docx`, para 663 | Describes the Grifols model as a "thirty-sheet quarterly model." | Change to 31-sheet. |
| FAIL | `Credit_Optionality_Treatise.docx`, para 752 | Describes the Grifols model as a "thirty-sheet IFRS quarterly model." | Change to 31-sheet. |
| FAIL | `Sponsor_Negotiation_Playbook.docx`, para 632 | Cites EUR 1,728m LTM EBITDA and EUR 17.3bn EV. | Re-anchor after LBO decision. |
| FAIL | `Sponsor_Negotiation_Playbook.docx`, para 637 | Cites about 2.9x MOIC and 25% annualized IRR. | Re-anchor after LBO decision. |

### Priority 3 - Directional Companion Controls

| Status | Location | Extracted text / issue | Action |
|---|---|---|---|
| WARN | `LevFin_Options_Valuation_Model.xlsx`, `Cover!B36` | Says the workbook is directional and `Grifols_Model_v8.xlsx` is source of record. | No edit required if this remains purely directional. |
| WARN | `LevFin_Options_Valuation_Model.xlsx`, `Inputs!B4` | Enterprise value input is EUR 18,194m, labelled as Grifols mean enterprise value. | If the workbook is marketed as Grifols-default, refresh or add a clearer directional-only note. |
| WARN | `LevFin_Options_Valuation_Model.xlsx`, `Inputs!B10` | Opening leverage is 4.48x and note references Grifols at about 4.8x. | If the workbook is marketed as Grifols-default, refresh or add a clearer directional-only note. |
| FAIL | `Sponsor_Efficiency_Frontier_Model.xlsx`, `Playbook Inputs` | LBO setup uses older EV, EBITDA, debt, and sponsor equity figures. | Refresh once the LBO source decision is made. |

## Supporting Files

| File | Status | Finding |
|---|---|---|
| `Grifols_Model_v8_TieOut_Memo_20260524.docx` | PASS | Correctly identifies `Grifols_Model_v8.xlsx` as source-of-record and supersedes the pre-v8 memo. |
| `Grifols_Option_Layer_CrossCheck.docx` | WARN | Subtitle says it benchmarks `Grifols_Model_v7`. Treat as support-only unless updated to v8. |
| `Grifols_Model_v6_Assessment.docx` | WARN | Explicitly v6-vintage and should stay support-only. |
| `Grifols_ReAnchoring_Reconciliation.md` | WARN | Pre-v8/v2 reconciliation list. Consider moving to archive or adding a superseded banner later. |

## Recommended Next Cleanup Sequence

1. Decide the LBO source-of-record: keep current v8 LBO outputs, or revise v8 to the prior canonical efficiency-frontier setup.
2. Update the LBO-dependent book/deck/workbook language after that decision.
3. Fix the "thirty-sheet" references in the lender treatise to 31-sheet.
4. Add a superseded banner to `Grifols_ReAnchoring_Reconciliation.md` or move it to `Archive`.
5. Review the directional `LevFin_Options_Valuation_Model.xlsx` labels so readers do not treat its Grifols-labelled inputs as source-of-record figures.

## Non-Changes Confirmed

- No `.docx`, `.pptx`, `.xlsx`, `.xls`, or `.pdf` files were edited for this audit.
- The audit is a Markdown control artifact only.
