# Module 8: IFRS 3 — Business Combinations
## IFRS Deep Learning Series | Case Study: Grifols S.A. (FY2025)

---

## 1. Why This Standard Exists

Every major acquisition raises the same accounting question: how do you bring another
company's assets, liabilities, revenues, and profits onto your own financial statements?
Before IFRS 3, companies could choose from multiple methods — the pooling of interests
method simply combined the two companies' historical balance sheets at book value, as
if they had always been combined. This made it possible to acquire companies at massive
premiums without recognizing any goodwill, instantly inflating post-acquisition returns
on equity and distorting comparability across transactions.

IFRS 3 eliminates this discretion. There is now exactly **one method**: the
**acquisition method**. It requires every business combination to be accounted for
from the perspective of the acquiring entity, with all acquired assets and liabilities
recognized at **fair value** at the acquisition date, and any excess of the total
consideration paid over the net fair value of those assets recognized as **goodwill**.

This standard is the origin story for the €6,833M of goodwill on Grifols' balance
sheet. Every euro of that goodwill represents a premium paid above the fair value of
net assets in a past acquisition — Talecris, Novartis Diagnostics, Biotest, and
dozens of smaller plasma center acquisitions. Understanding IFRS 3 means understanding
where that goodwill came from, why it is as large as it is, and what risks it carries.

---

## 2. Scope — What Is a Business Combination?

### 2.1 The Business Definition — The Critical Gateway

IFRS 3 applies only when the transaction involves the acquisition of a **business**,
not merely a group of assets. This distinction matters enormously because:

- If it is a **business combination**: acquire at fair value, recognize goodwill,
  apply IFRS 3 in full
- If it is an **asset acquisition**: allocate cost across individual assets and
  liabilities based on their relative fair values; no goodwill recognized

**IFRS 3 defines a business** as an integrated set of activities and assets capable
of being conducted and managed for the purpose of providing a return in the form of
dividends, lower costs, or other economic benefits. The 2018 amendments introduced
a practical **concentration test**: if substantially all of the fair value of the
gross assets acquired is concentrated in a single identifiable asset or group of
similar assets, it is not a business — it is an asset acquisition.

**In Grifols**: When Grifols acquires a single plasma collection center from a local
operator — a building, some equipment, a lease, and a trained staff — it is acquiring
a business (it has inputs, processes, and produces output: collected plasma). The
acquired center is integrated into Grifols' collection network, and a small amount
of goodwill may be recognized if the price exceeds fair value of net assets.

However, when Grifols has occasionally acquired just real estate assets or standalone
equipment without the associated processes and staff, those are asset acquisitions.
The accounting treatment is fundamentally different.

### 2.2 Transactions Not Covered

IFRS 3 does not apply to:
- Acquisitions of assets that do not constitute a business
- Combinations of entities under common control (e.g., internal restructurings
  within the Grifols group)
- Formation of joint ventures (IFRS 11)
- Acquisitions of investments in associates (IAS 28, with equity method)

---

## 3. The Acquisition Method — Step by Step

IFRS 3.5 specifies that every business combination must be accounted for using
the acquisition method, which involves four steps:

1. **Identify the acquirer**
2. **Determine the acquisition date**
3. **Recognize and measure identifiable assets, liabilities, and NCI**
4. **Recognize and measure goodwill or a bargain purchase gain**

### 3.1 Step 1 — Identify the Acquirer

The acquirer is the entity that obtains control of the acquiree. Control is defined
per IFRS 10 (Consolidated Financial Statements — Module 20): an investor controls
an investee when it is exposed to variable returns and has the ability to affect
those returns through its power over the investee.

In most transactions, identifying the acquirer is straightforward — the entity
paying cash or issuing equity is the acquirer. In reverse acquisitions (where the
smaller entity is legally the acquirer but the larger entity's shareholders end up
with control), the substance overrides the legal form.

**In Grifols**: In the Biotest acquisition (2022), Grifols is unambiguously the
acquirer — it paid cash consideration and obtained 96% of voting rights, giving
it unequivocal control over the combined entity.

