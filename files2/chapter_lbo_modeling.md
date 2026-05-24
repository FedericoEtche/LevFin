# The LBO Model: From Operating Projections to Transaction Analysis

## Introduction: The Leap from Corporate to LBO

A corporate financial model has been constructed. Revenue flows from drivers. Costs build from components. The three statements link and balance. Scenarios stress-test the business. The DRIVERS framework has served its purpose.

The next phase involves wrapping a transaction around this foundation.

The corporate model reveals what the business does — how it generates revenue, incurs costs, and produces cash flow. The LBO model analyzes what occurs when an acquirer purchases this business using borrowed capital.

This distinction is fundamental. It represents a transformation.

In a corporate model, the company exists in isolation. It has whatever capital structure it has. Debt might be €50m or €500m — whatever's on the balance sheet. The model projects forward from that starting point.

In an LBO model, the capital structure is a *choice*. A private equity sponsor is acquiring the business, and they're deciding how much debt to use, what type, at what price. They're engineering the capital structure to maximise their returns while (hopefully) not blowing up the company.

The corporate model asks: given this business and this capital structure, what happens?

The LBO model asks: given this business, what capital structure should we use, and what returns can we generate?

Same business. Different question. Different model.

### The Sequencing Principle

A common error in model sequencing: the LBO model cannot be constructed until the corporate model is complete.

This sounds obvious, but the implication is important. The operating projections — revenue, EBITDA, cash flow — must come *first*. Only then can you determine how much debt the business can support. Only then can you structure the transaction. Only then can you calculate returns.

A well-structured LBO model follows a clear progression:

1. **Operating model** — Project the business (the DRIVERS framework)
2. **Debt capacity analysis** — Determine how much leverage the cash flows support
3. **Transaction structure** — Set Sources & Uses, capital structure
4. **Pro-forma balance sheet** — Build the Day One starting point
5. **Debt schedules** — Track instruments through the projection period
6. **Returns analysis** — Calculate IRR, MoC, sensitivities

Skip steps or do them out of order, and you end up with circular logic or a model that doesn't tie.

### The Dual Perspective

LBO analysis presents a distinctive challenge: two distinct parties with different objectives must be simultaneously satisfied.

**The Lender's Perspective**

The banks and credit funds providing the debt care about one thing: getting repaid. They want to know:
- Can the company service the interest? (Coverage ratios)
- Will leverage decline over time? (Deleveraging trajectory)
- What happens if things go wrong? (Downside scenarios)
- Is there enough cushion? (Covenant headroom)

This alignment with the corporate modeling chapter's emphasis: credit metrics, the 50% rule, stress testing. The lender's focus remains fixed on avoiding losses, not on equity returns.

**The Sponsor's Perspective**

The private equity fund acquiring the business cares about something entirely different: making money. They want to know:
- What is the return on equity? (IRR)
- How much capital is returned? (Multiple of Capital, or MoC)
- How sensitive is the return to assumptions? (Entry/exit multiple sensitivity)
- What mechanisms can improve returns? (Value creation bridges)

The sponsor is an equity investor. They're putting in €150m and hoping to get back €400m in five years. Their entire analysis is oriented around that payoff.

**The Beautiful Tension**

These perspectives are linked yet remain misaligned.

More debt means higher returns for the sponsor (if things go well) but higher risk for the lender (if things go poorly). The sponsor wants to maximise leverage; the lender wants to constrain it.

The LBO model captures this tension. It shows you the deal from both angles — credit metrics for the lender, equity returns for the sponsor — and lets you find the structure that works for both.

When a deal "works," it means the lender is comfortable with the credit risk *and* the sponsor is satisfied with the expected return. When one can't find that overlap, the deal doesn't happen.

### Chapter Scope

This chapter takes the Europa Packaging corporate model and transforms it into a complete LBO model. The additions include:

1. **Transaction assumptions** — purchase price, financing structure
2. **Sources & Uses** — where the money comes from, where it goes
3. **The EV-to-Equity bridge** — adjusting for debt-like items
4. **Acquisition accounting** — goodwill, purchase price allocation, tax effects
5. **The Day One balance sheet** — the company's new starting point
6. **Debt schedules** — detailed tracking of each instrument
7. **Sponsor returns** — IRR, MoC, equity bridge
8. **Integrated outputs** — credit metrics AND sponsor economics on one page

By the end, you'll have a model that answers: should the lender provide the debt? Should the sponsor do the deal? And at what price does the answer to both questions become "yes"?

---

## The Transaction: Acquiring Europa Packaging

A transaction scenario is presented below.

Olympus Partners, a mid-market European private equity fund, is acquiring Europa Packaging from its current owner (a family that built the business over three generations and is now seeking monetization).

The key transaction parameters:

| Item | Value | Notes |
|------|-------|-------|
| Enterprise Value | €500m | Based on 6.4x FY24 EBITDA of €78m |
| Equity Value | €480m | EV adjusted for net debt and debt-like items |
| Transaction Date | 31 December 2024 | Clean year-end close |
| Projection Period | FY25E - FY29E | Five-year hold period |
| Exit Date | 31 December 2029 | Sponsor targets 5-year exit |

Why 6.4x EBITDA? Because that's roughly where comparable European packaging deals have traded. It's not cheap, it's not expensive — it's market.

The sponsor needs to finance this €500m enterprise value somehow. That's where the capital structure comes in.

---

## The Enterprise Value to Equity Value Bridge

When we say Olympus is paying €500m Enterprise Value, that's not quite the full story.

