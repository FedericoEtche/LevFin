# The Modular Approach to Corporate Financial Modeling

A financial model isn't one thing—it's several interconnected things, each with its own logic. The mistake many analysts make is applying the same thinking everywhere. But the framework that works for revenue doesn't work for depreciation. The logic that drives working capital is different from the logic that drives interest expense.

Think of the model as a collection of **modules**, each with a distinct analytical framework. Master each framework separately, then connect them.

---

## The Nine Modules

| Module | Primary Framework | Key Question |
|--------|------------------|--------------|
| **1. Revenue** | Volume × Price | How many units at what price? |
| **2. Cost of Goods Sold** | Volume × Price | What does it cost to produce each unit? |
| **3. Operating Expenses** | Fixed vs. Variable | What scales with activity vs. what doesn't? |
| **4 & 5. Capex, Fixed Assets & D&A** | Asset Category Waterfalls | What assets exist, what are we buying, and how do they decay? |
| **6. Financial Income/Expense** | Balance-Based | What's the average balance and the rate? |
| **7. Tax** | Rule-Based | What are the statutory rules and timing differences? |
| **8. Working Capital** | Days/Turnover | How long does cash stay trapped in operations? |
| **9. Debt Schedule** | Contractual | What do the documents require? |

---

## Module 1: Revenue (Top Line)

**Framework:** Volume × Price, segmented appropriately

Revenue is the anchor of the model. Everything else—costs, capital needs, debt capacity—flows from what the business sells.

**Decomposition Logic:**
```
Revenue = Σ (Volume × Price) across segments
```

**Segmentation options:**
- By geography (UK, Germany, France...)
- By product line (Packaging, Labels, Containers...)
- By customer type (Retail, Industrial, Food & Beverage...)
- By channel (Direct, Distribution, OEM...)

**The right segmentation captures how the business actually operates.** If management thinks in terms of regions, segment by region. If they think in terms of product families, segment that way. The model should mirror the business.

**Typical drivers:**
- Volume: units sold, customers served, stores opened, capacity utilization
- Price: average selling price, price per unit, revenue per customer

**Example: Europa Packaging**
```
                        FY24A    FY25E    FY26E
FOOD & BEVERAGE
  Volume (mn units)      142      149      156
  Price (€/unit)        0.82     0.84     0.86
  Revenue               116      125      134

INDUSTRIAL  
  Volume (mn units)       87       89       91
  Price (€/unit)        0.71     0.72     0.73
  Revenue                62       64       66

TOTAL REVENUE           178      189      200
```

---

## Module 2: Cost of Goods Sold (Gross Margin)

**Framework:** Volume × Price, mirroring revenue segmentation

COGS follows the same logic as revenue—it should be decomposed the same way. If you segment revenue by product line, segment COGS by product line. This lets you calculate **gross margin by segment**, which is where the real insight lives.

**Decomposition options:**
- By input type (raw materials, direct labor, packaging, freight-in)
- By segment (matching revenue segmentation)
- Hybrid (materials by type, labor by segment)

**Typical drivers:**
- Raw materials: volume × cost per unit (or % of revenue if pricing is pass-through)
- Direct labor: headcount × cost per head (or hours × rate)
- Energy: consumption × rate

**Example:**
```
RAW MATERIALS
  Resin (tonnes)          45       47       49
  Cost per tonne (€)   1,200    1,236    1,273
  Total Resin Cost        54       58       62

  Additives (tonnes)      12       13       13
  Cost per tonne (€)     800      824      849
  Total Additives         10       11       11

TOTAL RAW MATERIALS       64       69       73
```

**Key insight:** Understanding whether cost inflation can be passed through to pricing is critical. If resin costs rise 5% but you can only raise prices 3%, margin compresses. The modular structure makes this visible.

---

## Module 3: Operating Expenses

**Framework:** Fixed vs. Variable

Below gross profit, the logic shifts. Instead of volume × price, think **fixed vs. variable**.

