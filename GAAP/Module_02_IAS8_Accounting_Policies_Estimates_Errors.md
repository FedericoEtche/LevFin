# Module 2: IAS 8 — Accounting Policies, Changes in Accounting Estimates and Errors
## IFRS Deep Learning Series | Case Study: Grifols S.A. (FY2025)

---

## 1. Why This Standard Exists

Financial statements are only useful if users can trust that numbers are comparable
across periods and across companies. IAS 8 exists to enforce that trust by answering
three questions:

- **How should an entity select and apply its accounting policies?**
- **What happens when something changes?** (a policy choice, an estimate, or the
  discovery of an error)
- **How should each type of change be reflected in the financial statements?**

The reason this matters so much is that the treatment is fundamentally different
depending on whether something is a change in policy, a change in estimate, or a
correction of an error. Getting the classification wrong means the financial statements
are misstated — either by distorting current-period profit or by failing to restate
prior periods when they should have been restated.

---

## 2. The Three Concepts — And Why the Distinction Matters

IAS 8 deals with three distinct concepts, each with its own accounting treatment:

| Concept | Definition | How It's Treated |
|---|---|---|
| **Accounting policy** | The specific principles, bases, conventions, rules and practices applied by an entity | Changes applied **retrospectively** (restate prior periods) |
| **Accounting estimate** | Monetary amounts subject to measurement uncertainty | Changes applied **prospectively** (current + future periods only) |
| **Prior period error** | Omissions or misstatements from failure to use reliable available information | Corrected **retrospectively** (restate prior periods) |

The key mental model:

- Policy change = "We've decided to measure/present this differently going forward,
  and we need to make the past look like we always did it this way."
- Estimate change = "We had an estimate, new information arrived, we've updated it.
  No need to rewrite history — the old estimate was reasonable at the time."
- Error = "We got it wrong. The information was available but we missed it or
  misused it. History needs to be corrected."

---

## 3. Accounting Policies in Detail

### 3.1 What Is an Accounting Policy?

An accounting policy is not just a vague principle — it is a **specific, concrete choice**
about how to recognize, measure, present, or disclose a particular type of transaction.

Examples of accounting policies in Grifols:

- **Inventories**: Measured at the lower of cost and net realizable value, with cost
  determined using weighted average cost (this is a policy choice — FIFO would be
  an alternative)
- **PP&E**: Measured using the cost model (policy choice — the revaluation model
  under IAS 16 would be an alternative)
- **Revenue recognition**: Net revenue recognized at the point in time when control
  transfers to the customer (as opposed to over time)
- **Goodwill**: Not amortized, tested annually for impairment at the CGU level
  (this is not a choice — IFRS requires this treatment)
- **Leases**: Right-of-use assets measured at cost; incremental borrowing rate used
  when the implicit rate is not determinable

### 3.2 How Policies Are Selected

IAS 8 establishes a hierarchy for selecting accounting policies:

**Step 1**: If an IFRS standard specifically covers the transaction, apply that standard
(and consider its implementation guidance).

**Step 2**: If no IFRS standard specifically applies, management must use judgment to
develop a policy that produces information that is both relevant and reliable. In doing
so, management must refer to (in descending order):
  - (a) Requirements in IFRS standards dealing with **similar and related** issues
  - (b) The definitions and concepts in the IASB's **Conceptual Framework**

**Step 3**: Management may also consider (but is not required to):
  - Pronouncements of other standard-setters (e.g., US GAAP)
  - Other accounting literature
  - Accepted industry practices

This hierarchy matters in practice. When Grifols encounters a transaction that no IFRS
standard directly addresses, it cannot simply invent a treatment — it must look to
analogous standards first, then the Conceptual Framework, before turning to other
sources.

### 3.3 Changes in Accounting Policies

An entity may only change an accounting policy if:

**(a)** The change is **required by a new or amended IFRS standard**, or

**(b)** The change results in financial statements providing **more relevant and reliable**
information (a voluntary change)

**Treatment: Retrospective application.** You restate comparative periods as if the new
policy had always been applied. The cumulative effect of the change for periods before
those presented is adjusted against opening retained earnings (or another equity
component) of the earliest comparative period.

**Exception**: When a new IFRS standard provides specific transitional provisions,
those provisions override the general retrospective approach. This is common — for
example, IFRS 16 (Leases) offered a modified retrospective approach that allowed
entities to avoid fully restating comparatives.