### 3.2 Step 2 — Determine the Acquisition Date

The acquisition date is the date on which the acquirer obtains control. This is
generally the date on which the consideration is transferred, unless the parties
agree otherwise in the acquisition agreement. For the Biotest acquisition, this
was **April 2022** — the date on which Grifols received the shares tendered in
the public offer and obtained majority voting control.

The acquisition date is critical because it determines:
- Which assets and liabilities are recognized (those that exist at that date)
- The fair values of those assets and liabilities
- The exchange rate used to translate the consideration (for USD/EUR transactions)
- The date from which the acquiree's results are consolidated

### 3.3 Step 3 — Recognizing and Measuring Identifiable Net Assets

At the acquisition date, the acquirer must recognize **all** of the acquiree's
identifiable assets and liabilities, measured at **fair value** — regardless of
whether the acquiree had previously recognized them.

This produces the purchase price allocation (PPA) — the most judgmentally intensive
exercise in acquisition accounting.

#### The Recognition Criteria

IFRS 3 has specific rules that override the normal recognition criteria in other
IFRS standards:

**Assets**: Recognized if it is probable that future economic benefits will flow to
the acquirer AND the fair value can be measured reliably — but more importantly,
**even if the acquiree did not previously recognize the asset** (as discussed in
Module 6: IAS 38, this is why acquired customer relationships, brands, and IPR&D
appear on the acquirer's balance sheet even though they were never on the acquiree's).

**Contingent liabilities**: Recognized at fair value even if it is **not probable**
that an outflow of economic benefits will be required — provided the fair value
can be measured reliably. This is broader than the IAS 37 recognition criterion for
provisions (which requires probable outflow). In a business combination, even
possible legal claims and environmental obligations get recognized at fair value.

**Assembled workforce**: **Not recognized** as a separate intangible asset (IAS 38
prohibition — it is not separable and does not arise from contractual rights). Its
value is absorbed into goodwill.

#### The Fair Value Exercise — Purchase Price Allocation (PPA)

This is where the numbers get constructed. For the Biotest acquisition, Grifols
(with the help of independent valuers) would have worked through:

| Asset Category | Valuation Approach |
|---|---|
| PP&E (fractionation plant Goch, plasma centers) | Depreciated replacement cost or market approach |
| Customer relationships (blood banks, hospital customers) | Multi-period excess earnings method (MEEM) |
| Fractionation technology and know-how | Relief-from-royalty method |
| Biotest brand and trademarks | Relief-from-royalty method |
| IPR&D: Trimodulin, IgM, Fibrinogen | Risk-adjusted DCF or cost-to-recreate |
| Inventory (plasma, WIP, finished product) | Net realizable value approach |
| Financial liabilities at fair value | Discounted cash flows at current market rates |
| Contingent liabilities (legal claims) | Probability-weighted expected outflows |
| Deferred tax adjustments on above | Tax-effected fair value step-ups |

**The inventory fair value step-up**: This is one of the most consequential PPA items
for P&L impact in the post-acquisition period. Inventory is acquired at fair value
(NRV of finished goods, or NRV minus completion costs for WIP). Because Grifols
would have previously been costing plasma at its own plasma cost-per-liter (CPL),
the acquired Biotest inventory is recorded at a premium. When that inventory is sold
in the quarters following the acquisition, the higher fair value flows through
cost of goods sold — creating a one-time "inventory step-up charge" that suppresses
post-acquisition gross margins. Analysts always add this back in the first 1-2 years
post-acquisition.

**The deferred tax liability on intangibles**: This is another critical PPA adjustment.
When Grifols recognizes €X of customer relationships or technology at fair value in
the PPA, those intangibles have a zero tax base (under German or Spanish tax law,
they were not previously recognized by Biotest for tax purposes). The difference
creates a deferred tax liability: the intangible asset's book value will be
amortized but there is no corresponding tax deduction. IAS 12 requires recognition
of this deferred tax liability — and paradoxically, this increases goodwill because:

> Goodwill = [Consideration + NCI] − [FV of identifiable net assets, net of deferred taxes]

