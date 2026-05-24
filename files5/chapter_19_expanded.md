# Chapter 19: Case Study — Modeling the Meridian LBO

This chapter walks through the construction and interpretation of an LBO model for Meridian Plasma Group, a plasma therapeutics company with €1.4 billion of revenue. The chapter begins with a simple annual model suitable for first-pass screening and progressively adds complexity where the underlying business mechanics justify it.

---

## The Assignment

This case study examines the LBO model construction process through a hypothetical acquisition scenario. Meridian Plasma Group is one of the world's largest plasma therapeutics companies. The Lindqvist family, which has maintained tight control, is exploring a sale after market turbulence that saw valuations decline. The transaction has an indicative enterprise value range of €14–16 billion, with an offer submission deadline two weeks away.

The core job of an LBO model is to translate a business thesis into numbers and determine whether those numbers work for all parties who must consent. The seller requires an acceptable price. Lenders require credit metrics that meet their underwriting standards. The sponsor requires returns that justify the risk and the capital commitment. If no single price point satisfies all three constraints, the transaction does not proceed.

The construction that follows demonstrates this constraint-satisfaction process across a simple baseline model.

---

## Part 1: The Simple Annual Model

### Why Start Simple

Model complexity often escalates unnecessarily. Quarterly periodicity, multiple debt tranches with differentiated amortization schedules, circular references for cash sweeps, PIK toggles, dividend recapitalizations, and management rollovers with hurdle-based ratchets are all available as modeling features. The temptation to employ all such features simultaneously is particularly acute for practitioners new to the discipline.

This temptation should be resisted, at least in the screening phase.

Here's why: a simple annual model delivers approximately 90% of the analytical answer in roughly 20% of the time. It forces attention toward what actually determines the investment decision — the business drivers, the entry price, and the capital structure — rather than scattering focus across mechanical details. Complexity can be layered on afterward. But if the simple model fails the return test, adding complexity will not salvage the investment case.

Sophisticated model architecture is appropriate only where the underlying business genuinely requires it. For initial screening, a simple annual model is preferable for three reasons: it concentrates attention on the drivers that determine the answer; it is faster to build and audit; and it produces a result quickly enough to feed back into deal screening before resources are committed.

The model constructed in this chapter employs:
- Annual periods (7 forecast years)
- One senior debt tranche
- Simple amortization (1% per year)
- No cash sweep mechanism
- No PIK instruments
- No circular references

This represents disciplined constraint, not limitation. Complexity will be addressed in Part 2 when its necessity is established.

---

## Section 1: Transaction Assumptions

### Opening the Model

The model structure (Meridian_Plasma_Group_LBO_Model.xlsx) employs two primary sheets:

**LBO Summary** — The primary dashboard. Key inputs appear at the top (debt amount, entry multiple, exit multiple, exit year), with the resulting IRR and money-on-money multiple displayed prominently. Below these controls, sensitivity tables show how returns vary across different exit multiples and holding periods, plus a summary of operating and financial performance across the projection period.

**LBO Model** — The detailed calculation engine, organized in sections:
- Income Statement (rows 4-19)
- Balance Sheet (rows 21-38)
- Cash Flow Statement (rows 40-60)
- Operating Assumptions (rows 62-111) — including three scenarios
- Transaction Assumptions (rows 113-142) — Sources & Uses
- Debt Schedule (rows 144-160)
- Key Financial Metrics (rows 162-171)
- Sponsor Returns (rows 173-202)
- Tax Schedule (rows 205-232)
- Working Capital Schedule (rows 235-256)
- PP&E Schedule (rows 259-293)

The structural logic follows a standard pattern: historical data (columns D-E, FY2020-2021) flows into adjusting columns (F-G) that construct the pro-forma balance sheet (column H), which then projects forward through the forecast period (columns I-O).

This architecture — Historical → Adjustments → Pro-Forma → Forecast — is the standard LBO model design and should be internalized as a reference structure.

### The Entry Price

Every LBO starts with a price. For Meridian, the indicative enterprise value is €14–16 billion. The first analytical question is: what does this range imply in terms of valuation multiple?

Let's anchor to EBITDA. Based on FY2024 financials (scaled for our teaching example):

| Metric | Value |
|--------|-------|
| Revenue | €2,400m |
| EBITDA | €720m |
| EBITDA Margin | 30% |

At €7.2 billion enterprise value, this represents 10x EBITDA. (The actual model displays this valuation in cell C117, pulling from the LBO Summary input cell C7.)

A 10x entry multiple is aggressive relative to historical norms in most leveraged transactions. However, business context determines appropriateness. Meridian exhibits characteristics of a defensive healthcare asset:

- **Recurring revenue** — Chronic patients need ongoing treatment. Nobody stops their immunoglobulin therapy because of a recession.
- **High barriers to entry** — Plasma collection networks take decades to build. You can't just wake up one day and decide to compete with Meridian.
- **Regulatory moats** — FDA and EMA approvals are expensive and time-consuming. Even if you built the collection network, you'd need years of clinical trials.
- **Inelastic demand** — When the economy crashes, people cut back on luxury goods. They don't cut back on life-saving medicine.

These characteristics justify a premium relative to capital structure leverage alone. The question is how much premium the market will award.

For the model base case:
- **Entry EV/EBITDA: 10x** (cell C7 on LBO Summary)
- **Exit EV/EBITDA: 10x** (cell C9 on LBO Summary)

