# Section: Does Complexity Actually Change the Answer?

## The Experiment

We've talked in abstract terms about when complexity matters and when it doesn't. Let me show you concretely.

I built the same Meridian deal eight different ways, starting with our simple annual model and progressively adding features until I had a full quarterly model with all the bells and whistles. At each step, I tracked three metrics:

- **Sponsor IRR** — The headline return number that drives the investment decision
- **Average Interest Coverage Ratio** — A key credit metric (EBITDA ÷ Interest Expense, averaged across the hold period)
- **Cumulative Cash Flow Available for Debt Service** — Total cash generated before debt repayment, a measure of the business's raw cash-generating power

Same company. Same entry price. Same operating assumptions. Just different levels of model sophistication.

Here's what I found:

### The Complexity Waterfall

| Model Version | Feature Added | IRR | Δ vs. Simple | Avg ICR | Δ vs. Simple | Cum. CFADS | Δ vs. Simple |
|---------------|---------------|-----|--------------|---------|--------------|------------|--------------|
| **1. Simple Annual** | Baseline | 13.2% | — | 4.8x | — | €1,844m | — |
| **2. Quarterly Periods** | 32 quarters instead of 7 years | 13.1% | -0.1% | 4.8x | 0.0x | €1,839m | -€5m |
| **3. Multi-Tranche Debt** | RCF + TLB + Senior Notes | 12.9% | -0.3% | 4.6x | -0.2x | €1,784m | -€60m |
| **4. Cash Flow Sweep** | 50% ECF mandatory prepayment | 13.4% | +0.2% | 4.7x | -0.1x | €1,784m | €0m |
| **5. Working Capital Seasonality** | Quarterly WC with collection lag | 13.3% | +0.1% | 4.7x | -0.1x | €1,734m | -€50m |
| **6. PIK Toggle** | €200m mezz with PIK option | 13.6% | +0.4% | 4.4x | -0.4x | €1,814m | -€30m |
| **7. Dividend Recap** | €300m recap at Year 3 | 15.1% | +1.9% | 4.2x | -0.6x | €1,814m | -€30m |
| **8. Management Dilution** | 8% to mgmt (rollover + options) | 14.3% | +1.1% | 4.2x | -0.6x | €1,814m | -€30m |

*Note: Each row includes all features from previous rows. "Δ vs. Simple" shows cumulative change from the baseline model.*

Let's walk through what's happening at each step.

### Step by Step: What Each Feature Actually Does

**Step 1 → 2: Adding Quarterly Periodicity**

Impact: IRR -0.1%, ICR unchanged, CFADS -€5m

Almost nothing changes. Why? Because Meridian is a stable healthcare business with minimal seasonality. Q1 looks like Q2 looks like Q3 looks like Q4. When you model it quarterly, you just get the same annual numbers divided by four.

The tiny IRR decrease comes from more precise timing of cash flows — interest accrues within quarters rather than being assumed at year-end. For a business with extreme seasonality (retail, construction, agriculture), this step would matter much more. For Meridian, it's rounding error.

**Step 2 → 3: Adding Multiple Debt Tranches**

Impact: IRR -0.3%, ICR -0.2x, CFADS -€60m

Now we're replacing our simple 6% term loan with a real capital structure:
- €200m Revolving Credit Facility at EURIBOR + 425bps (plus 50bps undrawn fee)
- €2,200m Term Loan B at EURIBOR + 475bps
- €600m Senior Secured Notes at 8.375% fixed

The blended cost of debt is higher than our simple 6% assumption — more like 6.5% when you account for the fixed-rate notes and the commitment fee on the undrawn revolver. That's €15m more interest annually, which compounds over five years.

The IRR drops because we're paying more for debt. The coverage ratio drops for the same reason. CFADS falls because higher interest expense means less cash available.

This is a real difference, but it doesn't change the investment decision. A 10.5% IRR is still below hurdle, just like 10.8% was.

**Step 3 → 4: Adding an Excess Cash Flow Sweep**

Impact: IRR +0.4%, ICR +0.1x, CFADS unchanged

Here's something interesting: adding the cash sweep *improves* returns.

The sweep requires 50% of excess cash flow to prepay debt (stepping down to 25% when leverage falls below 3.5x). This accelerates deleveraging, which means:
- Less debt at exit → Higher exit equity value
- Lower average debt balance → Less interest expense in later years
- Earlier paydown → Slightly higher IRR due to time value

CFADS doesn't change because it's measured before debt repayment. But the sweep redirects where that cash goes — to lenders instead of sitting on the balance sheet.