The DTL on acquired intangibles reduces the net assets denominator, which increases
the residual goodwill numerator. This is why you cannot compute goodwill by simply
subtracting a simplistic asset value from the purchase price.

### 3.4 Step 4 — Measuring Goodwill

The goodwill formula:

> **Goodwill = (A + B) − C**
>
> Where:
> - **A** = Fair value of consideration transferred
> - **B** = Fair value (or proportionate NCI share) of non-controlling interest
> - **C** = Fair value of identifiable net assets acquired (assets minus liabilities)

If the result is positive → **goodwill** (the most common outcome)
If the result is negative → **bargain purchase gain** (recognized immediately in P&L)

A bargain purchase is rare — it implies you acquired a business for less than the
sum of its parts. When it occurs, IFRS 3 requires the acquirer to reassess all
measurements before recognizing the gain, because a bargain purchase often reflects
an error in the PPA rather than a true below-market transaction.

---

## 4. Measuring Non-Controlling Interests — The Policy Choice

### 4.1 Two Options

For business combinations where the acquirer does not buy 100% of the acquiree,
IFRS 3 provides a choice of how to measure NCI at the acquisition date:

**Option 1 — Full Goodwill Method (Fair Value)**:
NCI is measured at its fair value. This typically means taking the per-share price
implied by the acquisition consideration and applying it to the NCI percentage of
shares. Goodwill is recognized for the full business (acquirer's share + NCI's
share) — hence "full goodwill."

**Option 2 — Proportionate Method (Partial Goodwill)**:
NCI is measured at its proportionate share of the acquiree's **identifiable net
assets** (not total enterprise fair value). Goodwill is recognized only for the
acquirer's share — the NCI receives no goodwill allocation.

The choice can be made on a transaction-by-transaction basis.

### 4.2 Consequences of Each Method

