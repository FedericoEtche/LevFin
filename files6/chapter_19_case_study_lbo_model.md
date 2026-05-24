# Chapter 19: Case Study — Modeling the Meridian LBO

*This chapter walks through the construction and interpretation of an LBO model for Meridian Plasma Group. We start with a simple annual model — the kind you might build in a first-pass screening — and then discuss when and why more complexity is warranted.*

---

## The Assignment

Your Managing Director's instructions were clear: "Build the model. Let's see if the math works."

You have two weeks before the expression of interest is due. In that time, you need to determine whether Helios Capital can pay a price that (a) the Lindqvist family will accept, (b) lenders will finance, and (c) generates returns that justify the risk.

This is the core job of an LBO model: translate a business thesis into numbers, and see if those numbers work for everyone who needs to say yes.

Let's build it.

---

## Part 1: The Simple Annual Model

### Why Start Simple

There's a temptation, especially among junior bankers, to build the most sophisticated model possible. Quarterly periodicity. Multiple debt tranches with different amortization schedules. Circular references for cash sweeps. PIK toggles. The works.

Resist this temptation — at least initially.

A simple annual model gets you 90% of the answer in 20% of the time. It forces you to focus on what actually matters: the business drivers, the entry price, and the capital structure. You can always add complexity later. But if the simple model doesn't work, the complex model won't save you.

The model we're about to build has:
- Annual periods (7 forecast years)
- One senior debt tranche
- Simple amortization (1% per year)
- No cash sweep
- No PIK instruments
- No circular references

This is not a limitation. This is a feature.

---

## Section 1: Transaction Assumptions

### The Entry Price

Every LBO starts with a price. In Meridian's case, we're looking at an indicative enterprise value of €14-16 billion. But what does that actually mean in terms of valuation?

Let's anchor to EBITDA. Based on FY2024 financials (scaled for our teaching example):

| Metric | Value |
|--------|-------|
| Revenue | €2,400m |
| EBITDA | €720m |
| EBITDA Margin | 30% |