The assumption of no multiple expansion reflects disciplined underwriting. Assuming a sale price exceeding the purchase price without explicit operational justification constitutes speculation rather than analysis. If the deal produces acceptable returns at flat multiples — the same EBITDA multiple at entry and exit — it merits classification as a sound investment. If returns depend on multiple expansion, the thesis relies on market timing and sentiment rather than on fundamental value creation.

Investment memos frequently assume 1–2 turns of multiple expansion in the base case ("We're buying at 8x but exiting at 10x due to operational improvements and enhanced market positioning"). Such expansion may materialize. Conversely, market conditions at exit may be less favorable than at entry, producing compression. Conservative underwriting builds models that satisfy return hurdles without multiple expansion, treating any expansion as upside rather than base case assumption.

### The Capital Structure

With €720m of EBITDA, how much debt can Meridian support?

This is where your conversations with debt capital markets colleagues become important. The answer isn't just mathematical (what can the cash flows support?) — it's also market-dependent (what are lenders willing to provide today?).

In the current environment, a high-quality healthcare business can typically lever 5-6x EBITDA in the syndicated loan market. Aggressive structures might push higher, but you'd need either subordinated debt or very sponsor-friendly terms.

For the base case, the model employs €3,000m of new debt (cell C5 on LBO Summary), which represents 4.2x the €720m entry EBITDA. This conservative approach answers the core screening question: does the deal work with reasonable capital structure assumptions, not stretched ones?

Look at the Sources & Uses section in the model (rows 131-142):

| Uses of Funds | Amount | Multiple |
|---------------|--------|----------|
| Acquisition of 100% Equity | €6,350m | 8.8x |
| Refinancing of Existing Debt | €800m | 1.1x |
| Minimum Cash to Company | €50m | 0.1x |
| Transaction Costs | €152m | 0.2x |
| **Total Uses** | **€7,352m** | **10.2x** |

| Sources of Funds | Amount | Multiple |
|------------------|--------|----------|
| Sponsor Equity Contribution | €4,302m | 6.0x |
| New Financial Debt | €3,000m | 4.2x |
| Company Cash Used | €50m | 0.1x |
| **Total Sources** | **€7,352m** | **10.2x** |

A few things to notice:

**Transaction costs represent material cash outflows.** Financing fees (2% of debt = €60m), advisory fees (1.5% of equity = €95m), and miscellaneous costs (€30m) aggregate to €152m. These amounts must be funded by the sponsor and do not contribute to the purchase price of the business. When calculating sponsor returns, transaction costs are components of the total invested capital.

**The equity check exceeds enterprise value minus debt.** A superficial calculation might suggest: €7,200m enterprise value minus €3,000m debt equals €4,200m equity required. This approach omits two material items: transaction costs and minimum cash required for working capital at closing. The actual sponsor equity injection is €4,302m.

**Sources must equal uses.** This is a fundamental accounting identity, and the model enforces it. A common modeling error involves asymmetric treatment of existing debt: including it as a use (to be refinanced at closing) but omitting it from sources (cash that does not need to be raised because existing lenders are being satisfied from acquisition proceeds). The model includes a balance check in row 38 that should always equal zero.

### Debt Terms

The senior secured term loan employs the following assumptions (rows 152-153):

| Term | Assumption | Rationale |
|------|------------|-----------|
| Interest Rate | 6.0% | EURIBOR (~2%) + 400bps margin |
| Amortization | 1% per year | Standard TLB terms |
| Maturity | 7 years | Typical for sponsor-backed |

The 6% all-in rate reflects current market conditions. In a lower-rate environment, this might be 4-5%. In a stressed market, 7-8%. The model should be flexible enough to sensitize this — you can change cell I152 and see the impact flow through.

A key assumption: the model employs a fixed 6% rate for simplicity. Actual market practice would use floating-rate debt (EURIBOR + margin), creating interest expense variation as rate environments change. For screening models, fixed rates are acceptable. For financing presentations to institutional investors, scenarios with different rate environments should be shown.

---

## Section 2: Operating Assumptions

### The Scenario Framework

The Operating Assumptions section (rows 62-111) employs a three-scenario framework rather than a single forecast path. This reflects the reality that market participants hold materially different expectations about future performance.

| Scenario | Description | Purpose |
|----------|-------------|---------|
| **Management Case** | Assumptions reflecting management's stated targets | Basis for equity return underwriting |
| **Bank Case** | Conservative case reflecting lender stress testing | Basis for debt sizing and covenant analysis |
| **Downside Case** | Severe stress case | Tests covenant compliance and credit resilience |

Cell C64 contains a dropdown selector that switches between scenarios. The forecast columns (I-O) update dynamically to reflect the selected case.

The three-scenario approach exists because equity and debt investors operate with systematically different expectations. Sponsors are equity holders and naturally optimistic — their case analysis assumes management execution, favorable market conditions, and scenario outcomes aligned with the business plan. Lenders are debt holders and structurally pessimistic — they are compensated for making the correct assessment of downside risk, not for participating in upside. Lender stress tests typically assume EBITDA performance 20–30% below the management case, with covenant headroom calculated against the Bank Case rather than the base plan.

Embedding all three scenarios within a single model enables conversations with both audiences using consistent mechanics and comparable definitions.

### The Revenue Build

Let's talk about what's actually driving the forecast.

