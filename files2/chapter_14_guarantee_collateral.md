# Chapter 14: Guarantee and Collateral

## Introduction

The guarantee and collateral package is the bedrock of credit support in leveraged finance. It determines who can claim what, from whom, and in what order. Yet in European transactions, the reality of this credit support often diverges dramatically from appearances.

This chapter examines the architecture of credit support in European leveraged finance—how guarantees and collateral function, how they interact, and most importantly, how the contractual framework systematically filters what lenders actually receive. Understanding this architecture is essential because it determines your recovery in distress.

The gap between what you *think* you have secured and what you *actually* have secured is often the difference between a full recovery and a significant loss.

---

## 14.1 Foundations: Guarantees vs. Collateral

These two concepts are frequently conflated but serve distinct functions.

### What is a Guarantee?

A guarantee is a promise by an entity that is *not* the primary obligor to be responsible for the debt if the primary obligor fails to pay.

Consider a simple example: ABC Company is the borrower under a term loan. Its wholly-owned subsidiary DEF Corp. guarantees this term loan. If ABC fails to pay, lenders can proceed against DEF to collect. DEF is the "secondary obligor"—its assets are available to satisfy the debt.

The critical implication: if ABC later issues bonds that DEF does *not* guarantee, holders of those bonds would be **structurally subordinated** to the term loans. They have no direct claim against DEF's assets; they can only claim the residual equity value of DEF after DEF's own creditors (including the term loan lenders via the guarantee) are paid.

### What is Collateral?

Collateral refers to specific assets pledged to secure debt obligations. A lien on collateral gives the secured creditor a priority claim against those particular assets.

If ABC pledges its factory building to secure the term loan, and later issues unsecured bonds, the term loan lenders have a priority claim on the factory. The bondholders are **lien subordinated** to the term loans with respect to that asset—they can only claim value remaining after the secured creditors are satisfied.

### How They Work Together

Guarantees and collateral frequently complement each other:

- A guarantee can be **unsecured**: the guarantor promises to pay, but no specific assets are pledged
- A guarantee can be **secured**: the guarantor promises to pay *and* pledges specific assets to back that promise

A secured guarantee provides both:
1. A direct claim against the guarantor (the guarantee)
2. A priority claim against specific assets of the guarantor (the collateral)

The distinction matters enormously in recovery analysis. An unsecured guarantee ranks pari passu with the guarantor's other unsecured creditors. A secured guarantee gives you priority over those creditors to the extent of the pledged collateral.

### Using Them as Alternatives

Guarantees and collateral can also function as alternatives for creating effectively senior debt:

**Scenario A (Collateral Route):** New debt is secured by assets not previously pledged. This debt is "lien senior" to existing unsecured debt regarding those assets.

**Scenario B (Guarantee Route):** New debt is guaranteed by a subsidiary that does not guarantee existing debt. This debt is "structurally senior" to existing debt regarding that subsidiary's assets.

Both routes achieve priority—through different mechanisms. Understanding which route is available under specific documentation is critical for identifying priming risk.

---

## 14.2 Agreed Security Principles: The European Filter

In European transactions, **Agreed Security Principles (ASPs)** are the fundamental rules determining what credit support lenders actually receive. They are far more than boilerplate legal schedules—they are the filter that determines which assets are pledged and which subsidiaries provide guarantees.

While U.S. lenders generally expect comprehensive "all-asset" pledges, European deals are governed by ASPs that systematically limit security based on cost, legal constraints, and practical considerations.

### The Core Tenets

**1. Cost-Benefit Analysis**

This is the overriding principle. Security will not be required if the cost of obtaining it is disproportionate to the benefit obtained by lenders.

"Cost" is defined broadly:
- Stamp duty and registration taxes
- Notary fees
- Legal costs of perfection
- Even the "implied cost of management time"

This creates enormous discretion. What constitutes "disproportionate" is subjective, and the borrower typically controls the analysis.

**2. Legal and Statutory Limitations**

ASPs codify that security and guarantees will be limited by local laws regarding:
- **Financial assistance**: Restrictions on subsidiaries guaranteeing acquisition debt
- **Corporate benefit**: Requirements that guarantors receive adequate consideration
- **Capital maintenance**: Rules protecting creditors of the guarantor itself
- **Thin capitalization**: Tax rules limiting deductibility of interest on excessive debt