**The impracticability exception**: If it is genuinely impracticable to determine the
cumulative or period-specific effects of a retrospective change (e.g., the data was
never collected), the entity applies the new policy from the earliest date practicable.

### 3.4 In Grifols: Accounting Policy Changes and New Standards

Grifols' Nota 2 discloses the following regarding standards applied for the first time
in 2025:

> The application of new standards and interpretations has not had significant impacts
> on these consolidated annual accounts.

This is the typical outcome — most years, the new standards effective are minor
amendments. The important section is where Grifols flags **future standards not yet
effective**, particularly:

| Standard | Effective Date | Impact |
|---|---|---|
| IFRS 9/IFRS 7 amendments (financial instruments classification) | 1 January 2026 | Under assessment |
| IFRS 18 (Presentation and Disclosure — replacing IAS 1) | 1 January 2027 | Will significantly change P&L structure |
| IAS 21 amendments (hyperinflationary translation) | 1 January 2027 | Under assessment |

Grifols specifically calls out IFRS 18 as particularly significant because it will:
- Define a structured income statement with five categories (operating, investing,
  financing, tax, discontinued)
- Require defined subtotals including operating profit
- Mandate disclosure of management-defined performance measures (like adjusted EBITDA)

For an analyst, this "future standards" disclosure is valuable intelligence — it tells
you how the financial statements will change in coming years and what new information
will become available.

---

## 4. Accounting Estimates in Detail

### 4.1 What Is an Accounting Estimate?

An accounting estimate is a monetary amount in the financial statements that is
**subject to measurement uncertainty**. The accounting *policy* sets the objective
(e.g., "measure inventory at the lower of cost and NRV"), while the *estimate*
is the actual number produced when applying that policy under uncertainty
(e.g., "NRV of this batch of albumin is €X per unit").

IAS 8 clarifies that developing an estimate involves using **judgments or assumptions
based on the latest available, reliable information**. The use of estimates does not
undermine the reliability of financial statements — it is a necessary and normal part
of financial reporting.

### 4.2 Examples of Estimates

The standard lists several common estimates:

- Loss allowances for expected credit losses
- Net realizable value of inventories
- Fair value of assets or liabilities
- Depreciation expense (useful lives, residual values, depreciation pattern)
- Provisions for warranty obligations

### 4.3 Grifols' Key Estimates — This Is Where It Gets Rich

Grifols' Nota 2.a provides an unusually detailed and transparent disclosure of its
key estimates and judgments. This is exactly where a sophisticated reader focuses,
because **estimates are where management has the most discretion over the numbers**.

**Estimate 1: Useful lives of tangible and intangible assets**

Grifols must estimate how long its fractionation plants, purification equipment,
patents, and customer relationships will generate economic benefits. Factors
considered include technological evolution, commercial life cycles of pharmaceutical
products, regulatory changes, and physical wear. A change in estimated useful life
is a change in estimate under IAS 8 — treated prospectively, affecting depreciation/
amortization from the change date forward. It does NOT require restating prior periods.

**Estimate 2: Recoverable amount of goodwill and CGUs**

This is the biggest estimate in Grifols' accounts. €6,833M of goodwill must be
tested annually for impairment. The test requires projecting future cash flows,
selecting discount rates, and estimating terminal growth rates. The Diagnostic CGU
alone carries €2,525M of goodwill, and the audit report flagged this as a "key audit
matter" because small changes in assumptions could materially affect the result.

Key assumptions disclosed in Nota 6:
- Revenue growth rates for MDS, BTS, and CDx business lines
- EBITDA margins by segment
- Discount rates reflecting business risk
- Terminal growth rates

If next year Grifols changes its discount rate assumption from 9% to 10%, that is a
change in estimate — applied prospectively. It might trigger an impairment charge
in the current year, but prior years' financial statements are not restated.

**Estimate 3: Fair values in business combinations**

When Grifols acquires a company (like Biotest), it must estimate the fair value of
all identifiable assets and liabilities. This involves projecting cash flows from
acquired product portfolios, estimating the probability of success for in-development
drugs, selecting discount rates, and determining the useful lives of acquired
intangibles. These estimates directly determine the amount of goodwill recognized.

**Estimate 4: Revenue deductions (gross-to-net)**

