# Chapter 9: Debt and Liens Covenants

## Introduction

Chapter 8 explained how value *leaves* the credit box—through dividends, investments, and the trap doors sponsors use to extract cash. This chapter addresses the opposite problem: how additional *leverage* gets layered on top of your position, and who gets paid first when things go wrong.

If the Restricted Payments covenant is the dam holding back value from flowing to equity, the Debt and Liens covenants are the throttle controlling how much senior or pari passu debt can be stacked above you. Understanding these covenants is essential because in distress, your recovery depends not just on what remains in the credit box, but on how many other creditors are competing for it—and whether they're ahead of you in line.

The Debt and Liens covenants serve two strategic objectives: preserving the asset base available to service debt, and limiting the total quantum of claims against that base. Mastering them is the first and most critical step in identifying credit risk.

---

## 9.1 The Two Questions

Every time a borrower wants to incur new secured debt, there are two separate questions that must be answered:

**Question One: Can the borrower incur this debt?**
This is governed by the Debt covenant (or "Limitation on Indebtedness").

**Question Two: Can the borrower secure it?**
This is governed by the Liens covenant.

These are independent inquiries. Having capacity under the Debt covenant does not automatically mean the debt can be secured. Having capacity under the Liens covenant is useless without permission to incur the debt in the first place. For secured debt to be permitted, you need separate permissions in *both* covenants.

This independence creates opportunity for issuers—and traps for analysts who only check one covenant. It also means that answering "What's this company's secured debt capacity?" requires working through two parallel analyses.

---

## 9.2 The Hierarchy of Claims: Understanding Priority

Before diving into covenant mechanics, you must understand how priority works. In any enforcement or insolvency, the hierarchy of claims determines the payment waterfall and creditor recoveries.

### Payment Subordination

A contractual agreement where one debt ranks junior in right of payment to another. In insolvency, senior debt must be paid in full before subordinated debt receives anything. This is the most direct form of subordination.

### Lien Subordination

Relates to priority of claims on specific collateral. Debt can be equal in payment priority (*pari passu*) but have different lien priority. First-lien and second-lien term loans are typically equal in payment rights, but upon enforcement against shared collateral, first-lien lenders must be repaid in full before second-lien receives any proceeds.

### Structural Subordination

Arises from corporate structure. Debt issued by an operating subsidiary is effectively senior to holding company debt with respect to that subsidiary's assets. The subsidiary's creditors have a direct claim; the holding company's creditors only have a claim on the equity of that subsidiary, which is residual after the subsidiary's own debts are paid.

This makes the distinction between **Guarantor** and **Non-Guarantor** subsidiaries critical. Debt at a Non-Guarantor is structurally senior to debt at the parent level.

### Effective Subordination

Defines unsecured debt's status relative to secured debt. With respect to specific collateral, secured creditors have priority. Unsecured creditors can only claim value remaining after secured creditors are paid.

This is particularly significant in European financings where collateral packages are often limited to "soft" assets (share pledges, bank accounts) and exclude "hard" assets (machinery, IP, real estate).

---

## 9.3 The Debt Covenant: Regulating Incurrence

The typical high-yield Debt covenant is structured as a general prohibition followed by crucial exceptions. It states that the issuer and its Restricted Subsidiaries may not incur any indebtedness—then qualifies this with two categories of permissions:

1. **Ratio-based debt capacity ("Ratio Debt")**
2. **Specific carve-outs ("Permitted Debt" baskets)**

### Ratio Debt: The Incurrence Test

Ratio Debt is the principal mechanism allowing a growing company to take on more debt. This capacity is dynamic—available only when the company meets a specified performance test calculated pro forma for the new debt.

**Fixed Charge Coverage Ratio (FCCR):** Measures ability to cover fixed charges (cash interest) with cash flow (EBITDA). Common test: FCCR ≥ 2.0x.

**Leverage Ratio:** Measures debt relative to EBITDA. Test is met if leverage remains below a specified ceiling pro forma for the incurrence.

In documents featuring both tests, borrowers often only need to satisfy *one*. Furthermore, modern leverage tests are almost always **net tests**—permitting "cash netting" where cash is subtracted from gross debt. There's typically no cap on cash that can be netted or requirement that cash be used for repayment.

### Permitted Debt Baskets

These provide ability to incur specified amounts regardless of financial performance. Key baskets include:

**Credit Facilities Basket:** Despite the name, "Credit Facility" is typically defined to include not just bank loans but bonds and most other debt forms—making this a powerful general-purpose basket.