| Feature | Full Goodwill | Proportionate |
|---|---|---|
| NCI balance at acquisition | Higher (includes NCI goodwill) | Lower (no NCI goodwill) |
| Goodwill recognized | Higher (full enterprise) | Lower (acquirer's share only) |
| Future impairment testing | More conservative (larger pool to test) | Less conservative (smaller pool) |
| P&L impact of impairment | Larger potential write-down | Smaller |
| Balance sheet leverage | Assets and equity both higher | Both lower |

### 4.3 The Biotest Case — A Structurally Complex NCI

Biotest's capital structure at acquisition was unusual: **96% of voting rights but
only 70% of share capital**. This split arises from Biotest's dual share structure:

- **Biotest ordinary shares (voting)**: Grifols acquired ~96% of the voting shares,
  giving it control
- **Biotest preference shares (non-voting)**: The preference shares carry economic
  rights (dividends, liquidation preference) but no votes. The preference shareholders
  — who remained as NCI after the acquisition — hold approximately 30% of the
  economic interest

This structure has significant consequences:
- Grifols consolidates Biotest 100% (it controls via voting rights)
- But ~30% of Biotest's net assets and earnings belong to preference shareholders (NCI)
- The €2,332M NCI balance on Grifols' consolidated balance sheet is dominated by
  this Biotest preference share NCI

The NCI's size relative to Grifols' own equity is notable: €2,332M of NCI out of
total equity of approximately €6.8bn means that roughly 34% of the consolidated
equity value belongs to minority holders. For credit analysis, this is a crucial
distinction — that €2,332M of equity does not absorb losses on Grifols' debt in the
same way as the parent equity.

---

## 5. Grifols' Acquisition History — PPA in Practice

### 5.1 Talecris (2011) — The Transformational Deal

The 2011 acquisition of Talecris Biotherapeutics for approximately **€3.4bn** was
the transaction that made Grifols the world's third-largest plasma fractionator.

**The economics of the PPA:**
Talecris had been built through the carve-out of Bayer Biological Products' US plasma
business, then significantly expanded. By 2011, it had:
- The Gamunex immunoglobulin franchise (a top-3 IVIG brand in the US)
- A network of plasma collection centers
- A large fractionation facility in Clayton, NC

The PPA allocated approximately:
- ~€800-1,000M to customer relationships (US hospital and specialty pharmacy accounts)
- ~€500-700M to product licenses and technology (Gamunex, fractionation IP)
- ~€200-300M to PP&E step-up
- Remainder (>€1,500M) to goodwill

Fourteen years later, most of the Talecris customer relationship and technology
intangibles have been fully amortized (useful lives of 10-15 years). The only
permanent legacy is the goodwill — and the North Carolina fractionation plant, now
a cornerstone of Grifols' US manufacturing.

**The leverage consequence**: Grifols financed the Talecris acquisition largely with
debt, taking leverage from comfortable levels to approximately 5x. The subsequent
years were spent deleveraging — until the Biotest acquisition reversed that progress
in 2022.

### 5.2 Novartis Diagnostics (2014) — Building the Diagnostic Division

Grifols acquired the Novartis Diagnostics division (subsequently rebranded as Grifols
Diagnostic Solutions, or GDS) for approximately **€1.7bn**. This deal created the
Diagnostic segment by bringing:
- The DG Gel blood typing technology (dominant global position)
- NAT (nucleic acid testing) platforms for blood screening
- Customer relationships with blood banks and hospital transfusion services globally

The PPA recognized substantial intangible assets:
- Customer relationships with blood banks: long-duration, contract-based relationships
- The DG Gel technology platform: proprietary blood typing gel card technology
- Regulatory approvals across markets

Much of this PPA has also amortized significantly. The remaining Diagnostic intangibles
(in Nota 7) represent the combination of this acquisition plus subsequent additions.

### 5.3 Biotest (2022) — The Most Recent Major Transaction

The acquisition of Biotest AG for approximately **€2bn** in April 2022 is the most
recently concluded major business combination, and therefore the one where the PPA
methodology and results are most visible in the current accounts.

**Transaction structure:**
- Grifols launched a voluntary public takeover offer for all Biotest ordinary shares
  at €43 per share
- Biotest preference shares were not part of the initial offer — Grifols was obligated
  under German tender offer law to eventually offer to acquire them too (Conditional
  Obligatory Offer / COO)
- Post-offer: Grifols holds ~96% of voting ordinary shares, ~70% of total economic
  interest
- Biotest remains listed on the Frankfurt Stock Exchange (preference shares trade)

**Why 70% economic / 96% voting**: Biotest's preference shares outnumber ordinary
shares significantly. Grifols acquired essentially all ordinary shares (the voting
class) but left the preference shares (non-voting economic class) in public hands.
This gave Grifols full operational control (96% vote) at a lower cash outlay than
acquiring 100% of all share classes.

**The PPA for Biotest:**

| Identified Asset/Liability | Fair Value at Acquisition (Approx.) |
|---|---|
| PP&E (Goch fractionation plant, Haema/BPC plasma centers) | ~€600-800M |
| IPR&D: Trimodulin (sepsis IgM) | ~€150-200M |
| IPR&D: Fibrinogen concentrate | ~€80-120M |
| IPR&D: IgM for neurology | ~€50-80M |
| Customer relationships (Biotest blood group serology) | ~€100-150M |
| Technology and know-how | ~€80-120M |
| Inventory at fair value (step-up) | ~€50-80M |
| Financial liabilities at fair value | (~€200-300M) |
| Contingent liabilities | (~€30-50M) |
| Deferred tax liabilities (on intangible step-ups) | (~€120-180M) |
| **Net identifiable assets at fair value** | **~€600-800M** |
| **Consideration + NCI fair value** | **~€2,000-2,200M** |
| **Goodwill** | **~€1,200-1,600M** |

The Biotest goodwill represents Grifols' premium for:
- The strategic value of securing European fractionation capacity
- Expected cost synergies (shared plasma procurement, combined manufacturing overhead)
- The option value of the Biotest pipeline (even after allocating specific values
  to the IPR&D assets, there is residual value in the combined R&D infrastructure)
- The assembled Biotest scientific and regulatory workforce (not separately recognizable
  under IAS 38)

**The Conditional Obligatory Offer (COO) as contingent consideration**: Under German
law, Grifols is required to make a subsequent offer to preference shareholders under
certain conditions. IFRS 3 requires contingent consideration to be recognized at fair
value at the acquisition date. Depending on the probability-weighted valuation of
the COO obligation, Grifols may have included an estimate of future preference share
acquisition cost as part of the consideration transferred — increasing the goodwill
recognized.

**The inventory step-up**: In the quarters immediately following the April 2022
acquisition, Grifols' Biopharma cost of goods sold included the Biotest inventory
fair value step-up flowing through as sold — a one-time earnings headwind that
suppressed margins in H2 2022 and early 2023. Analysts excluded this from adjusted
EBITDA, correctly treating it as a purchase accounting artifact rather than an
ongoing cost.

---

## 6. The Measurement Period

### 6.1 Provisional Values and the 12-Month Window

A full PPA takes time. Independent valuers need access to the acquiree's records,
management projections, customer contracts, and regulatory files. IFRS 3.45 addresses
this by permitting **provisional values** to be used in the initial post-acquisition
financial statements, subject to retrospective adjustment within the **measurement
period** — a maximum of **12 months** from the acquisition date.

During the measurement period, any additional information obtained about facts and
circumstances that existed at the acquisition date can be used to adjust the
provisional values retrospectively — as if the correct values had been recognized
from day one. The comparative period is restated accordingly.

After the measurement period closes, changes to PPA values are recognized
prospectively in the current period's P&L — not as PPA adjustments.

### 6.2 In Grifols: Biotest PPA Finalization

For the Biotest acquisition (April 2022), the measurement period closed in April 2023.
The 2022 accounts presented provisional values; the 2023 accounts finalized them.
Retrospective adjustments to provisional Biotest PPA values would have been shown
as restatements of the 2022 comparative balance sheet — with corresponding adjustments
to goodwill (the residual absorber of PPA changes).

---

## 7. Subsequent Accounting — After the Acquisition Date

### 7.1 Integration into Consolidated Statements

From the acquisition date, the acquiree's results are consolidated 100% into Grifols'
statements, with the NCI's share of profit/loss presented separately at the bottom
of the income statement and as a component of equity on the balance sheet.

### 7.2 Acquisition-Related Costs

Under IFRS 3, **acquisition-related costs are expensed as incurred**. Legal fees,
due diligence costs, investment banking advisory fees, and integration consultants are
all P&L items — they cannot be capitalized as part of the cost of the acquisition.

For a transaction the size of Biotest (~€2bn), acquisition costs (M&A advisory,
legal, accounting) could run to €50-100M+. These appear in the P&L in the year of
acquisition, suppressing reported operating profit. Again, adjusted EBITDA excludes
these as non-recurring.

### 7.3 Subsequent Acquisition of NCI — Not IFRS 3

When an acquirer that already controls an entity subsequently acquires additional
shares from NCI shareholders (increasing from, say, 70% to 85%), this is **not a
new business combination**. Control was already established; the subsequent purchase
is a transaction between equity holders.

Under IFRS 10, subsequent acquisitions of NCI are accounted for entirely within
equity — the consideration paid reduces equity, NCI decreases, and **no goodwill is
recognized** and **no gain/loss goes through P&L**. The difference between
consideration paid and the book value of NCI eliminated is recognized directly in
retained earnings (or a separate equity component).

**In Grifols 2025**: The €129M NCI acquisition shown in the financing section of
the cash flow statement (Module 3) represents Grifols buying additional preference
shares or minority interests from NCI holders. Under IFRS 10, this reduces NCI on
the balance sheet and reduces equity attributable to the parent — without any
goodwill or P&L effect. The financing classification in the cash flow statement
(not investing) correctly reflects that this is a transaction between equity holders,
not an asset acquisition.

---

## 8. Step Acquisitions — Obtaining Control in Stages

### 8.1 The Accounting Treatment

If an entity previously held a non-controlling equity interest (accounted for under
IFRS 9 or the equity method under IAS 28) and then acquires additional shares to
obtain control, IFRS 3 treats this as a single acquisition at the step-acquisition date:

- The previously held interest is **remeasured to fair value** at the date control
  is obtained
- The remeasurement gain or loss goes through P&L
- Goodwill is then calculated as: [FV of consideration for new stake + FV of
  previously held interest + FV of NCI] minus [FV of net assets]

This remeasurement gain/loss can be significant. When Grifols increased its stake
in Haema (the German plasma collection company that was part of the Biotest group)
from a minority position to control, any previously held Haema investment would have
been remeasured to fair value at the control date.

---

## 9. The Haema/BPC Controversy — IFRS 3 in Dispute

### 9.1 The Gotham City Allegation

The 2024 Gotham City Research report alleged, among other things, that Grifols'
consolidation of certain entities — particularly BPC (Biotest Plasma Center) and
Haema — was inappropriate, and that EBITDA attributed to these entities was being
counted in Grifols' group EBITDA while the cash flows were not freely accessible
to service group debt.

The heart of the allegation: if BPC and Haema are controlled by both Grifols and
Scranton Enterprises (the Grifols family vehicle), consolidating their full EBITDA
into the Grifols group without appropriate NCI adjustment artificially inflates the
group's leverage numerator (EBITDA) while the associated cash flows flow
disproportionately to the NCI holders.

### 9.2 The IFRS 3/IFRS 10 Framework Response

Under IFRS 10, consolidation requires **control** — the power to affect variable
returns. If Grifols has control of BPC and Haema, it must consolidate them. The
NCI's share of their earnings is disclosed separately (reducing reported net income
attributable to owners of the parent) — but in an EBITDA metric that excludes NCI
adjustments (as most credit agreement definitions do), the NCI earnings become
invisible.