- **Variable costs** scale with activity (commissions, distribution, some energy)
- **Fixed costs** don't scale—at least not in the short term (rent, base salaries, insurance)

**Why this matters:** In a downside scenario, fixed costs stay fixed. A business with high operating leverage (lots of fixed costs) sees profit collapse faster when revenue drops. The model should make this distinction explicit.

**Common categories:**
```
VARIABLE (model as % of revenue or volume-linked)
- Sales commissions
- Distribution/logistics  
- Variable portion of utilities
- Outsourced services (if volume-linked)

FIXED (model as absolute amounts, inflating over time)
- Personnel (base salaries, benefits)
- Rent and occupancy
- Insurance
- Professional fees
- IT infrastructure
- Marketing (often semi-fixed)
```

**Typical drivers:**
- Personnel: FTEs × cost per FTE (then inflate annually)
- Rent: contracted amounts (step up per lease terms)
- Variable costs: % of revenue (or % of volume)

**Example:**
```
PERSONNEL COSTS
  Headcount (FTEs)        420      430      440
  Avg Cost/FTE (€k)        52       54       55
  Total Personnel          22       23       24

DISTRIBUTION (Variable)
  % of Revenue           4.5%     4.5%     4.5%
  Distribution Cost         8        9        9

MARKETING (Semi-Fixed)
  Base Spend               3        3        3
  Variable (% Rev)       1.0%     1.0%     1.0%
  Total Marketing           5        5        5
```

---

## Modules 4 & 5: Capital Expenditure, Fixed Assets & Depreciation

**Framework:** Asset Category Waterfalls

Capex, fixed assets, and D&A are deeply intertwined—they're best understood as a single integrated system. The elegant approach is to model them together using **parallel waterfalls** for gross assets and accumulated depreciation, broken down by asset category.

### The Architecture

Each asset category (machinery, buildings, vehicles, IT, etc.) has its own waterfall with three components that move in lockstep:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPEX BY CATEGORY                        │
│  (What are we buying, and what type of asset is it?)        │
└─────────────────────┬───────────────────────────────────────┘
                      │ feeds into
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              GROSS ASSET ROLL-FORWARD                       │
│  Opening + Additions (Capex) - Retirements = Closing        │
└─────────────────────┬───────────────────────────────────────┘
                      │ drives
                      ▼
┌─────────────────────────────────────────────────────────────┐
│         ACCUMULATED DEPRECIATION ROLL-FORWARD               │
│  Opening + Additions (D&A) - Retirements = Closing          │
└─────────────────────┬───────────────────────────────────────┘
                      │ results in
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  NET PP&E = Gross Assets (Closing) - Accum. Depr. (Closing) │
└─────────────────────────────────────────────────────────────┘
```

### Why This Approach?

1. **Retirements work correctly.** When an asset is fully depreciated, it exits both gross assets AND accumulated depreciation simultaneously. The simple "gross PP&E minus accumulated depreciation" approach often ignores this, causing the gross asset base to grow indefinitely.

2. **Different asset lives are handled naturally.** Machinery might depreciate over 10 years, vehicles over 5, IT over 3. Each category has its own depreciation rate.

3. **Capex decisions link to specific assets.** Instead of abstract "capex," you're buying machinery or vehicles or buildings. This forces clearer thinking about what the business actually needs.

4. **The balance sheet ties automatically.** Net PP&E flows directly from the waterfall—no plugs, no reconciling items.

---

### Step 1: Capex by Asset Category

Break down capex not just by maintenance vs. growth, but by **what type of asset** is being acquired:

```
CAPEX BY ASSET CATEGORY
                              FY24A    FY25E    FY26E    FY27E
MACHINERY & EQUIPMENT
  Maintenance                    3.0      3.2      3.4      3.5
  Growth (new production line)    —       8.0       —        —
  Subtotal                       3.0     11.2      3.4      3.5