Grifols' gross revenue is €10,603M, but net revenue is €7,524M — a difference of
€3,079M in chargebacks, discounts, and rebates. Estimating these deductions,
particularly US government program rebates (Medicare/Medicaid: €182M) and
chargebacks (€2,524M), requires significant judgment about future claims rates
and contract terms. These are estimates that are revised each period as actual
claims data becomes available.

**Estimate 5: Deferred tax assets**

The €416M net deferred tax asset requires management to estimate that future
taxable profits will be sufficient to absorb the deductible temporary differences.
If the profit forecast changes, the DTA may need to be written down — a prospective
change in estimate.

**Estimate 6: Provisions and contingencies**

Nota 18 discloses €154M of provisions. Estimating the amount and timing of these
outflows (legal claims, restructuring costs, environmental obligations) involves
significant judgment.

### 4.4 Changes in Estimates — The Treatment

Changes in accounting estimates are recognized **prospectively**:

- If the change affects only the **current period**: recognized entirely in the
  current period's P&L (e.g., a revised estimate of a provision)
- If the change affects the **current and future periods**: recognized over both
  (e.g., a change in useful life of an asset changes depreciation from now on)

**Prior periods are never restated for changes in estimates.**

This is the critical difference from policy changes and errors. The logic is sound:
the old estimate was the best available at the time, so the prior financial statements
were correct given the information available then. The change reflects new information,
not a mistake.

### 4.5 The Gray Zone: Policy vs Estimate

Sometimes the distinction is unclear. IAS 8 provides a pragmatic rule: **when it is
difficult to distinguish a change in policy from a change in estimate, treat it as a
change in estimate** (i.e., prospective treatment). This default protects against
unnecessary restatements.

The 2021 amendments to IAS 8 introduced a clearer framework:
- A **change in measurement technique** is a change in estimate (unless it results
  from correcting an error)
- A **change in measurement basis** is a change in accounting policy

Example: If Grifols switches from using one DCF model to another for its goodwill
impairment test, that is a change in measurement technique (estimate). But if Grifols
switched from historical cost to fair value for measuring PP&E, that would be a change
in measurement basis (policy).

---

## 5. Prior Period Errors

### 5.1 Definition

A prior period error is an omission or misstatement in financial statements for one
or more prior periods arising from a failure to use, or misuse of, reliable information
that:

**(a)** Was available when those financial statements were authorized for issue, AND

**(b)** Could reasonably be expected to have been obtained and used

Errors include mathematical mistakes, mistakes in applying accounting policies,
oversights, misinterpretations of facts, and fraud.

**Critical distinction from estimates**: If management made a reasonable estimate at
the time based on available information, and that estimate later proves incorrect
because new information emerges, that is NOT an error — it is a change in estimate.
An error exists only when the information was available at the time but was not used
or was misused.

### 5.2 Treatment: Retrospective Restatement

Material prior period errors are corrected by:

- Restating comparative amounts for the period(s) in which the error occurred, OR
- If the error occurred before the earliest period presented, restating the opening
  balances of assets, liabilities, and equity for that earliest period

The correction is EXCLUDED from the current period's profit or loss. This is important:
finding a €50M error from 2023 does not reduce 2025 profit by €50M. Instead, the
2023 comparatives are restated, and opening retained earnings for 2024 are adjusted.

### 5.3 In Grifols: The Restatement Footnote

The 2023 figures in Grifols' P&L, OCI, cash flow statement, and changes in equity
are marked with an asterisk: *"Cifras reexpresadas (Nota 2.d)"* — restated figures.

The equity statement shows the specific adjustments:

| Item | Amount (€M) |
|---|---|
| Adjustment to reserves at 31 Dec 2022 | (23) |
| Adjustment to reserves at 31 Dec 2023 | (17) |

These adjustments reduced reserves (and therefore equity) by €23M as at end-2022
and a further €17M as at end-2023. The fact that they adjusted opening equity of
prior periods confirms this was treated as an **error correction** under IAS 8.42,
not as a change in estimate or policy.

This is IAS 8 working exactly as designed: the prior period financial statements
contained a misstatement, reliable information existed at the time but was not
correctly applied, and the correction was made by restating comparatives rather
than running it through the current year P&L.

### 5.4 Required Disclosures for Errors

IAS 8 requires disclosure of:
- The nature of the error
- The amount of the correction for each prior period presented
- The amount of the correction at the beginning of the earliest prior period
- If retrospective restatement is impracticable, an explanation