This is a genuine structural issue in IFRS: EBITDA is a consolidated measure that
includes 100% of the controlled entity's performance, but the cash that actually
flows to service debt (free cash flow to Grifols parent) is net of what must be
passed to NCI holders. For covenant compliance purposes, many credit agreements
use EBITDA without NCI adjustment — which can overstate true cash generation
available to bondholders when NCI is large.

**Deloitte's position**: The audit opinion confirmed that the consolidation was
appropriate under IFRS. The entities meet the control criteria. The disclosures
of NCI are compliant with IFRS 12. The controversy was more about whether the
economic substance aligned with the legal form of control — a question that falls
at the intersection of IFRS 10, IFRS 3, and political/governance considerations
beyond the accounting standards themselves.

---

## 10. Disclosures — Where the Acquisition Story Is Told

IFRS 3.59-63 requires extensive disclosures for material business combinations.
The objective is to enable users to evaluate the financial effects of acquisitions
during the current and prior periods.

**Required disclosures include:**

**(a)** Name and description of the acquiree

**(b)** Acquisition date

**(c)** Percentage of voting equity interest acquired

**(d)** Primary reasons for the combination and a description of how the acquirer
obtained control

**(e)** Qualitative description of the factors that make up the goodwill recognized
(expected synergies, assembled workforce, etc.)