Plasma is a growth business. Global demand for immunoglobulins grows 6-8% annually, driven by:
- Expanding indications (new diseases being treated)
- Improved diagnosis rates (more patients being identified)
- Aging populations (higher disease prevalence)
- Emerging market adoption (China, Middle East, Latin America)

For Meridian, the model assumes the following growth paths (rows 67-69):

| Scenario | Year 1-2 | Year 3-7 |
|----------|----------|----------|
| Management Case | 6% | 5% |
| Bank Case | 3% | 3% |
| Downside Case | 0% | 0% |

Growth decelerates after Year 2 in all scenarios. This reflects empirical observation: management projections consistently overestimate the duration of high growth rates. Markets mature over time. Competitive dynamics intensify as market opportunity attracts competitors. Readily accessible growth vectors are exhausted. Perpetual 6% growth represents wishful thinking; modeling a decline to 5% as markets stabilize represents realistic conservatism.

The Downside Case assumes zero growth — flat revenue in perpetuity. This assumption appears pessimistic, but it answers the critical credit question: absent revenue growth or operational improvement, do cash flows support the debt? Does the credit remain viable? If the answer is no at zero growth, the transaction exhibits structural credit vulnerability.

### The Margin Structure

Look at rows 71-84 for the cost assumptions:

| Line Item | Management | Bank | Downside |
|-----------|------------|------|----------|
| COGS (% of Revenue) | 50% | 52% | 54% |
| Operating Expenses (% of Revenue) | 20% | 22% | 24% |
| D&A (% of Revenue) | 5% | 5% | 5% |

The math for EBITDA margin in each scenario:
- **Management:** 100% - 50% - 20% = 30% margin
- **Bank:** 100% - 52% - 22% = 26% margin
- **Downside:** 100% - 54% - 24% = 22% margin

Notice that D&A doesn't change across scenarios. That's because depreciation is driven by the existing asset base and capital expenditure policy, not by how well the business performs operationally. A struggling company doesn't depreciate its assets more slowly.

Also notice the relationship: the Downside isn't "Management Case minus 2%." It's a different margin structure entirely. The Bank Case gives you 400bps less margin than Management. The Downside gives you another 400bps less. These step-downs matter because they compound with the revenue differences.

### Working Capital: Where Cash Actually Lives

This is where plasma businesses differ from typical manufacturing. Look at rows 93-106:

**Days Inventory Outstanding (DIO): 90 days**

This seems high compared to, say, a software company (which might have zero inventory) or even a normal manufacturer (30-45 days). But plasma inventory is special:

- Raw plasma must be held 60 days for viral safety testing. This isn't a policy choice — it's a regulatory requirement. You cannot release plasma-derived products until you've completed the safety hold.
- Work-in-process fractionation takes weeks. Plasma fractionation is a complex, multi-step manufacturing process.
- Finished goods require cold storage. These are biological products with specific handling requirements.

Material reduction of DIO would require either relaxation of regulatory safety requirements or acceptance of foregone sales. Neither is viable for a business dependent on product safety reputation and market access. Plasma DIO is therefore a structural feature of the business rather than an operational inefficiency available for improvement.

**Days Sales Outstanding (DSO): 45 days**

Typical for healthcare. Hospital customers pay slowly. Government payers (European national health systems) pay even more slowly — some countries run 90-120 days or longer. Private insurers pay faster. The 45-day assumption is a blend across customer types.

**Days Payable Outstanding (DPO): 40 days**

Plasma donors are paid immediately — you can't negotiate payment terms with individual donors. Equipment suppliers and service providers get standard terms. The 40-day assumption reflects this mix.

**The Net Working Capital Impact:**

The Working Capital Schedule (rows 235-256) calculates the actual balance sheet impacts:

```
Accounts Receivable = (Revenue / 365) × DSO
Inventory = (COGS / 365) × DIO
Accounts Payable = (COGS / 365) × DPO
Net Working Capital = A/R + Inventory - A/P
```

The formula for change in working capital is in row 256. It's negative when the company is growing — because growth consumes cash. Every €100m of revenue growth requires roughly €15-20m of incremental working capital investment. This is real cash that comes out of free cash flow.

A frequent modeling error involves calculating working capital changes as a percentage of revenue growth when the correct approach is to base changes on absolute balance sheet account movements. The model constructs this calculation correctly, and the logic should be clearly understood before adjusting underlying assumptions.

### Capital Expenditures

Rows 108-111 show CapEx as a percentage of revenue:

| Scenario | CapEx % |
|----------|---------|
| Management | 5% |
| Bank | 4% |
| Downside | 3% |

CapEx declines in stress scenarios because management behavior shifts toward cash preservation as business conditions deteriorate. Management defers expansion projects, extends equipment replacement cycles, and prioritizes liquidity over growth investments.

This response creates a future problem: under-investment erodes productive assets, market position, and operational efficiency over time. However, in a stressed scenario, near-term survival takes precedence over long-term optimization. The model reflects this management behavior pattern.

For the Management Case base assumption, 5% of revenue (approximately €120m annually) is sufficient to maintain the existing asset base and fund modest network expansion. A more aggressive growth strategy — construction of new plasma centers, addition of fractionation capacity — would require CapEx intensity of 7–8% of revenue.

---

## Section 3: Building the Forecast

### Following the Math Through the Model