**General Debt Basket:** A flexible catch-all for any purpose, often substantial in size.

**Acquisition / Acquired Debt Basket:** Facilitates M&A by permitting debt to finance acquisitions or allowing existing debt at targets to remain in place.

**Non-Guarantor / Foreign Subsidiary Debt Basket:** A critical source of structural subordination. Allows sponsors to issue debt at operating subsidiaries with priority claims on valuable assets, leaving holding company creditors with claims only on residual equity.

**Other Material Baskets:** Capital leases, purchase money debt, local lines for overseas subsidiaries, receivables financings.

### Growers and Reclassification

Debt capacity is not static. Modern covenants contain expansion mechanics:

**Grower Baskets:** Most fixed-dollar baskets are structured as the greater of a hard-dollar amount and a percentage of EBITDA or Total Assets. A **super-grower** or **high-watermark** permanently ratchets the fixed-dollar floor to the highest grower value ever achieved—creating disconnect between *current* debt-service ability and *permitted* incurrence capacity.

**Reclassification:** Allows borrowers to re-designate debt from one basket to another. Common strategy: once performance improves, reclassify debt from a fixed basket to Ratio Debt capacity. This "reloads" the fixed basket for use again—even if performance later deteriorates.

### The Incremental Facility (Accordion)

Credit agreements typically allow borrowers to increase facility size through:

1. **Free-and-Clear Tranche:** Fixed amount available regardless of leverage, often with a grower
2. **Unlimited Ratio Tranche:** Available if pro forma leverage test is satisfied

**Maturity Erosion:** Historically, incremental debt was required to mature *no earlier* than existing term loans. This protection has eroded through exceptions for bridge loans, escrow debt, and capped baskets for inside-maturity debt. Sponsors can now layer in shorter-dated debt that effectively primes original lenders in the maturity queue.

**MFN Sunset:** Most Favored Nation provisions historically required incremental pricing not exceed existing debt by more than ~50 bps. MFN protections now routinely sunset after 6-12 months, and increasingly don't apply to debt in separate "side-car" facilities.

### The Refinancing Loophole

The Permitted Refinancing carve-out allows new debt to refinance existing debt. But if refinancing debt incurred under a capped basket doesn't simultaneously reduce that basket's capacity, the transaction effectively "empties" the basket—allowing it to be used again for new debt.

---

## 9.4 The Liens Covenant: Controlling Security and Priority

While the Debt covenant governs the *amount* of claims, the Liens covenant governs their *priority*. In distress, a creditor's position in the security structure is often the single most decisive factor in recovery.

### The Core Mechanic

Like the Debt covenant, the Liens covenant begins with a general prohibition—the issuer may not create or permit liens on any assets to secure indebtedness—followed by a list of exceptions: "Permitted Liens."

### Negative Pledge vs. True Liens Covenant

**Negative Pledge (Unsecured Bonds):** Does not limit how much debt can be secured. Instead, if other debt gets secured by collateral, the bonds must also be equally and ratably secured. "Permitted Liens" carve out exceptions where security can be granted *without* extending it to the bonds.

**True Liens Covenant (Secured Bonds/Loans):** Flatly prohibits granting liens except as permitted by "Permitted Liens" (for non-collateral assets) and "Permitted Collateral Liens" (for collateral assets).

### The European Blended Approach

Most European secured high yield bonds use a blended structure:

- **For Collateral assets:** A true liens covenant applies
- **For Non-Collateral assets:** A negative pledge applies

This distinction matters enormously. European collateral packages are often limited to share pledges and bank accounts—meaning vast pools of operating assets sit *outside* the collateral package. The Permitted Liens definition determines who can grab those assets.

### Key Permitted Liens Carveouts

**General Permitted Liens Basket:** Fixed-dollar basket (usually with grower) allowing liens securing any permitted debt.

**Liens Securing Credit Facilities Debt:** Allows the corresponding Credit Facilities basket debt to be secured. In secured bond deals, this can create risk if it allows debt to be secured on a super-senior basis.

**Liens Securing Refinancing Debt:** Critical vulnerability—often lacks requirement that new liens be of *no higher priority* than original liens. Loophole could allow junior-lien debt to be refinanced with first-lien.

**Junior Liens on Collateral:** Common European feature granting blanket permission for permitted debt to be secured by junior liens on bond collateral—creating significant dilution risk.

---

## 9.5 Agreed Security Principles: The European Architecture