BUILDINGS & LEASEHOLD
  Maintenance                    0.5      0.5      0.6      0.6
  Growth (warehouse expansion)    —        —       5.0       —
  Subtotal                       0.5      0.5      5.6      0.6

VEHICLES & FLEET
  Replacement cycle              1.0      1.2      1.0      1.2
  Subtotal                       1.0      1.2      1.0      1.2

IT & SOFTWARE
  Ongoing                        0.5      0.6      0.6      0.7
  ERP upgrade                     —       2.0      1.0       —
  Subtotal                       0.5      2.6      1.6      0.7

TOTAL CAPEX                      5.0     15.5     11.6      6.0
  of which: Maintenance          5.0      5.5      5.6      6.0
  of which: Growth                —      10.0      6.0       —
```

**Note:** The maintenance vs. growth distinction remains valuable for credit analysis (what's deferrable in a downside?), but now it's layered on top of the asset category breakdown.

---

### Step 2: Gross Asset Roll-Forward (by Category)

Each asset category follows the same logic:

```
Opening Balance + Additions (Capex) - Retirements = Closing Balance
```

**Retirements** occur when assets reach the end of their useful life. If machinery has a 10-year life, then machinery purchased in FY15 retires in FY25.

```
GROSS ASSETS - MACHINERY & EQUIPMENT
                              FY24A    FY25E    FY26E    FY27E
Opening Balance               100.0    103.0    114.2    117.6
+ Additions (Capex)             3.0     11.2      3.4      3.5
- Retirements                    —        —        —      (8.0)
Closing Balance               103.0    114.2    117.6    113.1

GROSS ASSETS - BUILDINGS & LEASEHOLD
                              FY24A    FY25E    FY26E    FY27E
Opening Balance                60.0     60.5     61.0     66.6
+ Additions (Capex)             0.5      0.5      5.6      0.6
- Retirements                    —        —        —        —
Closing Balance                60.5     61.0     66.6     67.2

GROSS ASSETS - VEHICLES & FLEET
                              FY24A    FY25E    FY26E    FY27E
Opening Balance                 8.0      9.0      9.0      8.8
+ Additions (Capex)             1.0      1.2      1.0      1.2
- Retirements                    —      (1.2)    (1.2)    (1.2)
Closing Balance                 9.0      9.0      8.8      8.8

GROSS ASSETS - IT & SOFTWARE
                              FY24A    FY25E    FY26E    FY27E
Opening Balance                 6.0      6.5      9.1     10.0
+ Additions (Capex)             0.5      2.6      1.6      0.7
- Retirements                    —        —      (0.7)    (0.8)
Closing Balance                 6.5      9.1     10.0      9.9

TOTAL GROSS ASSETS
                              FY24A    FY25E    FY26E    FY27E
Opening Balance               174.0    179.0    193.3    203.0
+ Additions (Capex)             5.0     15.5     11.6      6.0
- Retirements                    —      (1.2)    (1.9)   (10.0)
Closing Balance               179.0    193.3    203.0    199.0
```

---

### Step 3: Accumulated Depreciation Roll-Forward (by Category)

The accumulated depreciation waterfall mirrors the gross asset waterfall:

```
Opening Balance + Additions (D&A Expense) - Retirements = Closing Balance
```

**Critical insight:** When an asset retires, it leaves BOTH schedules. A machine that cost €10m and is now fully depreciated has €10m in gross assets and €10m in accumulated depreciation. Upon retirement, both decrease by €10m—net PP&E is unchanged, but the books are cleaner.

**Depreciation rates by category:**

| Category | Useful Life | Annual Rate |
|----------|-------------|-------------|
| Machinery & Equipment | 10 years | 10% |
| Buildings & Leasehold | 25 years | 4% |
| Vehicles & Fleet | 5 years | 20% |
| IT & Software | 3 years | 33% |

```
ACCUMULATED DEPRECIATION - MACHINERY & EQUIPMENT
                              FY24A    FY25E    FY26E    FY27E