Enterprise Value is a measure of business value — what the operating assets are worth, independent of how they're financed. But Olympus isn't buying "business value." They're buying equity — the residual claim after all other stakeholders are satisfied.

To get from EV to the equity cheque, you need to bridge the gap. And that bridge has more items than most junior analysts realise.

### The Standard Bridge

```
ENTERPRISE VALUE TO EQUITY VALUE
═══════════════════════════════════════════════════════════════════════════════════
Enterprise Value                                              €500m
───────────────────────────────────────────────────────────────────────────────────
Less: Total Debt                                              (€20m)
Plus: Cash                                                     €20m
───────────────────────────────────────────────────────────────────────────────────
Equity Value (Simple)                                          €500m
═══════════════════════════════════════════════════════════════════════════════════
```

If Europa had €20m of debt and €20m of cash, the simple bridge says EV equals Equity Value. The debt and cash offset.

But this is naive. There are other claims on the business that function like debt — obligations that will consume future cash flows before equity holders see a penny.

### Debt-Like Items

A thorough LBO analysis requires identifying and quantifying all liabilities that function like debt. These items represent non-equity claims on the company's future cash flows and thereby increase the effective purchase price. Getting this bridge wrong means mispricing the deal.

**Underfunded Pension Obligations**

If Europa has a defined benefit pension plan that's underfunded by €15m, that's a real liability. The company will need to make contributions to close the gap. It functions exactly like debt — a claim on future cash flows that the new owner inherits.

```
Less: Underfunded Pension                                      (€10m)
```

**Minority Interests**

If Europa owns 80% of a subsidiary, there's a 20% minority interest that appears in consolidated equity but belongs to someone else. Either you buy them out (a use of funds) or you recognise that 20% of that subsidiary's cash flows aren't yours. If not bought out, it remains a claim on a portion of the consolidated entity's cash flows and must be valued accordingly.

```
Less: Minority Interest                                        (€Xm)
```

**Fair Valuation of Derivatives**

Any existing derivative contracts held by the target must be marked to market. If Europa has interest rate swaps or currency hedges that are out-of-the-money, those represent a liability. If they're in-the-money, an asset. This revaluation can create a new asset or liability on the pro-forma balance sheet.

```
Less: Derivative Liabilities (net)                             (€5m)
```

**Warranty and Other Provisions**

Provisions for warranties, legal claims, restructuring — these are future cash outflows. If Europa has €8m of warranty provisions, that's €8m the new owner will eventually pay. They represent predictable future cash outflows that effectively increase the acquisition cost.

```
Less: Warranty Provisions                                      (€5m)
```

### The Complete Bridge

```
ENTERPRISE VALUE TO EQUITY VALUE — COMPLETE
═══════════════════════════════════════════════════════════════════════════════════
Enterprise Value                                              €500m
───────────────────────────────────────────────────────────────────────────────────
Less: Total Debt                                              (€20m)
Plus: Cash                                                     €20m
Less: Underfunded Pension                                     (€10m)
Less: Minority Interest                                           —
Less: Warranty Provisions                                      (€5m)
Less: Derivative Liabilities                                   (€5m)
Plus: Non-Operating Assets                                        —
───────────────────────────────────────────────────────────────────────────────────
Equity Value (Adjusted)                                        €480m
═══════════════════════════════════════════════════════════════════════════════════
```

Now the €480m equity cheque makes sense. The sellers get €480m because that's what's left after accounting for all the other claims on the business.

For Europa, the model assumes modest debt-like items: a small pension deficit (€10m), some warranty provisions (€5m), and derivative liabilities (€5m). These net out to €20m of adjustments.

In many deals — especially industrial companies with legacy pension obligations or businesses with significant warranty exposure — these adjustments can be tens or hundreds of millions of euros. Miss them, and you've mispriced the deal.

---

## Sources & Uses: The Transaction's Master Ledger

Every LBO starts with the same question: where does the money come from, and where does it go?

This is captured in the **Sources & Uses** table — the definitive summary of the LBO transaction. Its strategic importance lies in its simplicity: it ensures the total capital being provided for the deal (the Sources) precisely matches the total capital required to complete it (the Uses). It acts as the transaction's master ledger.

### The Uses Side

The "Uses" side is simpler and is examined first. The funds are deployed toward the following purposes:

| Use of Funds | Amount (€m) | Notes |
|--------------|-------------|-------|
| Purchase Equity | 480 | Payment to selling shareholders |
| Refinance Existing Debt | 20 | Pay off the company's current debt |
| Transaction Fees | 25 | Advisory, legal, financing, due diligence |
| Cash to Balance Sheet | 25 | Minimum operating cash post-close |
| **Total Uses** | **550** | |

These items are addressed in turn:

**Purchase Equity (€480m):** This is the cheque to the sellers — the equity value we calculated in the bridge.

**Refinance Existing Debt (€20m):** The company has €20m of existing bank debt. In most LBOs, you pay this off and replace it with new acquisition financing. Clean slate.

**Transaction Fees (€25m):** These are real costs that real people charge:
- M&A advisory fees (1-2% of EV)
- Legal fees (buyer and seller counsel)
- Accounting and due diligence fees
- Debt arrangement and underwriting fees
- Other professional fees

5% of EV for total fees is aggressive but not unusual for a deal this size.

**Cash to Balance Sheet (€25m):** The company needs operating cash. You don't want to close the deal and immediately have a liquidity crisis. €25m is about 5% of revenue — a reasonable cash buffer.

**Total Uses: €550m**

This is the cheque that needs to be written. Now, where does it come from?

### The Sources Side

The "Sources" side answers: who's providing the €550m?

