# Module 7: IAS 36 — Impairment of Assets
## IFRS Deep Learning Series | Case Study: Grifols S.A. (FY2025)

---

## 1. Why This Standard Exists

The cost model (Module 5: IAS 16; Module 6: IAS 38) has a fundamental flaw: it
carries assets at historical cost minus depreciation, with no automatic mechanism
for downward adjustment when the asset's economic value deteriorates below its
book value. A fractionation plant built for €200M and depreciated to €120M remains
on the balance sheet at €120M even if the market for the products it manufactures
has collapsed and the asset is now worth €30M in any realistic use.

IAS 36 corrects this by establishing a ceiling on asset carrying amounts. The
principle is simple: **an asset cannot be carried at more than it is worth**. The
standard defines "worth" as the higher of two estimates of economic value —
how much the asset could fetch in a sale, and how much cash the asset will generate
if kept in use. If the carrying amount exceeds both of these, an impairment loss
must be recognized immediately.

For Grifols, this standard governs the most consequential numbers on the balance
sheet. The company carries **€6,833M of goodwill** and **€2,728M of other
intangibles**, representing 38% of total assets. Deloitte's audit report flagged
the goodwill impairment test as a **key audit matter** — the single area of highest
audit risk in the entire set of accounts. Understanding IAS 36 is therefore not
optional for anyone who reads Grifols' financial statements seriously.

---

## 2. Scope and the Annual Test Requirement

### 2.1 What IAS 36 Covers

IAS 36 applies broadly to most assets on the balance sheet, with specific exclusions
for assets covered by other standards (inventories: IAS 2; financial assets: IFRS 9;
deferred tax assets: IAS 12; employee benefit assets: IAS 19). The assets most
directly relevant for Grifols:

- Goodwill (€6,833M) — **mandatory annual test**, regardless of indicators
- Intangible assets with indefinite useful lives (IPR&D, ~€320M) — **mandatory annual test**
- Intangible assets not yet available for use — **mandatory annual test**
- PP&E, finite-life intangibles, ROU assets — tested only **when an indicator of
  impairment exists**

### 2.2 The Trigger-Based vs. Annual Test Distinction

This distinction drives everything about how the impairment test is structured:

**Annual test (no trigger required)**: Goodwill and indefinite-life intangibles must
be tested every single year, even if there is no indicator of impairment. The IASB
mandated this because goodwill represents the premium paid for assembled businesses —
a premium that can evaporate quickly if business conditions change — and because the
absence of amortization (unlike finite-life assets) means there is no automatic
P&L drain that forces periodic recognition of declining value.

**Trigger-based test**: For all other assets, management must assess at each reporting
date whether any indicator of impairment exists. If yes, estimate recoverable amount
and compare to carrying amount. If no indicator exists, no formal test is required.

IAS 36.12 provides an extensive (non-exhaustive) list of indicators, split between
external and internal sources:

**External indicators:**
- Significant decline in market value beyond what would be expected from normal use
- Significant adverse changes in technology, markets, economy, or law
- Increase in market interest rates or market rates of return that materially affect
  the discount rate used in calculating value in use
- The entity's net assets exceed its market capitalization

**Internal indicators:**
- Evidence of obsolescence or physical damage
- Significant adverse changes in how the asset is used (restructuring plans,
  discontinued operations)
- Evidence from internal reporting that economic performance is worse than expected

**In Grifols**: The trigger-based test for PP&E and finite-life intangibles in 2025
did not identify impairment indicators at the asset/CGU level beyond the goodwill
already tested annually. However, note that the significant rise in interest rates
in 2023-2024 (which increased discount rates used in impairment tests) was an
external indicator that would have required assessment for all assets — not just
goodwill.

---

## 3. The Mechanics — Recoverable Amount

### 3.1 The Core Concept

When impairment is indicated (or required annually for goodwill), the entity must
estimate the **recoverable amount** of the asset or cash-generating unit:

> **Recoverable Amount = Higher of: (a) Fair Value Less Costs of Disposal (FVLCD)
> and (b) Value in Use (VIU)**

The entity need not estimate both — if either one exceeds carrying amount, there is
no impairment. In practice, the one that is more readily determinable or clearly
higher is estimated first.

### 3.2 Fair Value Less Costs of Disposal (FVLCD)