Opening Balance               (45.0)   (55.3)   (66.7)   (78.5)
+ D&A Expense (10% of avg)    (10.3)   (11.4)   (11.8)   (11.5)
- Retirements                    —        —        —       8.0
Closing Balance               (55.3)   (66.7)   (78.5)   (82.0)

ACCUMULATED DEPRECIATION - BUILDINGS & LEASEHOLD
                              FY24A    FY25E    FY26E    FY27E
Opening Balance               (18.0)   (20.4)   (22.8)   (25.4)
+ D&A Expense (4% of avg)      (2.4)    (2.4)    (2.6)    (2.7)
- Retirements                    —        —        —        —
Closing Balance               (20.4)   (22.8)   (25.4)   (28.1)

ACCUMULATED DEPRECIATION - VEHICLES & FLEET
                              FY24A    FY25E    FY26E    FY27E
Opening Balance                (4.0)    (5.7)    (6.5)    (6.3)
+ D&A Expense (20% of avg)     (1.7)    (2.0)    (1.9)    (1.8)
- Retirements                    —       1.2      1.2      1.2
Closing Balance                (5.7)    (6.5)    (7.2)    (6.9)

ACCUMULATED DEPRECIATION - IT & SOFTWARE
                              FY24A    FY25E    FY26E    FY27E
Opening Balance                (3.5)    (5.6)    (8.2)    (9.8)
+ D&A Expense (33% of avg)     (2.1)    (2.6)    (2.3)    (2.5)
- Retirements                    —        —       0.7      0.8
Closing Balance                (5.6)    (8.2)    (9.8)   (11.5)

TOTAL ACCUMULATED DEPRECIATION
                              FY24A    FY25E    FY26E    FY27E
Opening Balance               (70.5)   (87.0)  (104.2)  (120.0)
+ D&A Expense                 (16.5)   (18.4)   (18.6)   (18.5)
- Retirements                    —       1.2      1.9     10.0
Closing Balance               (87.0)  (104.2)  (120.9)  (128.5)
```

---

### Step 4: Net PP&E (Balance Sheet)

The payoff—net PP&E calculates automatically:

```
NET PP&E SUMMARY
                              FY24A    FY25E    FY26E    FY27E
Gross Assets (Closing)        179.0    193.3    203.0    199.0
Accumulated Depr. (Closing)   (87.0)  (104.2)  (120.9)  (128.5)
NET PP&E                       92.0     89.1     82.1     70.5

Check: Change in Net PP&E
  Capex                         5.0     15.5     11.6      6.0
  Less: D&A                   (16.5)   (18.4)   (18.6)   (18.5)
  Net Change                  (11.5)    (2.9)    (7.0)   (12.5)
  Equals Δ Net PP&E?             ✓        ✓        ✓        ✓
```

---

### The Challenge: Existing Assets

This methodology works perfectly for new capex—you know what you're buying, when, and can depreciate it accordingly. But what about **the existing asset base**?

When you inherit a balance sheet with €179m of gross PP&E and €87m of accumulated depreciation, you rarely know the vintage breakdown. What was bought when? What's nearly fully depreciated? What has years of life remaining?

**Practical approaches:**

1. **Ask management.** A good FP&A team will have a fixed asset register showing acquisition dates and remaining useful lives. This is the gold standard.

2. **Use the implied remaining life.** If net PP&E is €92m and D&A is €16.5m, the implied average remaining life is ~5.6 years. You can model existing assets as a single pool that depreciates over this period.

3. **Hybrid approach.** Model existing assets as a declining pool (using implied remaining life), while tracking new capex through the full vintage waterfall. Over time, the legacy pool shrinks and the model becomes increasingly precise.

```
SIMPLIFIED LEGACY ASSET TREATMENT
                              FY24A    FY25E    FY26E    FY27E
