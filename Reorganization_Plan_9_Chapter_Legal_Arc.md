# Reorganization Plan: The 9-Chapter Legal & Documentation Arc

**Date:** April 7, 2026
**Purpose:** Map the proposed 9-chapter structure against all existing manuscript content, showing exactly what moves where, what's new, and what gets consolidated.

---

## Proposed Structure vs. Current Manuscript

The proposed 9-chapter arc would replace the current Parts III, IV, and V (roughly chapters 12-28), consolidating ~15 existing chapters into a tighter, narrative-driven sequence. The remaining chapters (Parts I-II, VI-VIII) would be unaffected.

---

## CHAPTER-BY-CHAPTER MAPPING

### NEW Ch. 1: The European Leveraged Loan Market — From Maintenance to Cov-Lite

**Theme:** The "bondification" of European loans as the central organizing thesis.

| Source Content | Current Location | Action |
|---|---|---|
| LMA vs bond-style documentation history | `chapter_eu_vs_us_documentation.txt` — "STRUCTURAL AND HISTORICAL CONTEXT" section | **MOVE** entire section |
| Covenant-lite movement and consequences | `chapter_financial_covenants.txt` — §19.1 "The Covenant-Lite Revolution" | **MOVE** |
| Convergence of EU and US documentation | `chapter_eu_vs_us_documentation.txt` — "CONVERGENCE AND DIVERGENCE" section | **MOVE** |
| Maintenance vs incurrence regimes | `chapter_covenant_fundamentals.txt` — §7.2 "Maintenance vs. Incurrence" | **MOVE** |
| The springing covenant: RCF protection | `chapter_covenant_fundamentals.txt` — §7.4 "The Springing Covenant" | **MOVE** |
| Market trend: less protection, more risk | `chapter_financial_covenants.txt` — §19.9 "The Market Trend" | **MOVE** |

**Content gap — NEW WRITING needed:**
- A unified "bondification thesis" narrative tying these sections together
- Updated market statistics (% cov-lite in EU, convergence metrics)
- The role of CLO demand in driving cov-lite adoption (cross-ref from `chapter_clo_mechanics.txt`)

---

### NEW Ch. 2: Structural Architecture — The Restricted Group, Guarantors, and the ICA

**Theme:** How the European credit structure is built — who's in, who's out, who pays first.

| Source Content | Current Location | Action |
|---|---|---|
| Restricted group concept | `chapter_covenant_fundamentals.txt` — §7.3 "The Restricted Group Concept" | **MOVE** |
| Restricted group architecture (enriched) | `chapter_debt_liens_expanded.txt` — "RESTRICTED GROUP ARCHITECTURE" section | **MOVE** |
| Unrestricted subsidiaries primer (enriched) | `chapter_debt_liens_expanded.txt` — "UNRESTRICTED SUBSIDIARIES" section | **MOVE** |
| Guarantor coverage — the 80% illusion (enriched from 9fin) | `chapter_debt_liens_expanded.txt` — "GUARANTOR COVERAGE MECHANICS" section | **MOVE** |
| Single point of enforcement (enriched from 9fin) | `chapter_debt_liens_expanded.txt` — "SINGLE POINT OF ENFORCEMENT" section | **MOVE** |
| Agreed Security Principles | `chapter_guarantee_collateral.txt` — §14.2 "Agreed Security Principles" | **MOVE** |
| Hollow Guarantor Coverage Test | `chapter_guarantee_collateral.txt` — §14.3 "The Hollow Guarantor Coverage Test" | **MOVE** |
| Guarantee Release / Chewy Phantom | `chapter_guarantee_collateral.txt` — §14.4 "Guarantee Release Provisions" | **MOVE** |
| Intercreditor Agreement mechanics | `chapter_guarantee_collateral.txt` — §14.5 "The Intercreditor Agreement" | **MOVE** |
| ICA: Europe's Structural Defense (enriched) | `chapter_amend_extend.txt` — §17.11 "The Intercreditor Agreement" | **MOVE** (consolidate with above) |
| Soft security reality | `chapter_guarantee_collateral.txt` — §14.6 "The Soft Security Reality" | **MOVE** |
| Structural subordination risk mapping | `chapter_guarantee_collateral.txt` — §14.7 "Structural Subordination Risk Mapping" | **MOVE** |
| EU guarantor/security packages | `chapter_eu_vs_us_documentation.txt` — "GUARANTOR AND SECURITY PACKAGES" section | **MOVE** (consolidate) |
| EU security trust structure | `chapter_debt_liens_expanded.txt` — "THE SECURITY TRUST STRUCTURE" section | **MOVE** |
| Cross-border considerations | `chapter_debt_liens_expanded.txt` — "CROSS-BORDER CONSIDERATIONS" section | **MOVE** |