At €7.2 billion enterprise value, we'd be paying 10x EBITDA. That's aggressive for a levered buyout, but not unreasonable for a defensive healthcare business with:
- Recurring revenue (chronic patients need ongoing treatment)
- High barriers to entry (plasma collection networks take decades to build)
- Regulatory moats (FDA/EMA approvals are expensive and time-consuming)
- Inelastic demand (patients don't stop treatment in recessions)

For our model, we'll use:
- **Entry EV/EBITDA: 10x**
- **Exit EV/EBITDA: 10x** (no multiple expansion assumed)

Why no multiple expansion? Because assuming you'll sell for more than you paid is hope, not analysis. If the deal works at flat multiples, it's a good deal. If it only works with expansion, you're speculating.

### The Capital Structure

With €720m of EBITDA, how much debt can Meridian support?

The answer depends on who's lending and what the market will bear. In today's environment, a high-quality healthcare business can typically lever 5-6x EBITDA in the syndicated loan market. For our base case:

| Sources | Amount | Multiple | % of Total |
|---------|--------|----------|------------|
| Senior Secured Term Loan | €3,000m | 4.2x | ~42% |
| Sponsor Equity | €4,100m | 5.7x | ~58% |
| **Total Sources** | **€7,200m** | **10.0x** | **100%** |

Wait — €3,000m + €4,100m = €7,100m, not €7,200m. What happened?

Transaction costs and adjustments:
- Financing fees (2% of debt): €60m
- Advisory fees (1.5% of equity): €62m
- Other transaction costs: €30m
- Minimum cash to company: €50m
- Less: existing cash used: (€50m)
- Less: existing debt refinanced: (€800m)

When you net it all out, the sources equal the uses. The sponsor writes a check for roughly €4.1 billion.

### Debt Terms

For the senior secured term loan:

| Term | Assumption | Rationale |
|------|------------|-----------|
| Interest Rate | 6.0% | EURIBOR + 400bps margin |
| Amortization | 1% per year | Standard TLB terms |
| Maturity | 7 years | Typical for sponsor-backed |
| Covenants | Springing leverage test | Tested only if RCF drawn |

The 6% all-in rate reflects current market conditions. In a lower-rate environment, this might be 4-5%. In a stressed market, 7-8%. The model should be flexible enough to sensitize this.

---

## Section 2: Operating Assumptions

### The Revenue Build

Plasma is a growth business. Global demand for immunoglobulins grows 6-8% annually, driven by:
- Expanding indications (new diseases being treated)
- Improved diagnosis rates (more patients identified)
- Aging populations (higher disease prevalence)
- Emerging market adoption (China, Middle East, Latin America)

For Meridian, we model three scenarios:

| Scenario | Year 1-2 | Year 3-7 | Rationale |
|----------|----------|----------|-----------|
| **Management Case** | 6% | 5% | Market growth + share gains |
| **Bank Case** | 3% | 3% | Conservative; used for debt sizing |
| **Downside Case** | 0% | 0% | Flat; tests covenant headroom |

The Management Case is what we're underwriting. The Bank Case is what the lenders will use. The Downside Case is what keeps you up at night.

### The Margin Structure

Meridian's cost structure is relatively fixed in the short term:

| Line Item | % of Revenue | Notes |
|-----------|--------------|-------|
| **COGS** | 50% | Plasma collection, fractionation, manufacturing |
| **OpEx** | 20% | SG&A, R&D, corporate overhead |
| **D&A** | 5% | Capital-intensive business |
| **EBITDA** | **25%** | After normalizing for plasma-specific dynamics |

In our simplified model, we're using 30% EBITDA margin (50% COGS + 20% OpEx = 70% costs, 30% EBITDA). This is slightly optimistic versus Grifols' actual 25% — representing the value creation thesis that new ownership can improve operations.

### Working Capital: The Plasma Twist

Here's where plasma businesses differ from typical manufacturing:

**Days Inventory Outstanding (DIO): 90 days**

This seems high, but plasma inventory is special:
- Raw plasma must be held 60 days for viral safety testing
- Work-in-process fractionation takes weeks
- Finished goods have long shelf life but require cold storage

You cannot meaningfully reduce plasma DIO without compromising safety or losing sales. This is a structural feature of the business, not an inefficiency to fix.

**Days Sales Outstanding (DSO): 45 days**

Typical for healthcare. Hospital customers pay slowly. Government payers (European national health systems) pay even more slowly. Private insurers pay faster.

**Days Payable Outstanding (DPO): 40 days**

Plasma donors are paid immediately (you can't negotiate payment terms with donors). Equipment suppliers and service providers get standard terms.

**Net Working Capital Impact:**

The long inventory cycle means plasma businesses consume significant working capital as they grow. Every €100m of revenue growth requires roughly €15-20m of incremental working capital investment. This is real cash that comes out of free cash flow.

### Capital Expenditures

| Category | % of Revenue | Annual Amount |
|----------|--------------|---------------|
| Maintenance CapEx | 3% | €72m |
| Growth CapEx | 2% | €48m |
| **Total CapEx** | **5%** | **€120m** |

For the base case, we use 5% of revenue — enough to maintain the asset base and fund modest network expansion. A more aggressive growth plan (new plasma centers, capacity expansion) would require 7-8%.

---

## Section 3: Building the Forecast

### The Income Statement Flow

With our assumptions set, the income statement builds mechanically:

**Year 1 Forecast (Management Case):**

| Line Item | Calculation | Amount |
|-----------|-------------|--------|
| Revenue | €2,400m × 1.06 | €2,544m |
| COGS | Revenue × 50% | (€1,272m) |
| Gross Profit | | €1,272m |
| OpEx | Revenue × 20% | (€509m) |
| D&A | Revenue × 5% | (€127m) |
| **EBIT** | | **€636m** |
| Interest Expense | €3,000m × 6% | (€180m) |
| EBT | | €456m |
| Tax (25%) | | (€114m) |
| **Net Income** | | **€342m** |

**EBITDA: €636m + €127m = €763m** (up from €720m at entry)

### The Cash Flow Cascade

This is where the model gets interesting. The cash flow statement tells you how much debt you can actually pay down — which drives your equity returns.

**Year 1 Cash Flow:**

| Item | Amount | Notes |
|------|--------|-------|
| EBITDA | €763m | |
| Change in Working Capital | (€35m) | Growth consumes cash |
| CapEx | (€127m) | 5% of revenue |
| Cash Taxes | (€114m) | |
| Interest Income | €1m | On cash balance |
| **Cash Available for Debt Service** | **€488m** | |
| Interest Expense | (€180m) | |
| Mandatory Amortization | (€30m) | 1% of original principal |
| **Free Cash Flow After Debt Service** | **€278m** | |

That €278m is real cash that either stays on the balance sheet or goes to the sponsor. In most LBOs, it stays — building liquidity and paying down debt faster through optional prepayments.

### The Debt Paydown

With 1% mandatory amortization plus excess cash flow:

| Year | Beginning Debt | Amortization | Ending Debt | Leverage |
|------|----------------|--------------|-------------|----------|
| Entry | - | - | €3,000m | 4.2x |
| 1 | €3,000m | (€30m) | €2,970m | 3.9x |
| 2 | €2,970m | (€30m) | €2,940m | 3.6x |
| 3 | €2,940m | (€30m) | €2,910m | 3.4x |
| 4 | €2,910m | (€30m) | €2,880m | 3.2x |
| 5 | €2,880m | (€30m) | €2,850m | 3.0x |

Leverage drops from 4.2x to 3.0x over five years — purely from EBITDA growth (no excess cash sweeps). This is the "deleveraging" story that makes LBOs work.

---

## Section 4: Sponsor Returns

### The Exit Math

At Year 5, assuming a 10x exit multiple:

| Item | Amount |
|------|--------|
| Exit EBITDA | €920m |
| Exit Multiple | 10x |
| Enterprise Value | €9,200m |
| Less: Net Debt | (€2,850m - €500m cash) = (€2,350m) |
| **Equity Value** | **€6,850m** |

The sponsor invested €4,100m and receives €6,850m five years later.

### IRR and MoC

| Metric | Value |
|--------|-------|
| Money-on-Money (MoC) | 1.67x |
| Internal Rate of Return (IRR) | 10.8% |

Is that good? It depends on your hurdle rate.

For a large-cap buyout fund, typical targets are:
- **Minimum acceptable IRR:** 15%+
- **Target IRR:** 20%+
- **MoC floor:** 2.0x

At 10.8% IRR and 1.67x MoC, this deal doesn't clear the bar. Not even close.

### What Went Wrong?

The math reveals the problem: we paid 10x EBITDA for a business growing at 5-6%. Even with leverage, even with operational improvements, the returns are mediocre.

This is why entry multiple matters more than anything else in an LBO. You can't operational-improve your way out of a bad price.

### Sensitizing the Model

Let's see what it takes to hit 20% IRR:

| Entry Multiple | Exit Multiple | Revenue Growth | IRR |
|----------------|---------------|----------------|-----|
| 10x | 10x | 5% | 10.8% |
| 10x | 12x | 5% | 16.3% |
| 8x | 10x | 5% | 18.2% |
| 8x | 10x | 7% | 21.4% |
| 7x | 10x | 5% | 23.1% |

The answer is clear: you need to pay less. At 8x EBITDA (€5.76bn EV), the deal starts to make sense. At 7x (€5.04bn EV), it's attractive.

This is the insight you take back to your MD: "The deal doesn't work at the indicative €14-16bn range. We need to be at €5-6bn, which is 60-70% below where they're hoping to trade."

That's probably a non-starter. But at least now you know.

---

## Section 5: The Credit Perspective

### Leverage and Coverage Ratios

The model also tells you whether lenders will play:

| Metric | Entry | Year 1 | Year 3 | Year 5 |
|--------|-------|--------|--------|--------|
| Gross Debt / EBITDA | 4.2x | 3.9x | 3.4x | 3.0x |
| Net Debt / EBITDA | 4.1x | 3.5x | 2.6x | 1.9x |
| Interest Coverage | n/a | 4.2x | 4.8x | 5.4x |
| DSCR | n/a | 2.3x | 2.6x | 2.8x |

These ratios are healthy. Leverage below 5x at entry, declining steadily. Interest coverage above 4x. DSCR above 2x.

From a credit perspective, this is a solid deal. The business can easily support the debt load. The problem isn't credit risk — it's that the equity returns are weak.

### Covenant Headroom

If the credit agreement includes a leverage covenant (say, 5.5x with 40% headroom), how much EBITDA decline can we absorb?

| Year | Debt | Covenant Test | Min EBITDA | Actual EBITDA | Headroom |
|------|------|---------------|------------|---------------|----------|
| 1 | €2,970m | 5.5x | €540m | €763m | 29% |
| 3 | €2,910m | 5.5x | €529m | €856m | 38% |
| 5 | €2,850m | 5.5x | €518m | €920m | 44% |

EBITDA could drop 29% in Year 1 before tripping covenants. By Year 5, that buffer grows to 44%. This is a well-structured credit.

---

## Section 6: What the Simple Model Tells You

After an hour of work, you know:

1. **The deal doesn't work at asking price.** 10x EBITDA yields 11% IRR — below hurdle.

2. **The business is solid.** Credit metrics are healthy. This is a financing story, not a credit story.

3. **Price is the problem.** You need 7-8x to make the returns work. That's 30-40% below indicative.

4. **Multiple expansion is required (or price reduction).** At 10x entry, you need 12x exit to hit 16% IRR. That's aggressive.

5. **The leverage is appropriate.** 4.2x entry, declining to 3.0x at exit. Room for more debt if price is lower.

This is the value of a simple model: it gives you the answer quickly, so you can have the right conversation.

---

## Part 2: When to Add Complexity

### The Quarterly Question

The model we built uses annual periods. For a first-pass screen, that's fine. But when does it make sense to go quarterly?

To illustrate the difference, consider what a "full" quarterly LBO model looks like:

| Feature | Simple Annual Model | Complex Quarterly Model |
|---------|---------------------|-------------------------|
| **Periods** | 7 annual | 32 quarterly |
| **Sheets** | 2 | 10+ |
| **Revenue modeling** | Flat annual growth | Quarterly seasonality (Q1: 5%, Q2: 20%, Q3: 30%, Q4: 45%) |
| **Working capital** | DSO/DIO/DPO days | Multi-quarter collection waterfall |
| **Debt structure** | Single senior tranche | Revolver + Senior TL + Subordinated |
| **Cash management** | Excess accumulates | Cash sweep, revolver draw/repay |
| **Tax** | Simple rate × EBT | NOL tracking and utilization |
| **Synergies** | None | Year-by-year phase-in schedule |
| **Circularity** | None | Interest ↔ Debt ↔ Cash Flow loops |
| **Build time** | 1-2 hours | 1-2 days |

### Inside a Complex Quarterly Model

A proper quarterly model isn't just an annual model with more columns. It's architecturally different.

**Revenue Seasonality**

Many businesses have significant intra-year revenue patterns. A retailer might do 45% of annual revenue in Q4. A construction company might do 70% between April and September. An accounting firm peaks in Q1.

If you model these businesses annually, you assume smooth cash flows throughout the year. But the reality is different: they might be cash-negative for three quarters and massively cash-positive in one. This matters for:
- Peak revolver utilization (and associated interest costs)
- Covenant testing timing (you might trip a covenant in a weak quarter)
- Working capital financing needs

**Working Capital Collection Patterns**

Our simple model assumes A/R turns over every 45 days, smoothly. A complex model tracks the actual collection waterfall:

| Revenue Period | Collected in Same Q | Collected Q+1 | Collected Q+2 | Collected Q+3 |
|----------------|---------------------|---------------|---------------|---------------|
| Q1 Revenue | 0% | 35% | 45% | 20% |
| Q2 Revenue | 0% | 35% | 45% | 20% |
| ... | ... | ... | ... | ... |

With 180-250 day DSO (common in healthcare, government contracting, some B2B), you're collecting Q1 sales in Q3 and Q4. This creates significant working capital timing mismatches that annual models miss entirely.

**Multiple Debt Tranches**

A real LBO capital structure often includes:

1. **Revolving Credit Facility (RCF)**: Undrawn until needed, then drawn to cover working capital swings or shortfalls. Interest only on drawn amounts, plus commitment fee on undrawn capacity.

2. **Senior Secured Term Loan**: The main debt, usually 1% annual amortization, bullet at maturity.

3. **Subordinated / Mezzanine Debt**: Higher rate, often with PIK toggle (pay cash or accrue to principal). Sits behind senior in the waterfall.

4. **Holdco PIK Notes**: Sometimes sponsors add debt at the holding company level, which compounds.

Modeling these correctly requires quarterly precision because:
- Revolver draws and repays happen within quarters
- PIK interest compounds quarterly
- Cash sweeps are calculated annually but paid from quarterly cash

**The Circularity Problem**

Complex models often have circular references:

```
Interest Expense → depends on → Debt Balance
Debt Balance → depends on → Cash Available for Paydown  
Cash Available → depends on → Interest Expense
```

In annual models, you can usually ignore this or use a simple iteration. In quarterly models with revolvers, the circularity is unavoidable. You need either:
- Excel's iterative calculation (dangerous — can mask errors)
- A "copy-paste values" macro approach
- A dedicated circularity breaker cell

**Cash Flow Sweeps**

Many credit agreements require "excess cash flow" sweeps — a percentage of annual free cash flow must go to debt paydown. The calculation is complex:

```
Consolidated Net Income
+ Depreciation and Amortization
- Capital Expenditures (maintenance only, growth may be excluded)
- Scheduled Debt Payments
- Working Capital Increase
- Permitted Investments
- Cash Taxes Paid
- Cash Interest Paid
± Other permitted add-backs and deductions
= Excess Cash Flow

× Sweep Percentage (often 50-75%, with step-downs based on leverage)
= Mandatory Prepayment
```

This is a year-end calculation, but it depends on quarterly cash flows throughout the year. Getting it right requires quarterly tracking.

### When Complexity Changes the Answer

The key question: does quarterly precision change your investment decision?

**Complexity matters when:**

1. **Seasonality is extreme.** If Q4 is 45% of revenue and Q1 is 5%, annual averaging hides critical cash flow dynamics. You might need peak revolver capacity that's 3x the annual average working capital need.

2. **You're close to covenant levels.** If annual average leverage is 4.8x but Q1 leverage is 5.3x, you'll trip a quarterly test. This happens when EBITDA is seasonal but debt is constant.

3. **Working capital timing creates liquidity risk.** Long collection cycles combined with seasonal revenue can create quarters where you're deeply drawn on the revolver. Annual models miss this.

4. **Debt structure has moving parts.** Cash sweeps, PIK toggles, revolver utilization — all benefit from quarterly tracking.

5. **You're running the company.** Post-close, you need quarterly forecasts for board reporting, covenant compliance, and treasury management.

**Complexity doesn't matter when:**

1. **You're screening.** First-pass analysis to decide if a deal is worth pursuing.

2. **The business is stable.** Healthcare, essential services, subscription software — low seasonality, predictable cash.

3. **Debt structure is simple.** Single term loan, no revolver or subordinated debt.

4. **You're far from covenant levels.** If leverage is 3x with a 5.5x covenant, quarterly fluctuations don't matter.

5. **You're presenting to committee.** Senior decision-makers want to understand the story, not audit 32 periods.

### Beyond Quarterly: Advanced Model Features

Even annual models can incorporate sophisticated features when the deal structure warrants. Here's what "Level 5" complexity looks like:

**1. Public Company Take-Private Mechanics**

When acquiring a public company like Meridian (or Twitter), the model must handle:

| Element | Calculation |
|---------|-------------|
| **Offer price** | Current share price × (1 + Premium) |
| **Diluted shares** | Basic + Options (Treasury Stock Method) + RSUs + PSUs |
| **Purchase equity value** | Offer price × Diluted shares |
| **Enterprise value** | Equity value + Debt - Cash - NOL value |

The Treasury Stock Method for options is often overlooked. If you're paying €10/share and there are 1 million options with a €6 strike price, those options are in-the-money. But the exercise generates cash: 1M × €6 = €6M. The net dilution is only the difference: 1M shares - (€6M / €10) = 400,000 net new shares.

**2. Purchase Price Allocation (PPA)**

When you pay more than book value, the premium must be allocated:

```
Purchase Premium = Equity Purchase Price - Seller's Book Value + Existing Goodwill
                 = Total Allocable Premium

Allocation:
(-) Write-up of PP&E (e.g., 10% of PP&E value, depreciated over 20 years)
(-) Write-up of Intangibles:
    - Indefinite-lived (15% of premium, no amortization)
    - Definite-lived (5% of premium, amortized over 10 years)
(+) New Deferred Tax Liability (25% of write-ups)
(=) Goodwill Created (the residual)
```

This matters because the depreciation and amortization of write-ups creates tax shields that affect cash flow and covenant calculations.

**3. Multiple Debt Tranches with Different Economics**

Real LBO capital structures often include:

| Tranche | Rate | Amortization | Cash Flow Sweep | Other Features |
|---------|------|--------------|-----------------|----------------|
| **Revolver** | SOFR + 425bps | None | None | Undrawn fee 50bps |
| **Term Loan B** | SOFR + 475bps, 0.5% floor | 1% | 50% | Senior secured |
| **Senior Secured Notes** | Fixed 8.375% | None | 100% | Non-call period |
| **Margin Loan** | SOFR + 300bps | 5% | 100% | Prepayment penalty 1.5% |
| **Conv. Preferred** | 14% PIK dividend | None | None | Converts at exit |

Each tranche has its own waterfall priority for cash sweeps: Revolver first (repaid), then Term Loan, then Senior Notes, then Subordinated.

**4. PIK Interest and Dividend Toggle**

Some instruments allow interest to accrue to principal rather than pay cash:

```
Beginning Subordinated Notes: €100M
(+) PIK Interest (5%):        €5M
(-) Cash Interest (5%):       (€5M) paid from cash flow
(=) Ending Balance:           €105M
```

PIK increases the debt balance over time, which can trap you if operating performance disappoints. The Twitter deal included a margin loan with PIK toggle — if cash flow was tight, Musk could elect to accrue rather than pay.

**5. Management Incentive Structures**

Sophisticated models track three types of management economics:

- **Rollover equity**: Management rolls a percentage of their existing stake into the new structure (typically 10-20%)
- **Options pool**: Post-deal options at the offer price (typically 5-10% of diluted equity)
- **Earn-out tiers**: Marginal profit sharing above return thresholds

Example earn-out structure:
```
Tier 1: 5% of proceeds above 1.5x equity multiple
Tier 2: 10% of proceeds above 2.0x equity multiple

If initial equity = €500M and exit equity = €1,500M (3.0x):
  Tier 1 payout: (€1,000M - €750M) × 5% = €12.5M
  Tier 2 payout: (€1,500M - €1,000M) × 10% = €50M
  Total management earn-out: €62.5M
```

**6. Dividend Recapitalizations**

Sponsors sometimes take a "dividend recap" — raising additional debt mid-investment to pay themselves a dividend:

```
Year 3:
  EBITDA: €150M
  Div recap leverage: 2.0x
  New debt issued: €300M
  Less: issuance fees (2%): (€6M)
  Dividend to sponsor: €294M
```

This accelerates returns (cash out earlier = higher IRR) but increases risk (more debt on the business). The model must track the new tranche separately, including its own amortization and cash flow sweep.

**7. Returns Attribution**

Advanced models decompose returns into sources:

| Source | Contribution |
|--------|--------------|
| EBITDA growth | €X of exit EV increase |
| Multiple expansion | €Y of exit EV increase |
| Debt paydown | €Z less debt at exit |
| Dividend recap | €W cash distributed early |
| **Total equity return** | **€Total** |

This tells you *why* the deal worked (or didn't). A deal that only works with multiple expansion is speculative. A deal that works primarily on debt paydown is safe but boring. The best deals work on multiple levers.

**8. Tax Complexity**

Real models must address:

- **Interest deductibility limits**: Post-2017 US law limits interest deductions to 30% of EBITDA
- **NOL utilization**: Section 382 limits how quickly you can use acquired NOLs after a change of control
- **R&D capitalization**: Post-2022 US law requires capitalizing R&D over 5 years (domestic) or 15 years (foreign)

These can materially affect cash taxes and therefore cash available for debt service.

### The Meridian Verdict: Matching Complexity to Purpose

For Meridian Plasma Group, where does our simple model fall short, and does it matter?

| Feature | Our Simple Model | Advanced Model | Impact on Decision? |
|---------|------------------|----------------|---------------------|
| **Periodicity** | Annual | Quarterly | Low — stable business |
| **Share dilution** | Not modeled | TSM for options, RSUs | Medium — affects equity check |
| **PPA** | Not modeled | Full allocation | Low — affects tax shields |
| **Debt tranches** | Single TLB | Revolver + TLB + Notes | Medium — affects interest cost |
| **Cash sweeps** | None | 50% ECF sweep | Medium — faster delevering |
| **Management incentives** | Not modeled | Rollover + options + earn-out | Low — affects sponsor returns |
| **Dividend recap** | Not modeled | Year 3 recap option | Medium — affects IRR timing |
| **Tax complexity** | Simple rate | Interest limits, NOLs | Low — Meridian has clean taxes |

The honest assessment: our simple model tells us the deal doesn't work at asking price. An advanced model would tell us the same thing with more precision — maybe 10.3% IRR instead of 10.8%, or 1.65x instead of 1.67x.

**When to invest in complexity:**

1. **Pre-LOI screening**: Simple model. Get the answer fast.
2. **Post-LOI diligence**: Add tranches, management terms, PPA impacts.
3. **Financing roadshow**: Full quarterly model for bank presentations.
4. **Post-close budgeting**: Maximum complexity for operational management.

The purpose determines the precision. Don't build a quarterly model to answer an annual question.

---

## Part 3: Connecting to Documentation

### Where the Model Meets the Covenants

The model we built assumes certain things about how the capital structure works. Those assumptions are either confirmed or contradicted by the credit documentation.

**Interest Rate:**
- Model assumes: 6% fixed
- Documentation reality: EURIBOR + 400bps margin, with rate cap at 2% EURIBOR
- Impact: If rates rise, interest expense increases. The cap provides protection but not complete hedging.

**Amortization:**
- Model assumes: 1% annual
- Documentation reality: Need to check credit agreement for mandatory amortization schedule, excess cash flow sweep provisions
- Impact: If there's a 50% excess cash flow sweep, debt paydown is faster than modeled, improving returns

**EBITDA Definition:**
- Model assumes: Revenue - COGS - OpEx + D&A
- Documentation reality: Adjusted EBITDA per credit agreement includes addbacks for restructuring, transaction costs, synergies
- Impact: Credit agreement EBITDA is typically 5-10% higher than GAAP EBITDA. This provides covenant cushion.

**Covenant Tests:**
- Model assumes: 5.5x leverage test with 40% headroom
- Documentation reality: Need to check if covenant is maintenance or incurrence-only, whether there's a covenant holiday, what the ratchet looks like
- Impact: Covenant-lite documentation (incurrence only) provides more flexibility but less protection

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

*"We like the business. We can finance it. But the returns don't work at your asking price. Here's what we can pay, and here's the analysis that supports it."*

That's what the model is for. Not to produce a precise answer, but to define the boundaries of what makes sense.

---

*Next: Chapter 20 steps back from the technicals to discuss what twenty years of practice teaches about leveraged finance — the lessons that don't fit in a spreadsheet.*
