# Corporate Financial Modeling

## Introduction: The Modeling Trap

Let me tell you something that took me years to understand.

When I started in leveraged finance, I thought modeling was the job. Master the three-statement model, learn to build sensitivities, get fast at Excel shortcuts — that was the path. The best bankers, I assumed, were the best modelers. The way to get ahead was to build more sophisticated models than anyone else.

I was wrong.

Here's what I've learned after two decades: the people who succeed in leveraged finance aren't the best modelers. They're the ones who understand what a model is *for*. They see its limitations. They know when to trust it and when to override it. They use the model as a tool for thinking, not a substitute for thinking.

This isn't to say modeling doesn't matter. It does. You need to master the mechanics — three-statement integration, credit ratios, scenario analysis, decision frameworks. If you can't build a model, you can't do the job.

But the trap is thinking that modeling *is* the job. It's not. The job is understanding businesses, structuring transactions, managing risk, and making decisions. The model serves those ends. It doesn't replace them.

I say this at the outset because this chapter is going to teach you how to build models. We'll go deep — deeper than most textbooks, deeper than most training programs. By the end, you'll be able to construct a sophisticated corporate financial model from scratch, one that captures the operational drivers of a business and stress-tests whether a capital structure can survive.

But as you learn these techniques, hold them loosely. Remember that the model is a map, not the territory. Europa Packaging — our case study — exists in the real world, with real factories and real customers and real competitive pressures. The model is a simplified representation of that reality. Useful, but incomplete.

The goal isn't to build impressive models. The goal is to build *useful* models — and to know the difference.

### What This Chapter Covers

This chapter teaches you to build a corporate financial model from an operational and business perspective. We start with the company as it exists: its revenue drivers, cost structure, working capital dynamics, capital expenditure needs. We project these forward, stress-test them under different scenarios, and assess whether the business generates enough cash to service debt.

This is the foundation. It's what you need before you can analyse any leveraged transaction.

In the next chapter, we'll take this foundation and add the complexity of an LBO: a new capital structure, acquisition accounting adjustments, sponsor economics. But you can't run before you walk. The LBO model is built *on top of* the corporate model. If your corporate model is flawed, your LBO model inherits those flaws.

So we start here. We start with the business.

---

## Before You Build: The Philosophy of Model Architecture

Here's a confession that might surprise you: the most impressive financial models contain not a single complex formula.

This runs counter to everything you might expect. Surely sophisticated analysis requires sophisticated machinery — nested IF statements, array formulas, VBA wizardry? Surely the model that handles the €500m leveraged buyout should be more elaborate than the one tracking your personal budget?

No. The opposite is true.

The most powerful models are the simplest ones. Not simple in what they accomplish — they can model intricate capital structures, multi-currency debt tranches, complex covenant calculations — but simple in how they accomplish it. Each formula does one thing. Each cell has one purpose. The logic flows in one direction. Anyone can open the file and understand what's happening.

This isn't aesthetic preference. It's survival strategy.

A model you build today will be used by someone else tomorrow. That someone might be a colleague covering for you while you're on holiday. It might be a credit committee member who wants to stress-test an assumption. It might be you, six months from now, having forgotten why you structured things the way you did.

If that person can't understand the model, the model is worthless. Worse than worthless — it's dangerous. A model that produces numbers nobody can verify is a model that produces numbers nobody should trust.

So before we talk about frameworks and formulas, before we talk about debt schedules and working capital and tax shields, let's talk about how to build something that works. Not just today, but always. Not just for you, but for everyone.

### The Cardinal Sins of Financial Modeling

Over years of reviewing models — building them, auditing them, inheriting them from predecessors who've moved on — certain patterns emerge. Call them sins, crimes, anti-patterns. Whatever the label, they share a common feature: they make models fragile, opaque, and prone to failure.

**Sin #1: Hard-Coded Numbers in Formulas**

This is the original sin. The one from which all other sins flow.

You're building a revenue forecast. Growth is 3%. You write:

```
Revenue (FY25) = Revenue (FY24) * 1.03
```

It works. Revenue grows 3%. You move on.

Six months later, someone asks: "What if growth is 2%?" Now you have to find every cell where you typed "1.03" and change it to "1.02". Miss one, and your model is internally inconsistent. Miss several, and you've got chaos.

The fix is obvious but requires discipline: every assumption lives in a dedicated cell, clearly labeled, in a dedicated section. Your formula becomes:

```
Revenue (FY25) = Revenue (FY24) * (1 + GrowthRate)
```

Where GrowthRate is a cell reference, not a number. Change the assumption once, and it flows through everywhere.

This seems trivial. It is trivial. And yet, I have seen models from major investment banks — models used to commit hundreds of millions of euros — riddled with hard-coded numbers buried in formulas. The analysts who built them were smart, capable people. They just got lazy, once, and then again, and then it became habit.

Don't let it become habit.

**Sin #2: Merged Cells**

Excel lets you merge cells. This is a trap.

Merged cells break sorting. They break filtering. They break copy-paste. They break the fundamental grid structure that makes spreadsheets work.

You merge cells because it looks nice — a header spanning multiple columns, a title centered across a section. But the moment you try to insert a row, or copy a range, or run a macro, the merged cells fight you.

Never merge cells. Use "Center Across Selection" formatting if you need the visual effect. Or just don't — nobody ever failed to understand a model because the headers weren't centered.

**Sin #3: Inconsistent Formulas Across a Row**

In a time-series model, each row represents one concept calculated across multiple periods. Revenue in FY24, FY25, FY26, and so on.

The formula structure should be identical across the row. If FY25's formula is:

```
= FY24 Revenue * (1 + Growth Rate)
```

Then FY26's formula should be:

```
= FY25 Revenue * (1 + Growth Rate)
```

Not:

```
= FY24 Revenue * (1 + Growth Rate) * 1.02
```

Or:

```
= 520
```

When someone audits your model, they'll check that formulas are consistent by selecting a row and looking for variations. If your FY26 is different from FY25, that's a red flag. Maybe it's intentional — there's a one-time adjustment, a step change in assumptions. But now the auditor has to figure out why, and if you didn't document it, they won't know if it's a feature or a bug.

Keep formulas consistent. If something genuinely changes in a specific period, handle it through flags and switches in the assumptions, not through formula variations in the output.

**Sin #4: The Black Box Calculation**

You inherit a model. You open it. You see:

```
=IF(AND(OR($B$4="Base",$B$4="Upside"),YEAR(D$2)>2024,D15>0),
  INDEX($M$10:$P$15,MATCH($A16,$L$10:$L$15,0),MATCH(D$2,$M$9:$P$9,0))*
  (1+VLOOKUP($A16,Assumptions!$B$20:$F$45,4,FALSE))^(YEAR(D$2)-2024),0)
```

What does this calculate? Who knows. You'd need thirty minutes and a whiteboard to deconstruct it.

This is a black box. It might be correct. It might be elegant, even — accomplishing in one cell what lesser modelers would need five for. But it's also unauditable, unmodifiable, and terrifying.

Break complex calculations into steps. Use intermediate rows. Label them clearly. The goal isn't to minimise cell count; it's to maximise transparency.

If your formula is longer than the formula bar can display without scrolling, it's too long. Split it up.

**Sin #5: Circular References Solved by Iteration**

Excel has a setting: "Enable iterative calculation." Turn it on, and Excel will attempt to solve circular references by repeatedly recalculating until values converge.

This is seductive. Your debt model has a circularity — interest depends on debt, debt depends on cash flow, cash flow depends on interest. Enable iteration, and Excel just... handles it.

Except when it doesn't.

Iterative calculation is slow. It's unstable — small changes can cause the model to converge to different values, or fail to converge at all. It's opaque — you can't see the iterations happening, can't verify the logic.

And it disables Goal Seek and Data Tables, two of Excel's most powerful analytical tools.

There are better approaches — using the RCF as a plug that absorbs the circularity, or for the truly ambitious, a User-Defined Function that replicates the circular logic in VBA and solves it algebraically in a single pass. We'll cover these later. The point for now: don't let Excel's iteration engine solve your circularities. Solve them yourself, explicitly, in a way you can audit and trust.

**Sin #6: Meaningless Colors**

Color in a model should be functional, not decorative.

A common convention:
- **Blue font**: Inputs (numbers you type)
- **Black font**: Formulas (calculations)
- **Green font**: Links to other sheets

This isn't the only convention. Some modelers use yellow cell shading for inputs. Some use red for checks. The specific scheme matters less than consistency — pick a system and apply it uniformly.

What doesn't work: using colors because they're pretty. A rainbow spreadsheet where headers are orange, totals are purple, and every section has its own palette is not easier to read. It's harder. The colors convey no information; they're just noise.

Keep it simple. Let the structure, not the formatting, tell the story.

### The Architecture of a Good Model

Avoiding sins is necessary but not sufficient. A model that commits no crimes can still be confusing, poorly organised, hard to use. Let's talk about what good looks like.

**Principle 1: Separate Inputs, Calculations, and Outputs**

A well-structured model has three types of content, and they shouldn't be mixed:

- **Inputs**: Assumptions you can change. Growth rates, margins, interest rates, days outstanding. These live in a dedicated section, clearly labeled, easy to find.

- **Calculations**: The machinery that transforms inputs into results. Revenue builds, cost builds, working capital schedules, debt schedules. These live in the middle of the model, each in its logical place.

- **Outputs**: The answers you care about. Financial statements, credit metrics, scenario comparisons, sensitivity tables. These come at the end, summarising everything that came before.

When someone opens your model, they should be able to find assumptions immediately. They shouldn't have to dig through calculation sheets to discover that growth is 3% — it should be obvious, upfront, in the assumptions section.

**Principle 2: Logical Flow, Top to Bottom, Left to Right**

Time flows left to right. Always. Period. FY24 is to the left of FY25 which is to the left of FY26. No exceptions.

Calculations flow top to bottom. Revenue comes before costs. EBITDA comes before interest. Net income comes before cash flow. The income statement comes before the balance sheet.

This isn't arbitrary. It mirrors how businesses actually work (revenue enables costs enables profit) and how analysis proceeds (understand the past, project the future). Fighting this natural flow creates confusion.

Within a sheet, the structure should be:
1. Timeline and flags (top)
2. Inputs and drivers (below the timeline)
3. Calculations (middle)
4. Outputs and checks (bottom)