The following analysis traces how operating assumptions flow into calculated results. Year 1 of the Management Case provides the illustrative example.

**The Income Statement (rows 6-19):**

Start in cell I6 (Revenue, Year 1). The formula is:
```
=H6*(1+I66)
```

Translation: Take the pro-forma revenue (€2,400m in H6) and grow it by the Year 1 growth rate (6% from the Management Case lookup in I66). Result: €2,544m.

Now cell I7 (COGS):
```
=-I6*I71
```

Translation: Revenue times the COGS percentage (50% from I71). Negative because it's a cost. Result: -€1,272m.

Gross Profit (I8) is just Revenue plus COGS: €1,272m.

Operating Expenses (I10) follows the same pattern as COGS: Revenue times the OpEx percentage. Result: -€509m.

D&A (I11): Revenue times the D&A percentage. Result: -€127m.

EBIT (I12) is the sum: €636m.

**At this point, the model incorporates the financing structure:** Interest expense (I15) links to the debt schedule:
```
=I150
```

This creates a link between the operating model and the financing structure. Change the debt amount, and interest expense changes automatically.

Interest income (I14) applies a return rate to the beginning cash balance:
```
=H29*I86
```

In the Management Case, this is 2% on whatever cash you're holding.

EBT (I16) is EBIT plus interest income minus interest expense. Tax calculation (I18) does not employ a simple EBT × rate formula. Instead, it pulls a computed value from the Tax Schedule at row 228:
```
=I228
```

The tax schedule incorporates statutory detail that materially affects cash taxes paid, and this detail is explained in the following section.

Net Income (I19) is EBT plus tax expense (negative number): €342m.

**And the EBITDA?** It's calculated in the Cash Flow section at row 42:
```
=I12-I11
```

EBIT minus D&A (which adds it back, since D&A is negative). Result: €763m, up from €720m at entry.

### The Cash Flow Cascade

This is where the model tells you whether the LBO actually works. The cash flow statement (rows 40-60) shows you how much money is available to service debt — and what's left over.

**Year 1 Cash Flow (Management Case):**

| Item | Formula | Amount |
|------|---------|--------|
| EBITDA | =I12-I11 | €763m |
| Change in Working Capital | =I256 | -€35m |
| Capital Expenditures | =-I6*I108 | -€127m |
| Income Tax Expense | =I18 | -€114m |
| Other Non-Operating Cash | =I14 | €1m |
| **Cash Available for Debt Service (CFADS)** | =SUM | **€488m** |
| Interest Expense | =I15 | -€180m |
| Debt Principal Repayment | =I148 | -€30m |
| **Cash Flow After Debt Service** | =I47+SUM(I49:I50) | **€278m** |

Let's unpack this:

**CFADS of €488m** tells you the business generates plenty of cash before financing costs. This is a healthy, cash-generative business.

**Interest of €180m** is substantial but manageable. Interest coverage (EBITDA/Interest) is 4.2x — well above the 2.5x minimum most lenders require.

**Amortization of €30m** is just 1% of the original €3,000m principal. Term Loan B structures typically have minimal amortization, with the bulk of principal repaid at maturity through refinancing or sale.

**Free Cash Flow of €278m** is real money that accumulates on the balance sheet. This is what makes the LBO work over time.

Now trace what happens to that €278m. The model checks if cash is sufficient (row 54), calculates if additional equity is needed (row 56, which should be zero in base case scenario), and determines if dividends are paid (row 59 — in the Meridian model, dividends are disabled with the flag in cell H155).

The ending cash balance (row 60) equals beginning cash plus cash flow after debt service plus any dividends (negative) plus any equity injections. Watch this number accumulate over the projection period. It's the visual representation of value creation.

### The Debt Schedule

The Debt Schedule (rows 144-160) tracks what happens to the €3,000m of debt over time.

The structure is straightforward:
```
Beginning Balance (I147) = Previous period ending balance = H149
Mandatory Amortization (I148) = -MIN(Beginning Balance, Original × Amort%)
Ending Balance (I149) = Beginning + Amortization
Interest Paid (I150) = -Interest Rate × Beginning Balance
```

Watch the ending balance decline:

| Year | Beginning | Amortization | Ending | Leverage |
|------|-----------|--------------|--------|----------|
| Entry | - | - | €3,000m | 4.2x |
| 1 | €3,000m | -€30m | €2,970m | 3.9x |
| 2 | €2,970m | -€30m | €2,940m | 3.6x |
| 3 | €2,940m | -€30m | €2,910m | 3.4x |
| 4 | €2,910m | -€30m | €2,880m | 3.2x |
| 5 | €2,880m | -€30m | €2,850m | 3.0x |

Leverage drops from 4.2x to 3.0x over five years — achieved purely from EBITDA growth, with no excess cash sweeps active. If the structure included a 50% cash sweep, deleveraging would accelerate further.

This is the "deleveraging" story that makes LBOs work: the business generates cash, EBITDA grows, debt stays roughly constant (or declines), and leverage drops. The equity value increases because you've paid down debt while the enterprise value has grown.

### The Tax Schedule

Tax calculation warrants detailed treatment. The simple approach — applying a flat rate to EBT — is common in early screening models and produces an acceptable approximation for initial analysis.

However, material tax statutes affect cash taxes paid in leveraged transactions. Post-2017 US tax law and equivalent European rules under ATAD (Anti-Tax Avoidance Directive) limit interest deductibility. The limit is generally set at 30% of EBITDA.

