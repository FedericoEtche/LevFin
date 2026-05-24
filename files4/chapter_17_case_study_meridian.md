# Chapter 17: Case Study — Meridian Plasma Group

*The following case study is based on a composite of publicly available information about companies in the plasma therapeutics sector. Company name, specific figures, and certain details have been adjusted for teaching purposes. Any resemblance to actual transaction outcomes is coincidental.*

---

## The Opportunity

It's March 2024. You're a Vice President at Helios Capital Partners, a €65 billion European alternative asset manager investing across private equity, credit, and infrastructure. Your Managing Director has just forwarded you an email from Deutsche Bank's Financial Sponsors Group:

> "Meridian Plasma Group — potential take-private. Family shareholders exploring strategic options following recent market dislocation. Indicative EV €14-16bn. Preliminary materials attached. Expression of interest due in two weeks."

Meridian is one of the world's largest plasma therapeutics companies — a business you've tracked for years but never seriously underwritten because the founding family maintained tight control and the valuation never made sense. Now, after a turbulent twelve months that saw the stock drop 40% from its peak, the family is finally ready to talk.

Your MD's message is brief: "This could be interesting. Build the model. Let's see if the math works."

---

## Company Overview

### History and Ownership

Meridian Plasma Group S.A. traces its origins to 1912, when Dr. Henrik Lindqvist established a clinical laboratory in Stockholm focused on blood analysis and transfusion medicine. The company pioneered early plasmapheresis techniques in the 1950s and began commercial plasma fractionation in the 1970s.

Through a series of acquisitions — most notably Atlantis Biologics (US, 2011) and Nordic Plasma Systems (Germany, 2022) — Meridian transformed from a regional European player into a global leader. Today, it operates the world's second-largest private plasma collection network and ranks among the top three plasma-derived medicine manufacturers globally.

The Lindqvist family retains approximately 31% of voting rights through a dual-class share structure (Class A: one vote per share; Class B: ten votes per share). The family has held board seats continuously since founding, though day-to-day management transitioned to professional executives in 2019 following governance reforms.

**Current Listings:**
- Stockholm Stock Exchange (Primary): MPG, MPG-B
- NASDAQ (ADR): MPGR

**Employees:** ~24,500 globally

**Headquarters:** Stockholm, Sweden (operational HQ in Dublin for tax purposes)

---

## Business Segments

### Biotherapeutics (76% of FY2023 Revenue)

Meridian's core business transforms donated human plasma into life-saving therapeutic proteins through a complex manufacturing process called fractionation.

**Product Portfolio:**

| Product Category | Key Products | FY2023 Revenue | Growth | Use Cases |
|------------------|--------------|----------------|--------|-----------|
| Immunoglobulins | Immunex IV, Immunex SC | €3,420m | +14% | Primary/secondary immunodeficiency, neurological disorders |
| Albumin | Albunex 20%, 25% | €1,580m | +18% | Critical care, liver disease, surgery |
| Alpha-1 Antitrypsin | Prolunex | €485m | +3% | Genetic emphysema (Alpha-1 deficiency) |
| Specialty Products | Factor VIII, Fibrinogen, Hyperimmunes | €415m | +7% | Hemophilia, bleeding disorders, specific infections |
| **Total Biotherapeutics** | | **€5,900m** | **+12%** | |

**Market Position:**
- #2 globally in immunoglobulins (behind CSL Behring)
- #1 in Europe for albumin
- #3 globally in Alpha-1 antitrypsin

**Why Plasma Cannot Be Replaced:**

Unlike most pharmaceuticals, plasma-derived therapies cannot be synthesized. Each product requires human plasma as the raw material. A single Alpha-1 patient requires plasma from approximately 900 donations per year for treatment. An immunodeficiency patient on IVIG therapy requires 130+ donations annually.

This biological constraint creates:
- Permanent supply limitations (donor pool is finite)
- High barriers to entry (building collection networks takes decades)
- Pricing power in undersupplied markets
- Captive, chronic patient populations

### Diagnostics (11% of FY2023 Revenue)