| Source of Funds | Amount (€m) | % of Total | Multiple | Notes |
|-----------------|-------------|------------|----------|-------|
| Senior Secured Term Loan B | 300 | 54.5% | 3.8x | E + 450bps, 7-year bullet |
| Senior Secured RCF | — | — | — | €50m committed, undrawn at close |
| **Total Debt** | **300** | **54.5%** | **3.8x** | |
| Sponsor Equity | 250 | 45.5% | 3.2x | Olympus Partners |
| **Total Equity** | **250** | **45.5%** | **3.2x** | |
| **Total Sources** | **550** | **100%** | | |

**Sources = Uses. Always.**

This is an accounting identity. Every euro used must come from somewhere. If your sources don't equal your uses, you've made an error.

The capital structure is set out below:

**Senior Secured Term Loan B (€300m):** This is the core debt — a seven-year bullet loan priced at EURIBOR + 450 basis points. At current EURIBOR of ~3.5%, the all-in cost is about 8%. This is the instrument that credit funds and CLOs will buy.

Why €300m? Because at €78m of EBITDA, that's 3.8x leverage — within the acceptable range for a business of this quality. Push it to €350m (4.5x) and lenders get nervous. Drop it to €250m (3.2x) and the sponsor's returns suffer.

**Revolving Credit Facility (€50m committed, undrawn):** The RCF is the company's liquidity backstop. It's there if they need it — for working capital swings, for unexpected cash needs. It's committed but undrawn at close, so it doesn't appear in Sources. But it matters for liquidity analysis.

**Sponsor Equity (€250m):** This is Olympus Partners writing a cheque. It's the "skin in the game" — the capital at risk. Everything above the debt is equity.

€250m of equity on a €550m total capitalisation is 45% equity contribution. That's conservative by LBO standards — many deals run at 35-40% equity. But with EBITDA margins in the mid-teens and a cyclical industry, lenders want more cushion.

### The Leverage Multiple

Notice how each source is also expressed as a multiple of EBITDA:

- Debt: €300m / €78m = 3.8x
- Equity: €250m / €78m = 3.2x
- Total: €550m / €78m = 7.0x (this is your EV/EBITDA entry multiple, adjusted for fees and cash)

These multiples are the language of leveraged finance. When someone says "the deal is 4x levered," they mean total debt equals 4x EBITDA. When they say "it's a 7x entry," they mean total enterprise value is 7x EBITDA.

### Checking the Logic

Does this structure make sense?

**From the lender's perspective:**
- 3.8x leverage is manageable for a packaging business
- Interest coverage at close: €78m EBITDA / €24m interest = 3.3x — adequate
- The business should deleverage to ~2x by exit if the base case holds

**From the sponsor's perspective:**
- €250m equity investment
- If EBITDA grows to €98m and they exit at 6.5x, EV = €637m
- Minus ~€100m remaining net debt = ~€540m equity value
- That's a 2.2x MoC (€540m / €250m) and ~17% IRR
- Acceptable for a stable business

These figures are refined in subsequent sections, but the rough math indicates the transaction is feasible.

---

## Acquisition Accounting: The Pro-Forma Balance Sheet

The pro-forma balance sheet is the central hub for all transaction-related adjustments in an LBO model. It serves as the primary financial statement that bridges the target company's pre-deal standalone structure with the post-deal, highly leveraged entity. Building it correctly is the foundational step upon which the integrity of the entire LBO analysis rests.

When a company is acquired, its balance sheet doesn't just continue as before. It gets *rewritten*. Old equity disappears. New debt appears. Goodwill emerges from the ether. The company that exists on January 1st post-acquisition is financially a different entity than the one that existed on December 31st.

This is acquisition accounting. It is governed by IFRS 3 (or ASC 805 in the US) and is surprisingly complicated. The essentials are covered below.

### The Conceptual Process

The process for creating the pro-forma balance sheet is a logical sequence:

1. **Establish a baseline:** Begin with the target's last historical balance sheet
2. **Model transaction financing:** Incorporate the new capital structure from Sources
3. **Account for fees and equity extinguishment:** Write down existing book equity to zero
4. **Revalue assets to fair market value:** The purchase price allocation (PPA)
5. **Calculate goodwill:** The residual after all other adjustments

### Step 1: The Pre-Acquisition Balance Sheet

Europa's pre-acquisition balance sheet (simplified):

| Assets | €m | Liabilities & Equity | €m |
|--------|-----|---------------------|-----|
| Cash | 20 | Payables | 45 |
| Receivables | 57 | Other current liabilities | 15 |
| Inventory | 55 | Existing debt | 20 |
| PP&E (net) | 164 | Pension obligations | 10 |
| Intangibles | 10 | Provisions | 5 |
| Other assets | 15 | Deferred tax liability | 15 |
| | | **Total Liabilities** | **110** |
| | | Equity | 211 |
| **Total Assets** | **321** | **Total Liab + Equity** | **321** |

The book value of equity is €211m. Olympus is paying €480m for that equity. Why the premium?

### Step 2: Fair Value the Assets (Purchase Price Allocation)

Upon acquisition, accounting rules require that the target's assets and liabilities be "written up" or "written down" to their fair market value. This process, known as purchase price allocation (PPA), can have a significant impact on the balance sheet.

Some assets are worth more than book value:

| Asset | Book Value | Fair Value | Adjustment |
|-------|------------|------------|------------|
| PP&E | 164 | 180 | +16 |
| Customer relationships | 0 | 45 | +45 |
| Tradenames/brands | 5 | 25 | +20 |
| Other intangibles | 5 | 5 | — |