EXISTING ASSETS (Legacy Pool)
  Opening Net PP&E             92.0     75.5     60.8     47.9
  D&A (implied 5.6yr life)    (16.5)   (14.7)   (12.9)   (11.2)
  Closing Net PP&E             75.5     60.8     47.9     36.7

NEW ASSETS (Vintage Tracking)
  Capex                         5.0     15.5     11.6      6.0
  Cumulative D&A on New         —      (2.7)    (6.4)    (9.7)
  Net New Assets                5.0     12.8      5.2     (3.7)

TOTAL NET PP&E                 80.5     73.6     53.1     33.0
```

This isn't perfect, but it's pragmatic. The model captures the key dynamics while acknowledging the limitations of available data.

---

### Key Ratios (Now More Meaningful)

With the full waterfall in place, these ratios have cleaner interpretations:

- **Capex / D&A:** Still the key sustainability metric. Below 100% = shrinking asset base. Above 100% = investing for growth (or catching up on deferred maintenance).

- **Capex / Revenue:** Capital intensity, comparable across peers.

- **Average Asset Age:** (Accumulated Depreciation / D&A) gives you a rough sense of how old the asset base is.

- **Remaining Useful Life:** (Net PP&E / D&A) tells you how many years of depreciation remain.

---

### Why This Matters for Credit Analysis

1. **FCF visibility.** The gap between D&A (non-cash) and capex (cash) is clearer when both are modeled rigorously.

2. **Downside scenarios.** You can cut growth capex and see the asset base shrink over time—and watch D&A eventually decline as those deferred investments flow through.

3. **Asset-heavy businesses.** For manufacturers, logistics companies, and infrastructure businesses, this level of detail is essential. The asset base *is* the business.

4. **Exit assumptions.** In an LBO, the exit buyer is acquiring the asset base. Understanding its age, condition, and replacement needs affects terminal value.

---

## Module 6: Financial Income & Expense

**Framework:** Balance-Based (Average Balance × Rate)

Interest expense isn't linked to operations—it's linked to **what you owe and what rate you pay**. This module connects directly to the debt schedule.

**The logic:**
```
Interest Expense = Average Debt Balance × Interest Rate
```

**Considerations:**
- Use average balance (not period-end) for accuracy
- Different tranches have different rates
- Floating rate debt needs a rate assumption (or sensitivity)
- Include commitment fees on undrawn revolvers
- Don't forget amortization of financing fees (non-cash but hits P&L)

**Example:**
```
INTEREST EXPENSE
                           FY25E    FY26E
Term Loan B
  Opening Balance           300      285
  Closing Balance           285      270
  Average Balance           293      278
  Interest Rate (EURIBOR + 450)  7.50%    7.25%
  Interest Expense           22       20

Revolver (Undrawn)
  Commitment (€50m)          50       50
  Utilization                 0        0
  Commitment Fee           0.50%    0.50%
  Fee Expense                 0.25     0.25

TOTAL CASH INTEREST          22       20
Amortization of OID           2        2
TOTAL INTEREST EXPENSE       24       22
```

---

## Module 7: Tax

**Framework:** Rule-Based

Tax is driven by statutory rules, not operational logic. The challenge is capturing the gap between accounting profit and taxable income.

**Key concepts:**
- **Statutory rate:** The headline corporate tax rate
- **Effective rate:** What you actually pay (after adjustments)
- **Cash taxes:** What actually leaves the door
- **Deferred tax:** Timing differences between book and tax

**Simple approach (for most models):**
```
Tax Expense = Pre-Tax Profit × Effective Tax Rate
Cash Taxes = Tax Expense ± Change in Deferred Tax
```

**When to go deeper:**
- NOL carryforwards that shield near-term taxes
- Jurisdictional mix (different rates by country)
- Interest deductibility limits (Section 163(j) in US, similar in EU)
- Transfer pricing considerations

**Example:**
```
TAX CALCULATION
                           FY25E    FY26E
Pre-Tax Profit               42       48
Statutory Rate             25.0%    25.0%
Tax at Statutory Rate        11       12