**(f)** Fair value of total consideration transferred (broken down by type: cash,
equity instruments, contingent consideration, etc.)

**(g)** Fair value of NCI at the acquisition date and the measurement basis used
(fair value or proportionate)

**(h)** For contingent consideration: the amount recognized, a description of the
arrangement, and a range of potential payment outcomes

**(i)** Amounts recognized at acquisition date for each major class of assets
and liabilities

**(j)** Revenue and profit/loss of the acquiree since the acquisition date and
on a full-year pro-forma basis (as if acquired at the start of the reporting period)

The pro-forma disclosure **(j)** is particularly valuable for analysts modeling the
first full year of consolidation — it shows what the combined entity would have
looked like if the acquisition had been completed at 1 January rather than April.
For the Biotest deal, this disclosure allowed analysts to estimate the full-year
contribution of Biotest to Grifols' 2022 P&L, avoiding distortion from the
nine-month consolidation period.

---

## 11. The LBO Angle — Business Combinations in Credit Analysis

### 11.1 The Goodwill Creation Machine

Every major acquisition creates goodwill — the permanent balance sheet residual
of paying a control premium. In an LBO context, the leveraged acquisition itself
creates goodwill: if a PE sponsor buys Grifols at, say, 8x EBITDA (€13.5bn
enterprise value) and the fair value of net assets is €10bn, the LBO creates
€3.5bn of new goodwill. That goodwill requires annual impairment testing under
the new owner (IAS 36 — Module 7).