Rows 207-213 calculate this:

```
Tax EBITDA (I209) = Operating EBITDA
Interest Capacity (I210) = 30% × EBITDA
Total Net Interest Expense (I211) = Interest paid - Interest earned
Deductible Interest (I212) = MIN(Capacity, Actual Interest)
Non-Deductible Interest (I213) = Actual - Deductible
```

In the Meridian model, interest expense of €180m versus capacity of €763m × 30% = €229m means all interest remains deductible. The structure operates comfortably within the limit.

A more leveraged structure with €250m of interest would face different treatment: only €229m would be deductible, with €21m added back to taxable income, producing approximately €5m+ of incremental cash taxes that a simple rate-based approach would miss.

The model also tracks net operating loss (NOL) carryforwards in rows 215–222. When a company generates losses, those losses offset future taxable income, reducing cash taxes in profitable future periods. The calculation tracks beginning NOL balance, new losses generated, NOL utilization, and ending balance.

This level of tax detail may appear excessive for a screening model. It is not. Interest limitation and NOL effects are material — capable of swinging cash flow by 5–10% across a hold period — and errors in their calculation directly flow through to sponsor return calculations.

---

## Section 4: Sponsor Returns

### The Exit Math

The fundamental sponsor question the exit analysis answers is: what cash return does an initial €4.3bn capital commitment generate five years forward?

Look at the Sponsor Returns section (rows 173-202).

At Year 5, assuming a 10x exit multiple (same as entry):

| Item | Formula | Amount |
|------|---------|--------|
| Exit EBITDA | =L42 | €920m |
| Exit Multiple | =L176 | 10x |
| Enterprise Value | =L175×L176 | €9,200m |
| Cash Balance at Exit | =L29 | €500m |
| Debt Balance at Exit | =-L33 | -€2,850m |
| **Exit Equity Value** | =EV + Cash - Debt | **€6,850m** |

The sponsor invested €4,302m (cell C139) and receives €6,850m five years later.

### IRR and MoC

The return metrics are calculated in rows 195-202:

| Metric | Formula | Value |
|--------|---------|-------|
| Money-on-Money (MoC) | =Exit Value / Initial Investment | 1.67x |
| Internal Rate of Return (IRR) | =(MoC^(1/Years))-1 | 10.8% |

Is that good? Depends on your hurdle rate.

For a large-cap buyout fund, typical targets are:
- **Minimum acceptable IRR:** 15%+
- **Target IRR:** 20%+
- **MoC floor:** 2.0x

At 10.8% IRR and 1.67x MoC, this deal doesn't clear the bar. Not even close.

### The Model Output: Key Findings

The model output produces the following conclusions at the indicative €14–16 billion valuation:

At €7.2 billion enterprise value (10x entry EBITDA), the transaction produces an IRR of 11% — below most sponsor hurdle rates of 15%+. To achieve acceptable equity returns, the entry price would need to decline substantially. The sensitivity analysis examines this relationship:

**Required Entry Price Analysis:**
To achieve a 16% IRR (a typical sponsor minimum hurdle), the entry price would need to fall to 7–8x EBITDA, representing €5.0–5.8 billion enterprise value. This represents approximately 30–40% discount from the seller's indicative €14–16 billion range.

**Credit Analysis:**
From the lender perspective, credit metrics remain acceptable at the 10x entry valuation: 4.2x entry leverage declining to 3.0x at exit, interest coverage above 4.0x throughout the projection period. Credit capacity is not the binding constraint. The transaction can be financed at virtually any price point within the seller's range. The equity return requirement creates the actual constraint.

**The Sensitivity Table:**

| Entry Multiple | Exit Multiple | Revenue Growth | IRR |
|----------------|---------------|----------------|-----|
| 10x | 10x | 5% | 10.8% |
| 10x | 12x | 5% | 16.3% |
| 8x | 10x | 5% | 18.2% |
| 8x | 10x | 7% | 21.4% |
| 7x | 10x | 5% | 23.1% |

| Entry Multiple | Exit Multiple | Revenue Growth | IRR |
|----------------|---------------|----------------|-----|
| 10x | 10x | 5% | 10.8% |
| 10x | 12x | 5% | 16.3% |
| 8x | 10x | 5% | 18.2% |
| 8x | 10x | 7% | 21.4% |
| 7x | 10x | 5% | 23.1% |

This analysis reveals several paths to achieve a 16% hurdle IRR:

1. **At 10x entry, exit at 12x:** Requires two turns of multiple expansion. Healthcare multiples have compressed over recent years, making this outcome speculative.

2. **At 10x entry, accelerate growth to 7%:** Requires growth significantly above the 5% assumption and above observed market growth rates for plasma therapeutics. This path assumes successful competitive share capture.

3. **Lower entry multiples:** Accepting 7–8x entry produces acceptable returns without multiple expansion or above-market growth, though this represents 30–40% discount from seller expectations.

The model's value lies in rapidly illuminating which variables matter most to the investment decision. At the €14–16 billion valuation, the transaction fails to meet sponsor return hurdles without either significant multiple expansion (unlikely) or growth performance well above historical industry averages (speculative). These constraints define the economic problem that must be solved through negotiation or deal rejection.

---

## Section 5: The Credit Perspective

### The Other Side of the Table