Meridian's Diagnostics division supplies blood banks, hospitals, and laboratories with testing equipment and reagents.

| Product Line | FY2023 Revenue | Growth | Description |
|--------------|----------------|--------|-------------|
| NAT Screening | €310m | +2% | Nucleic acid testing for blood-borne pathogens |
| Blood Typing Solutions | €285m | +11% | Immunohematology reagents and analyzers |
| Immunoassays | €115m | +8% | Infectious disease and specialty testing |
| **Total Diagnostics** | **€710m** | **+5%** | |

Business model: Razor/razorblade. Place analyzers (often via rental/lease), generate recurring revenue from reagent sales and service contracts.

### Bio Supplies (5% of FY2023 Revenue)

Sells biological materials — plasma fractions, proteins, and specialty reagents — to research institutions, clinical trial sponsors, and other manufacturers.

| Category | FY2023 Revenue | Notes |
|----------|----------------|-------|
| Research reagents | €195m | Universities, pharma R&D |
| Clinical trial materials | €95m | Biotech customers |
| Manufacturing inputs | €70m | Third-party fractionators |
| **Total Bio Supplies** | **€360m** | |

### Corporate / Eliminations

Intercompany sales and unallocated corporate costs: (€120m)

### **Consolidated Revenue: €6,850m**

---

## The Plasma Value Chain

Understanding Meridian's economics requires understanding the plasma value chain. This is where the operational complexity — and the modeling challenge — lives.

### Stage 1: Plasma Collection

**The Network:**

Meridian operates 385 plasma donation centers globally:
- United States: 295 centers
- Germany (via Nordic Plasma acquisition): 62 centers  
- Hungary: 18 centers
- Egypt: 10 centers (joint venture, expanding)

Centers are located in areas where paid plasma donation is legal. The United States dominates global plasma supply (~70% of world production) because it permits donor compensation while most of Europe prohibits it.

**Center Economics:**

A typical U.S. plasma center:

| Metric | Value | Notes |
|--------|-------|-------|
| Annual plasma collections | 38,000-45,000 liters | Varies by location, donor demographics |
| Collections per day | 120-150 donations | ~250 operating days/year |
| Plasma per donation | ~800-880 mL | Based on donor weight |
| Donors per center | 8,000-12,000 registered | ~30% active in any month |
| Staff per center | 25-35 FTEs | Phlebotomists, nurses, admin |
| Center size | 8,000-12,000 sq ft | Leased space typical |

**Cost Per Liter (CPL):**

This is the most important operational metric in the plasma business.

| Cost Component | % of CPL | FY2023 | Notes |
|----------------|----------|--------|-------|
| Donor compensation | 38% | €72/liter | Fees paid to donors |
| Labor | 28% | €53/liter | Center staff wages/benefits |
| Facilities | 14% | €27/liter | Rent, utilities, maintenance |
| Testing & supplies | 12% | €23/liter | Screening tests, collection kits |
| Other overhead | 8% | €15/liter | IT, insurance, compliance |
| **Total CPL** | **100%** | **€190/liter** | Down from €245 peak (July 2022) |

**CPL Trajectory:**

The COVID-19 pandemic severely disrupted plasma collections. Donors — often lower-income individuals for whom compensation is meaningful — faced competing demands on their time (childcare, gig work paying better). Donor fees spiked to attract supply:

| Period | Avg. Donor Fee (US) | CPL | Collections YoY |
|--------|---------------------|-----|-----------------|
| Q4 2019 (Pre-COVID) | $45 | €155 | Baseline |
| Q2 2021 (Trough) | $85 | €210 | -25% |
| Q3 2022 (Peak) | $95 | €245 | -15% |
| Q4 2023 (Current) | $62 | €190 | +10% |
| Target (2026) | $55 | €165 | +5% annual |

Management's Operational Improvement Plan targets:
- Donor fee reduction through loyalty programs, experience improvements
- Labor productivity gains (collections per FTE up 30%+ since 2022)
- Center consolidation (closed 22 underperforming centers in 2023)
- Digitalization of donor scheduling and screening