Across sheets, the structure should be:
1. Cover / Table of Contents
2. Assumptions (all inputs in one place)
3. Operational schedules (revenue, costs, working capital, capex)
4. Financing schedules (debt, interest, cash flow waterfall)
5. Financial statements (IS, BS, CF — integrated)
6. Outputs (summary, metrics, scenarios, sensitivities)

**Principle 3: Build in Checks**

A model without checks is a model waiting to break.

The most fundamental check: does the balance sheet balance?

```
Check = Total Assets - Total Liabilities - Total Equity
```

This should be zero. Always. In every period. If it's not, something is wrong.

Display this check prominently. Format it to turn red if it's non-zero. Check it constantly as you build.

Other useful checks:
- Does cash flow's ending cash equal balance sheet cash?
- Does retained earnings movement equal net income minus dividends?
- Do debt schedules tie to balance sheet debt?
- Do depreciation schedules tie to income statement D&A?

Build these as you go. Don't wait until the model is "finished" to discover that nothing ties.

**Principle 4: Use Flags for Time-Based Logic**

Models often need different logic for different periods. The construction period behaves differently from the operating period. The first year after acquisition differs from the steady state.

Handle this with flags — TRUE/FALSE values at the top of each column that indicate which period type you're in.

```
Construction Flag:    TRUE    TRUE    FALSE   FALSE   FALSE
Operating Flag:       FALSE   FALSE   TRUE    TRUE    TRUE
Year 1 Flag:          FALSE   FALSE   TRUE    FALSE   FALSE
```

Then use the flags in your formulas:

```
Construction Costs = IF(ConstructionFlag, ConstructionBudget / ConstructionPeriods, 0)
Operating Revenue = IF(OperatingFlag, RevenueBase * (1 + GrowthRate)^YearNumber, 0)
```

This is vastly cleaner than writing different formulas for different periods. The logic is explicit, visible, controllable. Change the timing, and the flags change, and everything flows through.

**Principle 5: Document What's Not Obvious**

Not everything can be made self-evident through structure. Some assumptions have stories behind them. Some calculations have nuances.

Use comments. Use text boxes. Use a dedicated "Notes" column. Whatever method you prefer — just make sure the reasoning is captured.

When you assume receivable days of 43, note where that came from (FDD page 47). When you model a step-up in interest margin, note the trigger (leverage below 3.0x per credit agreement section 2.4). When you exclude something from working capital, note why (deferred tax liabilities are non-operating).

Six months from now, you won't remember. Write it down.

### The Payoff

None of this is glamorous. Color conventions and check cells don't make for exciting conversation. Nobody ever got promoted because their formula structure was consistent across rows.

But models built on these principles work. They survive. They adapt.

When a managing director asks "What if we increase growth by 50bps?" you can answer in ten seconds, because assumptions are centralised. When an auditor reviews the financing structure, they can follow the logic, because calculations are transparent. When a deal pivots — different structure, different timing, different scenarios — the model flexes, because it was built to flex.

This is the payoff: confidence. Confidence that the model does what you think it does. Confidence that changes will flow through correctly. Confidence that the analysis you're presenting is actually the analysis you intended.

That confidence is earned through discipline. Through avoiding the sins. Through embracing the principles.

It starts here, before you write a single formula.

---

## When to Go Quarterly: Choosing Your Model's Heartbeat

Here's a question that doesn't get asked often enough: how frequently should your model tick?

Most models default to annual periods. It's simpler. Fewer columns. Cleaner layout. And for many purposes, annual is fine — you're projecting five years forward, you want to see the trajectory, you don't need to know what happens in March versus September.

But annual models are blunt instruments. They smooth over the bumps, hide the valleys, average away the crises. An annual forecast might show comfortable liquidity while concealing the fact that cash goes negative every Q3 before receivables come in during Q4. An annual model might show covenant compliance while missing that leverage spikes above the threshold in Q2 before EBITDA recovers in the back half.

Annual models show you the destination. Quarterly models show you the journey.

Knowing when to use which is a judgment call. Get it wrong, and you're either drowning in unnecessary complexity or blind to risks that matter.

### When Annual Isn't Enough

There are specific situations where quarterly (or even monthly) granularity isn't a luxury — it's a necessity.

**Seasonality That Matters**

Some businesses earn their money unevenly. A ski resort makes most of its revenue in three months. A toy manufacturer ships half its product in Q4. An agricultural supplier extends credit in spring and collects in autumn.

For these businesses, annual working capital figures are almost meaningless. Year-end might show €40m of net working capital. But in Q3, before the holiday rush, it might peak at €65m. If your RCF is sized based on year-end numbers, you could have a mid-year liquidity crisis that the annual model never warned you about.

The same applies to EBITDA. A retailer with 40% of earnings in Q4 has a very different risk profile than one earning evenly across quarters. In a recession, losing part of your Q4 is catastrophic. The annual model shows "EBITDA down 15%." The quarterly model shows "EBITDA down 40% in the quarter that matters."

**Covenant Testing**

Credit agreements don't test annually. They test quarterly — sometimes monthly for distressed credits. A leverage covenant of 5.5x isn't tested once a year; it's tested at each quarter-end, using LTM EBITDA and period-end debt.

If your model only shows year-end figures, you can't assess covenant headroom properly. You might show comfortable compliance at December but have no idea what happened in March, June, or September. The credit agreement doesn't care about December if you breached in June.

Covenant testing also often uses "springing" triggers — the covenant only applies if a certain condition is met (like RCF drawings exceeding a threshold). Quarterly models let you track when covenants spring and whether you're compliant when they do.

**Near-Term Liquidity Concerns**

When cash is tight, annual granularity is dangerous.

A company with €20m of cash and €50m of FCF looks fine on an annual basis — cash grows to €70m by year-end. But what if the €50m of FCF is earned €5m in Q1, €5m in Q2, €5m in Q3, and €35m in Q4? And what if there's a €30m debt amortisation payment in Q2?

Q1: €20m + €5m = €25m
Q2: €25m + €5m - €30m = €0m ← Problem
Q3: €0m + €5m = €5m
Q4: €5m + €35m = €40m

The company ends the year with €40m of cash. The annual model shows this and declares victory. The quarterly model shows the company hit zero in Q2 and might have missed payroll.

When you're worried about survival — turnarounds, distressed situations, highly levered credits — you need to see the intra-year path, not just the destination.

**Complex Debt Structures**

Some debt structures have timing mismatches that annual models can't capture.

Interest might accrue monthly but pay semi-annually. The RCF might have quarterly commitment fee calculations. Mandatory amortisation might occur in specific months. Cash sweeps might be calculated annually but paid from quarterly excess cash flow.

An annual model smooths all of this into averaged annual figures. A quarterly model shows when cash actually arrives and leaves — which is what matters for liquidity management.

### The Master Timeline Principle

If you decide to build a quarterly model, there's one architectural principle that trumps all others: the Master Timeline.

Every sheet in your model should have the same timeline structure at the top. Same dates. Same periods. Same flags. No exceptions.

This sounds obvious. It isn't.

I've seen models with monthly sheets for the construction period and separate semi-annual sheets for operations. Models where the debt schedule runs January-December but the revenue build runs April-March. Models where each section has its own timeline, formatted differently, with dates in different rows.

These models are nightmares to audit, nightmares to modify, and nightmares to trust.

The Master Timeline eliminates this chaos. At the top of every sheet, you have:

```
Row 1: Period End Date        31-Mar-25   30-Jun-25   30-Sep-25   31-Dec-25
Row 2: Quarter                    Q1          Q2          Q3          Q4
Row 3: Fiscal Year              FY25        FY25        FY25        FY25
Row 4: Operating Flag           TRUE        TRUE        TRUE        TRUE
Row 5: Days in Period             90          91          92          92
```

Every formula on the sheet can reference these rows. Need to know if you're in the operating period? Check the Operating Flag. Need to calculate interest precisely? Use Days in Period. Need to aggregate to annual figures? Use Fiscal Year.

Change the start date, and the timeline updates, and everything flows through. Add a new quarter, and the structure accommodates it. The timeline is the spine of the model; everything else hangs off it.

### Aggregating Quarterly to Annual

One challenge with quarterly models: you still need annual summaries. Credit committees want to see annual metrics. Covenants often test LTM figures. Comparisons with prior years require annual totals.

The clean approach uses SUMIF to aggregate quarterly data into annual buckets:

```
Annual Revenue (FY25) = SUMIF(FiscalYearRow, "FY25", QuarterlyRevenueRow)
```

This formula sums all quarterly revenue figures where the Fiscal Year row equals "FY25." Add a quarter, and it's automatically included. Change the fiscal year-end, and the aggregation adjusts.

For LTM (Last Twelve Months) calculations, you sum the trailing four quarters:

```
LTM EBITDA (Q2 FY25) = Q3 FY24 + Q4 FY24 + Q1 FY25 + Q2 FY25
```

Build a dedicated LTM row that always references the current quarter and three prior quarters. This becomes your input for leverage and coverage ratios.

### The Hybrid Approach

Not every model needs to be quarterly throughout.

A common — and sensible — approach is quarterly for the near term, annual for the outer years. Years 1 and 2 are modeled quarterly, capturing the seasonal patterns, covenant tests, and liquidity dynamics that matter most. Years 3-5 are annual, recognising that precision beyond two years is largely illusory anyway.

This hybrid gives you granularity where it matters and simplicity where it doesn't.

The transition requires care. Your Year 2 Q4 needs to flow cleanly into your Year 3 annual period. Opening balances must tie. The LTM calculation for Year 3 needs to reach back into Year 2's quarterly figures.

Structure it right, and the hybrid approach gives you the best of both worlds. Structure it wrong, and you have two models awkwardly stitched together, with gaps at the seams.

### When Annual Is Fine

Despite everything I've said, annual models are often appropriate.

If the business has minimal seasonality — revenue and costs spread evenly across quarters — annual captures the economics accurately. If liquidity is comfortable — ample cash, undrawn RCF, no near-term maturities — you don't need to track the intra-year path. If covenants are distant — leverage at 3x against a 5.5x covenant — quarterly testing is academic.

For early-stage screening, annual is fine. You're trying to figure out if the deal makes sense at all, not whether Q2 looks different from Q3.

For outer years of a projection, annual is fine. Nobody knows what Q3 of Year 5 looks like. Pretending otherwise is false precision.

The judgment is this: does the intra-year path matter? If yes, go quarterly. If no, stay annual. If uncertain, ask yourself what would happen in a downside scenario — would the quarterly dynamics suddenly matter? If the answer is yes, build the quarterly model now, not when you're already in trouble.