Sponsor and lender analytical frameworks diverge fundamentally. Sponsors focus on IRR calculations. Lenders focus on whether principal and interest will be repaid in full.

Look at the Key Financial Metrics section (rows 162-171):

| Metric | Entry | Year 1 | Year 3 | Year 5 |
|--------|-------|--------|--------|--------|
| Gross Debt / EBITDA | 4.2x | 3.9x | 3.4x | 3.0x |
| Net Debt / EBITDA | 4.1x | 3.5x | 2.6x | 1.9x |
| Interest Coverage (EBITDA/Interest) | n/a | 4.2x | 4.8x | 5.4x |
| DSCR (CFADS/Debt Service) | n/a | 2.3x | 2.6x | 2.8x |

These ratios tell a different story than the IRR. From a credit perspective, this is a solid deal:

**Leverage starts reasonable and improves.** 4.2x isn't stretched for a high-quality healthcare business. The steady deleveraging to 3.0x means the lender's exposure decreases over time.

**Interest coverage is healthy.** Above 4x throughout means the company can pay its interest bill four times over. Even if EBITDA dropped by 50%, you'd still cover interest.

**DSCR is strong.** Above 2x means the company generates twice as much cash as it needs to service all debt obligations (interest plus principal).

From a credit standpoint, this deal works at any price. The business generates plenty of cash to support the debt. The constraint isn't credit capacity — it's that the equity returns are weak.

### Covenant Headroom

The model includes a covenant calculation at row 160. A leverage covenant of 5.5x is set with 40% headroom (meaning the covenant level is set at 40% above the projected leverage level).

How much can EBITDA decline before tripping the covenant?

| Year | Debt | Covenant | Min EBITDA | Actual EBITDA | Headroom |
|------|------|----------|------------|---------------|----------|
| 1 | €2,970m | 5.5x | €540m | €763m | 29% |
| 3 | €2,910m | 5.5x | €529m | €856m | 38% |
| 5 | €2,850m | 5.5x | €518m | €920m | 44% |

EBITDA could drop 29% in Year 1 before tripping covenants. By Year 5, that buffer grows to 44% because debt has amortized while EBITDA has grown.

For context: a 30% EBITDA decline is a serious recession. The 2008-2009 financial crisis saw healthcare EBITDA decline maybe 10-15% for the most affected companies. A 30% drop would be an existential event for the industry — and even then, you'd survive from a covenant perspective.

This is a well-structured credit.

### The Lender Perspective: Different Metrics, Different Constraints

Lender economics diverge fundamentally from sponsor economics. Lenders receive fixed interest rates and principal repayment — their return is independent of sponsor IRR. Whether sponsor equity achieves an 8% or 28% IRR has no effect on lender compensation. Their upside is capped at the contractual coupon; their downside is principal loss in default scenarios.

This asymmetry explains different metric focus:

- **Entry leverage** — Lower ratios provide greater deterioration buffer.
- **Coverage ratios** — Higher ratios ensure debt service viability across stress scenarios.
- **Deleveraging trajectory** — Lenders prefer to see leverage decline over time, reducing exposure.
- **Covenant headroom** — Lenders need buffer between projected performance and covenant breach levels.

Deal attractiveness can diverge between sponsors and lenders. A transaction can be favorable to lenders but unattractive to sponsors (solid credit metrics but insufficient equity returns), or favorable to sponsors but problematic for lenders (high returns achieved through stretched credit). Optimal transactions satisfy both constituencies — the model permits evaluation of whether that condition is met.

---

## Section 6: Simple Model Conclusions

After the model construction and analysis detailed above, several clear conclusions emerge:

1. **The transaction fails to achieve sponsor return hurdles at asking price.** 10x EBITDA produces an 11% IRR, falling below typical sponsor minimum thresholds of 15%.

2. **The underlying business is sound from a credit perspective.** Lender metrics are healthy. The transaction's viability constraint is equity returns, not credit capacity.

3. **Entry price is the primary constraint.** Sponsor returns reach acceptable levels only at 7–8x EBITDA entry, representing 30–40% discount from the seller's €14–16 billion expectation.

4. **Multiple expansion offers limited solution path.** Exit multiples of 12x would be required to hit 16% IRR at 10x entry — an aggressive outcome in a market where healthcare sector multiples have contracted.

5. **Capital structure has appropriate leverage.** 4.2x entry leverage declining to 3.0x provides healthy credit metrics. Additional debt capacity exists, but this does not affect the equity return constraint.

6. **Downside scenarios remain creditworthy.** Bank Case (conservative growth, lower margins) and Downside Case (zero growth) still support debt repayment. The transaction exhibits reasonable credit resilience.

The simple model's value is in answering the foundational question — does the transaction satisfy sponsor hurdle rates? — with sufficient speed to permit rapid iteration and decision-making. The model enables informed conversations with sponsors, lenders, and sellers about whether price adjustments or alternative structures could resolve the return gap.

---

## Part 2: When to Add Complexity

### The Complexity Problem

Model complexity often escalates without discipline. Experienced practitioners encounter models exhibiting:

- 50+ calculation sheets
- Circular references that fail when modified
- Multi-line formulas that exceed single-cell viewing capacity
- Legacy VBA macros whose authors have departed

These models exist because complexity was layered incrementally without evaluation of necessity. One feature led to another, and a model that began as a screening tool evolved into a calculation system requiring 45 minutes to recalculate, fragile during sensitivity analysis, and difficult to audit.