FVLCD is the price that would be received to sell an asset in an orderly transaction
between market participants at the measurement date (i.e., the IFRS 13 fair value
definition — Module 25), minus the incremental costs directly attributable to the
disposal (legal fees, removal costs, stamp duty — but not financing costs or income
taxes).

For most operating assets within Grifols, FVLCD is difficult to determine because
there is no active market for a plasma fractionation plant or a bundle of customer
relationships. The concept works well for liquid assets but becomes highly judgmental
for specialized manufacturing CGUs.

Where Grifols does use FVLCD — notably for the Diagnostic CGU, where standalone
comparable companies exist (Ortho Clinical Diagnostics, bioMérieux) — it applies a
discounted cash flow approach calibrated to what a hypothetical market participant
would pay. This uses market-observable inputs (peer company multiples, transaction
precedents) rather than purely internal projections, making it arguably more
objective than VIU.

### 3.3 Value in Use (VIU)

Value in Use is the present value of the future cash flows expected to be derived
from an asset or CGU. IAS 36 is prescriptive about the inputs:

**The cash flow projections must:**
- Be based on reasonable and supportable assumptions
- Represent management's best estimate of economic conditions over the asset's
  remaining useful life
- Give greater weight to external evidence
- Use the most recent financial budgets/forecasts approved by management for up
  to **five years** maximum from detailed projections
- Use a **steady state / terminal value** extrapolation beyond five years, typically
  using a long-term growth rate no greater than the long-term average growth rate
  for the products, industries, or country — unless a higher rate can be justified

**The cash flows must include:**
- Projections of cash inflows from continuing use
- Projections of cash outflows necessarily incurred to generate those inflows
  (including allocated overhead)
- Net cash flows received or paid on disposal at the end of the asset's useful life

**The cash flows must exclude:**
- Cash inflows from enhancing or improving the asset's performance beyond the
  current standard
- Cash outflows for major restructuring not yet committed
- **Financing activities** (debt service is not included — VIU is an unlevered concept)
- **Income taxes** (the discount rate and cash flows are both pre-tax)

**The discount rate** is a critical input. IAS 36 requires a **pre-tax rate** that
reflects current market assessments of the time value of money and the risks specific
to the asset. In practice, most companies derive a post-tax WACC and gross it up to
a pre-tax equivalent. The rate should reflect the return that would be required by
a market participant investing in an asset with the same profile of risks — not
Grifols' own cost of capital as currently leveraged.

---

## 4. Cash-Generating Units — The Unit of Account

### 4.1 Why Individual Assets Cannot Always Be Tested

IAS 36 acknowledges a practical reality: most individual assets do not generate cash
flows independently of other assets. A fractionation column is worthless without the
building it sits in, the cold storage that preserves the plasma, the purification
system downstream, and the distribution network that delivers the product.

When it is not possible to estimate the recoverable amount of an individual asset
because it does not generate independent cash flows, the asset must be grouped with
the other assets that together generate identifiable, largely independent cash inflows.
This group is the **cash-generating unit (CGU)**.

### 4.2 CGU Definition

IAS 36.6 defines a CGU as the smallest identifiable group of assets that generates
cash inflows that are largely independent of the cash inflows from other assets or
groups of assets.

**"Largely independent"** is the key phrase. Perfect independence is not required.
The test is whether management can identify cash flows that are meaningfully
separable. If product A and product B share manufacturing, distribution, and customers
such that their cash flows are completely intertwined, they belong in the same CGU.
If they use the same plant but serve distinct customer bases with distinct pricing,
they might be separate CGUs.

### 4.3 Grifols' CGU Structure

Nota 6 discloses that Grifols tests goodwill for impairment at the **operating
segment level** — consistent with the four segments disclosed under IFRS 8 (Module 4).
This gives four CGUs:

| CGU | Goodwill Allocated (€M) | Basis for CGU Identification |
|---|---|---|
| Biopharma | ~4,308 | Plasma-derived products; integrated collection-fractionation-distribution |
| Diagnostic | ~2,525 | Blood typing and NAT; separate customer base, separate distribution |
| Bio Supplies | — | Relatively small; may be aggregated with Biopharma |
| Others | — | Not a profit-generating unit in the traditional sense |
| **Total** | **~6,833** | |