Adjustments:
  Non-deductible expenses     1        1
  R&D credits                (1)      (1)
  
Tax Expense                  11       12
Effective Rate             25.2%    24.8%

Change in Deferred Tax        2        1
Cash Taxes Paid               9       11
```

---

## Module 8: Working Capital

**Framework:** Days Outstanding / Turnover

Working capital is cash trapped in operations. The framework shifts again—now we think in terms of **how long cash is tied up**, measured in days.

**The core metrics:**
- **Days Sales Outstanding (DSO):** How long to collect receivables
- **Days Inventory Outstanding (DIO):** How long inventory sits
- **Days Payables Outstanding (DPO):** How long you take to pay suppliers
- **Cash Conversion Cycle = DSO + DIO - DPO**

---

### The Simple Approach (Annual Models)

For annual models, the standard formula works well:

```
Receivables = (Revenue / 365) × DSO
Inventory = (COGS / 365) × DIO  
Payables = (COGS / 365) × DPO
```

Hold days constant (or trend them slightly) and let the balances calculate based on the P&L.

**Example:**
```
WORKING CAPITAL (Annual)
                           FY25E    FY26E
Revenue                      189      200
COGS                         115      121

DSO (days)                    45       45
Receivables                   23       25

DIO (days)                    60       60
Inventory                     19       20

DPO (days)                    50       50
Payables                      16       17

Net Working Capital           26       28
Change in NWC                  2        2
  (Cash outflow)
```

This approach is quick, intuitive, and sufficient for most annual projections. But it has a fundamental limitation: it tells you the **ending balance**, not the **cash movement during the period**. For annual models, that's fine—you calculate the change in NWC and move on.

For quarterly models, you need more precision.

---

### The Sophisticated Approach: Balance Roll-Forwards

When modeling on a quarterly (or monthly) basis, the simple days formula breaks down. A 45-day DSO assumption doesn't translate cleanly into quarterly cash flows—does it mean all Q1 sales get collected in Q2? Some in Q1, some in Q2? The formula obscures the actual cash timing.

**The solution:** Treat each working capital account as a balance with its own roll-forward, just like fixed assets:

```
Opening Balance + Additions - Deletions = Closing Balance
```

For **Accounts Receivable:**
- **Additions** = Revenue (you've earned it, customer owes you)
- **Deletions** = Cash collections (customer pays)

For **Inventory:**
- **Additions** = Purchases / Production
- **Deletions** = COGS (goods sold and shipped)

For **Accounts Payable:**
- **Additions** = Purchases (you owe suppliers)
- **Deletions** = Cash payments (you pay suppliers)

This approach is more elegant and flexible. It explicitly shows the cash movement—collections and payments—rather than backing into them from balance changes.

---

### Accounts Receivable: The Roll-Forward Method

Let's walk through receivables in detail. The same logic applies to inventory and payables.

**The structure:**
```
ACCOUNTS RECEIVABLE ROLL-FORWARD
                              Q1       Q2       Q3       Q4
Opening Balance               20       23       25       24
+ Additions (Revenue)         45       48       46       50
- Collections (Cash In)      (42)     (46)     (47)     (49)
Closing Balance               23       25       24       25
```

**The key question:** How do you determine collections?

This is where your DSO assumption translates into actual cash timing. If DSO is 45 days, it means on average customers pay 45 days after the sale. In a quarterly model (90 days per quarter), that means:

- Roughly half of each quarter's sales are collected within that quarter
- The other half spills into the next quarter
- Plus you're collecting the spillover from the prior quarter

**A practical collection model:**

Assume DSO of 45 days. You can model collections as:

```
Collections in Quarter = (Prior Quarter Revenue × Spillover %) + (Current Quarter Revenue × In-Quarter %)
```

Where:
- **Spillover %** ≈ DSO / 90 (portion of prior quarter's sales collected this quarter)
- **In-Quarter %** ≈ 1 - (DSO / 90) (portion of current quarter's sales collected this quarter)

For DSO = 45 days:
- Spillover % = 45/90 = 50%
- In-Quarter % = 50%

```
COLLECTIONS CALCULATION (DSO = 45 days)
                              Q1       Q2       Q3       Q4