The PP&E was depreciated on the old owner's books, but the machinery and real estate are worth more than the carrying value. An independent valuation says €180m.

Customer relationships and brands weren't on the balance sheet at all (they were internally developed, not acquired). But they have value — quantified by the accountants during PPA. This revaluation directly impacts the amount of goodwill recorded, as goodwill is the residual value after all identifiable tangible and intangible assets have been marked to market.

### Step 3: Account for the Deferred Tax Impact

Here's a subtlety that trips up many models.

The asset write-ups are for *book* purposes only. The *tax* basis doesn't change. This creates a book/tax discrepancy that generates a Deferred Tax Liability:

```
BOOK VS TAX BASIS
═══════════════════════════════════════════════════════════════════════════════════
                            Book Basis      Tax Basis       Difference
───────────────────────────────────────────────────────────────────────────────────
PP&E                           €180m          €164m           €16m
Intangibles (new)              €70m           €10m            €60m
───────────────────────────────────────────────────────────────────────────────────
Total                          €250m          €174m           €76m
═══════════════════════════════════════════════════════════════════════════════════

DTL from Write-Ups = €76m × 25% = €19m
```

This €19m DTL gets added to the existing €15m DTL, giving us €34m total. The DTL reflects the future cash taxes that will be paid as the company depreciates the written-up book value of its assets — book depreciation will exceed tax-deductible depreciation.

### Step 4: Calculate Goodwill

Goodwill is the residual — the amount you paid that can't be allocated to identifiable assets. It arises because the purchase price is typically higher than the fair market value of identifiable net assets.

```
Purchase Price (Equity Value)           €480m
Plus: Debt assumed/refinanced            €20m
Plus: Debt-like items assumed            €20m
Equals: Total Consideration             €520m

Less: Fair value of net assets acquired
  Assets at fair value                  €337m  (321 + 16)
  Plus: New intangibles                  €65m  (customer relationships + brands)
  Less: Liabilities assumed            (€110m)
  Less: Additional DTL from write-ups   (€19m)
  Net assets acquired                   €273m

Goodwill = €520m - €273m = €247m
```

Goodwill of €247m. This represents the "overpayment" — or more charitably, the value of things that can't be separately identified: the workforce, the market position, the synergies, the growth potential. It's an intangible asset representing value that exists but can't be touched or sold separately.

### Step 5: Construct the Day One Balance Sheet

Now we rebuild the balance sheet as it exists immediately after the acquisition closes:

| Assets | €m | Liabilities & Equity | €m |
|--------|-----|---------------------|-----|
| Cash | 25 | Payables | 45 |
| Receivables | 57 | Other current liabilities | 15 |
| Inventory | 55 | New Senior Debt (TLB) | 300 |
| PP&E (net) | 180 | Pension obligations | 10 |
| Customer relationships | 45 | Provisions | 5 |
| Tradenames | 25 | Deferred tax liability | 34 |
| Other intangibles | 5 | **Total Liabilities** | **409** |
| Goodwill | 247 | | |
| Other assets | 15 | Sponsor Equity | 250 |
| | | Retained Earnings | — |
| | | Cumulative Adjustments | (5) |
| **Total Assets** | **654** | **Total Liab + Equity** | **654** |

Notice what changed:

1. **Cash is €25m** — the target cash specified in Sources & Uses
2. **PP&E stepped up to €180m** — fair value adjustment
3. **New intangibles of €70m** — customer relationships and brands
4. **Goodwill of €247m** — the residual
5. **Old debt gone, new debt of €300m** — refinanced
6. **DTL increased to €34m** — includes the write-up effect
7. **Old equity wiped out, new equity of €250m** — the sponsor's investment

The balance sheet balances. €654m = €654m. The pro-forma is now ready for forward projection.

---

## Tax Complexities: NOLs and Change of Control

One more tax issue deserves attention: what happens to the target's net operating losses?

If Europa had accumulated losses from prior years, those NOLs would be valuable — they'd shield future profits from tax.

But here's the catch: change of control often limits NOL usage.

Tax laws in most jurisdictions restrict the annual utilisation of a target's NOLs following a change of control. In the US, Section 382 limits annual NOL usage to roughly:

```
Annual NOL Limit = Fair Value of Company × Long-Term Tax-Exempt Rate
```

European rules vary by jurisdiction but often include similar limitations. Germany, for instance, restricts NOL carryforwards after significant ownership changes.

If Europa had €100m of NOLs, it might only be able to use €20m per year post-acquisition. The rest might expire unused.

The modeling implication: don't assume the target's full NOL balance is available immediately. Build an NOL schedule that respects change-of-control limitations and tracks expiration dates. The FDD's tax section should identify these issues.

For the current model, Europa is assumed to have no material NOLs — the company has been consistently profitable. In turnaround situations or acquisitions of distressed assets, however, NOL limitations can materially impact deal economics.

---

## P&L Knock-On Effects

The comprehensive adjustments made to the pro-forma balance sheet have direct and material consequences for the company's projected Income Statement and Cash Flow Statement. These "knock-on" effects are not secondary details — they are fundamental to projecting the true cash-generating capacity and profitability of the newly leveraged entity.

**Increased Depreciation & Amortisation:**

The write-up of tangible and intangible assets creates a higher asset base, leading to increased annual D&A:

- PP&E write-up of €16m at 6.7% depreciation = ~€1m additional D&A annually
- Customer relationships of €45m over 15 years = €3m amortisation annually
- Brands of €20m over 20 years = €1m amortisation annually
- Total additional D&A: ~€5m per year

This reduces reported EBIT and net income but is entirely non-cash.