**Content gap:** None — this is the most content-rich chapter thanks to the 9fin enrichments. May actually need trimming.

---

### NEW Ch. 3: The Restricted Payments Covenant — Value Leakage and Its Prevention

**Theme:** How value leaves the credit box.

| Source Content | Current Location | Action |
|---|---|---|
| Full chapter | `chapter_restricted_payments_expanded.txt` — ALL sections (20.1-20.10) | **MOVE** entire chapter |
| RP covenant comparison EU vs US | `chapter_eu_vs_us_documentation.txt` — "RESTRICTED PAYMENTS AND DISTRIBUTIONS" section | **MERGE** into RP chapter |
| Investment covenant interaction | `chapter_restricted_payments_expanded.txt` — §20.6 already covers this | **KEEP** as-is |

**Content gap:**
- Could be enriched with the 6 Restricted Payments files from the 9fin Legal Research Index (builder baskets, permitted payments, CNI baskets, Available Amount, payment restrictions in ICAs, using RPs to pay parent debt) — these were flagged as "strong existing coverage" in the gap analysis but could add depth

---

### NEW Ch. 4: The Debt and Liens Covenants — Capacity, Ratio Tests, and Permitted Baskets

**Theme:** How additional leverage gets layered on.

| Source Content | Current Location | Action |
|---|---|---|
| Debt covenant in HY bonds | `chapter_debt_liens_expanded.txt` — "THE DEBT COVENANT IN HIGH YIELD BONDS" through "CONTRIBUTION DEBT" | **MOVE** |
| Permitted debt baskets taxonomy | `chapter_debt_liens_expanded.txt` — "PERMITTED DEBT BASKETS AND THEIR TAXONOMY" | **MOVE** |
| Ratio test for debt incurrence | `chapter_debt_liens_expanded.txt` — "THE RATIO TEST" | **MOVE** |
| Debt covenant in leveraged loans | `chapter_debt_liens_expanded.txt` — "THE DEBT COVENANT IN LEVERAGED LOANS" through "AVAILABLE AMOUNT FOR INCREMENTAL DEBT" | **MOVE** |
| Liens covenant in HY bonds | `chapter_debt_liens_expanded.txt` — "THE LIENS COVENANT IN HIGH YIELD BONDS" through "RATIO-BASED LIEN BASKETS" | **MOVE** |
| Liens covenant in loans | `chapter_debt_liens_expanded.txt` — "THE LIENS COVENANT IN LEVERAGED LOANS" through "INCREMENTAL EQUIVALENT DEBT" | **MOVE** |
| Interaction between debt and liens | `chapter_debt_liens_expanded.txt` — "THE INTERACTION BETWEEN DEBT AND LIENS" | **MOVE** |
| EU vs US permitted debt/lien baskets | `chapter_eu_vs_us_documentation.txt` — "PERMITTED DEBT AND LIEN BASKETS" section | **MERGE** |
| EBITDA definitions and adjustments | `chapter_ebitda_expanded.txt` — §18.2-18.6 (core EBITDA mechanics) | **MOVE** or cross-reference |
| EBITDA in the covenant architecture | `chapter_ebitda_expanded.txt` — §18.7 | **MOVE** |
| Accordion/incremental mechanics | `chapter_accordion_incremental.txt` — ALL sections | **MOVE** (this is the operational application of debt baskets) |