### A Final Warning

Quarterly models are more work. More columns, more formulas, more chances for error. A model with 20 annual columns becomes a model with 80 quarterly columns. The complexity compounds.

This complexity is only justified if you actually use the granularity. A quarterly model that nobody stress-tests by quarter, that nobody uses for covenant monitoring, that gets summarised to annual figures before anyone looks at it — that's complexity for its own sake. Wasted effort.

Build quarterly when you need quarterly. Use it when you build it. Otherwise, stick with annual and save yourself the headache.

---

## Building the Model: The DRIVERS Framework

There are countless resources that can teach you to build a three-statement financial model from scratch. My goal here isn't to replicate those — it's to show you a straightforward approach that captures exactly what we need from a leveraged finance model.

The model we'll build is intentionally basic. It can be expanded, refined, made more sophisticated. But even in its simplest form, it does the job: it characterises the business through drivers, links the statements correctly, and lets you stress-test the capital structure.

To make the process memorable, I use an acronym: **DRIVERS**.

| Step | Action | What You're Doing |
|------|--------|-------------------|
| **D** | **Data** | Arrange historical data into your model's layout |
| **R** | **Relate** | Link the three statements together |
| **I** | **Identify** | Produce KPIs and drivers from historical information |
| **V** | **Venture** | Project forward — drivers become inputs, accounts become formulas |
| **E** | **Explore** | Create scenarios (base, best, worst) |
| **R** | **Roll** | Extend formulas across the forecast period |
| **S** | **Scrutinise** | Analyse results, iterate, visualise |

Let's walk through each step using Europa Packaging.

---

## D — Data: Arrange Historical Information Into Your Model's Layout

Before you can model anything, you need to organise what you know. This sounds obvious. It is obvious. And yet, a remarkable number of models fail at exactly this step — not because the data is wrong, but because it's arranged in a way that makes everything that follows harder than it needs to be.

### The Layout Problem

Here's the thing about financial models: they're not just spreadsheets. They're arguments. They have a logic, a flow, a narrative. And like any good argument, they need structure.

You can dump three years of audited financials into Excel in about ten minutes. Copy, paste, done. You now have data. What you don't have is a model. You have a mess that happens to contain numbers.

The goal of this first step is to transform raw data into organised data — arranged in a layout that will make the next six steps possible.

### The Golden Rules of Layout

**Rule 1: Time flows left to right.**

This is not negotiable. Historical periods on the left, forecast periods on the right, each column representing one period (usually a year, sometimes quarters). Your eye should be able to scan from left to right and see the story unfold: what happened, what's projected to happen.

It sounds trivial. It's not. I've seen models where time flows right to left, models where historical and forecast periods are interleaved, models where 2023 is in column D and 2022 is in column M. These models are not wrong, exactly. They're just unusable.

**Rule 2: Inputs separated from calculations.**

Your model will have two types of cells: inputs (numbers you type in) and calculations (formulas that derive from inputs and other calculations). These should be visually distinct and, ideally, physically separated.

Common conventions:
- Blue font for inputs, black font for formulas
- A dedicated "Assumptions" or "Inputs" section at the top or on a separate sheet
- Yellow cell shading for inputs (though this can get garish)

Pick a convention and stick to it. The goal is that anyone opening your model can immediately see what's an assumption and what's arithmetic.

**Rule 3: One row, one concept. No merging. No exceptions.**

Each row should represent one thing. Revenue. Cost of goods sold. Depreciation. Cash. Each column should represent one period. The intersection of a row and a column is a single value: Revenue in 2023. COGS in 2024. Cash at year-end 2025.

Do not merge cells. Do not have a single row that means "Revenue" in some columns and "Revenue growth" in others. Do not get creative. Creativity in model layout is not a virtue. It's a warning sign.

**Rule 4: Structure mirrors logic.**

Your layout should reflect how the business actually works. For Europa Packaging, that means:

- Revenue broken out by segment (Food & Beverage, Personal Care, Industrial)
- Within each segment, volume and price visible as drivers
- Costs broken out by type (materials, labour, other) with their own drivers
- Working capital by component (inventory, receivables, payables)
- Capex split between maintenance and growth

If your layout doesn't match your driver tree, something is wrong. Either your driver tree is incomplete, or your layout is too aggregated. Fix one or the other.

### What Data You Actually Need

For a leveraged finance model, you typically need three to five years of historical data. More is nice but rarely necessary. Less is a problem — you can't identify trends or calculate meaningful averages from two years of history.

Where does this data come from?

**Audited financial statements** provide the official numbers: revenue, EBITDA (sort of), net income, balance sheet items, cash flow statement. These are your anchor. If your model's historical output doesn't tie to the audited accounts, you have a problem.

**The Financial Due Diligence** provides everything else: the segment breakdowns, the volume and price data, the EBITDA adjustments, the working capital analysis, the capex split. This is where the driver-level detail lives.

**Management presentations** fill in gaps and provide forward-looking context: growth plans, margin targets, capex projects, strategic initiatives.

You're assembling a picture from multiple sources. The audited accounts tell you the totals. The FDD tells you the components. The management presentation tells you the story.

### Europa Packaging: Setting Up the Layout

Let's get concrete. Here's how the layout comes together for our case study.

**Sheet 1: Assumptions / Drivers**

This is where all inputs live. Nothing calculated here — just numbers you can change.

```
REVENUE DRIVERS
                                    FY21    FY22    FY23    FY24
Food & Beverage
  Volume (m units)                 1,210   1,255   1,290   [input]
  Volume growth (%)                        3.7%    2.8%    [input]
  ASP (€ per '000 units)            221     224     225    [input]
  ASP growth (%)                           1.4%    0.4%    [input]

Personal Care
  Volume (m units)                   435     460     480   [input]
  Volume growth (%)                        5.7%    4.3%    [input]
  ASP (€ per '000 units)            288     296     292    [input]
  ASP growth (%)                           2.8%   -1.4%    [input]

[...and so on for Industrial]

COST DRIVERS
Raw Materials
  Resin yield (kg per '000 units)    43      43      43    [input]
  Resin price (€ per tonne)        1,050   1,220   1,180   [input]

Labour
  Headcount - Production           1,250   1,270   1,280   [input]
  Headcount - Other                  510     515     520   [input]
  Avg cost per head (€k)              46      47      48    [input]

[...and so on]

WORKING CAPITAL DRIVERS
  Inventory days                      41      42      42    [input]
  Receivable days                     44      43      43    [input]
  Payable days                        48      49      49    [input]

CAPEX
  Maintenance capex (€m)              13      14      14    [input]
  Growth capex (€m)                   15       6       4    [input]
```

Notice what's happening here. For historical periods (FY21-FY24), the "inputs" are actually calculated from the underlying data — we're deriving the KPIs. But the *structure* is set up so that in the forecast period, these same cells become true inputs: assumptions you type in.

The layout is doing work. It's preparing for what comes next.

**Sheet 2: Income Statement**

```
INCOME STATEMENT
                                    FY21    FY22    FY23    FY24   FY25E  FY26E
Revenue
  Food & Beverage                    267     281     290    [f]    [f]    [f]
  Personal Care                      125     136     140    [f]    [f]    [f]
  Industrial                          54      51      50    [f]    [f]    [f]
Total Revenue                        446     468     480    [f]    [f]    [f]

Cost of Goods Sold
  Raw materials                      (84)    (99)   (100)   [f]    [f]    [f]
  Direct labour                      (48)    (51)    (54)   [f]    [f]    [f]
  Other COGS                         (42)    (44)    (46)   [f]    [f]    [f]
Total COGS                          (174)   (194)   (200)   [f]    [f]    [f]

Gross Profit                         272     274     280    [f]    [f]    [f]
Gross Margin (%)                    61.0%   58.5%   58.3%   [f]    [f]    [f]

Operating Expenses
  Labour - non-production            (22)    (23)    (24)   [f]    [f]    [f]
  Other opex                         (52)    (56)    (58)   [f]    [f]    [f]
Total Opex                           (74)    (79)    (82)   [f]    [f]    [f]

EBITDA                               198     195     198    [f]    [f]    [f]
EBITDA Margin (%)                   44.4%   41.7%   41.3%   [f]    [f]    [f]

Depreciation & Amortisation          (14)    (15)    (16)   [f]    [f]    [f]

EBIT                                 184     180     182    [f]    [f]    [f]

Interest expense                     [f]     [f]     [f]    [f]    [f]    [f]

EBT                                  [f]     [f]     [f]    [f]    [f]    [f]

Tax                                  [f]     [f]     [f]    [f]    [f]    [f]

Net Income                           [f]     [f]     [f]    [f]    [f]    [f]
```

Where you see `[f]`, that's a formula. Where you see a number, that's either pulled directly from source data (for historicals) or calculated from drivers (once we get to the forecast).

The layout mirrors the driver tree. Revenue is broken by segment. COGS is broken by component. Opex is separated. You can trace any number back to its source.

**Sheet 3: Balance Sheet**

```
BALANCE SHEET
                                    FY21    FY22    FY23    FY24   FY25E  FY26E
ASSETS
Current Assets
  Cash                               [f]     [f]     [f]    [f]    [f]    [f]
  Receivables                        [f]     [f]     [f]    [f]    [f]    [f]
  Inventory                          [f]     [f]     [f]    [f]    [f]    [f]
Total Current Assets                 [f]     [f]     [f]    [f]    [f]    [f]

Non-Current Assets
  PP&E (net)                         [f]     [f]     [f]    [f]    [f]    [f]
  Intangibles                        [f]     [f]     [f]    [f]    [f]    [f]
  Other                              [f]     [f]     [f]    [f]    [f]    [f]
Total Non-Current Assets             [f]     [f]     [f]    [f]    [f]    [f]

TOTAL ASSETS                         [f]     [f]     [f]    [f]    [f]    [f]

LIABILITIES
Current Liabilities
  Payables                           [f]     [f]     [f]    [f]    [f]    [f]
  Short-term debt                    [f]     [f]     [f]    [f]    [f]    [f]
  Other                              [f]     [f]     [f]    [f]    [f]    [f]
Total Current Liabilities            [f]     [f]     [f]    [f]    [f]    [f]

Non-Current Liabilities
  Long-term debt                     [f]     [f]     [f]    [f]    [f]    [f]
  Other                              [f]     [f]     [f]    [f]    [f]    [f]
Total Non-Current Liabilities        [f]     [f]     [f]    [f]    [f]    [f]

TOTAL LIABILITIES                    [f]     [f]     [f]    [f]    [f]    [f]

EQUITY
  Share capital                      [f]     [f]     [f]    [f]    [f]    [f]
  Retained earnings                  [f]     [f]     [f]    [f]    [f]    [f]
TOTAL EQUITY                         [f]     [f]     [f]    [f]    [f]    [f]

TOTAL LIABILITIES + EQUITY           [f]     [f]     [f]    [f]    [f]    [f]

Check (Assets - Liab - Equity)        0       0       0      0      0      0
```