**Higher Interest Expense:**

The €300m TLB at 8% = €24m annual interest expense. This is the big P&L impact — a real cash cost that reduces both earnings and cash flow. This expense is a primary driver of the post-LBO earnings profile.

**Transaction Fee Treatment:**

Fees paid to advisors and lenders can be treated different ways:
- Advisory fees: typically capitalised into goodwill (no P&L impact)
- Debt financing fees: capitalised as deferred financing costs, amortised over debt life (~€3m per year over 7 years)
- Other costs: may be expensed immediately

The treatment determines the timing and magnitude of their impact on the income statement.

**Net Impact on Cash Flow:**

The cash flow statement starts with net income, which is now lower due to higher D&A and interest expense. To calculate actual cash flow, the model must add back the new, higher non-cash D&A charges. This critical step ensures that the model reflects the true cash earnings of the business — which is the basis for debt repayment and returns to equity investors.

The net effect: cash flow is primarily reduced by the interest expense. The non-cash items wash out.

---

## The Debt Schedules: Tracking Every Instrument

The corporate model chapter addressed debt schedules at a conceptual level. This section develops them in detail for an LBO.

### The Term Loan B Schedule

```
SENIOR SECURED TERM LOAN B
═══════════════════════════════════════════════════════════════════════════════════
                            Entry   FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
Opening Balance               —      300     300     292     283     275
Drawdowns                    300       —       —       —       —       —
Scheduled Amortisation         —       —       —       —       —       —
Mandatory Prepayment (Sweep)   —       —      (8)     (9)     (8)    (10)
Voluntary Prepayment           —       —       —       —       —       —
Closing Balance              300     300     292     283     275     265
───────────────────────────────────────────────────────────────────────────────────
Average Balance              300     300     296     288     279     270
Interest Rate (E + 450)          8.0%    8.0%    8.0%    8.0%    8.0%
Cash Interest Expense            24.0    23.7    23.0    22.3    21.6
───────────────────────────────────────────────────────────────────────────────────
```

Key features:

**Bullet maturity:** No scheduled amortisation. The principal is due at Year 7 (beyond our model period).

**Cash sweep:** The credit agreement requires 25% of excess cash flow to prepay debt when leverage is between 2.5x-3.5x. As leverage drops below 2.5x, the sweep falls to 0%.

**Interest at EURIBOR + 450bps:** EURIBOR is assumed flat at ~3.5%, giving an all-in rate of 8.0%. In practice, a forward curve can be substituted for the flat-rate assumption.

### The Revolving Credit Facility Schedule

```
REVOLVING CREDIT FACILITY (€50m Commitment)
═══════════════════════════════════════════════════════════════════════════════════
                            Entry   FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
Opening Balance               —        —       —      15       —       —
Drawings                      —        —      15       —       —       —
Repayments                    —        —       —     (15)      —       —
Closing Balance               —        —      15       —       —       —
───────────────────────────────────────────────────────────────────────────────────
Available Capacity           50       50      35      50      50      50
───────────────────────────────────────────────────────────────────────────────────
Interest Rate (E + 350)          7.5%    7.5%    7.5%    7.5%    7.5%
Cash Interest (on drawn)          —      0.6     1.1     —       —
Commitment Fee (0.35%)          0.2     0.2     0.1     0.2     0.2
Total RCF Cost                  0.2     0.8     1.2     0.2     0.2
───────────────────────────────────────────────────────────────────────────────────
```

Key features:

**Undrawn at close:** The RCF is available but not used initially. Good — it means liquidity is adequate.

**Temporary draw in FY26:** The growth capex project in FY27 creates a temporary cash need in FY26. The RCF is drawn €15m and repaid the following year. The RCF is doing its job — providing flexibility.

**Lower spread than TLB:** RCF is E+350 vs TLB at E+450. The lower spread reflects its super-senior position — the RCF gets paid first.

### The Cash Sweep Mechanics

Most LBO credit agreements include a cash sweep — a mandatory prepayment of debt from excess cash flow:

```
EXCESS CASH FLOW CALCULATION
═══════════════════════════════════════════════════════════════════════════════════
                                        FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
EBITDA                                    82      86      91      94      98
Less: Cash Interest                      (24)    (24)    (24)    (23)    (22)
Less: Cash Taxes                          (8)     (9)    (10)    (11)    (12)
Less: Maintenance Capex                  (15)    (15)    (16)    (16)    (17)
Less: Working Capital Increase            (3)     (3)     (3)     (3)     (3)
Less: Scheduled Amortisation               —       —       —       —       —
───────────────────────────────────────────────────────────────────────────────────
Excess Cash Flow                          32      35      38      41      44
───────────────────────────────────────────────────────────────────────────────────
Net Leverage                            3.4x    3.0x    2.6x    2.3x    2.0x
───────────────────────────────────────────────────────────────────────────────────
Sweep Percentage:
  If leverage > 3.5x:                   50%
  If leverage 2.5x - 3.5x:              25%
  If leverage < 2.5x:                    0%
───────────────────────────────────────────────────────────────────────────────────
Applicable Sweep %                       25%     25%      0%      0%      0%
Cash Sweep Amount                          8       9       —       —       —
───────────────────────────────────────────────────────────────────────────────────
```

The cash sweep operates in the early years when leverage is higher. As the company deleverages below 2.5x, the sweep steps down to zero.

### The Debt & Cash Summary