**Content gap:**
- The accordion chapter (461 lines) is substantial. Could either be fully absorbed here or remain as a sub-chapter/appendix if Ch.4 becomes too long.
- The EBITDA chapter (764 lines) is also large. Consider whether it stays as a standalone chapter or the core mechanics move into Ch.4 while the "adjustment games" section moves to Ch.6 (Advanced Basket Mechanics).

**Decision point:** EBITDA is currently its own chapter (764 lines). Options:
- **(A)** Keep EBITDA standalone, cross-referenced from Ch.4 and Ch.6
- **(B)** Split: core definitions (§18.1-18.6) into Ch.4, adjustment games and manipulation (§18.7-18.9) into Ch.6
- **(C)** Move entirely into Ch.4 (makes it very large)

---

### NEW Ch. 5: Asset Sales, Change of Control, and Portability

**Theme:** How assets leave and who owns the box.

| Source Content | Current Location | Action |
|---|---|---|
| Full asset sales chapter | `chapter_asset_sales_coc.txt` — §21.1-21.8 (Part A) | **MOVE** |
| Full change of control chapter | `chapter_asset_sales_coc.txt` — §22.1-22.8 (Part B) | **MOVE** |
| Portability mechanics (enriched from 9fin) | `chapter_asset_sales_coc.txt` — §22.4A | **MOVE** |
| Disguised portability (enriched from 9fin) | `chapter_asset_sales_coc.txt` — §22.4B | **MOVE** |
| IPO implications for debt (enriched from 9fin) | `chapter_asset_sales_coc.txt` — §22.4C | **MOVE** |

**Content gap:** None — this chapter is already well-developed (615 lines) with the 9fin enrichments. Consider whether CoC/portability (§22.1-22.4C) should be split into its own sub-chapter given the volume of the portability material.

---

### NEW Ch. 6: Advanced Basket Mechanics — Super Growers, Universal Reallocation, and the Enabler Playbook

**Theme:** The frontier of documentation innovation — how sponsors build flexibility.

| Source Content | Current Location | Action |
|---|---|---|
| Decoy baskets and capacity reclassification | `chapter_liability_management.txt` — §5.1 | **MOVE** |
| Disregarded debt and ratio manipulation | `chapter_liability_management.txt` — §5.2 | **MOVE** |
| Super growers and high water marking | `chapter_liability_management.txt` — §5.3 | **MOVE** |
| Evergreen baskets and capacity recycling | `chapter_liability_management.txt` — §5.4 | **MOVE** |
| Capacity fungibility and reclassification | `chapter_restricted_payments_expanded.txt` — §20.5 | **MOVE** or cross-reference |
| EBITDA manipulation and add-back games | `chapter_ebitda_expanded.txt` — §18.5 "THE CAP GAME" and §18.9 "AUDITOR COMFORT" | **MOVE** (if EBITDA is split per option B above) |
| High water marking / super grower (9fin source) | 9fin "EBITDA and Financial Calculations" folder | Already incorporated into LME chapter |
| Ratio-no-worse provisions (9fin source) | 9fin "EBITDA and Financial Calculations" folder | Could be expanded here |

**Content gap — NEW WRITING needed:**
- This chapter would be largely extracted from the LME chapter's enabler sections (§5.1-5.4), but it needs a narrative frame: why these provisions exist, how they evolved, and how they interact with each other to create compounding flexibility
- The "pick-your-poison" concept (reallocation across RP/PI/debt baskets) needs a worked example
- The QXO transaction as an extended case study of extreme enabler provisions

---

### NEW Ch. 7: Voting, Amendments, and the Consent Architecture

**Theme:** Who controls the documents and how.

