# Module 3: IAS 7 — Statement of Cash Flows
## IFRS Deep Learning Series | Case Study: Grifols S.A. (FY2025)

---

## 1. Why This Standard Exists

The income statement tells you whether a company is profitable. The balance sheet
tells you what it owns and owes at a point in time. But neither tells you the most
fundamental question: **where did the cash come from, and where did it go?**

A company can report healthy profits while bleeding cash (if customers don't pay, or
if working capital is expanding). Conversely, a company can report losses while
generating strong cash (if depreciation charges are large but capex is low). The
statement of cash flows strips away all accrual accounting judgments and shows the
raw reality of cash movements.

IAS 7 exists because cash flow information serves purposes that neither the income
statement nor balance sheet can serve alone:

- **Liquidity assessment**: Can the entity pay its bills?
- **Solvency assessment**: Can the entity service its debt?
- **Quality of earnings**: Is reported profit backed by real cash generation?
- **Capital allocation**: How is management deploying the cash the business generates?

For an LBO analyst, the cash flow statement is arguably the most important financial
statement — it is the source of the numbers that determine whether debt can be repaid
and whether equity returns can be achieved.

---

## 2. Definitions

IAS 7 defines its key terms precisely:

**Cash**: Cash on hand and demand deposits.

**Cash equivalents**: Short-term, highly liquid investments that are (i) readily
convertible to known amounts of cash, and (ii) subject to an insignificant risk of
changes in value. Typically investments with maturities of three months or less
from the date of acquisition qualify.

**Cash flows**: Inflows and outflows of cash and cash equivalents.

**Operating activities**: The principal revenue-producing activities of the entity,
plus any activities that are not investing or financing.

**Investing activities**: The acquisition and disposal of long-term assets and
other investments not included in cash equivalents.

**Financing activities**: Activities that result in changes in the size and
composition of the contributed equity and borrowings of the entity.

### In Grifols: What Counts as Cash?

Nota 14 reveals:

| Component | 2025 (€M) | 2024 (€M) |
|---|---|---|
| Short-term deposits | 8 | 5 |
| Restricted cash | 24 | — |
| Cash at bank | 793 | 975 |
| **Total** | **825** | **980** |

The €24M of restricted cash is included in the total but flagged as having an
"operational limitation of an administrative nature" imposed by a financial institution.
The restriction does not alter ownership or nature of the cash. IAS 7.48 requires
disclosure of significant cash balances not available for use by the group — Grifols
complies by disclosing this and noting it does not significantly affect overall liquidity.

This matters for modeling: when computing "net debt," you should consider whether
the €24M restricted portion should be deducted from gross debt. Most LBO models
would exclude restricted cash from the net debt calculation.

---

## 3. The Three Sections

The cash flow statement must classify all cash flows into three categories. This
classification is **not optional** — it is required by IAS 7.10.

### 3.1 Operating Activities

Operating cash flows represent the cash generated (or consumed) by the entity's
core business activities. This is the section that measures the cash-generating
power of the business.

IAS 7 permits two methods for presenting operating cash flows:

**The Direct Method**: Shows actual cash receipts from customers, cash paid to
suppliers, cash paid to employees, etc. IAS 7 encourages this method because it
provides information useful for forecasting that the indirect method does not.

**The Indirect Method**: Starts with profit before tax (or net profit) and adjusts
for non-cash items, non-operating items, and working capital changes to arrive at
cash from operations. This is far more commonly used in practice.

**Grifols uses the indirect method.** The vast majority of IFRS reporters do,
because the direct method requires either maintaining cash-basis accounting records
or performing complex reconstructions — effort that most companies deem not worth
the benefit.

### 3.2 Investing Activities

Investing cash flows capture expenditures on and proceeds from long-term assets.
This section reveals how much the entity is reinvesting in its productive capacity
and how much it is divesting.