This is why heavily acquisitive leveraged companies can have goodwill representing
60-70% of their enterprise value: they are carrying not just one transaction's
premium but the accumulated premiums of all acquisitions, net of impairments
charged over the years.

### 11.2 PPA as an Earnings Management Tool

The allocation between finite-life intangibles (which amortize) and goodwill
(which doesn't) directly affects reported earnings. A company that aggressively
allocates to finite-life intangibles will have higher near-term amortization
charges (suppressing reported earnings) but lower impairment cliff risk. A company
that allocates more to goodwill avoids near-term amortization but carries a larger
time bomb of potential impairment.

As an analyst, you should review the PPA methodology in Nota 3 of the accounts
for each material acquisition: compare the useful lives assigned to intangibles,
the discount rates used in MEEM valuations, and the relative size of goodwill
versus identifiable intangibles. These choices tell you something about how
aggressive or conservative management is in structuring acquisition accounting.

### 11.3 Acquisition-Related Costs as Adjustments

Investment banking fees, due diligence costs, and integration consultants are all
one-time, non-cash (or cash-but-non-recurring) items. They are universally excluded
from adjusted EBITDA. However, in years of significant M&A activity, these can be
material. Grifols' 2022 P&L included significant Biotest acquisition costs — all
of which were excluded from the adjusted EBITDA figure used in leverage covenant
calculations.

### 11.4 Contingent Consideration — An Underappreciated Liability

Contingent consideration (earnouts, performance ratchets, conditional obligatory
offers) is recognized at fair value at the acquisition date. Subsequent changes
in fair value (as the probability of meeting conditions changes) flow through P&L
under IFRS 9 — they are not adjusted through goodwill.

For Grifols' COO for Biotest preference shares: if the probability of being required
to make the offer increases (e.g., Grifols reaches a squeeze-out threshold that
triggers mandatory acquisition under German law), the fair value of the contingent
consideration increases — with the change going through financial expense in the P&L.
This is a non-cash P&L item that should be separately tracked.

---

## 12. Summary: What to Take Away

IFRS 3 is the standard that creates goodwill and sets the rules for every major
transaction that has shaped Grifols into what it is today:

- **The acquisition method is mandatory**: No pooling, no exceptions; all acquired
  assets and liabilities recognized at fair value at the acquisition date
- **PPA is the most consequential exercise**: The allocation of purchase price across
  identifiable intangibles (finite-life, will amortize) and goodwill (no amortization,
  requires annual impairment test) shapes the P&L profile for decades
- **NCI measurement choice**: Full goodwill (NCI at fair value — larger goodwill) vs
  proportionate (NCI at net assets — smaller goodwill); Grifols has a €2,332M NCI
  driven by the Biotest preference share structure
- **Acquisition costs are expensed**: Advisory fees and due diligence costs hit the
  P&L immediately; always excluded from adjusted EBITDA
- **Subsequent NCI purchases are equity transactions**: No new goodwill; the difference
  between cost and book value of NCI goes directly to retained earnings
- **The Biotest deal** (April 2022, ~€2bn) created €1,200-1,600M of goodwill, added
  significant IPR&D (indefinite-life, no amortization), and resulted in a NCI
  structure (70% economic / 96% voting) that inflates consolidated EBITDA while some
  of the underlying cash flows are attributable to preference shareholders

The goodwill on Grifols' balance sheet is not a mysterious accounting construct —
it is the ledger of premiums paid over four decades of building a global plasma empire.
IAS 36 (Module 7) is what keeps that ledger honest.

---

*Module 8 complete. Next: Module 9 — IAS 2 (Inventories)*

*Reference: International GAAP 2026, Chapter 9; Grifols S.A. Nota 3 — Combinaciones de Negocios*