In jurisdictions like France or Spain, a subsidiary cannot guarantee parent debt if it puts the subsidiary at financial risk without commensurate benefit. The guarantee is either void or limited to the value of benefit received.

**3. Materiality Thresholds**

Security is often only required over "material" assets. Creating security over categories like real estate may be waived unless an individual asset exceeds a significance threshold.

**4. Excluded Jurisdictions**

ASPs often explicitly list jurisdictions where no group member is required to provide guarantee or security—regardless of materiality or cost. Subsidiaries in these jurisdictions are simply outside the credit support perimeter.

---

## 14.3 The Hollow Guarantor Coverage Test

European loans typically require that Guarantors represent a specified percentage of Consolidated EBITDA—usually **80%**. This sounds protective. In practice, ASPs can render it nearly meaningless.

### The Standard Test

The guarantor coverage test requires annual certification that aggregate EBITDA of guarantors equals at least 80% of group EBITDA. If coverage falls below the threshold, the borrower must cause additional subsidiaries to accede as guarantors.

### The Denominator Problem

Here is the trap: when calculating total group EBITDA (the *denominator*), ASPs typically allow the borrower to **exclude** EBITDA of subsidiaries that are unable to become guarantors due to:
- Legal limitations (financial assistance, corporate benefit)
- The ASPs themselves (cost-benefit, excluded jurisdictions)
- Not being wholly-owned

**The Result:** The 80% test is not 80% of the *entire* group's EBITDA. It is 80% of "guaranteeable" EBITDA—a smaller, filtered subset.

As the research notes: "Lenders' credit support could represent 80% of not very much at all."

### The Wholly-Owned Limitation

Most guarantor coverage tests only apply to **wholly-owned** subsidiaries. The rationale is protecting minority shareholder rights. The consequence is that any subsidiary with even 1% minority ownership is excluded from both:
- The numerator (not required to guarantee)
- The denominator (excluded from coverage calculation)

This creates the **Chewy vulnerability**: a sponsor can transfer a small equity stake in a valuable guarantor to an affiliate or third party. Once no longer wholly-owned, the subsidiary is released from its guarantee—and the coverage test is unaffected because it's excluded from the denominator.

### Testing and Grace Periods

The test is typically annual, certified with financial statements. Built-in grace periods compound the protection gap:
- Financial statements due 120 days after year-end
- Additional 90-120 day compliance period after delivery
- Further 90-120 day cure period in events of default

A company could operate for nearly a year below true coverage before facing any consequence.

---

## 14.4 Guarantee Release Provisions

European documentation provides extensive circumstances under which guarantees can be released *without bondholder consent*. Understanding these provisions is essential because the credit support you're counting on can disappear.

### Automatic Release Triggers

Indentures and credit agreements typically provide a "laundry list" of circumstances where guarantees are "automatically and unconditionally released and discharged":

**1. Designation as Unrestricted Subsidiary**

If a guarantor is designated as Unrestricted, its guarantee is released. The designation requires sufficient investment capacity under the RP covenant—but once achieved, the guarantor exits the credit support perimeter entirely.

This is the J. Crew/Intralot playbook. Valuable subsidiaries generating substantial EBITDA can be designated Unrestricted, guarantee released, and then used to support priming debt.

**2. Sale or Disposition of the Guarantor**

Guarantees release upon sale of shares where the guarantor ceases to be a Restricted Subsidiary, or upon sale of substantially all assets to third parties. The Asset Sales covenant must be complied with, but if the sale is permitted, the guarantee disappears.

"Transfer or other disposition" language can extend this to mergers, spin-offs, and even dividend distributions of shares.

**3. Release Under Credit Agreement**

Some bond indentures permit guarantee release if the guarantor is released under the issuer's bank credit agreement. This puts bank lenders in control—if they agree to release, bondholders follow automatically.

Credit agreements permit release in numerous circumstances:
- Permitted disposals and reorganizations
- Designation as Unrestricted Subsidiary
- No longer a material subsidiary (below 5% threshold)
- No longer required under ASPs
- Lender consent (majority or supermajority)