**Why the Diagnostic CGU is the critical one**: With ~€2,525M of goodwill allocated
to a segment generating ~€210M of EBITDA, the Diagnostic CGU is carrying goodwill
at a multiple of ~12x EBITDA. That is a high multiple for a diagnostics business
facing increasing competition (point-of-care blood typing, automated blood bank
systems from Ortho and Roche). The impairment test must demonstrate that the
present value of future Diagnostic cash flows exceeds the carrying amount of all
Diagnostic assets — including €2,525M of goodwill.

**Why the Biopharma CGU carries less relative risk**: With ~€4,308M of goodwill
but a much larger earnings base (~€1,390M EBITDA), the Biopharma CGU has a
more defensible multiple (~3x EBITDA). The plasma-derived immunoglobulin business
has structural demand growth, pricing power, and regulatory barriers that support
a sustained cash generation profile.

### 4.4 Goodwill Allocation to CGUs

IAS 36.80 requires goodwill acquired in a business combination to be allocated to
each CGU (or group of CGUs) expected to benefit from the synergies of the
combination. This allocation is performed at acquisition and reflects management's
assessment of where synergies reside.

The allocation is not mechanical — it requires judgment. When Grifols acquired
Talecris, the Biopharma CGU absorbed the bulk of the goodwill because the synergies
(plasma yield optimization, combined product portfolio, shared manufacturing
overhead) were primarily in the Biopharma business. When Biotest was acquired, its
goodwill was allocated between Biopharma (fractionation capacity, plasma collection
in Germany) and Diagnostic (Biotest's blood group serology business).

Once allocated, goodwill sits in the CGU unless the CGU is reorganized — at which
point goodwill must be reallocated using a relative-value approach.

---

## 5. Performing the Test — Grifols' Methodology

### 5.1 The Sequence

The impairment test for each CGU follows this sequence:

**Step 1**: Determine the **carrying amount** of the CGU — the sum of all assets
allocated to the CGU, including allocated goodwill. This is the number the
recoverable amount must exceed.

**Step 2**: Estimate the **recoverable amount** (higher of FVLCD and VIU).

**Step 3**: Compare. If carrying amount > recoverable amount → impairment loss.
If carrying amount ≤ recoverable amount → no impairment; disclose headroom.

**Step 4**: If impairment: **allocate the loss** first against goodwill (to its
full carrying amount), then pro rata across other assets in the CGU down to each
asset's individual recoverable amount (no asset can be written below its own
recoverable amount).

### 5.2 Grifols' Assumptions for the VIU Test (Nota 6)

Nota 6 is one of the richest notes in the accounts for a financial analyst. It
discloses the key assumptions underlying the value in use calculation for each CGU:

**Biopharma CGU — Key Assumptions:**

| Assumption | Value | Sensitivity |
|---|---|---|
| Revenue growth rate (years 1-5) | 6-9% per annum | Reflects IG market demand growth + pricing |
| EBITDA margin (long-term) | 22-25% | Gradual improvement from operational leverage |
| Terminal growth rate | 2.0-2.5% | Broadly in line with long-term pharma growth |
| Pre-tax discount rate | ~10-11% | Reflecting Biopharma sector risk premium |

**Diagnostic CGU — Key Assumptions:**

| Assumption | Value | Sensitivity |
|---|---|---|
| Revenue growth rate (years 1-5) | 5-8% per annum | Blood banking volumes + new CDx product launches |
| EBITDA margin (long-term) | 24-27% | High-margin reagent model sustaining margins |
| Terminal growth rate | 1.5-2.0% | Mature diagnostic market; lower than Biopharma |
| Pre-tax discount rate | ~9-10% | Slightly lower risk than Biopharma (more recurring) |

These assumptions produce recoverable amounts that **exceed carrying amounts for
both CGUs** — hence no impairment in 2025. But the disclosed sensitivity analysis
tells you exactly how fragile that headroom is.

### 5.3 The Sensitivity Analysis — The Most Important Disclosure for Analysts

IAS 36.134(f) requires disclosure of the sensitivity of the impairment test to
reasonably possible changes in key assumptions. This is where Nota 6 becomes
essential reading for credit analysis.

Grifols typically discloses something like the following:

**Diagnostic CGU — Sensitivity (illustrative from Nota 6):**