### Stage 2: Plasma Testing and Pooling

Collected plasma undergoes extensive testing for infectious diseases (HIV, Hepatitis B/C, etc.) before being pooled with plasma from other donors. A single manufacturing batch may contain plasma from 10,000+ donations.

Testing cost: ~€8-10 per liter (included in CPL above at collection stage, plus additional testing at pooling)

### Stage 3: Fractionation

Cold ethanol fractionation — the Cohn process, developed in the 1940s — separates plasma into protein fractions. This is capital-intensive manufacturing with long cycle times.

**Meridian's Fractionation Capacity:**

| Facility | Location | Capacity (liters/year) | Utilization |
|----------|----------|------------------------|-------------|
| Lindqvist BioCenter | Stockholm | 4.5m | 92% |
| Atlantic Works | North Carolina | 6.0m | 88% |
| Nordic Plasma Facility | Frankfurt | 3.5m | 78% |
| Dublin Finishing | Ireland | 2.0m | 85% |
| **Total** | | **16.0m** | **87%** |

**Manufacturing Economics:**

| Metric | Value |
|--------|-------|
| Plasma input cost | €190/liter (CPL) |
| Fractionation cost | €45/liter |
| Purification & finishing | €35/liter |
| Quality control | €15/liter |
| **Total manufacturing cost** | **€285/liter** |

**Yield — The Key Efficiency Metric:**

Not all plasma is created equal. Fractionation yield — grams of each protein extracted per liter of plasma — determines profitability.

| Product | Industry Avg. Yield | Meridian Yield | Improvement Potential |
|---------|---------------------|----------------|----------------------|
| IgG (immunoglobulin) | 4.0 g/L | 4.3 g/L | +5% with process optimization |
| Albumin | 25 g/L | 26 g/L | Limited |
| Alpha-1 | 0.8 g/L | 0.85 g/L | Modest |

A 5% improvement in IgG yield on 14 million liters processed = 2,800 kg additional IgG = ~€280m additional revenue at current pricing.

### Stage 4: Finished Goods and Distribution

Purified proteins are formulated into final dosage forms (vials, pre-filled syringes), packaged, and distributed globally. Cold chain logistics are required throughout.

**Inventory Cycle:**

| Stage | Duration |
|-------|----------|
| Plasma collection to pooling | 2-4 weeks |
| Pooling to fractionation start | 2-4 weeks |
| Fractionation | 8-12 weeks |
| Purification and finishing | 4-6 weeks |
| Quality release testing | 4-6 weeks |
| Distribution to customer | 2-4 weeks |
| **Total: Donation to Patient** | **9-12 months** |

This extended cycle creates significant working capital requirements. Meridian holds €2.1 billion in inventory at any time — approximately 110 days of COGS.

---

## Geographic Revenue Mix

| Region | FY2023 Revenue | % Total | Growth | Key Dynamics |
|--------|----------------|---------|--------|--------------|
| North America | €3,700m | 54% | +11% | Largest IG market, premium pricing |
| Europe | €1,850m | 27% | +8% | Home market, albumin strength |
| China & Asia | €890m | 13% | +22% | Albumin demand, JV distribution |
| Rest of World | €410m | 6% | +5% | Latin America, Middle East |
| **Total** | **€6,850m** | **100%** | **+11%** | |

**China Exposure:**

Meridian holds a 26% stake in Shanghai MedPlasma Corp., a leading Chinese plasma company. This investment is carried at €1.4 billion on the balance sheet and generates:
- Equity income: €85m (FY2023)
- Albumin distribution fees: €120m (FY2023)
- Strategic optionality in world's fastest-growing plasma market

Management is evaluating a partial sale of this stake to accelerate deleveraging.

---

## Financial Summary

### Income Statement (€ millions)