Disciplined model design requires explicit threshold questions: when does marginal complexity change the investment decision?

### The Quarterly Question

The Meridian model employs annual periods, which is appropriate for screening-stage analysis. The question for post-LOI analysis is: when does quarterly periodicity become necessary?

Here's a comparison:

| Feature | Simple Annual Model | Complex Quarterly Model |
|---------|---------------------|-------------------------|
| Periods | 7 annual | 28-32 quarterly |
| Sheets | 2 | 10+ |
| Revenue modeling | Flat annual growth | Quarterly seasonality |
| Working capital | DSO/DIO/DPO days | Multi-quarter collection waterfall |
| Debt structure | Single senior tranche | Revolver + TLB + Notes + Mezz |
| Cash management | Excess accumulates | Cash sweep, revolver draw/repay |
| Circularity | None | Interest ↔ Debt ↔ Cash loops |
| Build time | 1-2 hours | 1-2 days |

**Complexity matters when:**

1. **Seasonality is extreme.** If Q4 is 45% of revenue and Q1 is 5%, annual averaging hides critical cash flow dynamics. You might need peak revolver capacity that's 3x the annual average working capital need.

2. **You're close to covenant levels.** If annual average leverage is 4.8x but Q1 leverage is 5.3x (due to seasonal EBITDA), you'll trip a quarterly test. Annual models miss this.

3. **Working capital timing creates liquidity risk.** Long collection cycles (180+ day DSO) combined with seasonal revenue can create quarters where you're deeply drawn on the revolver. This matters.

4. **Debt structure has moving parts.** Cash sweeps (calculated annually, paid from quarterly cash), PIK toggles, revolver utilization — all benefit from quarterly tracking.

5. **You're running the company.** Post-close, you need quarterly forecasts for board reporting, covenant compliance, and treasury management.

**Complexity doesn't matter when:**

1. **You're screening.** First-pass analysis to decide if a deal is worth pursuing.

2. **The business is stable.** Healthcare, essential services, subscription software — low seasonality, predictable cash. Meridian falls in this category.

3. **Debt structure is simple.** Single term loan, no revolver or subordinated debt.

4. **You're far from covenant levels.** If leverage is 3x with a 5.5x covenant, quarterly fluctuations are irrelevant.

5. **You're presenting to committee.** Senior decision-makers want to understand the story, not audit 32 periods.

For Meridian, the simple annual model is appropriate. It's a stable healthcare business with predictable cash flows and a straightforward capital structure. Quarterly precision wouldn't change the investment decision.

### Advanced Features (When You Actually Need Them)

Once screening has progressed to post-LOI analysis where the transaction has moved from conceptual to committed, more sophisticated model architecture becomes appropriate. The following features warrant inclusion:

**Multiple Debt Tranches:**

Real LBO capital structures often include:

| Tranche | Rate | Amortization | Cash Sweep | Features |
|---------|------|--------------|------------|----------|
| Revolver | SOFR + 425bps | None | None | Undrawn fee 50bps |
| Term Loan B | SOFR + 475bps, 0.5% floor | 1% | 50% | Senior secured |
| Senior Notes | Fixed 8.375% | None | 100% | Non-call period |
| Mezz/Second Lien | SOFR + 800bps | None | 100% | Higher rate, subordinated |

Each tranche has its own waterfall priority for cash sweeps: Revolver first (repaid before you can sweep to others), then Term Loan, then Notes. The model needs to track each separately.

**PIK Interest:**

Some instruments allow interest to accrue to principal rather than pay cash:

```
Beginning Subordinated Notes: €100M
(+) PIK Interest (5%):        €5M
(-) Cash Interest (5%):       (€5M) paid from cash flow
(=) Ending Balance:           €105M
```

PIK increases the debt balance over time. It provides cash flow relief in early years but increases exit debt — a trade-off that needs to be modeled explicitly.

**Cash Flow Sweeps:**

Many credit agreements require "excess cash flow" sweeps — a percentage of annual free cash flow must go to debt paydown:

```
Consolidated Net Income
+ Depreciation and Amortization
- Capital Expenditures (maintenance only)
- Scheduled Debt Payments
- Working Capital Increase
- Cash Taxes Paid
- Cash Interest Paid
± Other permitted add-backs/deductions
= Excess Cash Flow

× Sweep Percentage (often 50-75%, with step-downs)
= Mandatory Prepayment
```

This accelerates deleveraging (good for credit) and affects sponsor returns (cash that could go to dividends goes to debt paydown instead).

**Dividend Recapitalizations:**

Sponsors sometimes take a "dividend recap" — raising additional debt mid-investment to pay themselves a dividend:

```
Year 3:
  EBITDA: €150M
  Div recap leverage: 2.0x
  New debt issued: €300M
  Less: issuance fees (2%): (€6M)
  Dividend to sponsor: €294M
```

This accelerates returns (cash out earlier = higher IRR) but increases risk (more debt on the business). The model must track the new tranche separately.

**Returns Attribution:**

Advanced models decompose returns into sources:

| Source | Contribution |
|--------|--------------|
| EBITDA growth | €X of exit EV increase |
| Multiple expansion | €Y of exit EV increase |
| Debt paydown | €Z less debt at exit |
| Dividend recap | €W cash distributed early |
| **Total equity return** | **€Total** |