That last row matters. A balance sheet that doesn't balance is broken. Having a visible check at all times catches errors immediately.

**Sheet 4: Cash Flow Statement**

```
CASH FLOW STATEMENT
                                    FY21    FY22    FY23    FY24   FY25E  FY26E
OPERATING ACTIVITIES
Net Income                           [f]     [f]     [f]    [f]    [f]    [f]
Depreciation & Amortisation          [f]     [f]     [f]    [f]    [f]    [f]
Changes in Working Capital
  (Increase)/decrease in receivables [f]     [f]     [f]    [f]    [f]    [f]
  (Increase)/decrease in inventory   [f]     [f]     [f]    [f]    [f]    [f]
  Increase/(decrease) in payables    [f]     [f]     [f]    [f]    [f]    [f]
Cash from Operations                 [f]     [f]     [f]    [f]    [f]    [f]

INVESTING ACTIVITIES
Capital expenditure                  [f]     [f]     [f]    [f]    [f]    [f]
Other                                [f]     [f]     [f]    [f]    [f]    [f]
Cash from Investing                  [f]     [f]     [f]    [f]    [f]    [f]

FINANCING ACTIVITIES
Debt drawdown/(repayment)            [f]     [f]     [f]    [f]    [f]    [f]
Interest paid                        [f]     [f]     [f]    [f]    [f]    [f]
Dividends                            [f]     [f]     [f]    [f]    [f]    [f]
Cash from Financing                  [f]     [f]     [f]    [f]    [f]    [f]

NET CHANGE IN CASH                   [f]     [f]     [f]    [f]    [f]    [f]

Opening Cash                         [f]     [f]     [f]    [f]    [f]    [f]
Closing Cash                         [f]     [f]     [f]    [f]    [f]    [f]

Check (Closing Cash = BS Cash)        0       0       0      0      0      0
```

Another check row. The cash flow statement's ending cash must equal the balance sheet's cash. If they diverge, you've got a leak somewhere.

### The Point of All This

You haven't done anything clever yet. You haven't built a single formula that matters. You've just arranged data into rows and columns.

But here's what you've actually accomplished:

1. **You know what you have.** The act of arranging data forces you to confront what's there and what's missing. Gaps become visible.

2. **You've created the scaffolding.** Every formula you write from now on has a place to live. The structure is ready.

3. **You've made the model readable.** Someone else (or future you) can open this and understand immediately what's happening. Time flows left to right. Each row is one thing. Inputs are blue. Calculations are black.

4. **You've prepared for the driver-based approach.** Your layout matches your driver tree. When you start projecting, the path is clear: drivers flow into statements.

This is not the exciting part of modelling. But it's the part that determines whether everything else works. A model with brilliant analysis built on a chaotic layout is still a chaotic model. A model with a clean layout and basic analysis is still usable.

Do this step well, and the next six get easier.

---

## R — Relate: Link the Three Statements Together

Here's a dirty secret about corporate finance: the three financial statements are not three things. They're one thing, viewed from three angles.

The income statement tells you what happened over a period. The balance sheet tells you where you stand at a moment. The cash flow statement reconciles the two — explaining how the "what happened" turned into the "where you stand."

They're connected. Intimately, mechanically, inescapably connected. Change one number in one statement, and something else must change somewhere else to keep everything in balance.

This is either obvious or profound, depending on how much accounting you've internalised. For our purposes, it's practical: if you get the linkages right, your model works. If you get them wrong, your model produces nonsense — balance sheets that don't balance, cash that appears from nowhere, profits that vanish into the void.

So let's get them right.

### The Core Linkages

There are maybe a dozen connections that matter. Learn these, and you can build any three-statement model.

**Linkage 1: Net Income → Retained Earnings**

This is the most fundamental link. The income statement's bottom line — net income — flows into the balance sheet through retained earnings.

```
Retained Earnings (end) = Retained Earnings (begin) + Net Income - Dividends
```

Every euro of profit the company earns increases equity. Every euro of dividends paid decreases it. That's it. That's the link between "how much did we make?" and "how much are we worth?"

If your model's net income doesn't flow to retained earnings, your balance sheet won't balance. Full stop.

**Linkage 2: Depreciation & Amortisation — The Great Reconciler**

D&A is beautiful. Not aesthetically — it's an accounting entry, not a sunset. But structurally, it's the thing that makes the statements fit together.

On the income statement, D&A is an expense. It reduces profit.

On the balance sheet, D&A reduces the value of fixed assets (PP&E) and intangibles. It's the accumulated wear and tear, the recognition that assets don't last forever.

On the cash flow statement, D&A gets added back to net income. Why? Because it reduced profit but didn't cost any cash. The cash went out the door when you bought the asset, not when you depreciate it.

The linkages:

```
Income Statement:  EBITDA - D&A = EBIT
Balance Sheet:     PP&E (end) = PP&E (begin) + Capex - Depreciation
Cash Flow:         Net Income + D&A = (starting point for operating cash flow)
```

Same number, three different roles. If your D&A isn't consistent across all three statements, something's broken.

**Linkage 3: Capital Expenditure — Cash Leaves, Assets Arrive**

When the company spends cash on a new machine, two things happen:

1. Cash goes down (cash flow statement, investing section)
2. PP&E goes up (balance sheet)

```
Cash Flow:    Capex is a cash outflow (negative)
Balance Sheet: PP&E (end) = PP&E (begin) + Capex - Depreciation
```

Capex and depreciation are the yin and yang of fixed assets. Capex adds to the pile; depreciation wears it down. The balance sheet captures the net.

**Linkage 4: Working Capital — The Bridge Between Accrual and Cash**

This is where people get confused. And the confusion is understandable, because working capital linkages require you to think about the difference between *earning* money and *collecting* money.

The income statement is accrual-based. Revenue is recognised when earned, not when collected. Costs are recognised when incurred, not when paid.

But cash flow is... cash. Actual money moving.

Working capital is the bridge.

**Receivables:**
```
Income Statement:  Revenue (what you earned)
Balance Sheet:     Receivables = Revenue you earned but haven't collected yet
Cash Flow:         Increase in receivables = Cash you didn't collect = Negative adjustment
```

If receivables go *up*, it means you earned revenue but didn't get the cash. That's a use of cash — you're funding your customers. In the cash flow statement, an increase in receivables is *subtracted* from net income.

If receivables go *down*, you collected more than you earned — cash came in from old sales. That's a source of cash.

**Inventory:**
```
Income Statement:  COGS (what you sold, at cost)
Balance Sheet:     Inventory = Stuff you bought but haven't sold yet
Cash Flow:         Increase in inventory = Cash spent on stuff still sitting there = Negative adjustment
```

If inventory goes *up*, you spent cash buying stuff that's still on the shelf. That's a use of cash.

If inventory goes *down*, you sold stuff without replacing it — you monetised the stockpile. Source of cash.

**Payables:**
```
Income Statement:  Costs (what you incurred)
Balance Sheet:     Payables = Costs you incurred but haven't paid yet
Cash Flow:         Increase in payables = Costs you haven't paid = Positive adjustment
```

This one works the opposite way. If payables go *up*, you incurred costs but didn't pay cash. Your suppliers are funding you. That's a source of cash.

If payables go *down*, you paid more than you incurred — settling old bills. Use of cash.

**The working capital summary:**

| Item | Increases | Cash Flow Impact |
|------|-----------|------------------|
| Receivables | ↑ | Negative (use of cash) |
| Inventory | ↑ | Negative (use of cash) |
| Payables | ↑ | Positive (source of cash) |

The signs trip people up constantly. Here's a mnemonic: *Assets increasing = cash trapped. Liabilities increasing = cash freed.*

Receivables and inventory are assets. When they grow, cash gets trapped in them. Payables are liabilities. When they grow, you're keeping cash that would otherwise have gone out the door.

**Linkage 5: Debt — Principal, Interest, and the Two Statements That Care**

Debt lives on the balance sheet. Interest expense lives on the income statement. Cash payments for both live on the cash flow statement.

```
Balance Sheet:     Debt (end) = Debt (begin) + Drawdowns - Repayments
Income Statement:  Interest Expense = Debt × Interest Rate
Cash Flow:         Interest Paid (operating section) + Principal Repaid (financing section)
```

A subtlety: interest expense and interest paid aren't always the same. If interest accrues but isn't paid in cash (PIK interest, for instance), expense hits the income statement but cash doesn't leave. For most models, though, you can assume interest expense equals interest paid.

The debt repayment schedule matters for leveraged finance models. Mandatory amortisation (if any), cash sweeps, bullet maturities — these drive the "Debt Repaid" line in cash flow and the "Debt" line on the balance sheet.

**Linkage 6: Cash — The Ultimate Check**

Cash is where everything lands. The cash flow statement explains how cash moved from beginning to end. The balance sheet shows beginning and ending cash. They must match.

```
Cash Flow:         Opening Cash + Net Change in Cash = Closing Cash
Balance Sheet:     Cash (this period) = Closing Cash from Cash Flow
```

This is your integrity check. If the balance sheet cash doesn't equal the cash flow's closing cash, you have an error somewhere. Find it.

### The Circular Reference Problem

Here's where it gets interesting.

In a leveraged finance model, you need to calculate interest expense. Interest expense depends on debt. Fine. But what's the cash balance? The cash balance depends on cash flow. Cash flow depends on interest expense. Interest expense depends on... wait.

If the company has excess cash, it might pay down debt. If it pays down debt, interest expense goes down. If interest expense goes down, cash flow goes up. If cash flow goes up, there's more cash to pay down debt.

You see the problem. It's circular.

```
Debt → Interest Expense → Net Income → Cash Flow → Debt Repayment → Debt
```

Spreadsheets don't love circular references. They can handle them — Excel has an "enable iterative calculation" setting — but they can also spiral into chaos or silently give you wrong answers.

There are two ways to handle this:

**Option 1: Accept the circularity.**