| | FY2021 | FY2022 | FY2023 | FY2024E |
|--|--------|--------|--------|---------|
| Revenue | 5,420 | 5,890 | 6,850 | 7,350 |
| Growth % | -3% | +9% | +16% | +7% |
| Gross Profit | 2,170 | 2,240 | 2,810 | 3,090 |
| Gross Margin | 40.0% | 38.0% | 41.0% | 42.0% |
| EBITDA (Reported) | 1,085 | 1,060 | 1,440 | 1,690 |
| EBITDA Margin | 20.0% | 18.0% | 21.0% | 23.0% |
| EBITDA (Adjusted)* | 1,140 | 1,180 | 1,520 | 1,750 |
| Adj. EBITDA Margin | 21.0% | 20.0% | 22.2% | 23.8% |
| D&A | (380) | (410) | (450) | (470) |
| EBIT | 705 | 650 | 990 | 1,220 |
| Net Interest | (285) | (320) | (395) | (420) |
| Other Income/(Expense) | 45 | (60) | 85 | 90 |
| PBT | 465 | 270 | 680 | 890 |
| Tax | (95) | (55) | (140) | (180) |
| Effective Tax Rate | 20% | 20% | 21% | 20% |
| Net Income | 370 | 215 | 540 | 710 |
| Minority Interest | (85) | (95) | (115) | (125) |
| Net Income to Equity | 285 | 120 | 425 | 585 |

*Adjustments include: restructuring costs (€45m in FY2023), acquisition integration (€25m), non-cash stock compensation (€20m), litigation provisions (€10m estimated)

### Balance Sheet Summary (€ millions, as of December 31, 2023)

**Assets:**
| | Amount |
|--|--------|
| Cash and equivalents | 485 |
| Accounts receivable | 1,180 |
| Inventory | 2,150 |
| Other current assets | 290 |
| **Total Current Assets** | **4,105** |
| PP&E (net) | 2,840 |
| Intangible assets & goodwill | 4,650 |
| Equity investments (Shanghai MedPlasma) | 1,420 |
| Right-of-use assets (IFRS 16) | 980 |
| Other non-current | 540 |
| **Total Assets** | **14,535** |

**Liabilities:**
| | Amount |
|--|--------|
| Accounts payable | 720 |
| Accrued expenses | 580 |
| Current debt maturities | 385 |
| Other current liabilities | 410 |
| **Total Current Liabilities** | **2,095** |
| Long-term debt | 8,240 |
| Lease liabilities (IFRS 16) | 890 |
| Deferred tax | 620 |
| Pension & other | 385 |
| **Total Liabilities** | **12,230** |
| Minority interests | 680 |
| Shareholders' equity | 1,625 |
| **Total Equity** | **2,305** |
| **Total Liab. & Equity** | **14,535** |

### Cash Flow Summary (€ millions)

| | FY2021 | FY2022 | FY2023 | FY2024E |
|--|--------|--------|--------|---------|
| EBITDA | 1,085 | 1,060 | 1,440 | 1,690 |
| Working capital change | (180) | (320) | (210) | (140) |
| Cash interest paid | (265) | (295) | (375) | (400) |
| Cash taxes paid | (75) | (45) | (110) | (145) |
| Other operating | (40) | (55) | (35) | (25) |
| **Operating Cash Flow** | **525** | **345** | **710** | **980** |
| Capex — maintenance | (180) | (195) | (210) | (220) |
| Capex — growth | (280) | (420) | (260) | (200) |
| Acquisitions | (85) | (2,150) | (45) | — |
| Asset disposals | 25 | 15 | 40 | 1,350* |
| **Investing Cash Flow** | **(520)** | **(2,750)** | **(475)** | **930** |
| Debt proceeds | 450 | 2,400 | 1,250 | 1,100 |
| Debt repayments | (380) | (220) | (1,180) | (2,250) |
| Dividends | (90) | (45) | — | — |
| Other financing | (25) | (35) | (25) | (20) |
| **Financing Cash Flow** | **(45)** | **2,100** | **45** | **(1,170)** |
| **Net Change in Cash** | **(40)** | **(305)** | **280** | **740** |

*FY2024E includes expected proceeds from partial sale of Shanghai MedPlasma stake

---

## Capital Structure (As of December 31, 2023)