```
DEBT & CASH SUMMARY
═══════════════════════════════════════════════════════════════════════════════════
                            Entry   FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
Gross Debt (TLB)             300     300     292     283     275     265
RCF Drawn                      —       —      15       —       —       —
Total Debt                   300     300     307     283     275     265
Cash                          25      45      28      58      91     128
Net Debt                     275     255     279     225     184     137
───────────────────────────────────────────────────────────────────────────────────
EBITDA                        78      82      86      91      94      98
Net Leverage                3.5x    3.1x    3.2x    2.5x    2.0x    1.4x
───────────────────────────────────────────────────────────────────────────────────
```

Note the FY26 blip — net leverage actually ticks up slightly because of the RCF draw for the growth capex project. By FY27, it's repaid and deleveraging resumes.

By exit, the company has €128m of cash against €265m of gross debt — net debt of €137m, down from €275m at entry. That's €138m of value accretion the sponsor will capture.

---

## Sponsor Returns: IRR and Multiple of Capital

Now we get to the fun part — at least if you're the sponsor.

The private equity fund invested €250m. What do they get back?

### The Exit Valuation

At exit (December 2029), the sponsor will sell the company. The proceeds depend on:

1. **Exit EBITDA** — what the business is earning at exit
2. **Exit Multiple** — what a buyer will pay for those earnings

**Exit EBITDA (FY29E): €98m** — from our projections.

**Exit Multiple: 6.5x** — a slight premium to the 6.4x entry multiple.

Why a premium? The company has deleveraged, proven it can grow, and is now a less risky asset. Buyers typically pay more for proven performers than for turnaround situations.

```
EXIT VALUATION
═══════════════════════════════════════════════════════════════════════════════════
Exit EBITDA                                    €98m
Exit Multiple                                  6.5x
Enterprise Value at Exit                       €637m
Less: Net Debt at Exit                        (€137m)
Equity Value at Exit                           €500m
═══════════════════════════════════════════════════════════════════════════════════
```

The sponsor gets €500m for their equity.

### IRR and MoC Calculation

**Multiple of Capital (MoC):**

```
MoC = Equity Value at Exit / Equity Invested
MoC = €500m / €250m = 2.0x
```

For every euro invested, the sponsor gets €2.00 back. A solid return.

**Internal Rate of Return (IRR):**

IRR is the discount rate that makes the NPV of cash flows equal zero. For a simple LBO with no interim dividends:

```
-€250m at t=0
+€500m at t=5

IRR = (500/250)^(1/5) - 1 = 14.9%
```

A 14.9% IRR over five years. That's at the low end of acceptable for private equity — around the typical hurdle rate of 15%. Not spectacular, but workable for a lower-risk, stable business.

### The Returns Waterfall

The sources of return are decomposed as follows:

```
EQUITY VALUE BRIDGE
═══════════════════════════════════════════════════════════════════════════════════
Entry Equity Investment                                          €250m
───────────────────────────────────────────────────────────────────────────────────
EBITDA Growth Effect:
  Entry EBITDA: €78m → Exit EBITDA: €98m = +€20m
  At exit multiple of 6.5x: +€20m × 6.5x =                       +€130m

Multiple Expansion Effect:
  Entry multiple: 6.4x → Exit multiple: 6.5x = +0.1x
  Applied to entry EBITDA: +0.1x × €78m =                          +€8m

Deleveraging Effect:
  Entry Net Debt: €275m → Exit Net Debt: €137m
  Reduction =                                                    +€138m

Less: Transaction Fees (entry + exit, estimated)                  -€26m
───────────────────────────────────────────────────────────────────────────────────
Exit Equity Value                                                 €500m
MoC                                                               2.0x
IRR                                                              14.9%
═══════════════════════════════════════════════════════════════════════════════════
```

The returns come from three sources:

1. **EBITDA Growth (+€130m):** The business grew EBITDA from €78m to €98m. At the exit multiple, that's worth €130m of additional value.

2. **Multiple Expansion (+€8m):** A small benefit from the exit multiple being slightly higher than entry.

3. **Deleveraging (+€138m):** By paying down debt and accumulating cash, the sponsor captured €138m of value that previously belonged to lenders.

This is the private equity playbook in a nutshell: buy a business, grow it modestly, pay down debt aggressively, sell at a similar multiple. The magic is in the leverage — using borrowed money to amplify equity returns.

---

## The Integrated Output Page

Here's where the dual perspective comes together. One page. Both views. The complete picture.