| Source Content | Current Location | Action |
|---|---|---|
| Consent hierarchy: loans vs bonds | `chapter_amend_extend.txt` — §17.9 | **MOVE** |
| Sacred rights and the "not-so-sacred" trap | `chapter_amend_extend.txt` — §17.10 | **MOVE** |
| Disenfranchisement tactics | `chapter_amend_extend.txt` — §17.12 | **MOVE** |
| Yank-a-bank mechanism | `chapter_amend_extend.txt` — §17.13 | **MOVE** |
| Open market purchases and Dutch auctions | `chapter_amend_extend.txt` — §17.14 | **MOVE** |
| Exit consents and covenant stripping | `chapter_amend_extend.txt` — §17.15 | **MOVE** |
| Snooze-to-lose mechanics | `chapter_amend_extend.txt` — §17.16 | **MOVE** |
| Structural loan changes | `chapter_amend_extend.txt` — §17.17 | **MOVE** |
| EU vs US amendment/waiver mechanics | `chapter_eu_vs_us_documentation.txt` — "AMENDMENT AND WAIVER MECHANICS" section | **MERGE** |
| Covenant suspension mechanics | `chapter_financial_covenants.txt` — §19.10 | **MOVE** |
| Release conditions in SFAs | Already in §19.10.2 | **MOVE** with above |

**Content gap:** None — this is extremely well-covered after the voting/amendments enrichment.

---

### NEW Ch. 8: Creditor-on-Creditor Violence — LMEs, Uptiers, and Drop-Downs

**Theme:** The climax — how everything breaks.