### Debt Summary

| Instrument | Currency | Amount | Coupon | Maturity | Security |
|------------|----------|--------|--------|----------|----------|
| Senior Secured Term Loan A | EUR | €1,200m | E+2.00% | Mar 2026 | 1st lien |
| Senior Secured Term Loan B | USD | $2,400m | S+3.25% | Nov 2028 | 1st lien |
| Senior Secured Term Loan B | EUR | €1,100m | E+3.50% | Nov 2028 | 1st lien |
| Senior Secured Notes | EUR | €850m | 5.25% | Feb 2029 | 1st lien |
| Senior Unsecured Notes | EUR | €1,200m | 6.50% | Oct 2028 | Unsecured |
| Senior Unsecured Notes | USD | $650m | 7.00% | Oct 2028 | Unsecured |
| Revolving Credit Facility | Multi | €800m | E+1.75% | Mar 2026 | 1st lien |
| **Total Funded Debt** | | **€8,625m** | | | |
| Lease liabilities (IFRS 16) | | €980m | | Various | |
| **Total Debt (incl. leases)** | | **€9,605m** | | | |
| Less: Cash | | (€485m) | | | |
| **Net Debt** | | **€9,120m** | | | |

*USD amounts converted at €1 = $1.08

### Leverage and Coverage

| Metric | FY2022 | FY2023 | Covenant |
|--------|--------|--------|----------|
| Net Debt / EBITDA (Credit Agreement)* | 7.2x | 5.6x | <6.5x |
| Net Debt / EBITDA (IFRS, incl. leases) | 8.1x | 6.3x | N/A |
| Interest Coverage (EBITDA/Cash Int.) | 3.3x | 3.6x | >2.5x |
| Secured Leverage | 5.4x | 4.2x | <5.5x |

*Credit Agreement EBITDA includes addbacks for synergies, pro forma acquisitions, and other adjustments totaling ~€80m

### Maturity Profile

| Year | Maturities | Instruments |
|------|------------|-------------|
| 2024 | €385m | TLA amortization, other |
| 2025 | €420m | TLA amortization |
| 2026 | €1,680m | TLA maturity, RCF maturity |
| 2027 | — | |
| 2028 | €4,850m | TLB (USD + EUR), Unsecured Notes |
| 2029 | €850m | Secured Notes |

### Key Credit Agreement Terms

**Financial Covenants (TLA and RCF only):**
- Maximum Net Leverage: 6.5x (stepping down to 5.5x by Dec 2025)
- Minimum Interest Coverage: 2.5x

**Term Loan B Covenants:**
- Covenant-lite (no maintenance covenants)
- Incurrence test for Restricted Payments: Net Leverage < 4.0x
- Incurrence test for additional debt: Net Leverage < 5.0x or Fixed Charge Coverage > 2.0x

**Change of Control:**
- 101% put right on all notes
- Mandatory prepayment of term loans at par
- Triggered if >50% of voting shares acquired by non-permitted holder

**Restricted Payments Capacity:**
- Builder basket: 50% of cumulative Consolidated Net Income since closing
- General basket: Greater of €200m and 15% of LTM EBITDA
- Available Amount from asset sales: 100% of net proceeds not reinvested within 365 days

---

## Recent Events and Market Context

### The Short-Seller Attack (January 2024)

On January 15, 2024, activist short-seller Obsidian Research published a 40-page report titled "Meridian Plasma: The Emperor Has No Clothes." Key allegations:

1. **Leverage Understated:** Obsidian claimed true leverage was 9-11x, not the reported 5.6x, after:
   - Adding back factoring arrangements (€380m) as debt
   - Excluding EBITDA from minority-owned subsidiaries
   - Reversing aggressive adjustment addbacks

2. **Related Party Concerns:** The report highlighted loans between Meridian and Lindqvist family entities totaling €125m, allegedly inadequately disclosed.

3. **Shanghai MedPlasma Valuation:** Obsidian questioned the €1.4bn carrying value, arguing comparable transactions suggested fair value of €800-900m.