In European transactions, **Agreed Security Principles (ASPs)** determine the actual scope of the collateral package and guarantee structure. They are the "rules of engagement" that filter which assets are actually pledged and which subsidiaries provide guarantees.

### The Core Tenets

**Cost-Benefit Analysis:** Security will not be required if the cost of obtaining it is disproportionate to the benefit. "Cost" includes stamp duty, registration taxes, notary fees, and even "implied cost of management time."

**Legal and Statutory Limitations:** Security and guarantees are limited by local laws regarding financial assistance, corporate benefit, capital maintenance, and thin capitalization rules.

**Materiality:** Security often only required over "material assets." Creating security over categories like real estate may be waived unless individually significant.

**Excluded Jurisdictions:** The ASPs often explicitly list jurisdictions where no group member is required to provide guarantee or security.

### Why ASPs Matter: The Hollow Guarantor Test

European loans rely on a "Guarantor Coverage Test" requiring guarantors represent ~80% of Consolidated EBITDA. However, ASPs heavily dilute this protection.

**The Loophole:** When calculating total group EBITDA (the denominator), ASPs allow excluding EBITDA of subsidiaries unable to become guarantors due to legal reasons or the ASPs themselves.

**The Result:** The 80% test is not 80% of *entire* group EBITDA—it's 80% of *guaranteeable* EBITDA. Lenders' credit support could represent "80% of not very much at all."

### The "Soft" Security Reality

Because ASPs justify leaving hard assets unencumbered, European collateral is often limited to share pledges, intercompany receivables, and bank accounts. This creates a pool of Non-Collateral assets available to secure priming debt.

---

## 9.6 The Secured Debt Capacity Analysis

Answering "What's this company's secured debt capacity?" requires working through both covenants systematically.

### The Mix-and-Match Principle

Debt covenant permissions and Liens covenant permissions combine flexibly. Do not assume General Debt can only be secured under the General Liens basket.

An issuer with Ratio Debt capacity could secure that debt using:
- The leverage-based liens carveout
- The General Liens basket
- Any other available Permitted Liens

This flexibility multiplies secured debt capacity beyond what any single basket suggests.

### Why the Secured Leverage Test is NOT a Cap

This is the most common analytical error. A 4.0x Secured Leverage test in the liens covenant does *not* mean the company cannot exceed 4.0x secured leverage.

Each carveout is separate and independent. If the company cannot meet the 4.0x test, that specific carveout is unavailable—but the company can still incur secured debt under other Permitted Liens:
- The Credit Facilities basket (with its own size or ratio test)
- The General Liens basket
- Deal-specific carveouts

The leverage test is *one* source of liens capacity, not a ceiling on total secured debt.

### Worked Example

*Debt Covenant:*
- Ratio Debt: Available at 2.0x FCCR
- Credit Facilities basket: Greater of €200M or Secured Leverage ≤ 4.0x
- General Debt basket: €50M

*Liens Covenant:*
- Credit Facilities basket debt may be secured
- Leverage-based liens: Any debt may be secured at Secured Leverage ≤ 4.5x
- General Liens basket: €75M

If current Secured Leverage is 4.2x:
- Credit Facilities ratio prong unavailable (4.2x > 4.0x)
- But €200M fixed amount still available
- Leverage-based liens carveout unavailable (4.2x > 4.5x)
- But General Liens basket provides €75M

**Secured debt capacity = €200M + €75M + potential creative structuring of additional capacity.**

---

## 9.7 The Five Forms of Debt Priming

"Priming" means one class of debt moves ahead of another in priority—whether regarding right of payment, access to collateral, or recourse to specific assets. Understanding the mechanisms is essential for distress analysis.

### 1. Lien Subordination: The "Uptier"

The most direct form, popularized by Serta Simmons, Boardriders, and TriMark.

**The Mechanism:** Borrower amends existing documents to allow new "super-priority" debt ranking senior to existing facilities. Often paired with exchange offers where majority lenders swap into super-priority paper, leaving non-participating minority in a subordinated position.

**The Loophole:** In many U.S. credit agreements, subordination is not a "sacred right" and can be approved by simple majority (50.1%).

**European Context:** In loans, ranking changes usually require all-lender consent, making Serta-style uptiers contractually harder. However, European *high yield bonds* often lack these protections regarding lien priority, making them more vulnerable to uptiering via majority consent.

### 2. Structural Subordination: The "Drop-Down"