### 5.5 Immaterial Errors Made Intentionally

A subtle but important point: IAS 8 states that financial statements do not comply
with IFRS if they contain errors that are either **(a) material**, or **(b) immaterial
but made intentionally** to achieve a particular presentation.

This means that deliberate manipulation of numbers, even if each individual amount
is immaterial, constitutes non-compliance with IFRS. This is the standard's anti-
manipulation provision — you cannot "manage" earnings through a series of small,
intentional misstatements.

---

## 6. Disclosure Requirements

### 6.1 Accounting Policies

IAS 1 (as amended) requires entities to disclose **material accounting policy
information** rather than just "significant" policies. This 2023 amendment was
designed to reduce boilerplate disclosures and focus on entity-specific information.

Grifols' Nota 4 spans many pages and covers policies on consolidation, business
combinations, foreign currency, revenue recognition, financial instruments, PP&E,
intangibles, impairment, inventories, leases, provisions, employee benefits, and
taxes. It is a rich source because Grifols operates in a complex, multi-jurisdictional
environment with specialized activities.

### 6.2 Estimation Uncertainty

IAS 1.125 requires disclosure of information about the **assumptions concerning the
future**, and other major sources of estimation uncertainty, that have a significant
risk of resulting in a material adjustment to the carrying amounts of assets and
liabilities within the next financial year.

For those assets and liabilities, the entity must disclose their nature and carrying
amount. Grifols' Nota 2.a fulfills this by detailing six categories of critical
estimates (as discussed in section 4.3 above), each with the specific factors that
create uncertainty and the carrying amounts at risk.

### 6.3 Changes in Estimates

When a change in estimate has a material effect on the current period or is expected
to have a material effect in future periods, IAS 8 requires disclosure of:
- The nature of the change
- The amount of the change (or a statement that the amount is impracticable to
  estimate)

---

## 7. The Practical Importance for Financial Modeling

Understanding IAS 8 is essential for financial modeling because:

**1. Spotting restatements.** When you see restated comparatives (like Grifols' 2023
figures), you need to understand whether it's a policy change, an error, or a
reclassification. Each has different implications for your confidence in the numbers
and your forecasts. An error correction might signal weak internal controls. A policy
change might signal management trying to improve transparency — or trying to present
a more favorable picture.

**2. Understanding estimate sensitivity.** The estimates disclosed in Nota 2.a are
the exact points where management has discretion. When you build an LBO model, you
should stress-test these same assumptions: What if the discount rate for the
impairment test goes up 100bp? What if plasma pricing pressure compresses gross
margins? What if the tax rate normalization doesn't happen as expected?

**3. Detecting earnings management.** Changes in estimates flow through the P&L
prospectively. If Grifols extends the useful life of its fractionation plants from
15 years to 20 years, depreciation drops immediately — boosting profit without any
change in operations. This is a legitimate accounting treatment under IAS 8, but a
sharp analyst notices it and adjusts accordingly.

**4. Reading the future standards note.** Grifols' disclosure about IFRS 18 (effective
2027) tells you that the income statement structure will change materially. If you're
building a 5-year model, the P&L format in years 3-5 will look different from years
1-2. The disclosure also mentions IFRS 9/IFRS 7 amendments on financial instruments
classification, which could affect how Grifols' debt is presented.

---

## 8. Summary: What to Take Away

| Concept | Treatment | Restates Prior Periods? | Grifols Example |
|---|---|---|---|
| **Accounting policy** | Retrospective | Yes | Future IFRS 18 adoption in 2027 |
| **Accounting estimate** | Prospective | No | Goodwill impairment assumptions, useful lives, GTN deductions |
| **Prior period error** | Retrospective restatement | Yes | 2022/2023 restatement (€23M/€17M equity adjustments) |

The hierarchy for selecting policies matters: IFRS first, then analogous standards,
then the Conceptual Framework, then other sources. You cannot cherry-pick.

The distinction between policies and estimates has real consequences: getting it wrong
means either inappropriately restating history or inappropriately failing to do so.

When in doubt, IAS 8 defaults to estimate treatment (prospective) — the standard
prefers not to rewrite history unless clearly necessary.

---

*Module 2 complete. Next: Module 3 — IAS 7 (Statement of Cash Flows)*

*Reference: International GAAP 2026, Chapter 3 sections 4.2-4.7; Grifols S.A. Notas 2 and 4*