Turn on iterative calculations. Let Excel solve it. This works, but:
- You lose some control
- Debugging becomes harder
- Some cells might not converge properly
- It makes people nervous

**Option 2: Break the circle with a cash sweep plug.**

This is the cleaner approach. Instead of letting everything calculate simultaneously, you introduce a "plug" — typically a revolver or a cash balance — that absorbs the residual.

Here's how it works:

1. Calculate everything *except* the revolver/excess cash
2. Determine the cash surplus or deficit before discretionary items
3. If deficit: draw on the revolver
4. If surplus: either build cash or pay down revolver

```
Cash before revolver = Opening Cash + Operating CF + Investing CF + Non-Revolver Financing CF

If Cash before revolver < Minimum Cash:
    Revolver Draw = Minimum Cash - Cash before revolver
    Closing Cash = Minimum Cash
    
If Cash before revolver > Minimum Cash:
    Revolver Repayment = MIN(Revolver Balance, Cash before revolver - Minimum Cash)
    Closing Cash = Cash before revolver - Revolver Repayment
```

The revolver acts as a buffer. It flexes to keep cash at the target level. This breaks the circularity because you calculate everything else first, *then* solve for the revolver.

For Europa Packaging, we'll use this approach. The RCF is the plug. The model calculates operating performance, determines cash needs, and the revolver draws or repays to balance.

### The Linkage Map

Let's visualise how everything connects:

```
                    INCOME STATEMENT
                    ────────────────
                    Revenue
                    - COGS
                    - Opex
                    - D&A ─────────────────────────────┐
                    ────────                           │
                    EBIT                               │
                    - Interest ←───────────────────────┼───────┐
                    ────────                           │       │
                    EBT                                │       │
                    - Tax                              │       │
                    ────────                           │       │
                    Net Income ───────────┐            │       │
                                          │            │       │
                                          ▼            │       │
                    BALANCE SHEET         │            │       │
                    ─────────────         │            │       │
                    Assets:               │            │       │
                      Cash ←──────────────┼────────────┼───────┼───── (from CF)
                      Receivables ←───────┼────────────┼───────┼───── (from Revenue × Days)
                      Inventory ←─────────┼────────────┼───────┼───── (from COGS × Days)
                      PP&E ←──────────────┼────────────┼───────┘      (Capex - D&A)
                    Liabilities:          │            │
                      Payables ←──────────┼────────────┼────────────── (from Costs × Days)
                      Debt ←──────────────┼────────────┼───────┬───── (Draws - Repayments)
                    Equity:               │            │       │
                      Retained Earnings ←─┘            │       │
                                                       │       │
                                          ┌────────────┘       │
                    CASH FLOW STATEMENT   │                    │
                    ───────────────────   │                    │
                    Operating:            │                    │
                      Net Income ←────────┘                    │
                      + D&A                                    │
                      - ∆ Working Capital ←── (from BS changes)│
                    Investing:                                 │
                      - Capex ──────────────────────────────── │ ──→ (to BS: PP&E)
                    Financing:                                 │
                      + Debt Draws                             │
                      - Debt Repayments ───────────────────────┘
                      - Interest Paid
                      - Dividends
                    ────────
                    = Net Change in Cash ──────────────────────────→ (to BS: Cash)
```

Every arrow is a formula in your model. Miss one, and something won't tie.

### Building the Links in Europa Packaging

Let's make this concrete. For Europa's historical periods, most linkages are just organising source data. For the forecast, the linkages become formulas.

**Net Income to Retained Earnings:**
```
Retained Earnings (FY25E) = Retained Earnings (FY24) + Net Income (FY25E) - Dividends (FY25E)
```

**D&A across statements:**
```
Income Statement:  D&A (FY25E) = [input, or % of PP&E]
Balance Sheet:     PP&E (FY25E) = PP&E (FY24) + Capex (FY25E) - Depreciation (FY25E)
Cash Flow:         Add back D&A to Net Income
```

**Working Capital:**
```
Receivables (FY25E) = Revenue (FY25E) × (Receivable Days / 365)
Inventory (FY25E) = COGS (FY25E) × (Inventory Days / 365)
Payables (FY25E) = (COGS + Opex) (FY25E) × (Payable Days / 365)

∆ Receivables = Receivables (FY25E) - Receivables (FY24)   → subtract in CF
∆ Inventory = Inventory (FY25E) - Inventory (FY24)         → subtract in CF
∆ Payables = Payables (FY25E) - Payables (FY24)            → add in CF
```

**Debt and Interest:**
```
Interest Expense (FY25E) = Average Debt (FY25E) × Interest Rate
Where: Average Debt = (Opening Debt + Closing Debt) / 2
Closing Debt (FY25E) = Opening Debt (FY25E) + Draws - Repayments
```

**Cash:**
```
Closing Cash (FY25E) = Opening Cash (FY25E) + Net Change in Cash (FY25E)
Opening Cash (FY25E) = Closing Cash (FY24)
```

### The Beauty of Proper Linkages

When the linkages are right, something almost magical happens: the model starts to *behave*.

Change revenue growth, and receivables adjust automatically. Cash flow reflects the working capital impact. The balance sheet stays balanced.

Change capex, and PP&E responds. Depreciation (if linked to assets) adjusts over time. Cash flow captures the outflow.

Change the interest rate, and interest expense moves. Net income moves. Retained earnings move. The balance sheet absorbs it. Cash flow reflects it.

You don't have to manually update ten different cells when you change one assumption. The linkages propagate the change through the entire model.

This is the point. A well-linked model is a *system*. It responds to inputs the way an actual business would respond to actual changes. That's what makes it useful for analysis, for scenarios, for stress testing.

A model without proper linkages is just a collection of numbers that happen to be near each other. Change one thing and nothing else responds. It's not wrong, exactly. It's just not a model.

### Common Mistakes

**Mistake 1: Hard-coding historical data into formulas.**

In the historical period, it's tempting to just type the numbers. Revenue was €480m, so you type 480. This works — until you realise your historical cash flow statement doesn't tie to your historical balance sheet, and you can't figure out why because nothing is linked.

Even for historicals, build the linkages. Pull revenue from source data, but let the working capital formulas calculate receivables from revenue × days. If it doesn't match the historical balance sheet, you've learned something: either your days assumption is wrong, or there's something in receivables you don't understand.

**Mistake 2: Linking to the wrong period.**

Opening cash should equal *last period's* closing cash. Not this period's. It sounds obvious, but in the fog of formula-writing, people link to the wrong cell constantly. The model appears to work until you change something and cash goes haywire.

Be disciplined about period references. Opening = prior period ending. Ending = this period's calculation. Always.

**Mistake 3: Forgetting the signs.**

In the cash flow statement, capex is typically shown as a negative (cash outflow). But when you link it to the balance sheet, you're adding to PP&E, so the sign flips.

Establish a convention and stick to it:
- Cash outflows are negative in the cash flow statement
- Balance sheet additions are positive
- Use absolute values and manual signs if needed

**Mistake 4: Circular reference panic.**

Some people see a circular reference warning and immediately try to "fix" it by hard-coding something. This breaks the model logic. If you have a legitimate circularity (like the debt/interest/cash issue), either enable iterative calculation or build the plug structure described above. Don't just type over formulas.

### What You've Accomplished

At the end of this step, your model has veins. Data pumps through it. Change something in one place, and the effect ripples everywhere it should.

The statements don't just sit next to each other — they're connected. They're three views of a single reality.

You still don't have a forecast. You still don't have scenarios. But you have a model that *works* — one where the balance sheet balances, the cash flow reconciles, and everything ties.

That's the foundation. Now we can build on it.

---

## I — Identify: Produce KPIs and Drivers from Historical Information

Here's where the model starts to get interesting.

You've arranged the data. You've linked the statements. Everything ties, everything balances. You have a functioning representation of history.

But history, by itself, is useless.

No one pays you to tell them what already happened. They pay you to figure out what might happen next — and whether the capital structure can survive it. To do that, you need to move from *data* to *drivers*. From "revenue was €480m" to "revenue was €480m because they sold 1.96 billion units at €245 per thousand."

That transformation — from outcomes to explanations — is what this step accomplishes.

### The Reverse Engineering Problem

Think about what you're doing here. You have a set of financial statements: final answers to questions nobody asked you. Revenue. EBITDA. Working capital. These are outputs. Results. Consequences.

What you need are inputs. Causes. Levers.

So you work backwards. You take the output and decompose it into the factors that produced it. Revenue becomes volume times price. COGS becomes input quantity times input cost. Working capital becomes activity times days outstanding.

This is reverse engineering. You're disassembling the machine to understand how it works.

Why bother? Because once you understand the components, you can reassemble them with different assumptions. What if volume grows faster? What if prices decline? What if input costs spike? You can't ask these questions of "revenue." You can only ask them of the drivers beneath revenue.

### The Driver Extraction Process

For each major line item, you're asking the same question: *What explains this number?*

Sometimes the answer is simple. Depreciation is roughly 5% of PP&E. Done. That's your driver.

Sometimes the answer is complex. Revenue is the product of three segments, each with different volumes, prices, and growth trajectories, sold across four geographies with different dynamics. That requires a more elaborate driver structure.

The FDD and CDD have already done much of this work for you. They've decomposed historical performance into components. Your job is to translate their analysis into model inputs.

Let's walk through Europa Packaging.

### Revenue Drivers: Extracting the KPIs

The FDD gave us volumes and ASPs by segment. Now we calculate the implied growth rates and relationships.

**Volume Growth (%)**

| Segment | FY21→22 | FY22→23 | FY23→24 | Average |
|---------|---------|---------|---------|---------|
| Food & Beverage | +2.5% | +3.7% | +2.8% | +3.0% |
| Personal Care | +3.4% | +5.7% | +4.3% | +4.5% |
| Industrial | -2.4% | -4.9% | -2.6% | -3.3% |

Formula: `Volume Growth = (Volume This Year / Volume Last Year) - 1`

What do these numbers tell you? Food & Beverage is steady — 2.5-3.7% growth, probably tracking GDP plus a bit. Personal Care is the growth engine, though it's decelerating (from 5.7% to 4.3%). Industrial is in structural decline, consistently losing 2-5% annually.

These aren't just numbers. They're *characterisations*. When you forecast, you're not guessing "what will revenue do?" You're asking: "Will Food & Beverage continue growing at 3%? Will Personal Care stabilise at 4%? Will Industrial keep shrinking?"

**ASP Growth (%)**