**Market Reaction:**
- Stock fell 38% on publication day
- Bonds dropped 6-8 points
- Market cap declined from €7.2bn to €4.5bn

**Company Response:**
- Categorically denied all allegations
- Engaged independent auditor for special review
- Filed lawsuit against Obsidian in Stockholm
- Accelerated governance reforms (family members resigned executive roles)

### Strategic Review Announcement (February 2024)

On February 28, the Board announced:

> "Following expressions of interest from multiple parties, the Board has initiated a process to evaluate strategic alternatives for Meridian Plasma Group, including but not limited to a potential sale of the company, merger, or other transaction."

The Lindqvist family confirmed willingness to participate in a take-private transaction.

### Recent Trading

| Date | Share Price (MPG-A) | EV/EBITDA (LTM) | Notes |
|------|---------------------|-----------------|-------|
| Jan 1, 2024 | €14.80 | 9.8x | Pre-Obsidian |
| Jan 16, 2024 | €9.20 | 7.1x | Post-Obsidian |
| Feb 28, 2024 | €11.40 | 8.2x | Strategic review announced |
| Current (Mar 15) | €10.85 | 7.9x | |

**Shares Outstanding:**
- Class A: 485 million shares (€10.85 = €5.26bn market cap)
- Class B: 42 million shares (Lindqvist family, 10 votes each)
- Total economic shares: 527 million
- Family ownership: ~31% voting, ~8% economic

---

## Management Guidance and Targets

### FY2024 Guidance (Issued February 2024)

| Metric | Guidance | Assumptions |
|--------|----------|-------------|
| Revenue | €7.3-7.5bn | +7-10% growth |
| Adjusted EBITDA | €1.70-1.80bn | 23-24% margin |
| Free Cash Flow | €400-500m | Before Shanghai stake sale |
| Net Leverage | <5.0x | By year-end |
| Capex | €400-450m | ~6% of revenue |

### Medium-Term Targets (2027)

| Metric | Target |
|--------|--------|
| Revenue | €9.0bn |
| Adjusted EBITDA | €2.25bn |
| EBITDA Margin | 25% |
| Net Leverage | <4.0x |
| ROIC | >12% |

**Key Assumptions:**
- Immunoglobulin volume growth: 8-10% annually
- CPL reduction: €165/liter by 2026 (from €190 current)
- Yield improvement: +5% cumulative through process optimization
- No major acquisitions

---

## Investment Considerations

### The Bull Case

1. **Defensive, essential business:** Patients cannot switch away from plasma therapies. Demand is driven by chronic conditions and growing diagnosis rates.

2. **Structural undersupply:** Global IG demand growing 6-8% annually; plasma supply growth constrained by donor availability. Pricing power exists.

3. **Operational improvement runway:** CPL still 15% above pre-COVID levels. Yield improvements achievable. Center network can be further optimized.

4. **China optionality:** Shanghai MedPlasma stake provides exposure to fastest-growing plasma market with potential monetization path.

5. **Deleveraging momentum:** Cash flow inflection underway. Leverage declining without heroic assumptions.

### The Bear Case

1. **Still highly leveraged:** 5.6x net debt / EBITDA leaves limited margin for error. Rising rates have increased cash interest burden.

2. **Governance overhang:** Obsidian allegations, while disputed, raised legitimate questions about related-party transactions and family influence.

3. **Refinancing wall:** €2.1bn of debt matures in 2026, €4.85bn in 2028. Execution risk on refinancing at acceptable terms.

4. **Donor economics uncertainty:** If labor markets tighten or competitive intensity increases, CPL gains could reverse.

5. **Regulatory/reimbursement risk:** Government payers (especially in Europe) increasingly scrutinizing plasma therapy pricing.

---

## Your Assignment

Your Managing Director wants the following by end of week:

1. **LBO Model:** Full operating model with detailed revenue and cost drivers, working capital, capex, and debt schedule. Five-year forecast plus exit.

2. **Entry Valuation:** What can Helios pay and still achieve target returns (20% gross IRR)? Sensitivity analysis on entry multiple, leverage, and exit assumptions.