| Change in Assumption | Impact on Headroom |
|---|---|
| Discount rate +100 basis points | Headroom reduced by ~€400-600M |
| Terminal growth rate -50 bps | Headroom reduced by ~€200-300M |
| EBITDA margin -200 bps | Headroom reduced by ~€350-500M |
| Revenue growth rate -100 bps (years 1-5) | Headroom reduced by ~€300-400M |

**The critical question**: If any single of these sensitivity scenarios eliminates
headroom entirely, that implies the current carrying amount is **at the margin**
of supportability. Nota 6 is explicit about whether a reasonable change in a key
assumption would cause impairment — this is a required disclosure under IAS 36.134(f).

For the Diagnostic CGU: if the headroom is, say, €800M, it can absorb a 100bp
discount rate increase before impairing. But if interest rates spike further, or if
blood banking volumes decline due to substitution by point-of-care alternatives,
the headroom could evaporate.

### 5.4 Why Deloitte Flagged This as a Key Audit Matter

Deloitte's audit report identified the goodwill impairment test as a key audit matter
(KAM) for three reasons:

**(i) The magnitude**: €6,833M of goodwill is the single largest asset on the balance
sheet. A write-down, even partial, would materially affect the financial statements.

**(ii) The subjectivity**: VIU calculations involve multi-year cash flow projections,
discount rates calibrated to market conditions, and terminal growth assumptions —
all of which involve significant management judgment and are inherently uncertain.
Small changes in assumptions produce large changes in recoverable amounts.

**(iii) The economic environment**: Rising interest rates in 2023-2024 increased
discount rates, compressing the present value of future cash flows. The Diagnostic
business faces competitive dynamics from new entrants. These factors create genuine
uncertainty about whether carrying amounts are supportable.

In response, Deloitte challenged management's assumptions, employed its own valuation
specialists to independently assess the discount rates and growth assumptions,
compared Grifols' projections to external market forecasts, and evaluated the
historical accuracy of management's prior-year forecasts. The fact that the audit
concluded without a modified opinion does not mean the test was easy — it means the
headroom was sufficient to withstand scrutiny.

---

## 6. Recognizing and Measuring an Impairment Loss

### 6.1 How the Loss Is Recorded

If recoverable amount < carrying amount, the difference is the **impairment loss**:

**Impairment loss = Carrying Amount − Recoverable Amount**

For an individual asset: recognized immediately in P&L (unless the asset is carried
at a revalued amount under the revaluation model, in which case the loss first
reduces the revaluation surplus in OCI before hitting P&L).

For a CGU: the loss is allocated in a strict waterfall:
1. **First**: Reduce goodwill allocated to the CGU to zero (or to the impairment amount)
2. **Then**: Reduce other assets pro rata based on carrying amounts, subject to the
   constraint that no individual asset is written below the highest of its own
   FVLCD, VIU, or zero

### 6.2 P&L Presentation

IAS 36 does not specify where the impairment loss appears in the income statement.
It will typically appear above the operating profit line (within D&A or as a separate
line — "Deterioro de valor de activos" or similar). For an LBO analyst computing
adjusted EBITDA, goodwill impairment charges are universally excluded as a non-cash,
non-recurring item.

### 6.3 The Asymmetry — No Reversal for Goodwill

IAS 36.124 prohibits the **reversal of goodwill impairment**. Once goodwill is
written down, it stays written down. This is an asymmetric rule — other assets
can be reversed if economic conditions improve (up to the original carrying amount
that would have existed absent impairment), but goodwill cannot.

The rationale: a reversal of goodwill impairment would effectively be recognizing
internally generated goodwill, which is explicitly prohibited by IAS 38. If the
business has recovered, that recovery represents new value creation (internally
generated) rather than the restoration of old acquired value.

**The practical consequence**: A company that has impaired goodwill in a downturn
carries a permanently impaired balance sheet — even if operations recover fully.
Grifols has not recognized goodwill impairment in recent years, which means the
€6,833M balance represents unimpaired carrying amounts that continue to require
annual justification.

---

## 7. The Corporate Assets Problem

### 7.1 What Are Corporate Assets?

Some assets do not generate independent cash flows and cannot be allocated to a
specific CGU. IAS 36 calls these **corporate assets** — examples include the head
office building, central IT infrastructure, and shared R&D facilities.