**4. Repayment of Triggering Debt**

If a subsidiary became a guarantor only because it guaranteed other debt (via the Future Guarantors covenant), the guarantee can be released when that other debt is repaid or no longer guaranteed.

**5. Merger, Consolidation, or Liquidation**

Guarantees release upon merger into the issuer or another guarantor, or upon liquidation. The Mergers covenant must be complied with.

**6. Permitted Reorganizations**

Broadly drafted provisions allow release in connection with intragroup reorganizations, amalgamations, and mergers. Problems arise when drafting fails to require substantially equivalent guarantees after the reorganization.

**7. Investment Grade Suspension**

Some covenants suspend the Future Guarantors covenant or permit guarantee release upon achieving investment grade ratings.

### The Chewy Phantom Guarantee

The most aggressive formulation: automatic release when a guarantor ceases to be wholly-owned, without any further conditions or agent acceptance requirements.

In the PetSmart/Chewy transaction, Chewy's guarantees of the term loans were automatically released once a partial stake was transferred. No lender consent. No coverage test reconfirmation. The guarantee simply vanished.

**Chewy Blockers** now appear in some documentation, expressly stating that a guarantor cannot resign solely because it ceases to be wholly-owned. But these must be specifically negotiated.

---

## 14.5 The Intercreditor Agreement

When multiple secured creditor classes exist, the **Intercreditor Agreement (ICA)** is the master document governing their relative rights. In European multi-jurisdictional financings, it is essential because no single bankruptcy framework (like U.S. Chapter 11) provides a uniform structure.

### Primary Functions

**1. Ranking in Right of Payment**

The ICA establishes each creditor's relative position in the payment hierarchy. Subordinated creditors contractually agree they will not be repaid until senior creditors are satisfied in full.

This ranking remains valid after collateral enforcement proceeds are distributed—it governs residual unsecured claims.

A typical payment ranking:
1. Senior lender liabilities, hedging liabilities, second lien liabilities, senior secured notes—*pari passu*
2. Parent/holdco notes, senior subordinated debt

Note: Second lien debt is typically *not* payment-subordinated. It ranks equally in right of payment with first lien—the subordination is only regarding security interests.

**2. Ranking of Security Interests**

The ICA separately ranks claims *against the shared collateral*. This is lien priority, distinct from payment priority.

A typical security ranking:
1. Senior lender liabilities, hedging liabilities, senior secured notes
2. Second lien liabilities
3. Any unsecured liabilities with limited shared security

Second lien is lower ranking only regarding collateral enforcement. If collateral proceeds are insufficient, the remaining unsecured claims rank equally with first lien.

**3. Application of Proceeds Waterfall**

The ICA dictates how the Security Agent must distribute enforcement proceeds:

1. Sums owing to Security Agent and other agents
2. Enforcement costs and expenses
3. Super senior revolving credit and hedging liabilities
4. Senior lender liabilities, senior secured notes—*pro rata*
5. Second lien liabilities
6. Any limited-security unsecured liabilities
7. Residual to debtors

### Super Senior Treatment

In structures without a senior secured term loan, the revolving credit facility is typically designated "super senior." The RCF and senior secured notes:
- Rank equally in right of payment
- Share collateral on equal ranking

But on enforcement, RCF is repaid *first* from collateral proceeds. Only after the RCF is satisfied do proceeds flow to the notes.

This is contractual lien subordination: the notes are lien-junior to the RCF despite being pari passu in payment right.

### Unsecured Creditor Accession

Increasingly, future unsecured creditors are *not* required to accede to the ICA. Sponsors prefer this because it avoids practical constraints on incurring permitted unsecured debt.

**The Risk:** Without unsecured creditors being party to the ICA, secured creditors cannot be certain of protecting their priority rights in distress. The ICA governs only those who sign it.

---

## 14.6 The "Soft" Security Reality

European collateral packages are systematically "softer" than U.S. equivalents. ASPs justify leaving hard assets unencumbered, resulting in security limited to:

- **Share pledges** over subsidiaries
- **Intercompany receivables**
- **Bank accounts** (typically operating accounts)

What is often *missing*:
- Real estate mortgages
- Machinery and equipment liens
- Intellectual property pledges
- Inventory and receivables (beyond intercompany)