For sponsors, cash sweeps are usually seen as negative (less flexibility, can't dividend the cash out). But from a pure IRR perspective, paying down expensive debt faster is value-accretive.

**Step 4 → 5: Adding Working Capital Seasonality**

Impact: IRR +0.3%, ICR unchanged, CFADS -€80m

We added a realistic collection pattern: 35% of receivables collected in the following quarter, 45% in the quarter after that, 20% in the quarter after that. This creates working capital timing mismatches that require revolver draws in certain quarters.

The IRR actually ticks up slightly because of cash flow timing within years — more of the cash comes earlier in each year rather than being spread evenly. But cumulative CFADS drops because we're now paying interest on revolver drawings during working capital peaks.

For Meridian, this is a modest effect. For a business with 180-day DSO and heavy Q4 seasonality, this step would be much more significant.

**Step 5 → 6: Adding a PIK Toggle**

Impact: IRR +0.6%, ICR -0.3x, CFADS -€20m

We added €200m of mezzanine debt with a PIK toggle — the sponsor can choose to pay cash interest (10%) or let it accrue to principal (12% PIK rate).

In the model, we assume PIK for the first two years (preserving cash when leverage is highest) and cash pay thereafter. This creates an interesting dynamic:
- Early years: Lower cash interest expense, more cash available
- Later years: Larger debt balance from accrued PIK, higher cash interest on the now-larger balance
- Exit: More debt to pay off, but growth has outpaced the PIK accrual

The net effect is positive for IRR because the cash preservation in early years is worth more (time value) than the incremental interest paid later. But coverage ratios decline because we've added subordinated debt to the structure.

**Step 6 → 7: Adding a Dividend Recapitalization**

Impact: IRR +2.1%, ICR -0.5x, CFADS unchanged

This is the big one.

In Year 3, with leverage down to ~3.0x and EBITDA grown to €856m, the company raises €300m of incremental debt and dividends it to the sponsor. The mechanics:

```
Year 3 Dividend Recap:
  EBITDA: €856m
  Current leverage: 3.0x
  Post-recap leverage: 3.4x
  New debt raised: €300m
  Less: fees (2%): (€6m)
  Dividend to sponsor: €294m
```

The sponsor originally invested €4,302m. Getting €294m back in Year 3 means:
- Year 0: -€4,302m
- Year 3: +€294m
- Year 5: +€6,200m (reduced from €6,850m because of higher exit debt)

Even though total cash returned is similar, the *timing* is dramatically better. Getting money back earlier increases IRR substantially. The MoC actually drops slightly (from 1.67x to ~1.51x) because you're measuring final value against initial investment, but the IRR pops because of the interim cash flow.

This is why dividend recaps are so popular with sponsors — they juice the IRR number that gets reported to LPs.

From a credit perspective, coverage ratios decline because you've relevered the business. The company was on a nice deleveraging trajectory, and you just reversed part of it. Lenders generally don't love this, which is why dividend capacity is a heavily negotiated provision in credit agreements.

**Step 7 → 8: Adding Management Dilution**

Impact: IRR -0.8%, ICR unchanged, CFADS unchanged

Finally, we account for management's piece of the pie:
- 3% rollover equity (management keeps some of their existing stake)
- 5% option pool with hurdle-based vesting

The sponsor now owns 92% of the exit equity instead of 100%. Coverage ratios and CFADS are unchanged — these are company-level metrics, unaffected by who owns the equity. But sponsor IRR drops because they're sharing the upside.

This is a real economic cost that simple models often ignore. An 8% management promote on a €6.5bn exit is €520m that doesn't go to the fund.

### The Punchline

After all that work — quarterly periods, multiple debt tranches, cash sweeps, working capital seasonality, PIK instruments, a dividend recap, management dilution — where did we land?

| Metric | Simple Model | Complex Model | Change |
|--------|--------------|---------------|--------|
| **IRR** | 13.2% | 14.3% | +1.1% |
| **Average ICR** | 4.8x | 4.2x | -0.6x |
| **Cumulative CFADS** | €1,844m | €1,814m | -€30m |

The IRR increased by 1.1 percentage points — almost entirely from the dividend recap. Strip that out, and the complex model produces almost identical returns to the simple one.

The credit metrics actually got slightly worse (lower coverage) because we added subordinated debt and relevered for the dividend. The business generates roughly the same amount of cash either way.

**The fundamental conclusion hasn't changed: this deal is marginal at 10x EBITDA.**

A 14.3% IRR is better than 13.2%, but it's still below the 15%+ hurdle that most large-cap buyout funds target. The complex model tells us the same thing the simple model told us — we're right on the edge, and the deal only works with either a lower entry price or genuine operational improvement. It just took five times longer to get there.

### When the Answer *Would* Change

To be fair, there are deals where complexity genuinely matters. Here's what would have to be different:

**1. If Meridian had extreme seasonality**

Imagine 60% of revenue in Q4 (like a retailer). The simple model would show smooth annual cash flows, but the reality would be:
- Q1-Q3: Negative operating cash flow, heavy revolver draws
- Q4: Massive cash generation, revolver paydown

Peak revolver utilization might be 3x the annual average working capital need. Interest expense would be higher. And you might trip a quarterly leverage covenant in Q2 even though annual leverage is fine.

For Meridian (stable healthcare), this doesn't apply. For a seasonal business, the quarterly model would reveal risks the annual model hides.

**2. If we were close to covenant levels**

Our simple model showed 4.2x entry leverage against a 5.5x covenant — plenty of headroom. But imagine entry leverage of 5.2x against a 5.5x covenant.

In the annual model, you might show leverage declining smoothly: 5.2x → 4.8x → 4.4x → 4.0x.

But quarterly, with seasonal EBITDA, you might see:
- Q1 Year 1: 5.6x (seasonal EBITDA trough) — **covenant breach**
- Q2 Year 1: 5.0x
- Q3 Year 1: 4.8x
- Q4 Year 1: 4.4x (seasonal EBITDA peak)

The annual model would show comfortable compliance. The quarterly model would reveal you breach in the first quarter. That's a material difference.

**3. If the debt structure had complex interactions**

Our multi-tranche structure was relatively simple — different rates, but straightforward. Some deals have:
- Cash flow sweeps that change based on leverage (50% above 4x, 25% below)
- PIK that toggles automatically based on coverage ratios
- Springing covenants that only test when revolver utilization exceeds a threshold
- Subordination waterfalls where junior debt doesn't get cash pay until senior is below a certain level

These features create non-linear dynamics where the answer depends on the *path* of cash flows, not just the cumulative total. Annual models can't capture this; quarterly models can.

**4. If the deal was marginal**

Our deal showed 10.8% IRR against a 15% hurdle — clearly below. But what if the simple model showed 14.5%?

Now you're in the zone where the complexity features could tip the answer. The dividend recap alone added 2.1% IRR. A deal that looks marginal in a simple model might clear the hurdle once you add the recap. Or it might fall below hurdle once you add management dilution.

When you're close to the decision boundary, precision matters.

### The Real Lesson

The value of this exercise isn't the specific numbers — it's the framework for thinking about model complexity.

Before you build the quarterly model with all the bells and whistles, ask yourself:
1. Does this business have seasonality that annual periods would hide?
2. Am I close to covenant levels where quarterly fluctuations matter?
3. Does the debt structure have features that interact in non-linear ways?
4. Is the deal marginal, where 1-2% IRR difference would change the decision?

If the answer to all four is "no," the simple model is not just adequate — it's preferable. You'll get to the answer faster, the model will be easier to explain, and you won't introduce complexity-related errors.

If the answer to any is "yes," invest in the complexity. It'll be worth it.

For Meridian, we learned that our simple model was right: the deal doesn't work at asking price. The complex model confirmed it with more precision but the same conclusion. That's an hour well spent on complexity analysis — and several hours well saved by not building the full complex model from scratch for the initial screen.

---

## Visual: The Complexity Waterfall

*[Author's note: Insert waterfall chart here showing IRR progression from 10.8% to 12.1% as each feature is added]*

The chart would show:
- Starting bar: 13.2% (Simple Annual)
- Quarterly periodicity: -0.1%
- Multi-tranche debt: -0.2%
- Cash flow sweep: +0.5%
- Working capital seasonality: -0.1%
- PIK toggle: +0.3%
- Dividend recap: +1.5%
- Management dilution: -0.8%
- Ending bar: 14.3% (Full Complex)

What the waterfall reveals: most of the IRR improvement comes from one feature (the dividend recap) that has nothing to do with model precision and everything to do with deal structure. The "modeling complexity" features (quarterly periods, working capital seasonality) barely move the needle.

---

*In the accompanying Excel model, you can toggle each feature on and off to see its individual impact. The "Model Complexity Analysis" sheet provides a sensitivity showing how the answer changes as you add or remove features.*