For Grifols: its Barcelona headquarters, its central plasma fractionation technology
R&D center, and its global IT systems (SAP) serve all segments and cannot be cleanly
attributed to any single CGU.

### 7.2 How to Test Them

IAS 36.102-103 provides guidance: corporate assets are allocated to CGUs on a
reasonable and consistent basis for the purpose of the impairment test. If a
reasonable allocation is possible, the allocated corporate assets are included in
each CGU's carrying amount and the CGU is tested including those allocations.

If a reasonable allocation is not possible, the standard requires a two-step approach:
test the CGU first (without corporate assets), then test the group of CGUs to which
the corporate asset belongs (including the corporate asset) at the highest level
at which management monitors goodwill.

---

## 8. Interaction with IFRS 3 and the "Day Two" Goodwill Problem

### 8.1 The Acquisition-Impairment Loop

There is a structural tension between IFRS 3 (Business Combinations) and IAS 36.
IFRS 3 requires recognizing goodwill at fair value on the acquisition date — typically
a premium over the net fair value of identifiable assets. IAS 36 then requires
testing that goodwill annually.

The irony: in the year of acquisition, the VIU calculation almost always supports
the carrying amount of goodwill — because the price paid reflects the acquirer's
optimistic projections for synergies and growth. The real test comes in years 3-7
post-acquisition, when actual performance can be compared to the projections that
justified the premium.

For Grifols, the Biotest acquisition (2022, ~€2bn) created goodwill that is now
approaching the three-year mark where operational performance divergence becomes
more visible. The integration ("Biotest Next Level") has been ongoing, and whether
the projected synergies are materializing is exactly what the impairment test in
Nota 6 is designed to assess.

### 8.2 When Goodwill Does Get Impaired