### The Non-Collateral Asset Pool

This creates a substantial pool of **Non-Collateral assets**—hard operating assets that sit outside the security package. These assets can be:

1. Pledged to secure priming debt (creating effective subordination)
2. Transferred to non-guarantor subsidiaries
3. Sold without proceeds flowing through the Asset Sale waterfall (if structured as Permitted Investments)

The Permitted Liens covenant determines who can grab these Non-Collateral assets. A leverage-based liens carveout or General Liens basket can provide substantial capacity.

### Accell: The Blocker Circumvention

The Accell Group transaction demonstrated how Non-Collateral assets enable priming even with J. Crew blockers in place.

The blocker prohibited IP transfers to *Unrestricted* Subsidiaries. But Accell instead had a *Restricted* non-guarantor subsidiary borrow new money secured by IP that was outside the existing collateral package. The blocker was not triggered—yet existing creditors were effectively primed.

This illustrates why security analysis must go beyond "secured vs. unsecured" to map the actual collateral perimeter and identify Non-Collateral assets.

---

## 14.7 Structural Subordination Risk Mapping

ASPs define not only what assets are pledged but which subsidiaries provide guarantees. This simultaneously defines where **structural subordination risk** exists.

### The Mechanics

Debt incurred by a non-guarantor Restricted Subsidiary is structurally senior to debt at the parent/borrower level. The subsidiary's creditors have direct claims on its assets; the parent's creditors only have a claim on residual equity value.

### Sources of Structural Subordination

**1. Non-Guarantor Debt Baskets**

The Debt covenant typically permits non-guarantor subsidiaries to incur debt under general baskets or ratio capacity. This debt is structurally senior to parent-level obligations.

**2. ASP Exclusions**

Subsidiaries excluded from guarantee requirements by ASPs (cost-benefit, legal limitations, excluded jurisdictions) can incur debt that structurally primes parent creditors.

**3. Wholly-Owned Limitations**

Non-wholly-owned subsidiaries are typically excluded from guarantee requirements. Any debt they incur is structurally senior.

**4. Unrestricted Subsidiaries**

By definition outside the credit group. Debt incurred by Unrestricted Subsidiaries is structurally (and often contractually) senior.

### Quantifying the Risk

True credit analysis requires mapping:

1. Which subsidiaries are guarantors vs. non-guarantors?
2. What is the EBITDA and asset value at each level?
3. What debt capacity exists at non-guarantor subsidiaries?
4. How much value sits in excluded jurisdictions or entities unable to guarantee?

The answers often reveal that substantial enterprise value resides beyond creditors' reach.

---

## Summary: The Credit Support Diligence Framework

**Guarantee Analysis:**
- What is the stated guarantor coverage requirement?
- What is *excluded* from the denominator? (ASPs, legal limitations, non-wholly-owned)
- What is the *actual* coverage of guaranteeable EBITDA?
- Are there Chewy blockers preventing release via minority transfers?
- What automatic release triggers exist?

**Collateral Analysis:**
- What assets are actually in the collateral package?
- What is the universe of Non-Collateral assets?
- Can Non-Collateral assets be pledged to new creditors?
- What Permitted Liens capacity exists for priming?

**ASP Analysis:**
- Which jurisdictions are excluded?
- What cost-benefit thresholds apply?
- What legal limitations restrict upstream guarantees?
- How do ASPs interact with the guarantor coverage test denominator?

**Intercreditor Analysis:**
- What is the payment priority ranking?
- What is the security interest ranking?
- Is there super senior treatment? For what facilities?
- Do future unsecured creditors accede to the ICA?
- What amendment thresholds apply to ranking provisions?

**Structural Subordination Mapping:**
- What value resides at non-guarantor subsidiaries?
- What debt capacity exists at those subsidiaries?
- Where are the Unrestricted Subsidiaries and what assets do they hold?
- How much EBITDA is in excluded jurisdictions?

The gap between headline credit support and actual credit support is where losses occur. Close that gap before you invest.

---

*Next: Part V examines restructuring mechanics—how distressed situations are resolved through Amend & Extend transactions, UK Restructuring Plans, and the case studies that illustrate these principles in action.*