```
═══════════════════════════════════════════════════════════════════════════════════
                    EUROPA PACKAGING — LBO ANALYSIS SUMMARY
═══════════════════════════════════════════════════════════════════════════════════

TRANSACTION SUMMARY
───────────────────────────────────────────────────────────────────────────────────
Enterprise Value             €500m     Entry Multiple            6.4x
Net Debt at Entry           (€275m)    Total Debt               €300m
Equity Value                 €225m     Sponsor Equity           €250m
                                       Equity %                 45.5%
───────────────────────────────────────────────────────────────────────────────────

                                 BASE CASE PROJECTIONS
───────────────────────────────────────────────────────────────────────────────────
                        FY24    FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
Revenue                  480     498     516     533     550     567
  Growth %                —      3.8%    3.6%    3.3%    3.2%    3.1%
EBITDA                    78      82      86      91      94      98
  Margin %              16.2%   16.5%   16.7%   17.1%   17.1%   17.3%
Free Cash Flow            —       37      23      47      50      54
───────────────────────────────────────────────────────────────────────────────────

                              CREDIT METRICS (Lender View)
───────────────────────────────────────────────────────────────────────────────────
                        Entry   FY25E   FY26E   FY27E   FY28E   FY29E
───────────────────────────────────────────────────────────────────────────────────
Net Debt                 275     255     279     225     184     137
Net Leverage            3.5x    3.1x    3.2x    2.5x    2.0x    1.4x
Interest Coverage       3.3x    3.4x    3.6x    3.8x    4.1x    4.5x
───────────────────────────────────────────────────────────────────────────────────
Deleveraging vs Entry     —    -0.4x   -0.3x   -1.0x   -1.5x   -2.1x
Cumulative FCF            —      37      60     107     157     211
  as % of Entry Debt      —     12%     20%     36%     52%     70%
───────────────────────────────────────────────────────────────────────────────────

CREDIT ASSESSMENT
  ✓ Leverage declines from 3.5x to 1.4x — passes 50% test comfortably
  ✓ Interest coverage above 3.0x throughout — comfortable cushion
  ✓ Cumulative FCF of €211m = 70% of entry debt — strong repayment capacity
  ✓ FY26 RCF draw is temporary, fully repaid by FY27
───────────────────────────────────────────────────────────────────────────────────

                             SPONSOR RETURNS (Equity View)
───────────────────────────────────────────────────────────────────────────────────
Exit EBITDA                   €98m        Exit Multiple            6.5x
Exit Enterprise Value        €637m        Exit Net Debt          €137m
Exit Equity Value            €500m
───────────────────────────────────────────────────────────────────────────────────
Sponsor Equity Invested      €250m        MoC                      2.0x
Sponsor Equity Proceeds      €500m        IRR                     14.9%
───────────────────────────────────────────────────────────────────────────────────

RETURNS ATTRIBUTION
  EBITDA Growth Effect                               €130m    (52%)
  Multiple Expansion Effect                            €8m     (3%)
  Deleveraging Effect                                €138m    (55%)
  Fees & Other                                       (€26m)  (-10%)
  ─────────────────────────────────────────────────────────────────
  Total Value Creation                               €250m   (100%)
───────────────────────────────────────────────────────────────────────────────────

SPONSOR ASSESSMENT
  ⚠ IRR of 14.9% is at hurdle rate — acceptable but not compelling
  ✓ MoC of 2.0x represents meaningful value creation
  ✓ Deleveraging drives majority of returns — execution-dependent
  ⚠ Limited multiple expansion assumed — conservative
  ⚠ Upside requires operational improvement or add-on acquisitions
───────────────────────────────────────────────────────────────────────────────────
═══════════════════════════════════════════════════════════════════════════════════
```

One page. Both constituencies served. The lender sees credit metrics and deleveraging. The sponsor sees returns and value attribution. Everyone understands the deal.

---

## Sensitivity Analysis: Where the Conversation Gets Real

The base case looks acceptable. The lender is comfortable. The sponsor is borderline satisfied.

But what if the assumptions are wrong?

Sensitivity analysis is where you stress-test the assumptions — varying the key inputs and watching how outputs change. In an LBO, three variables dominate:

1. **Entry Multiple** — what you pay
2. **Exit Multiple** — what you sell for
3. **EBITDA** — how the business performs

### The IRR Sensitivity Matrix

```
SPONSOR IRR SENSITIVITY — ENTRY vs EXIT MULTIPLE
═══════════════════════════════════════════════════════════════════════════════════
                              Exit Multiple
               │    5.5x     6.0x     6.5x     7.0x     7.5x
───────────────┼─────────────────────────────────────────────
Entry    5.5x  │   17.0%    20.6%    23.8%    26.7%    29.4%
Mult     6.0x  │   12.3%    16.0%    19.3%    22.2%    24.9%
         6.4x  │    9.3%    13.0%    14.9%    19.8%    22.5%  ← Base
         7.0x  │    5.0%     9.0%    12.5%    15.5%    18.3%
         7.5x  │    1.5%     5.7%     9.3%    12.5%    15.3%
═══════════════════════════════════════════════════════════════════════════════════
```

Reading this matrix:

- **Base case (6.4x entry, 6.5x exit): 14.9% IRR** — our starting point
- **Pay too much (7.5x entry, 6.5x exit): 9.3% IRR** — well below hurdle, deal doesn't work
- **Multiple expansion (6.4x entry, 7.5x exit): 22.5% IRR** — great outcome
- **Multiple compression (6.4x entry, 5.5x exit): 9.3% IRR** — painful

The message is clear: entry price matters enormously. Overpay by one turn (6.4x → 7.5x) and your IRR drops by nearly 6 percentage points.

### The EBITDA Sensitivity

```
SPONSOR IRR SENSITIVITY — EXIT MULTIPLE vs EXIT EBITDA
═══════════════════════════════════════════════════════════════════════════════════
                              Exit Multiple
               │    5.5x     6.0x     6.5x     7.0x     7.5x
───────────────┼─────────────────────────────────────────────
Exit     €80m  │   (0.6%)    3.7%     7.5%    10.9%    14.0%
EBITDA   €90m  │    5.9%    10.0%    13.6%    16.8%    19.7%
         €98m  │    9.3%    13.0%    14.9%    19.8%    22.5%  ← Base
        €110m  │   13.8%    17.8%    21.2%    24.3%    27.1%
        €120m  │   17.1%    21.2%    24.7%    27.8%    30.7%
═══════════════════════════════════════════════════════════════════════════════════
```

EBITDA at exit is equally important:

- **Base case (€98m, 6.5x): 14.9% IRR**
- **Underperformance (€80m, 6.5x): 7.5% IRR** — deal struggles
- **Outperformance (€120m, 6.5x): 24.7% IRR** — home run

If EBITDA drops to €80m (an 18% miss vs projection), the deal barely returns capital even at a decent exit multiple.