A critical IAS 7 rule: **only expenditures that result in a recognized asset** on the
balance sheet can be classified as investing. If the expenditure is expensed (e.g.,
R&D costs that don't meet capitalization criteria), the related cash flow must be
classified as operating, even if the purpose of the expenditure is to generate
future revenue.

### 3.3 Financing Activities

Financing cash flows show how the entity has funded itself through equity and debt.
This section reveals the entity's reliance on external capital, its debt repayment
patterns, and its return of capital to shareholders.

---

## 4. Grifols' Cash Flow Statement — A Line-by-Line Walk

### 4.1 Operating Activities (Indirect Method)

| Line Item | 2025 | 2024 | 2023 | What It Means |
|---|---|---|---|---|
| **Profit before tax** | 615 | 444 | 206 | Starting point under indirect method |
| D&A | 450 | 438 | 446 | Added back: non-cash expense |
| Equity method (gain)/loss | 8 | (37) | (63) | Added back: non-cash P&L item |
| Impairment & provisions | 49 | 73 | 101 | Added back: non-cash charges |
| (Gain)/loss on asset disposal | 2 | 1 | 7 | Reclassified to investing |
| Grants credited to P&L | (7) | (15) | (10) | Non-cash income |
| Financial expenses/income | 628 | 681 | 556 | Reclassified to "other operating flows" |
| Other adjustments | 18 | 41 | (3) | Various non-cash items |
| **Total adjustments** | **1,148** | **1,182** | **1,034** | |
| Working capital changes | (31) | 23 | (363) | See discussion below |
| Interest paid | (532) | (571) | (529) | **Classification choice** |
| Interest received | 10 | 11 | 14 | |
| Tax paid | (169) | (176) | (159) | |
| Other | 6 | (11) | 14 | |
| **Operating cash flow** | **1,047** | **902** | **217** | |

**Key observations:**

**Starting point**: Grifols starts with "Resultado antes de impuestos" (profit before
tax) of €615M. This is a choice — IAS 7 allows starting from either profit before
tax or net profit. Starting from PBT means the tax cash payment appears as a
separate adjustment below; starting from net profit would require adding back
the P&L tax charge and then showing the cash tax payment. Grifols' approach is
clearer because it separates the P&L tax expense from the actual cash tax paid.

**The €1,148M of adjustments**: These reverse all non-cash items that were included in
profit before tax. The largest is D&A (€450M), followed by net financial expenses
(€628M). Why is the financial expense added back here? Because Grifols classifies
interest paid as an operating cash flow — so the accrual-basis interest expense
is added back in "adjustments" and then the actual cash interest paid (€532M) is
deducted separately below. This ensures the operating cash flow reflects the
actual cash cost of debt service.

**Working capital changes**: Only €(31)M in 2025, a dramatic improvement from
€(363)M consumption in 2023. This breaks down as:

| WC Component | 2025 | 2024 | 2023 |
|---|---|---|---|
| Inventories | (97) | 26 | (411) |
| Receivables | (32) | (42) | (69) |
| Other financial current assets | 4 | 10 | 13 |
| Payables | 94 | 29 | 104 |
| **Net WC change** | **(31)** | **23** | **(363)** |

The 2023 figure was devastating — €411M of cash absorbed by inventory buildup
(Grifols was building plasma inventory). By 2025, inventory is still consuming
cash (€97M) but at a much more manageable rate, and payables increased €94M
(essentially suppliers financing part of the growth).

### 4.2 The Critical Classification Choice: Interest Paid

This is one of the most important practical aspects of IAS 7 and one where Grifols'
choice has enormous consequences.

IAS 7 allows interest paid to be classified as either:
- **Operating** (Grifols' choice) — because it enters into the determination of profit
- **Financing** — because it is a cost of obtaining financial resources

Grifols classifies **€532M of interest paid as operating**. This means that operating
cash flow (€1,047M) is AFTER debt service. If Grifols had classified interest as
financing, operating cash flow would have been €1,047M + €532M = **€1,579M**.

This classification choice matters enormously for analysis:

- When comparing Grifols to a company that classifies interest as financing, you
  must adjust to a common basis
- When computing "free cash flow" for an LBO model, you need to be clear about
  whether your definition is before or after interest
- The €1,047M figure is more conservative (and arguably more useful) because it
  shows cash available after the mandatory cost of the existing debt structure

Similarly, Grifols classifies **dividends paid (€128M) as financing**, and
**tax paid (€169M) as operating**. IAS 7 allows alternatives for both. This is
a policy choice that must be applied consistently.

### 4.3 Investing Activities

| Line Item | 2025 | 2024 | 2023 |
|---|---|---|---|
| Acquisitions (subsidiaries, associates) | (108) | (286) | (29) |
| PP&E investment | (265) | (233) | (224) |
| Intangible investment | (158) | (139) | (86) |
| Financial asset investment | (57) | (44) | (93) |
| **Total payments** | **(588)** | **(702)** | **(432)** |
| Proceeds from SRAAS disposal | — | 1,564 | — |
| Other disposal proceeds | 9 | 24 | 38 |
| **Total receipts** | **9** | **1,588** | **38** |
| **Net investing** | **(579)** | **886** | **(394)** |

The 2024 figure is distorted by the €1,564M proceeds from the Shanghai RAAS
disposal — a one-off divestiture. Stripping this out, recurring investing outflows
run at €579M (2025) vs €(702M - 1,588M) = actually cash consuming excluding SRAAS.

**Maintenance vs growth capex**: The PP&E figure (€265M) includes both maintenance
and expansion capex. IAS 7 encourages (but does not require) disclosure of
expenditures to maintain operating capacity vs. expenditures to increase it. Grifols
does not make this distinction in the cash flow statement, so you would need to
estimate maintenance capex from the D&A charge (€450M total, but this includes
amortization of intangibles and right-of-use assets). A rough proxy: PP&E depreciation
alone runs around €240M (from Nota 9), suggesting €265M of PP&E capex is barely
above maintenance levels.

### 4.4 Financing Activities

| Line Item | 2025 | 2024 | 2023 |
|---|---|---|---|
| Debt issuance | 1,360 | 4,007 | 1,638 |
| Debt repayment | (1,550) | (5,248) | (1,351) |
| **Net debt flows** | **(309)** | **(1,352)** | **171** |
| Lease payments (principal) | (119) | (111) | (116) |
| Dividends paid | (128) | (1) | — |
| Financing costs in amortized cost | — | (58) | — |
| NCI acquisition | (129) | — | — |
| Other | 37 | 52 | 1 |
| **Net financing** | **(529)** | **(1,359)** | **172** |

**Critical observation on lease payments**: Under IFRS 16, lease payments are split:
the **principal portion** (€119M) appears in financing activities, while the **interest
portion** (€57M, per Nota 8) is included in operating activities (within the €532M
interest paid line). Before IFRS 16, the entire lease payment would have been in
operating cash flows. This means Grifols' operating cash flow is €119M higher than
it would have been under the old IAS 17 standard. When comparing to pre-IFRS 16
data or to companies not yet on IFRS 16, you must adjust for this.

**The €128M dividend**: This is the first significant dividend Grifols has paid in
years — a clear signal of improved financial confidence.

**The €129M NCI acquisition**: Grifols bought out minority interests during 2025.
This is correctly classified as financing (it's a transaction between equity holders)
per IAS 7.42A.

### 4.5 The FX Effect

| | 2025 | 2024 | 2023 |
|---|---|---|---|
| FX effect on cash | (94) | 22 | (15) |

This is the **translation effect** on cash balances held in foreign currencies. When
the Euro strengthened against the USD in 2025, the Euro value of Grifols' USD cash
balances decreased by €94M. This is not a cash flow — it's a revaluation. IAS 7.28
requires it to be reported separately from operating, investing, and financing cash
flows. This reconciles the movement in cash:

Opening cash (€980M) + Operating (€1,047M) + Investing (€-579M) + Financing
(€-529M) + FX effect (€-94M) = Closing cash (€825M).

---

## 5. The Indirect Method — Understanding the Mechanics

The indirect method can feel mechanical, but understanding *why* each adjustment
exists is crucial. The logic is:

**Start with accrual-basis profit** → **remove non-cash items** → **remove items that
belong in investing/financing** → **add working capital changes** → **arrive at
cash from operations**

Each adjustment falls into one of these categories:

**Non-cash charges added back:**
- D&A (€450M): Real economic cost spread over asset life, but no cash left the door
- Impairment/provisions (€49M): P&L charges that don't require immediate cash payment
- Share of equity-method losses (€8M): Grifols records its share of associate losses
  in the P&L, but no cash changes hands

**Items reclassified to other sections:**
- Financial expenses (€628M added back, then €532M cash interest deducted below):
  The net finance cost hits the P&L, but the actual cash interest is shown separately
- Gains/losses on asset disposal (€2M): The P&L effect is removed from operating;
  the actual cash proceeds appear in investing

**Working capital changes:**
- These capture the difference between accrual-basis revenues/expenses and the actual
  cash received/paid. If receivables increase, you earned revenue but didn't collect
  cash yet — so it's deducted. If payables increase, you incurred costs but haven't
  paid yet — so it's added.

---

## 6. What IAS 7 Does NOT Tell You (But You Need to Know)

### 6.1 Free Cash Flow Is Not Defined

IAS 7 does not define "free cash flow" (FCF). This is one of the most commonly used
metrics in finance, yet it has no authoritative IFRS definition. Different analysts
compute it differently:

| FCF Definition | Grifols 2025 |
|---|---|
| Operating CF − Capex (PP&E only) | 1,047 − 265 = **€782M** |
| Operating CF − Capex (PP&E + intangibles) | 1,047 − 423 = **€624M** |
| Operating CF − Total investing outflows | 1,047 − 588 = **€459M** |
| Operating CF + interest paid − Capex (unlevered FCF proxy) | 1,047 + 532 − 423 = **€1,156M** |

Each version tells a different story. For an LBO, you typically want unlevered free
cash flow (before debt service) to determine debt capacity, then layer in your own
assumed debt structure.

### 6.2 EBITDA to Cash Flow Reconciliation

A common analytical exercise is reconciling EBITDA to operating cash flow. For Grifols:

| Step | €M |
|---|---|
| Segment EBITDA | 1,693 |
| Less: corporate/unallocated costs | (235) |
| **Reported EBITDA (approx)** | **~1,458** |
| Equity-method results and other | (8) + 1 = (7) |
| **Operating result (EBIT)** | **1,243** |
| Add back D&A | 450 |
| **EBITDA (from P&L reconstruction)** | **~1,693** |
| Working capital change | (31) |
| Tax paid | (169) |
| Interest paid | (532) |
| Other operating adjustments | 86 |
| **Operating cash flow** | **1,047** |

The gap between EBITDA (€1,693M) and operating cash flow (€1,047M) is primarily
interest (€532M), tax (€169M), and working capital (€31M). This reconciliation is
not required by IAS 7 but is essential for understanding cash conversion.

### 6.3 Non-Cash Transactions

IAS 7.43 requires that investing and financing transactions that do not require the
use of cash be **excluded** from the statement of cash flows but disclosed elsewhere.
Examples include:

- Acquisition of assets by assuming related liabilities (e.g., lease inception)
- Conversion of debt to equity
- Non-cash asset exchanges

For Grifols, the most significant non-cash financing item is **new lease liabilities**
recognized under IFRS 16. In 2025, €143M of new right-of-use assets were recognized
(Nota 8), creating corresponding lease liabilities — but no cash changed hands. These
appear in the balance sheet but not in the cash flow statement.

---

## 7. Key Judgments and Practical Issues

### 7.1 Supply Chain Financing / Reverse Factoring

Recent amendments to IAS 7 (effective 2024) require new disclosures about supplier
finance arrangements. These are schemes where a financial institution pays the
entity's suppliers early, and the entity repays the financial institution later. The
concern is that such arrangements can obscure the true level of trade payables
(operating) by replacing them with bank debt (which might be financing).

The IFRS IC and standard-setters have scrutinized this area because some entities
used these arrangements to artificially inflate operating cash flows.

### 7.2 The Interest Classification Debate

Grifols' choice to classify interest paid as operating is conservative and common
in Europe. However, in the context of an LBO analysis, it creates a subtlety: the
reported operating cash flow already reflects the existing capital structure's debt
service cost. If you're modeling a hypothetical acquisition with a different debt
structure, you need to work with **pre-interest operating cash flow** (i.e., add back
the €532M interest paid to get a "clean" operating cash figure of €1,579M, then
apply your own assumed interest cost).

### 7.3 Acquisitions and Disposals — The Netting Problem

IAS 7.39 requires that aggregate cash flows from obtaining or losing control of
subsidiaries be presented separately and classified as investing. The 2024 figure
shows €1,564M from the SRAAS disposal — clearly investing. But the 2025 figure
shows €108M of acquisition payments — you need to check whether this is cash
consideration for new acquisitions or deferred payments for old ones (Nota 3).

---

## 8. Future Changes: IFRS 18 Impact on Cash Flows

IFRS 18 (effective 2027) will introduce changes to cash flow classification:

- The operating/investing/financing categories will be aligned with the new income
  statement categories
- **Interest and dividend classification** will become more prescriptive
- The starting point for the indirect method will be defined more precisely

This means Grifols' cash flow statement will look different from 2027 onward, and
classification choices currently available may be narrowed.

---

## 9. Summary: What to Take Away

The cash flow statement under IAS 7 is:

- The only financial statement prepared on a **cash basis** (everything else is accrual)
- Structured into **three mandatory categories**: operating, investing, financing
- Presented using either the **direct or indirect method** (indirect is far more common)
- Subject to **significant classification choices** (especially interest and dividends)
  that can dramatically affect how operating cash flow appears

For Grifols:

- Operating CF of **€1,047M** (after €532M interest paid — a classification choice)
- Capex of **€423M** (PP&E + intangibles), with PP&E capex roughly at maintenance levels
- Net debt reduction of **€190M** (€1,550M repaid minus €1,360M issued)
- First dividend in years: **€128M**
- IFRS 16 inflates operating CF by **€119M** (the lease principal portion shifted to financing)
- FX translation reduced closing cash by **€94M** — a non-cash effect shown separately

The gap between accrual-basis profit (€500M net income) and cash generation (€1,047M
operating CF) is explained by €450M of D&A and other non-cash addbacks minus the
€532M of interest paid and €169M tax paid that reduce cash but are already in the P&L.

---

*Module 3 complete. Next: Module 4 — IFRS 8 (Operating Segments)*

*Reference: International GAAP 2026, Chapter 36; Grifols S.A. Estado de Flujos de Efectivo, Notas 8, 14, 19*