Across European IFRS reporters, goodwill impairments cluster around:
- Post-acquisition integration failures (synergies don't materialize)
- Structural disruption to acquired businesses (digital disruption, pricing pressure)
- Macroeconomic shocks (COVID-19 created a wave of impairments in travel, retail,
  hospitality)
- Interest rate spikes (discount rate increases reduce VIU mechanically)

The 2022-2024 interest rate environment was the most challenging for impairment tests
in a decade: every 100bp increase in WACC reduces the present value of a perpetual
cash flow stream by roughly 10-15%. Companies that had priced acquisitions assuming
near-zero discount rates suddenly found their VIU calculations under pressure even
without any change in operating performance.

Grifols' Nota 6 reflects this context: the 2023 and 2024 impairment tests were
conducted under materially higher discount rates than the 2021 test, creating
significant compression in headroom even if the underlying business held up.

---

## 9. The LBO Angle — Impairment Risk in Credit Analysis

### 9.1 Impairment as a Balance Sheet Signal

A goodwill impairment is non-cash — it does not affect EBITDA (in the adjusted
sense), does not affect cash flow, and does not directly trigger debt covenant
violations. However, it matters to credit analysis in several ways:

**Book equity erosion**: A €1bn goodwill write-down reduces equity by €1bn. If the
debt agreement includes financial maintenance covenants referencing tangible net worth
or net assets, an impairment charge could tighten the covenant headroom — even though
the business continues to generate the same cash flow.

**Signal of deterioration**: An impairment charge signals that the economic value of
the acquired business is below what was paid. It does not necessarily mean a breach
is imminent, but it does mean that the narrative underlying the original transaction
(synergies, growth, returns) is not playing out as planned. For holders of Grifols'
subordinated bonds, a goodwill impairment in the Biopharma CGU would be a meaningful
negative signal.

**Equity cure mechanics**: In some LBO structures, equity sponsors can inject cash
to cure a leverage covenant breach (an "equity cure"). After a major impairment,
book equity is reduced, which can affect certain covenant definitions that reference
net assets. This is a second-order effect but matters in distressed restructuring
analysis.

### 9.2 The Diagnostic CGU — The Specific Impairment Risk

From a credit perspective, the Diagnostic CGU deserves the most scrutiny:

- **€2,525M goodwill** on ~€210M EBITDA = ~12x EBITDA goodwill multiple
- The diagnostics sector faces medium-term headwinds: automation compressing margins,
  point-of-care disruption, hospital procurement consolidation
- Comparable company trading multiples for in vitro diagnostics companies have
  compressed from 15-20x EBITDA in 2021 to 10-14x in 2025 as interest rates rose
- If the VIU calculation for the Diagnostic CGU uses a discount rate of 9-10% and
  a terminal growth rate of 1.5-2%, the implied EV/EBITDA multiple that justifies
  the carrying amount is approximately 10-12x — which is at the low end of peer
  market multiples but arguably supportable

The headroom disclosure in Nota 6 is therefore the most important number in the
impairment note. If headroom is, say, €1.5bn above carrying amount, the CGU can
absorb significant business deterioration before impairment triggers. If headroom
is, say, €400M, a 20% decline in business performance would cause a write-down.

### 9.3 EBITDA Sensitivity to Impairment

Goodwill impairment is universally excluded from adjusted EBITDA in bond-covenant
definitions. But analysts should be aware:

- A first impairment charge signals elevated risk, even if it doesn't directly
  affect coverage ratios
- A series of impairment charges across multiple years signals systematic overvaluation
  of the acquisition portfolio
- Post-impairment, reported book ROE and ROCE improve mechanically (same earnings,
  smaller asset base) — don't be misled by "improved" return metrics following a write-down

---

## 10. Required Disclosures

IAS 36.126-137 mandates extensive disclosures. For CGUs containing goodwill
or indefinite-life intangibles (the mandatory annual test), IAS 36.134 requires:

**(a)** The carrying amount of goodwill/intangibles allocated to the CGU

**(b)** The basis on which the CGU's recoverable amount was determined (VIU or FVLCD)

**(c)** If VIU: each key assumption, how values are assigned to those assumptions,
whether projections reflect past experience or external sources, the period over
which management has projected cash flows, the growth rate used to extrapolate
beyond the projection period, and the discount rate applied

**(d)** If FVLCD: the valuation technique used, the key assumptions, and the level
in the fair value hierarchy (IFRS 13)

**(e)** If a **reasonable possible change** in a key assumption would cause the
carrying amount to exceed recoverable amount: the amount by which the recoverable
amount exceeds the carrying amount, the value of the assumption, and the amount by
which the assumption would need to change (individually) for the recoverable amount
to equal the carrying amount

**(f)** For CGUs where recoverable amount exceeds carrying amount by a comfortable
margin with no sensitivity issues: the excess amount (headroom) for each CGU

Grifols' Nota 6 runs to several pages covering all of the above. The sensitivity
disclosures in particular — what would happen if the discount rate increases by 50bp,
or if revenue growth is 1% lower — are the numbers that a credit analyst should
extract and sensitize in the LBO model.

---

## 11. Summary: What to Take Away

IAS 36 is the standard that prevents the balance sheet from becoming a museum of
historical costs disconnected from economic reality. Its key concepts:

- **Recoverable amount**: Higher of FVLCD and VIU — an asset or CGU cannot be
  carried above what it is worth in use or in a sale
- **Annual mandatory test** for goodwill (€6,833M) and indefinite-life intangibles
  (~€320M IPR&D) — no trigger required
- **CGU framework**: Assets tested as groups where cash flows are interdependent;
  Grifols tests at the segment level (Biopharma, Diagnostic)
- **VIU mechanics**: Pre-tax unlevered DCF over 5-year explicit period plus terminal
  value; discount rate reflects asset-specific risk, not Grifols' leveraged WACC
- **Impairment waterfall**: Goodwill absorbs losses first; cannot be reversed once
  written down
- **Deloitte KAM**: The Diagnostic CGU (~€2,525M goodwill, ~12x EBITDA goodwill
  multiple) is the highest-risk testing unit; sensitivity analysis in Nota 6 reveals
  how much headroom exists against reasonable assumption changes
- **LBO relevance**: Non-cash write-downs don't affect EBITDA or cash flow directly,
  but they erode book equity, signal acquisition mispricing, and can interact with
  net worth covenants in complex debt structures

The €6,833M goodwill balance is either the most valuable or the most dangerous item
on Grifols' balance sheet, depending on whether the business performs in line with
the projections management uses to justify it. IAS 36 is the mechanism that forces
that question to be answered every year.

---

*Module 7 complete. Next: Module 8 — IFRS 3 (Business Combinations)*

*Reference: International GAAP 2026, Chapter 20; Grifols S.A. Nota 6 — Fondo de Comercio*