### The Credit Sensitivity

The lender cares less about IRR and more about coverage:

```
MINIMUM INTEREST COVERAGE — BY EBITDA SCENARIO
═══════════════════════════════════════════════════════════════════════════════════
EBITDA Scenario          Min Coverage    Max Leverage    Assessment
───────────────────────────────────────────────────────────────────────────────────
Upside (€110m FY29)          4.6x            1.2x        Excellent
Base (€98m FY29)             3.4x            1.4x        Comfortable
Stress (€85m FY29)           2.5x            2.0x        Adequate
Downside (€70m FY29)         2.0x            2.8x        Tight
Severe (€55m FY29)           1.5x            4.0x        Distressed
═══════════════════════════════════════════════════════════════════════════════════
```

Even in the severe downside (EBITDA falling to €55m — a 30% decline), coverage stays above 1x. The company can still pay its interest, though there's no cushion for anything else.

This tells the lender: the deal survives a bad recession. It won't be pretty, but it won't default.

### The Go/No-Go Matrix

```
DEAL ASSESSMENT MATRIX
═══════════════════════════════════════════════════════════════════════════════════
                    Lender Comfortable?     Sponsor Satisfied?     Deal Works?
───────────────────────────────────────────────────────────────────────────────────
Entry 5.5x, Base         ✓                       ✓✓                   ✓✓
Entry 6.4x, Base         ✓                       ⚠                    ⚠
Entry 7.0x, Base         ✓                       ✗                    ✗
Entry 7.5x, Base         ✓                       ✗                    ✗
───────────────────────────────────────────────────────────────────────────────────
Entry 6.4x, Upside       ✓✓                      ✓✓                   ✓✓
Entry 6.4x, Downside     ⚠                       ⚠                    ⚠
Entry 6.4x, Severe       ✗                       ✗                    ✗
═══════════════════════════════════════════════════════════════════════════════════
```

The deal is marginal at 6.4x entry — it works, but barely. At 7.0x or above, the sponsor can't earn acceptable returns even if the lender would lend.

This explains why pricing negotiations are so intense. Every 0.1x of entry multiple is meaningful to sponsor returns.

---

## What Makes a Good LBO?

After all this analysis, what actually makes an LBO work? What should you look for when evaluating a deal?

### For the Lender

1. **Entry leverage below 4x** — ideally with room to absorb a downturn
2. **Interest coverage above 3x** — preferably 3.5x+ for cyclical businesses
3. **Meaningful deleveraging** — leverage should fall to ~2x by exit
4. **Cumulative FCF above 50% of debt** — the 50% rule
5. **Downside scenarios don't break coverage** — should stay above 2x in stress

### For the Sponsor

1. **IRR above hurdle (typically 15-20%)** — after fees, in the base case
2. **MoC above 2x** — meaningful cash-on-cash return
3. **Multiple paths to return** — not entirely dependent on multiple expansion
4. **Defensible entry price** — supported by comps and precedents
5. **Operational improvement opportunities** — margin expansion, growth, add-ons

### For the Deal

1. **Both parties can say yes** — lender comfortable AND sponsor satisfied
2. **Reasonable assumptions** — base case is achievable, not aspirational
3. **Downside is survivable** — the company doesn't blow up in a recession
4. **Clear exit path** — identifiable buyers, proven comparable exits

Europa Packaging is marginal. It's not a spectacular deal — the IRR is right at hurdle. But it's workable if the sponsor has conviction in operational improvements or add-on acquisitions that could enhance returns.

That's often how deals get done: the base case is borderline, but the sponsor sees upside the model doesn't capture.

---

## Conclusion: The Model as Decision Framework

We started with a corporate model — a representation of how Europa Packaging operates as a business. We ended with an LBO model — a framework for evaluating whether to buy it, how to finance it, and what returns to expect.

The transformation involved:

1. **Adding transaction structure** — Sources & Uses, the EV-to-Equity bridge
2. **Rebuilding the balance sheet** — PPA, goodwill, the Day One starting point
3. **Accounting for tax complexities** — DTLs from write-ups, NOL limitations
4. **Tracking the debt** — detailed schedules for each instrument
5. **Calculating sponsor returns** — IRR, MoC, value attribution
6. **Integrating both perspectives** — credit metrics AND equity returns

The result is a model that serves two masters. The lender can assess credit risk. The sponsor can evaluate equity returns. Both can stress-test assumptions and understand where the deal works and where it breaks.

Is the model perfect? No. It's built on assumptions that will prove wrong. The future will surprise us in ways we haven't modeled.

But that's not the point. The model isn't a prediction — it's a decision framework. It structures your thinking. It forces you to make your assumptions explicit. It shows you the relationship between inputs and outputs.

In the end, value is created by making positive NPV investments. The LBO model is the analytical arena where an investment thesis is pressure-tested against the only benchmark that matters: its ability to generate returns that exceed the cost of capital.

When the credit committee asks "what if EBITDA falls 20%?", you have an answer. When the investment committee asks "what's the breakeven entry multiple?", you have an answer. When someone challenges an assumption, one can change it and immediately see the implications.

That's the value of the model. Not the specific numbers it produces, but the clarity of thought it enables.

Build the model. Understand the business. Make the decision.

That's leveraged finance.

---

*This completes the core modeling section of the book. The corporate model addresses business projection. The LBO model addresses wrapping a transaction around it. Subsequent chapters apply these tools to increasingly complex situations — distressed credits, covenant negotiations, restructurings. The foundation is now established: the reader can model a business, structure a transaction, and evaluate it from both sides of the capital structure.*