| Source Content | Current Location | Action |
|---|---|---|
| Full LME chapter minus enabler sections | `chapter_liability_management.txt` — §1-4 and §6-8 | **MOVE** (§5 enablers moved to Ch.6) |
| Uptier exchange mechanics (US + EU) | `chapter_liability_management.txt` — §2, 2.1, 2.2 | **KEEP** |
| J.Crew drop-down | `chapter_liability_management.txt` — §3.1-3.3 | **KEEP** |
| Full blocker taxonomy | `chapter_liability_management.txt` — §4.1-4.4 | **KEEP** |
| Cooperation agreements | `chapter_liability_management.txt` — §6 | **KEEP** |
| EU vs US LME mechanics | `chapter_liability_management.txt` — §7 | **KEEP** |
| Priming: the five forms | `chapter_debt_liens_expanded.txt` — "PRIMING: THE FIVE FORMS" through "ANTI-PRIMING PROVISIONS" | **MOVE** (consolidate with LME chapter) |
| Serta/J.Crew in distressed context | `chapter_distressed_debt.txt` — "THE SERTA, J. CREW, AND ENVISION PLAYBOOK" section | Cross-reference (don't duplicate) |

**Content gap:**
- Consider adding a "Timeline of Major LMEs" as a reference table
- The 9fin "Recent Trends" files (4 files on investor hot topics, distressed disposal, seasonal covenant updates) could add market color here

---

### NEW Ch. 9: When Documents Fail — Defaults, Restructuring, and Endgame Scenarios

**Theme:** The consequences.

| Source Content | Current Location | Action |
|---|---|---|
| Full events of default chapter | `chapter_events_of_default.txt` — ALL sections | **MOVE** |
| A&E core mechanics (not voting sections) | `chapter_amend_extend.txt` — §17.1-17.8 | **MOVE** |
| UK restructuring tools | `chapter_uk_restructuring.txt` — ALL sections | **MOVE** or keep as standalone |
| Distressed debt chapter | `chapter_distressed_debt.txt` — ALL sections | **MOVE** or keep as standalone |
| EU vs US restructuring/enforcement | `chapter_eu_vs_us_documentation.txt` — "RESTRUCTURING AND ENFORCEMENT DIFFERENCES" section | **MERGE** |

**Content gap:** None structurally, but this is very large (Events of Default: 413 lines + A&E core: ~350 lines + UK Restructuring: 593 lines + Distressed: 444 lines = ~1,800 lines). Consider whether this should be split into Ch.9a (Defaults + A&E) and Ch.9b (Restructuring + Distressed), making it a 10-chapter arc.

---

## WHAT HAPPENS TO THE EU vs. US DOCUMENTATION CHAPTER?

The current `chapter_eu_vs_us_documentation.txt` (767 lines, the largest single chapter) would be **disaggregated** across the new structure:

| Current Section | New Destination |
|---|---|
| Structural and Historical Context | **Ch.1** (bondification thesis) |
| Credit Agreement Structure | **Ch.1** (two architectures) |
| Guarantor and Security Packages | **Ch.2** (structural architecture) |
| Covenant Frameworks | **Ch.1** (cov-lite convergence) |
| Restricted Payments and Distributions | **Ch.3** (RP chapter) |
| Permitted Debt and Lien Baskets | **Ch.4** (debt/liens chapter) |
| Transfer and Assignment | Stays in **Part VII** (Secondary Market chapter) |
| Amendment and Waiver Mechanics | **Ch.7** (voting/amendments) |
| Events of Default and Remedies | **Ch.9** (defaults/endgame) |
| Intercreditor Agreement | **Ch.2** (structural architecture) |
| HY Bond Documentation | **Ch.4** or remains standalone reference |
| Direct Lending Documentation | Stays in **Part II** (Direct Lending chapter) |
| Restructuring Differences | **Ch.9** (restructuring) |
| Convergence and Divergence | **Ch.1** (conclusion) |

This is the right move. The current EU vs. US chapter is a 767-line omnibus that touches everything but goes deep on nothing. Distributing its content into the relevant topical chapters makes each chapter more complete while eliminating the need for a separate comparison chapter.

---

## REMAINING CHAPTERS (UNAFFECTED)

These chapters sit outside the legal/documentation arc and would keep their current structure:

**Part I: Foundations** — Ch.1-3 (What is LevFin, Ecosystem, Economics of Leverage)
**Part II: Instruments** — Ch.6-11 (Anatomy, Loans vs Bonds, Capital Structure, HY Bonds, Direct Lending, CLOs)
**Part VI: Analytical Tools** — Ch.29-35 (Credit Analysis, Working Capital, Rating Agencies, Financial Modeling, LBO Modeling, Case Studies)
**Part VII: Market Context** — Ch.36-39 (Secondary Market, Regulatory, Tax, ESG)
**Part VIII: The Profession** — Ch.40-43 (Twenty Years, Communication, Career, Personal Brand)

---

## SUMMARY: CONTENT FLOW

| New Chapter | Primary Sources (current files) | Lines | Status |
|---|---|---|---|
| **1. Bondification** | eu_vs_us (partial), covenant_fundamentals, financial_covenants (partial) | ~400 est. | Needs new narrative frame |
| **2. Structural Architecture** | guarantee_collateral (full), debt_liens (4 enriched sections), amend_extend (ICA section), eu_vs_us (partial) | ~600 est. | Well-covered, needs consolidation |
| **3. Restricted Payments** | restricted_payments_expanded (full), eu_vs_us (partial) | ~300 est. | Mostly complete, could expand with 9fin |
| **4. Debt & Liens** | debt_liens (core sections), ebitda (partial or full), accordion (full), eu_vs_us (partial) | ~1,200 est. | Largest chapter — may need splitting |
| **5. Asset Sales & CoC** | asset_sales_coc (full) | ~615 | Complete with 9fin enrichments |
| **6. Advanced Baskets** | liability_management §5 (enablers), ebitda (partial), restricted_payments §20.5 | ~350 est. | Needs new narrative frame |
| **7. Voting & Amendments** | amend_extend §17.9-17.17, financial_covenants §19.10, eu_vs_us (partial) | ~500 est. | Very well-covered |
| **8. LMEs** | liability_management §1-4, §6-8, debt_liens (priming sections) | ~350 est. | Complete |
| **9. Defaults & Endgame** | events_of_default (full), amend_extend §17.1-17.8, uk_restructuring (full), distressed_debt (full), eu_vs_us (partial) | ~1,800 est. | Very large — consider splitting |

**Total estimated:** ~6,100 lines across 9 chapters (vs. ~8,300 lines across 15 current chapters — consolidation eliminates ~25% redundancy)

---

## KEY DECISIONS NEEDED

1. **EBITDA:** Keep standalone, split across Ch.4 and Ch.6, or absorb entirely into Ch.4?
2. **Accordion/Incremental:** Absorb into Ch.4 or keep as sub-chapter?
3. **Ch.9 size:** Keep as single chapter (~1,800 lines) or split into 9a (Defaults + A&E) and 9b (Restructuring)?
4. **EU vs. US disaggregation:** Full disaggregation (recommended) or maintain a slimmed-down comparison chapter?
5. **Chapter numbering:** Renumber the entire book, or keep the legal arc as a "Part" with its own internal numbering?