| Segment | FY21→22 | FY22→23 | FY23→24 | Average |
|---------|---------|---------|---------|---------|
| Food & Beverage | +1.4% | +1.4% | +0.4% | +1.1% |
| Personal Care | +1.0% | +2.8% | -1.4% | +0.8% |
| Industrial | +0.8% | -0.8% | +1.2% | +0.4% |

Formula: `ASP Growth = (ASP This Year / ASP Last Year) - 1`

Interesting. ASP growth is low across the board — barely keeping up with inflation. Personal Care had a good year in FY23 (+2.8%) but gave it back in FY24 (-1.4%). Pricing power is limited.

This tells you something important about the business model: Europa Packaging is a volume story, not a pricing story. Growth will come from selling more units, not from charging more per unit. That has implications for margins, for competitive positioning, for how you think about downside scenarios.

### Cost Drivers: Finding the Levers

Costs are where driver-based modelling really earns its keep. A model that says "COGS is 42% of revenue" can't tell you anything about input cost inflation, efficiency improvements, or operating leverage. A model with proper cost drivers can.

**Raw Material Yield**

```
Resin Volume = Output Volume × Yield Factor

FY24: 84,280 tonnes = 1,960m units × 43 kg/'000 units
```

Formula: `Yield = Resin Volume / Output Volume`

Has yield been stable? Let's check:

| Year | Output (m units) | Resin (tonnes) | Yield (kg/'000) |
|------|------------------|----------------|-----------------|
| FY21 | 1,810 | 77,830 | 43.0 |
| FY22 | 1,850 | 79,550 | 43.0 |
| FY23 | 1,910 | 82,130 | 43.0 |
| FY24 | 1,960 | 84,280 | 43.0 |

Rock solid. 43 kg per thousand units, year after year. This is a mature manufacturing process — they've optimised the resin usage, and there's probably not much room for improvement. Your base case should assume 43 kg. An optimistic case might assume 42 kg (2-3% efficiency gain). A pessimistic case keeps it at 43 — you don't usually get *worse* at manufacturing.

**Raw Material Price**

| Year | Resin Cost (€m) | Volume (tonnes) | Price (€/tonne) |
|------|-----------------|-----------------|-----------------|
| FY21 | 81.7 | 77,830 | €1,050 |
| FY22 | 97.1 | 79,550 | €1,220 |
| FY23 | 96.9 | 82,130 | €1,180 |
| FY24 | 99.5 | 84,280 | €1,180 |

Formula: `Resin Price = Resin Cost / Resin Volume`

Now this is interesting. Resin prices spiked 16% in FY22 (from €1,050 to €1,220), then retreated to €1,180 where they've stabilised. The CDD mentioned this — petrochemical volatility, pandemic-era supply disruptions, then normalisation.

What's your forecast? You probably don't have strong views on resin prices. But you can bracket the range:
- Base case: €1,180 (current levels)
- Upside: €1,100 (return to FY21 levels)
- Downside: €1,350 (15% above peak)

The model will show you what each scenario means for EBITDA.

**Labour Cost per Head**

| Year | Labour Cost (€m) | Headcount | Cost/Head (€k) |
|------|------------------|-----------|----------------|
| FY21 | 79.5 | 1,760 | €45.2 |
| FY22 | 83.2 | 1,785 | €46.6 |
| FY23 | 86.7 | 1,800 | €48.2 |
| FY24 | 89.3 | 1,820 | €49.1 |

Formula: `Cost per Head = Total Labour Cost / Headcount`

Cost per head is growing about 3% annually — roughly inflation plus a bit for wage progression. Headcount is growing about 1% annually — roughly in line with volume growth, maybe slightly below (efficiency gains).

These are your levers. To forecast labour costs:
```
Labour Cost = Headcount × Cost per Head
Headcount = f(volume growth, efficiency assumptions)
Cost per Head = f(wage inflation, mix shifts)
```

You can now ask: what if wage inflation runs hot at 4%? What if they cut 5% of headcount through automation? The model can answer.

### Working Capital Drivers: The Days Calculation

Working capital drivers are the most formulaic. You're calculating "days outstanding" — how many days of activity are sitting in each balance sheet item.

**Receivable Days**

```
Receivable Days = (Receivables / Revenue) × 365
```

| Year | Receivables (€m) | Revenue (€m) | Days |
|------|------------------|--------------|------|
| FY21 | 52 | 446 | 43 |
| FY22 | 55 | 468 | 43 |
| FY23 | 57 | 480 | 43 |
| FY24 | 57 | 480 | 43 |

Perfectly stable at 43 days. Your customers pay in about six weeks, and that hasn't changed. Forecast at 43 unless you have reason to believe otherwise.

But remember the geographic mix data from the FDD: Southern Europe pays at 68 days, DACH at 38 days. If sales mix shifts toward Southern Europe, receivable days will creep up even without any change in customer behaviour. The model should let you test this.

**Inventory Days**

```
Inventory Days = (Inventory / COGS) × 365
```

The FDD gave us 42 days. Use their methodology rather than a crude calculation, as they've likely analysed inventory by component (raw materials vs. WIP vs. finished goods) against the relevant cost base for each.

**Payable Days**

```
Payable Days = (Payables / Purchases) × 365
```

The FDD gave us 49 days. Stable over time. The company pays its suppliers in about seven weeks.

### The Driver Dashboard

At the end of this step, you should have a complete list of KPIs extracted from historical data:

**Revenue Drivers**

| Driver | FY21 | FY22 | FY23 | FY24 | Avg/Trend |
|--------|------|------|------|------|-----------|
| F&B volume growth | — | +2.5% | +3.7% | +2.8% | +3.0% |
| F&B ASP growth | — | +1.4% | +1.4% | +0.4% | +1.1% |
| PC volume growth | — | +3.4% | +5.7% | +4.3% | +4.5% |
| PC ASP growth | — | +1.0% | +2.8% | -1.4% | +0.8% |
| Ind volume growth | — | -2.4% | -4.9% | -2.6% | -3.3% |
| Ind ASP growth | — | +0.8% | -0.8% | +1.2% | +0.4% |

**Cost Drivers**

| Driver | FY21 | FY22 | FY23 | FY24 | Avg/Trend |
|--------|------|------|------|------|-----------|
| Resin yield (kg/'000) | 43.0 | 43.0 | 43.0 | 43.0 | 43.0 |
| Resin price (€/t) | 1,050 | 1,220 | 1,180 | 1,180 | 1,158 |
| Headcount growth | — | +1.4% | +0.8% | +1.1% | +1.1% |
| Cost/head growth | — | +3.1% | +3.4% | +1.9% | +2.8% |

**Working Capital Drivers**

| Driver | FY21 | FY22 | FY23 | FY24 | Avg/Trend |
|--------|------|------|------|------|-----------|
| Receivable days | 43 | 43 | 43 | 43 | 43 |
| Inventory days | 42 | 42 | 42 | 42 | 42 |
| Payable days | 48 | 49 | 49 | 49 | 49 |

**Capex Drivers**

| Driver | FY21 | FY22 | FY23 | FY24 | Avg/Trend |
|--------|------|------|------|------|-----------|
| Maintenance capex (€m) | 12 | 13 | 14 | 14 | 13 |
| Maintenance as % rev | 2.7% | 2.8% | 2.9% | 2.9% | 2.8% |
| Growth capex (€m) | 8 | 15 | 6 | 4 | Project-specific |

### What You've Actually Done

You've translated history into language.

Before this step, you had numbers. Revenue was €480m. COGS was €200m. Working capital was €68m. Facts without explanation.

Now you have explanations. Revenue was €480m because volumes of 1.96 billion units were sold at €245 per thousand. COGS was €200m because 84,000 tonnes of resin at €1,180 per tonne, plus labour, plus overhead. Working capital was €68m because customers pay in 43 days, inventory sits for 42 days, and suppliers get paid in 49 days.

Every number has a *why* behind it. And once you know the why, you can ask *what if*.

What if volumes only grew 1%? What if resin prices spiked to €1,400? What if receivable days crept up to 50?

The model can now answer these questions — because you've identified the drivers that produce the answers.

---

## V — Venture: Project Forward

Now comes the moment of truth.

You've arranged historical data. You've linked the statements. You've identified the drivers that explain the past. The model works — for history. Everything ties, everything balances, everything makes sense.

But nobody cares about history.

What they care about is the future. Will the company generate enough cash to service the debt? Will EBITDA hold up in a downturn? Will the covenants be breached? These are forward-looking questions, and they require forward-looking answers.

So now you venture forward. You take the drivers you've identified and project them into the future. The model flips from *explaining what happened* to *predicting what might happen*.

### The Great Flip

Here's the conceptual shift you need to understand:

**In historical periods:**
- The financial statements are *data* (numbers from audited accounts)
- The drivers are *calculated* (formulas that derive KPIs from the data)

**In forecast periods:**
- The drivers are *inputs* (assumptions you type in)
- The financial statements are *calculated* (formulas that derive outputs from the drivers)

Everything inverts.

Take revenue. In the historical section, you had:
```
Revenue (FY24) = €480m                    [data from accounts]
Volume (FY24) = 1,960m units              [data from FDD]
ASP (FY24) = €245                         [data from FDD]
Volume growth = +2.8%                     [calculated: FY24/FY23 - 1]
```

In the forecast section, it flips:
```
Volume growth = +2.5%                     [input: your assumption]
Volume (FY25) = 1,960 × (1 + 2.5%)       [calculated from driver]
ASP growth = +1.0%                        [input: your assumption]
ASP (FY25) = €245 × (1 + 1.0%)           [calculated from driver]
Revenue (FY25) = Volume × ASP            [calculated from components]
```

The arrows reverse. Instead of decomposing outputs into drivers, you're composing drivers into outputs.

### The Art of Assumption-Setting

Let's be honest about what's happening here.

You're guessing.

Educated guessing. Informed guessing. Guessing constrained by historical patterns and market analysis and management guidance. But guessing nonetheless.

Nobody knows what Europa Packaging's volume growth will be in FY27. Not the CEO. Not the sponsor. Not the most sophisticated AI. The future is uncertain, and all you can do is make reasonable assumptions about what might happen.

This is uncomfortable for people who want precision. They want the "right" answer. They want the model to tell them exactly what will happen.

It won't. It can't. That's not what models do.

What the model *can* do is tell you: *if* these assumptions hold, *then* these outcomes follow. It's a conditional statement, not a prophecy. The value isn't in the specific numbers — it's in understanding the relationships between assumptions and outcomes.

So how do you set assumptions?

**Start with the historical average.** For stable drivers, the historical average is a reasonable baseline.

**Adjust for known factors.** Management says they're implementing a new ERP system. The CDD says a segment is entering a higher-growth phase. Interest rates have risen. Incorporate what you know.

**Apply the CDD's perspective.** The Commercial Due Diligence has views on market growth, competitive dynamics, pricing trends. These should inform your revenue assumptions.

**Be conservative on things that matter.** When in doubt, be conservative. You're a credit analyst, not an equity cheerleader.

**Understand the implied reality.** Every assumption implies something about the world. Make sure they tell a coherent story.

### Building the Forecast: Europa Packaging

Based on the historical analysis, the FDD, and the CDD, here's a reasonable base case for Europa Packaging:

**Revenue Drivers — Base Case**

| Driver | FY25E | FY26E | FY27E | FY28E | FY29E | Rationale |
|--------|-------|-------|-------|-------|-------|-----------|
| F&B volume growth | +2.5% | +2.5% | +2.0% | +2.0% | +2.0% | Matures toward market growth |
| F&B ASP growth | +1.5% | +1.5% | +1.5% | +1.5% | +1.5% | Inflation pass-through |
| PC volume growth | +4.0% | +3.5% | +3.0% | +3.0% | +2.5% | Decelerates from peak |
| PC ASP growth | +1.0% | +1.0% | +1.0% | +1.0% | +1.0% | Limited pricing power |
| Ind volume growth | -3.0% | -3.0% | -2.0% | -2.0% | -2.0% | Structural decline continues |
| Ind ASP growth | +0.5% | +0.5% | +0.5% | +0.5% | +0.5% | Barely keeps pace |

These assumptions aren't "right." They're *defensible*. You can explain why you chose them. Someone could disagree, and you could have a productive conversation about whether volume growth should be 2.5% or 2.0%.

The formulas take over from here. Volume × ASP = Revenue. Input volumes × input prices = Costs. Revenue - Costs = EBITDA. And so on through the three statements.

What emerges:

| Metric | FY24 | FY25E | FY26E | FY27E | FY28E | FY29E |
|--------|------|-------|-------|-------|-------|-------|
| Revenue | 480 | 498 | 516 | 533 | 550 | 567 |
| EBITDA | 78 | 82 | 86 | 91 | 94 | 98 |
| EBITDA Margin | 16.2% | 16.5% | 16.7% | 17.0% | 17.2% | 17.4% |
| Free Cash Flow | — | 43 | 45 | 38 | 52 | 58 |

Revenue grows from €480m to €567m — a 3.4% CAGR. EBITDA reaches €98m. Margins expand on operating leverage. Free cash flow is positive throughout.

See what happened? You didn't assume "revenue grows 3.4%." You assumed volume growth and price growth by segment, and revenue emerged as a consequence. The 3.4% is an output, not an input.

---

## E — Explore: Create Scenarios

Here's an uncomfortable truth about the forecast you just built: it's wrong.

Not wrong in the sense that you made an error — the formulas are fine, the linkages work, the balance sheet balances. Wrong in the sense that it won't happen. The future will not unfold exactly as your base case predicts.

This isn't a flaw in your model. It's a feature of reality. The future is uncertain.

So what do you do? You explore. You build scenarios. You ask: what if things go better than expected? What if they go worse? How bad can it get before the credit breaks?

### The Point of Scenarios

**Scenarios are not predictions.** You're not saying "there's a 30% chance of the downside case." You have no idea what the probability is.

**Scenarios are stress tests.** You're asking: if the world looks like *this*, can the company still service its debt?

**Scenarios reveal sensitivity.** By varying assumptions and watching outputs change, you learn which drivers matter most.

**Scenarios enable conversation.** When you present a financing to a credit committee, they won't accept a single-point forecast. Scenarios let you answer with analysis rather than hand-waving.

### The Classic Three

**Base Case:** Your best estimate of what will probably happen. Reasonable. Defensible.

**Upside Case:** Things go better than expected. The market grows faster, the company gains share, margins expand.

**Downside Case:** Things go worse than expected. Recession hits, volumes decline, pricing comes under pressure, input costs spike.

Good scenarios are *narratives*, not just numbers. Each scenario tells a story about what's happening in the world and how the company responds.

### Europa Packaging: Three Scenarios

**Base Case: "Steady As She Goes"**

The European packaging market grows at its historical pace. Europa maintains market share. Input costs track inflation. Nothing dramatic.

EBITDA grows from €78m to €98m. Free cash flow is €43-58m annually. The credit is comfortable.

**Upside Case: "The Growth Story Delivers"**

Personal Care takes off. Volume growth is higher. Pricing is stronger. Resin prices stay subdued. The company executes flawlessly.

EBITDA reaches €126m by FY29. Margins expand to nearly 20%. Free cash flow is robust even with higher capex.

**Downside Case: "The Cycle Turns"**

Recession hits in FY26. Consumer spending pulls back. Volumes decline. Pricing comes under pressure. Resin prices spike. The company cuts growth capex but can't avoid the pain.

EBITDA drops to a trough of €55m — a 30% decline from peak. Margins compress by 400bps. Free cash flow stays positive but drops to €16-18m during the trough.

### The Credit Question: Does It Survive?

In leveraged finance, two metrics matter above all others:

**Net Leverage = Net Debt ÷ EBITDA**

This tells you how much debt the company carries relative to its earnings power.

**Interest Coverage = EBITDA ÷ Interest Expense**

This tells you whether the company can service its debt.

For Europa with €300m of TLB at 8%:

**Base Case:**
- Net Leverage: 3.4x → 1.7x (deleverages significantly)
- Interest Coverage: 3.4x → 4.1x (comfortable throughout)

**Downside Case:**
- Net Leverage: 3.8x → 3.9x (no deleveraging)
- Interest Coverage: 3.1x → 2.3x at trough (tight but survivable)

The downside case is concerning but not catastrophic. Coverage stays above 2x. The company doesn't default — it just doesn't deleverage.

### The 50% Rule

Here's where it gets interesting.

The market's rule of thumb — unwritten but widely understood — is this: **A deal is creditworthy if net leverage at exit is approximately half of net leverage at entry.**

If you start at 5.0x and end at 2.5x, that's a good deal. An equivalent expression: **Cumulative free cash flow over the projection period should equal at least 50% of opening debt.**

Let's check Europa:

**Base Case:**
- Entry leverage: 3.8x → Exit leverage: 1.7x (-55% reduction) ✓
- Cumulative FCF: €235m = 78% of €300m opening debt ✓

**Downside Case:**
- Entry leverage: 3.8x → Exit leverage: 3.9x (+3% — no deleveraging) ✗
- Cumulative FCF: €128m = 43% of €300m opening debt ✗

The base case passes easily. The downside fails both tests.

What does this mean? The leveraged finance market isn't underwriting to full repayment. It's underwriting to *refinanceability*. The goal isn't to extinguish the debt — it's to get the company into a position where it can access new debt to replace the old.

The €150m that doesn't get repaid? It gets refinanced at maturity. Does any debt ever get fully repaid? At the systemic level, the answer is murky. Credit creation is how modern economies grow. The leverage never fully unwinds because unwinding it would shrink the economy.

What the 50% rule really tells you: the leveraged finance market isn't in the business of eliminating debt. It's in the business of *managing* debt.

---

## R — Roll: Extend Formulas Across the Forecast Period

This is the moment of truth.

You've built your assumptions. You've written your formulas. You've tested one year — maybe two — and everything seems to work.

Now you extend it. You select your forecast columns, grab the corner of the cell, and drag to the right. Five years. Seven years.

And then one of two things happens.

Either everything works — the formulas propagate, the statements stay linked, the balance sheet balances across every period.

Or something breaks. A circular reference error appears. The balance sheet diverges from zero. Cash goes negative when it shouldn't. A row of #REF! errors cascades across the screen.

The Roll step is mechanically simple — you're just copying formulas to the right. But it's where every small mistake you made in the earlier steps reveals itself. It's the moment of accountability.

### Why This Step Exists

The Roll step forces you to build your model in a way that actually works when extended. That constraint shapes how you construct the model in the first place.

If you hard-coded depreciation as €17.1m instead of linking it to PP&E and a depreciation rate, the roll will give you €17.1m in every future year. Wrong.

If you wrote a formula that references the wrong period, the error propagates across every future column. Wrong.

If your model is built correctly, the roll is trivial. If it's not, the roll exposes every shortcut.

### Common Problems When Rolling

**The Absolute Reference Mistake:** You wrote a formula that references a fixed cell when it should reference a relative one.

**The Hard-Coded Value:** Someone typed a number instead of writing a formula. The chain is broken.

**The Missing Row:** Your SUM formula doesn't include all the rows it should.

**The Circular Reference:** The debt/interest/cash loop creates problems.

**The Off-by-One-Year Error:** Your "change in receivables" looks at the wrong prior period.

### Post-Roll Checks

Once you've rolled successfully:

1. **Balance Sheet Check:** Does it balance in every period?
2. **Cash Reconciliation:** Does CF ending cash equal BS cash?
3. **Revenue Continuity:** Does it grow smoothly?
4. **Margin Stability:** No wild swings?
5. **Working Capital:** Stable as % of revenue?

If everything checks out, you have a working forecast model.

---

## S — Scrutinise: Analyse Results, Iterate, Refine

You've built the model. The data is arranged. The statements are linked. The drivers are identified. The projections are complete. The scenarios are constructed. The formulas are rolled across five years.

Now what?

Now comes the part that actually matters: figuring out what it all means.

### The Two Metrics That Rule Everything

In leveraged finance, two metrics matter above all others:

**Net Leverage = Net Debt ÷ EBITDA**

This answers: Is the debt load sustainable?

**Interest Coverage = EBITDA ÷ Interest Expense**

This answers: Can the debt be serviced today?

A credit can fail on either dimension. The ideal credit has moderate leverage *and* comfortable coverage, with a trajectory that improves both over time.

### Building the Output Page

Your model produces thousands of numbers. Your credit committee has twenty minutes. You need to distill.

```
═══════════════════════════════════════════════════════════════════════════════
                        EUROPA PACKAGING GROUP
                     Credit Analysis Summary
═══════════════════════════════════════════════════════════════════════════════

SCENARIO COMPARISON
────────────────────────────────────────────────────────────────────────────────
                            Base Case       Upside          Downside
────────────────────────────────────────────────────────────────────────────────
FY29E EBITDA                €98m            €126m           €69m
FY29E Net Leverage          1.7x            0.8x            3.9x
FY29E Interest Coverage     4.1x            5.3x            2.9x
────────────────────────────────────────────────────────────────────────────────
Minimum Coverage (period)   3.4x (FY25)     3.6x (FY25)     2.3x (FY27)
Maximum Leverage (period)   3.8x (FY24)     3.1x (FY25)     5.3x (FY27)
────────────────────────────────────────────────────────────────────────────────
Cumulative FCF              €235m           €293m           €128m
  as % of Opening Debt      78%             98%             43%
────────────────────────────────────────────────────────────────────────────────
Exit Leverage vs Entry      -55%            -79%            +3%
────────────────────────────────────────────────────────────────────────────────

ASSESSMENT
────────────────────────────────────────────────────────────────────────────────
✓ Base case shows strong deleveraging (3.8x → 1.7x), passing 50% test
✓ Interest coverage remains above 3.0x throughout in base case
✓ Free cash flow positive in all scenarios, all periods
⚠ Downside case shows limited deleveraging, coverage trough of 2.3x
⚠ Downside fails 50% cumulative FCF test (43%)
✓ No scenario shows coverage below 2.0x (payment default unlikely)
────────────────────────────────────────────────────────────────────────────────
```

One page. Three scenarios. The key metrics. The verdict.

### Sensitivity Analysis

Scenarios show you different futures. Sensitivity analysis shows you *which assumptions drive the differences*.

**Single-Variable Sensitivity:** Hold everything at base case except one driver. Flex it. Watch what happens.

Resin prices ranging from €1,100 to €1,350 produce EBITDA from €83m to €95m. A €12m swing. Meaningful, but not catastrophic.

Volume growth ranging from -2% to +6% produces EBITDA from €69m to €113m. A €44m swing. Volume is the dominant risk.

**Breakeven Analysis:** How bad can it get before something breaks?

At what volume growth does coverage fall below 2.0x? Answer: -4.8% annual decline.

At what EBITDA margin does leverage exceed 6.0x? Answer: 10.2% margin (vs 17% base case).

The breakevens suggest this is a robust credit. You'd need multiple, severe, simultaneous stress factors to break it.

### Iteration

The model is a conversation partner.

You build it with certain expectations. The numbers come out different. What do you do?

Don't force the model to match your expectations. If it's telling you something unexpected, *listen to it*.

Maybe your assumptions are inconsistent. Maybe your expectations were wrong. Better to learn now than after you've underwritten the deal.

The final model shouldn't just produce numbers you like. It should produce numbers that *follow logically from defensible assumptions*.

---

## Beyond the Basics: Advanced Modeling Topics

The DRIVERS framework gives you a working model. But working models and *good* models are different things.

A working model treats debt as a single line item. A good model captures the waterfall of instruments. A working model assumes taxes are 25% of EBT. A good model tracks deferred taxes and interest deductibility limits. A working model uses annual periods. A good model knows when quarterly granularity matters.

Let's go deeper.

---

## Advanced Topic 1: Modeling Debt Profiles

Real capital structures are messy.

A typical European LBO might include:
- **Super Senior RCF** (€50m, E+350, 5-year maturity)
- **Senior Secured TLB** (€250m, E+450, 7-year maturity)
- **Senior Secured Notes** (€100m, 6.5% fixed, 8-year maturity)
- **Holdco PIK Notes** (€75m, 12% PIK, 8-year maturity)
- **Shareholder Loan** (€50m, 10% PIK, no maturity)

Five instruments. Different rates. Different maturities. Different behaviours.

### The Debt Schedule

The heart of debt modeling is the debt schedule — a dedicated section that tracks each instrument separately:

```
SENIOR SECURED TLB (€250m)
────────────────────────────────────────────────────────────────────────────────
                            FY24    FY25E   FY26E   FY27E   FY28E   FY29E
Opening Balance             250     250     250     250     250     250
Scheduled Amortisation        0       0       0       0       0       0
Cash Sweep                    0       0       0       0       0     (50)
Closing Balance             250     250     250     250     250     200
Interest Rate               8.0%    8.0%    8.0%    8.0%    8.0%    8.0%
Cash Interest Expense       20.0    20.0    20.0    20.0    20.0    18.0
```

### Instrument-Specific Behaviors

**The RCF as a Plug:** The revolver flexes to absorb cash surpluses or deficits. It's the model's liquidity buffer.

**PIK Instruments:** Payment-in-Kind instruments don't pay cash interest. The interest accrues onto the principal balance. The Holdco PIK notes grow from €75m to €132m over five years — no cash left the building, but the debt grew.

**Cash Sweeps:** Many credit agreements require excess cash flow to prepay debt. A typical sweep: 50% of ECF if leverage > 4.0x, 25% if 3-4x, 0% below 3x.

### Which Leverage? Which Coverage?

With multiple instruments, be clear about definitions:
- *Senior Secured Net Leverage* = TLB + RCF + Notes - Cash
- *Total Net Leverage* = All debt including subordinated
- *Cash Interest Coverage* = EBITDA / Cash Interest (excludes PIK)

Know which definition your covenants test.

---

## Advanced Topic 2: Working Capital Modeling

The simple approach — Receivables = Revenue × Days — works for a first pass. It doesn't work for a good model.

### Seasonality

If the business builds inventory in Q3 to sell in Q4, year-end working capital might be €35m while Q3 peaks at €60m. Your RCF needs to accommodate the peak, not the trough.

### Mix Effects

Receivable days are averages. DACH customers pay in 38 days; Southern Europe in 68 days. If mix shifts toward Southern Europe, blended days creep up even without any change in customer behaviour.

### Negative Working Capital

Some businesses — subscriptions, fast-turning retail — have structurally negative working capital. Growth *releases* cash rather than absorbing it. Handle the signs carefully.

---

## Advanced Topic 3: Capex and Depreciation

### Vintage-Based Depreciation

The sophisticated approach treats each year's capex as a new "vintage" that depreciates independently over its useful life. The sum of all vintages equals total depreciation.

This matters when the capex profile is lumpy. Europa's FY27 expansion adds €40m of machinery. Depreciation jumps immediately in FY27-29. A simple "% of revenue" approach misses this.

### Asset Tracking

Track PP&E by category (buildings, machinery, vehicles), each with its own depreciation rate. Buildings last 40 years (2.5% depreciation). Machinery lasts 15 years (6.7%). IT equipment lasts 3 years (33%).

### IFRS 16 Leases

Operating leases now appear as right-of-use assets and lease liabilities. This affects leverage calculations. Know whether your covenant definition includes or excludes IFRS 16 leases.

---

## Advanced Topic 4: Tax Modeling

### Book Tax vs. Cash Tax

The tax expense on the income statement rarely equals cash paid to tax authorities. Common timing differences:
- Accelerated tax depreciation vs. straight-line book depreciation
- Provisions not deductible until realised
- Revenue taxable when received, not when earned

For cash flow, you need *cash tax*, not book tax.

### Net Operating Losses

NOLs let companies offset future profits against past losses. Track:
- Beginning balance
- NOLs generated (new losses)
- NOLs utilised (offsetting current profits)
- NOLs expired
- Ending balance

Many jurisdictions limit annual NOL usage (e.g., 80% of taxable income in the US).

### Interest Deductibility (ATAD)

The EU Anti-Tax Avoidance Directive limits interest deductions to 30% of EBITDA. For highly levered companies, this materially increases cash taxes.

```
ATAD IMPACT
────────────────────────────────────────────────────────────────────────────────
EBITDA                        €82m
30% Cap                       €25m
Net Interest Expense          €27m
Deductible Interest           €25m
Non-Deductible                €2m
Additional Tax (@ 25%)        €0.5m
────────────────────────────────────────────────────────────────────────────────
```

Model this explicitly. A highly levered deal can have materially different cash flows than a simple calculation suggests.

---

## Advanced Topic 5: Quarterly Models in Practice

### LTM Calculations

Credit ratios use Last Twelve Months figures:

```
LTM EBITDA (Q2 FY25) = Q3 FY24 + Q4 FY24 + Q1 FY25 + Q2 FY25
```

Build dedicated LTM rows that sum trailing four quarters.

### Covenant Testing

Covenants test quarterly. Build compliance checks:

```
COVENANT COMPLIANCE
────────────────────────────────────────────────────────────────────────────────
                      Q1 FY25  Q2 FY25  Q3 FY25  Q4 FY25
Net Leverage (LTM)       3.9x     3.8x     3.7x     3.4x
Covenant                 5.5x     5.5x     5.25x    5.25x
Headroom                 1.6x     1.7x     1.55x    1.85x
Status                    ✓        ✓        ✓        ✓
────────────────────────────────────────────────────────────────────────────────
```

### Cash Flow Timing

Quarterly models show when cash actually moves:

```
                      Q1      Q2      Q3      Q4      Full Year
EBITDA                18      21      22      24        85
Working Capital Δ      3      (7)     (4)      7        (1)
Free Cash Flow        11       0       1      17        29
```

Q2 and Q3 are tight — FCF is flat. The annual total looks fine (€29m), but the quarterly path shows the real story.

---

## Conclusion: The Model as a Tool for Thinking

We started this chapter with a warning about the modeling trap — the misconception that financial modeling is the most critical skill in leveraged finance.

Having now spent many pages on exactly how to build a model, let me reaffirm that warning.

The model is important. But it's important the way a map is important to an explorer. The map helps you navigate. It shows you where you are and where you might go.

But the map is not the territory.

Europa Packaging exists in the real world — factories producing plastic containers, trucks delivering to customers, workers showing up each morning. The model is a simplified representation of that reality. Useful, but incomplete.

The best practitioners use models rigorously but hold them loosely. They understand that a model showing 4.1x coverage doesn't mean coverage *will be* 4.1x. It means coverage will be 4.1x *if all the assumptions hold*.

So build good models. Use the DRIVERS framework. Calculate your leverage and coverage. Run your scenarios. Do the work.

Then step back and ask: does this make sense? Does the model's story match what I know about the business, the market, the competitive dynamics?

The model is the beginning of the analysis, not the end.

Use it wisely.

---

*In the next chapter, we'll take this corporate model and transform it into an LBO model — adding acquisition accounting, a new capital structure, and sponsor economics. But without this foundation, that chapter wouldn't be possible. The LBO model is built on top of the corporate model. Master this first.*