3. **Capital Structure:** Proposed financing structure. How much senior secured vs. unsecured? What terms should we expect? Impact of Change of Control provisions on deal execution.

4. **Value Creation Plan:** Operational improvements, potential add-on acquisitions, exit strategy. Where does the return come from?

5. **Key Risks and Mitigants:** What could go wrong? How do we protect downside?

The preliminary materials include:
- Audited financial statements (FY2021-2023)
- Management presentation and data book
- Existing credit agreement (redacted)
- Obsidian Research report
- Equity research (3 analysts)

Good luck. The IC meeting is in two weeks.

---

## Appendix A: Detailed Segment Information

### Biotherapeutics — Product Detail

**Immunoglobulins (IG):**

| Product | Format | FY2023 Revenue | Gross Margin | Key Markets |
|---------|--------|----------------|--------------|-------------|
| Immunex IV 5% | IVIG | €1,850m | 48% | US, EU, Japan |
| Immunex IV 10% | IVIG | €980m | 52% | US, China |
| Immunex SC 20% | SCIG | €590m | 55% | US, EU (growing) |
| **Total IG** | | **€3,420m** | **50%** | |

Market dynamics:
- Primary immunodeficiency (PID): ~500,000 diagnosed patients globally, but estimated 6 million affected (underdiagnosis)
- Secondary immunodeficiency (SID): Growing indication, driven by cancer treatments
- Neurology (CIDP, MMN): Fastest-growing indication, premium pricing
- SCIG gaining share: Home infusion, patient convenience, better margin

**Albumin:**

| Product | Concentration | FY2023 Revenue | Gross Margin | Key Markets |
|---------|---------------|----------------|--------------|-------------|
| Albunex 20% | High-conc. | €920m | 42% | China, Asia |
| Albunex 25% | Therapeutic | €480m | 45% | US, EU |
| Albunex 5% | Volume replacement | €180m | 35% | EU, ROW |
| **Total Albumin** | | **€1,580m** | **42%** | |

Market dynamics:
- China: 40% of global albumin consumption, driven by traditional medicine practices and ICU use
- Pricing pressure in developed markets
- Long-term growth linked to ICU capacity expansion in emerging markets

**Alpha-1 Antitrypsin:**

Single product (Prolunex) serving ~12,000 patients globally with genetic Alpha-1 deficiency. Orphan drug status provides pricing protection. Limited growth as patient pool is small and largely identified.

### Diagnostics — Product Detail

| Product Line | FY2023 Revenue | Gross Margin | Installed Base | Reagent Revenue % |
|--------------|----------------|--------------|----------------|-------------------|
| NAT Screening | €310m | 55% | 1,850 analyzers | 78% |
| Blood Typing | €285m | 52% | 4,200 systems | 72% |
| Immunoassays | €115m | 48% | 950 analyzers | 81% |
| **Total** | **€710m** | **53%** | | |

Business model: High reagent attachment rates create recurring revenue stream. Analyzer placements (often via reagent rental agreements) lock in multi-year consumable purchases.

---

## Appendix B: Plasma Collection Network Detail

### U.S. Network (295 Centers)

| Region | Centers | Avg. Volume (L/yr) | CPL | Notes |
|--------|---------|-------------------|-----|-------|
| Southeast | 82 | 42,000 | €185 | Best performing |
| Texas/Southwest | 68 | 39,000 | €195 | Strong growth |
| Midwest | 55 | 36,000 | €200 | Mature, stable |
| West | 48 | 35,000 | €205 | Higher labor costs |
| Northeast | 42 | 33,000 | €210 | Challenged |
| **Total US** | **295** | **38,500** | **€195** | |

Total US collections: ~11.4 million liters (FY2023)

### European Network (80 Centers)

| Country | Centers | Avg. Volume | CPL | Notes |
|---------|---------|-------------|-----|-------|
| Germany | 62 | 32,000 | €175 | Nordic acquisition |
| Hungary | 18 | 28,000 | €165 | Lower labor costs |
| **Total EU** | **80** | **31,000** | **€172** | |