Prior Quarter Revenue         42       45       48       46
  × Spillover (50%)           21       23       24       23

Current Quarter Revenue       45       48       46       50
  × In-Quarter (50%)          23       24       23       25

Total Collections             44       47       47       48
```

**Note:** This is a simplification. Real collection patterns aren't perfectly linear—some customers pay in 30 days, others in 60. But this approach captures the essential timing and is far more precise than the annual "days" formula.

---

### Handling Different DSO Assumptions

The collection percentages change with DSO:

| DSO | Spillover % | In-Quarter % | Interpretation |
|-----|-------------|--------------|----------------|
| 30 days | 33% | 67% | Fast collectors—most cash comes in-quarter |
| 45 days | 50% | 50% | Balanced—half now, half next quarter |
| 60 days | 67% | 33% | Slow collectors—most spills to next quarter |
| 90 days | 100% | 0% | Full quarter lag—all collections from prior quarter |

For **monthly models**, the same logic applies but with finer granularity:
- DSO 30 = collect in same month
- DSO 45 = ~50% same month, ~50% next month
- DSO 60 = collect two months later

---

### The Full Working Capital Roll-Forward

Apply the same methodology to all working capital accounts:

```
WORKING CAPITAL ROLL-FORWARDS (Quarterly)
                              Q1       Q2       Q3       Q4      FY
ACCOUNTS RECEIVABLE
  Opening                     20       23       25       24
  + Revenue                   45       48       46       50     189
  - Collections              (42)     (46)     (47)     (49)   (184)
  Closing                     23       25       24       25

INVENTORY
  Opening                     18       19       20       19
  + Purchases                 30       32       30       33     125
  - COGS                     (29)     (31)     (31)     (32)   (123)
  Closing                     19       20       19       20

ACCOUNTS PAYABLE
  Opening                     15       16       17       16
  + Purchases                 30       32       30       33     125
  - Payments                 (29)     (31)     (31)     (32)   (123)
  Closing                     16       17       16       17

NET WORKING CAPITAL
  Receivables                 23       25       24       25
  + Inventory                 19       20       19       20
  - Payables                 (16)     (17)     (16)     (17)
  Net WC                      26       28       27       28

CASH FLOW IMPACT
  Collections                 42       46       47       49     184
  - Payments                 (29)     (31)     (31)     (32)   (123)
  Net WC Cash Flow            13       15       16       17      61
```

**The power of this approach:** You can see exactly when cash moves. Q1 might have strong revenue but weak collections (customers are slow). Q3 might have lower revenue but strong collections (catching up from Q2). The annual total hides this; the quarterly roll-forward reveals it.

---

### Seasonality and Working Capital

The roll-forward approach is essential for seasonal businesses. Consider a retailer with Q4-heavy sales:

```
SEASONAL BUSINESS - RECEIVABLES
                              Q1       Q2       Q3       Q4