This tells you *why* the deal worked (or didn't). A deal that only works with multiple expansion is speculative. A deal that works primarily on debt paydown is safe but boring. The best deals work on multiple levers.

### The Meridian Verdict

For the Meridian case study, the impact of advanced features on model output is:

| Feature | Simple Model | Advanced Model | Impact on Returns |
|---------|-----------|----------|---------|
| Periodicity | Annual | Quarterly | Low — stable business, limited seasonality |
| Debt tranches | Single TLB | Multi-tranche (RCF + TLB + Notes) | Medium — higher blended cost of debt |
| Cash sweeps | None | 50% ECF mandatory prepayment | Medium — accelerated deleveraging |
| Management incentives | Not modeled | Rollover equity + options | Low to Medium — affects sponsor ownership %. |
| Dividend recap | Not modeled | Year 3 option | Medium — timing of cash distributions |
| Tax complexity | Modeled (interest limitation) | Modeled | Already included |

The simple model concludes that the transaction fails to achieve acceptable sponsor returns at the seller's €14–16 billion expectation. An advanced model would reach the same conclusion with marginally different precision — perhaps 10.3% IRR rather than 10.8%, or 1.65x MoC rather than 1.67x.

**Model Sophistication as Function of Deal Stage:**

1. **Pre-LOI Screening** → Simple annual model. Speed of analysis enables rapid iteration.
2. **Post-LOI Diligence** → Add debt tranches, management terms, working capital waterfall detail.
3. **Financing Roadshow** → Quarterly model with full debt structure for institutional investor presentations.
4. **Post-close Operational Budgeting** → Maximum complexity for board reporting, covenant compliance, treasury management.

Model precision should be calibrated to the decision-making stage. Constructing quarterly models to answer annual screening questions wastes resources and introduces unnecessary complexity risk.

---

## Part 3: Connecting to Documentation

### Where the Model Meets the Covenants

The model construction embodies specific assumptions about capital structure mechanics. Those assumptions are either confirmed or contradicted when the credit documentation is reviewed.

**Interest Rate:**
- Model assumes: 6% fixed
- Documentation reality: EURIBOR + 400bps margin, probably with a SOFR floor
- Impact: If rates rise above the floor, interest expense increases. Conversely, rates falling below the floor doesn't help you.

**Amortization:**
- Model assumes: 1% annual mandatory
- Documentation reality: Need to verify against Section 2.06 (or equivalent) of the credit agreement
- Impact: If documentation includes a 50% excess cash flow sweep not in the model, debt paydown will exceed projections

**EBITDA Definition:**
- Model assumes: Revenue - COGS - OpEx + D&A
- Documentation reality: "Adjusted EBITDA" per credit agreement typically includes add-backs for restructuring, transaction costs, projected synergies, non-cash items
- Impact: Credit agreement EBITDA is usually 5-15% higher than GAAP EBITDA. This matters for covenant calculations.

**Covenant Structure:**
- Model assumes: 5.5x leverage test with 40% headroom
- Documentation reality: Need to verify if covenant is maintenance (tested quarterly whether you draw or not) or incurrence-only (tested only when you take certain actions). Is there a covenant holiday? What's the ratchet look like?

Material differences emerge when documentation diverges from model assumptions — for example, when a model assumes maintenance covenants (continuous compliance requirement) while documentation provides incurrence-only testing (covenant tests triggered only upon specific actions). Such differences materially affect downside protection and credit resilience assessment.

### The Documentation Checklist

Before you finalize an LBO model, verify these against actual documents:

| Item | Model Assumption | Document Source |
|------|------------------|-----------------|
| Interest margin | 400bps | Credit Agreement, Section 2.05 |
| Amortization schedule | 1% p.a. | Credit Agreement, Section 2.06 |
| Mandatory prepayment | None | Credit Agreement, Section 2.07 |
| Excess cash flow sweep | None | Credit Agreement, Section 2.07 |
| EBITDA definition | Per GAAP | Credit Agreement, Section 1.01 |
| Leverage test | 5.5x | Credit Agreement, Section 7.11 |
| RP capacity | Builder basket | Indenture, Section 4.07 |
| Change of control | Put at 101 | Indenture, Section 4.14 |

The model is only as good as its assumptions. The assumptions are only as good as your documentation review.

---

## Summary: What Modeling Actually Does

The LBO model doesn't tell you whether to do a deal. It tells you the math.

For Meridian, the math says:
- At 10x EBITDA, returns are mediocre (11% IRR)
- At 8x EBITDA, returns are acceptable (18% IRR)
- At 7x EBITDA, returns are attractive (23% IRR)
- Credit metrics are solid at any of these prices
- The limiting factor is equity returns, not credit capacity

Armed with this, you can have an informed conversation:

The sponsor negotiation position becomes: "The business is sound and financeable. However, the equity return requirement at the stated asking price cannot be satisfied. Here are the price levels that would produce acceptable returns, with supporting analysis."

That's what the model is for. Not to produce a precise answer, but to define the boundaries of what makes sense. The precision is secondary; the insight is primary.

The concluding chapter addresses advanced topics in leveraged finance practice that extend beyond technical modeling mechanics.

---

*The Meridian Plasma Group LBO Model (Excel) accompanies this chapter and can be used to follow along with the calculations described above. The model is intentionally built with teaching in mind — formulas are visible, sections are labeled, and the architecture follows standard LBO conventions.*