Total EU collections: ~2.5 million liters (FY2023)

### Egypt Joint Venture (10 Centers)

- JV with Egyptian government (Meridian 60%, Gov't 40%)
- Targeting 20 centers by 2026
- Current collections: ~0.3 million liters
- Strategic importance: Demonstrates Middle East/Africa expansion capability

### Third-Party Supply Agreements

- Contracted purchases from independent collectors: ~1.5 million liters
- Higher cost (€220-240/liter) but provides supply flexibility
- Targeting reduction to <1 million liters as owned network grows

**Total Plasma Supply: ~15.7 million liters (FY2023)**

---

## Appendix C: Key Management and Board

### Executive Team

| Name | Title | Since | Background |
|------|-------|-------|------------|
| Marcus Johansson | CEO | 2019 | Former CFO; McKinsey alum |
| Elena Vasquez | CFO | 2022 | Ex-Fresenius, GSK |
| Dr. Henrik Nordström | Chief Scientific Officer | 2015 | Academic; joined 2008 |
| David Chen | President, Americas | 2020 | Ex-Baxter, Shire |
| Thomas Weber | President, Europe | 2022 | Came with Nordic acquisition |
| Maria Santos | Chief Operating Officer | 2021 | Ex-CSL Behring |

### Board of Directors

| Name | Role | Notes |
|------|------|-------|
| Karl Lindqvist | Chairman | Family; 3rd generation |
| Anna Lindqvist-Berg | Director | Family; Karl's daughter |
| Dr. James Morrison | Lead Independent | Former Roche executive |
| Sarah Chen | Independent | PE background (ex-KKR) |
| Dr. Michael Brennan | Independent | Biotech CEO |
| Henrik Magnusson | Independent | Former banker |
| Elisabeth Ström | Independent | Healthcare consultant |

Family representation: 2 of 7 board seats (down from 4 in 2022 following governance reforms)

---

## Appendix D: Comparable Company Data

### Public Comparables

| Company | EV (€bn) | Revenue | EBITDA | EV/Rev | EV/EBITDA | Net Debt/EBITDA |
|---------|----------|---------|--------|--------|-----------|-----------------|
| CSL Limited | €115 | €12.8bn | €3.8bn | 9.0x | 30x | 2.1x |
| Takeda (PDT segment est.) | €28* | €4.5bn | €1.2bn | 6.2x | 23x | N/A* |
| Kedrion | €3.5** | €1.1bn | €180m | 3.2x | 19x | 4.5x |
| **Meridian (Current)** | **€14.4** | **€6.85bn** | **€1.52bn** | **2.1x** | **9.5x** | **5.6x** |

*Takeda segment; PDT = Plasma-Derived Therapies
**Kedrion recently taken private; implied values from transaction

### Precedent Transactions

| Target | Acquirer | Date | EV | EV/EBITDA | Notes |
|--------|----------|------|----|-----------| ------|
| Biotest AG | Grifols | 2022 | €2.0bn | 18x | Strategic premium |
| Kedrion | Permira | 2022 | €3.5bn | 19x | Take-private |
| Shire (plasma) | Takeda | 2019 | €12bn* | 14x | Part of larger deal |
| Talecris | Grifols | 2011 | €3.4bn | 12x | Transformational |

*Allocated value to plasma assets within Shire acquisition

### Trading Observations

Meridian currently trades at a significant discount to plasma peers:
- CSL: 30x EBITDA (investment-grade, Australian premium, best-in-class margins)
- Kedrion (pre-deal): 19x (strategic bidding)
- Meridian: 9.5x (leverage concerns, Obsidian overhang, governance questions)

Even applying a conservative 12x EBITDA multiple to FY2024E Adjusted EBITDA of €1.75bn implies EV of €21bn — 45% above current trading level.

The opportunity, if it exists, is in (a) acquiring at a discount multiple, (b) executing operational improvements, (c) deleveraging, and (d) exiting at a normalized multiple once the business is de-risked.

---

*End of Case Materials*