Occurs when debt is incurred by a subsidiary that doesn't guarantee parent debt. That subsidiary's creditors must be paid in full before any value moves upstream.

**Unrestricted Subsidiaries (J. Crew Style):** Borrower designates a subsidiary holding valuable assets as Unrestricted, removing it from covenants. The Unrestricted Subsidiary incurs new debt secured by those assets—structurally senior to original lenders.

**Non-Guarantor Restricted Subsidiaries:** Modern covenants allow these to incur significant debt using general baskets or ratio capacity. Because they don't guarantee parent debt, any third-party debt is structurally senior.

### 3. Effective Subordination: Non-Collateral Assets

Relies on the distinction between Collateral and Non-Collateral assets.

**The Mechanism:** Borrower incurs new debt secured by assets *not* part of the existing collateral package. The new debt is "effectively senior" regarding those assets.

**European Vulnerability:** Unlike U.S. "all-asset" pledges, European security packages are often "soft"—limited to share pledges and intercompany receivables. This leaves large pools of Non-Collateral assets available to secure priming debt.

### 4. The "Double-Dip"

A recent innovation that mathematically dilutes existing creditors.

**The Mechanism:** A subsidiary (often non-guarantor or Unrestricted) incurs new debt. It lends proceeds to the existing borrower via an intercompany loan. New creditors get two claims:
1. Direct claim against the subsidiary borrower
2. Indirect claim against the parent via the pledged intercompany loan (often secured pari passu with existing lenders)

**The Result:** For every €100 of new debt, new creditors establish €200 of claims, diluting legacy lender recovery.

### 5. Contractual Priority: Super Senior Status

In European structures, "Super Senior" debt (typically RCF and hedging) ranks pari passu in security interest but gets paid *first* from enforcement proceeds per the Intercreditor Agreement.

Modern ICAs often include **"hollow tranches"**—pre-baked ability to add priming debt without further amendment.

---

## 9.8 The Role of the Intercreditor Agreement

When multiple secured creditor classes exist, the **Intercreditor Agreement** is the ultimate arbiter of ranking and priority. Its primary functions:

**Establishing the Payment Waterfall:** Dictates precise order for distributing enforcement proceeds among super-senior, senior, and junior creditors.

**Governing Enforcement:** Typically imposes a "standstill" period on junior creditors, preventing enforcement action for a specified time after default. Senior creditors control the process.

The Intercreditor Agreement is a cornerstone of credit protection in complex, multi-jurisdictional European structures where it provides essential clarity on rights and remedies.

---

## 9.9 Market Nuances: Europe vs. U.S.

| Feature | European Market | U.S. Market |
|---------|-----------------|-------------|
| **Sacred Rights** | HY bond sacred rights typically require 90% supermajority (all-or-nothing binding all holders) | "Affected holder" consent—changes cannot be imposed on non-consenting minority |
| **Intercreditor Role** | Highly critical in multi-jurisdictional structures | Important but arguably less central given single Chapter 11 framework |
| **Covenant Style** | Traditional LMA uses multiple distinct covenants (Acquisitions, JVs, Dividends) | Bond-style documents use single consolidated RP covenant |
| **Security Packages** | Often "soft" (share pledges, bank accounts only) | Typically "all-asset" pledges including hard assets |

---

## Summary: The Diligence Framework

When analyzing Debt and Liens covenants, map all sources of potential leverage—not just what's outstanding today, but what *could* be incurred tomorrow.

**Debt Covenant Analysis:**
- What Ratio Debt capacity exists under current performance?
- Size and conditions of each Permitted Debt basket?
- Are there growers or high-watermark mechanics?
- What reclassification flexibility exists?
- What inside-maturity capacity is available?

**Liens Covenant Analysis:**
- True liens covenant or negative pledge?
- What Permitted Liens carveouts exist and their sizing?
- Is there a leverage-based carveout, and what's the test?
- Can refinancing liens be elevated in priority?

**Structural Analysis:**
- What assets are actually in the collateral package?
- What assets are Non-Collateral and available for priming?
- What's the real (not "guaranteeable") EBITDA coverage?
- Where does structural subordination risk exist?

**Priming Risk Assessment:**
- Can uptier transactions be executed with majority consent?
- Is there capacity for drop-downs to Unrestricted Subsidiaries?
- Are double-dip structures possible?
- What blocker provisions exist, and can they be circumvented?

---

*Next: Chapter 10 covers Asset Sales, Change of Control, and other key negative covenants that complete the creditor protection architecture.*