Revenue                       30       35       40       95
Collections (DSO 45)          48       33       38       68
Closing Receivables           17       19       21       48
```

The annual model would show average receivables of ~€26m. But the quarterly model reveals the truth: receivables spike to €48m in Q4, consuming significant cash. If the business has a revolver covenant tested quarterly, Q4 could be the pinch point—invisible in the annual view.

---

### Why This Matters

1. **Cash timing precision.** The annual "change in NWC" is a black box. The roll-forward shows exactly when cash comes in and goes out.

2. **Covenant testing.** Many credit agreements test leverage quarterly. Working capital swings can push a company in or out of compliance—the roll-forward shows you where.

3. **Liquidity planning.** When does the business need the revolver? The roll-forward identifies the specific quarters where cash is tight.

4. **Seasonal businesses.** Retailers, agricultural companies, tourism—any business with uneven cash flows needs this precision.

5. **Integration with debt.** The debt module needs to know when cash is available for amortization or sweeps. The roll-forward provides that information.

---

### When to Use Each Approach

| Situation | Approach |
|-----------|----------|
| Annual model, stable business | Simple days formula |
| Annual model, first pass | Simple days formula |
| Quarterly model | Roll-forward method |
| Monthly model | Roll-forward method |
| Seasonal business | Roll-forward method (mandatory) |
| Covenant testing matters | Roll-forward method |
| Liquidity analysis | Roll-forward method |

**The judgment:** If intra-year cash timing matters—for covenants, liquidity, or understanding the business—use the roll-forward. If you just need a reasonable annual NWC change, the simple formula is fine.

---

**Key insight:** Growing companies consume working capital. Each euro of revenue growth requires incremental receivables and inventory. This is real cash that can't service debt. The roll-forward method makes this consumption visible quarter by quarter, not just as an annual afterthought.

---

## Module 9: Debt Schedule

**Framework:** Contractual

The debt schedule is driven by **what the documents say**: mandatory amortization, cash sweeps, maturity dates, prepayment provisions.

**Components:**
- Opening balance
- Mandatory amortization (per credit agreement)
- Cash sweeps (excess cash flow sweep, asset sale proceeds)
- Optional prepayments
- Closing balance

**Example:**
```
DEBT SCHEDULE
                           FY25E    FY26E
TERM LOAN B
  Opening Balance           300      285
  Mandatory Amort (5%)      (15)     (14)
  Cash Sweep                  0        0
  Closing Balance           285      271

REVOLVER
  Opening Drawn               0        0
  Draws / (Repayments)        0        0
  Closing Drawn               0        0
  Available                  50       50

TOTAL DEBT                  285      271
```

**This module links everywhere:**
- To cash flow (amortization = cash outflow)
- To interest expense (average balance × rate)
- To covenant compliance (leverage = debt / EBITDA)

---

## How the Modules Connect

```
┌─────────────────┐
│    REVENUE      │ ─── Volume × Price
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      COGS       │ ─── Volume × Price (mirrors revenue)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    OPEX         │ ─── Fixed vs. Variable
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│      D&A        │ ◄───│     CAPEX       │ ─── Asset Category Waterfalls
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       │ (cash outflow)
┌─────────────────┐     ┌────────┴────────┐
│   INTEREST      │ ◄───│  DEBT SCHEDULE  │ ─── Contractual
└────────┬────────┘     └─────────────────┘
         │                       ▲
         ▼                       │
┌─────────────────┐              │
│      TAX        │ ─── Rule-based
└────────┬────────┘              │
         │                       │
         ▼                       │
┌─────────────────┐              │
│   NET INCOME    │              │
└────────┬────────┘              │
         │                       │
         ▼                       │
┌─────────────────┐              │
│  WORKING CAP    │ ─── Days / Turnover
└────────┬────────┘              │
         │                       │
         ▼                       │
┌─────────────────┐              │
│   FREE CASH     │ ─────────────┘
└─────────────────┘   (feeds back to debt)
```

---

## Summary: One Model, Eight Frameworks

| Module | Framework | Think In Terms Of... |
|--------|-----------|---------------------|
| Revenue | Volume × Price | Units sold, price per unit |
| COGS | Volume × Price | Units produced, cost per unit |
| Opex | Fixed vs. Variable | What scales, what doesn't |
| Capex / Fixed Assets / D&A | Asset Category Waterfalls | Asset types, useful lives, retirements |
| Interest | Balance-Based | Debt balances, rates |
| Tax | Rule-Based | Statutory rules, timing |
| Working Capital | Days/Turnover | Cash conversion cycle |
| Debt | Contractual | What the docs require |

Master each framework. Connect them correctly. That's corporate financial modeling.
