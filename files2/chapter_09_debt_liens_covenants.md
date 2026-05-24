# Chapter 9: Debt and Liens Covenants

## Introduction

Chapter 8 explained how value *leaves* the credit box—through dividends, investments, and the various trap doors sponsors use to extract cash. This chapter addresses the opposite problem: how additional *leverage* gets layered on top of your position.

If the Restricted Payments covenant is the dam holding back value from flowing to equity, the Debt and Liens covenants are the throttle controlling how much senior or pari passu debt can be stacked above you. Understanding these covenants is essential because in distress, your recovery depends not just on what remains in the credit box, but on how many other creditors are competing for it—and whether they're ahead of you in line.

---

## 9.1 The Two Questions

Every time a borrower wants to incur new secured debt, there are two separate questions that must be answered:

**Question One: Can the borrower incur this debt?**
This is governed by the Debt covenant (or "Limitation on Indebtedness").

**Question Two: Can the borrower secure it?**
This is governed by the Liens covenant.

These are independent inquiries. Having capacity under the Debt covenant does not automatically mean the debt can be secured. Having capacity under the Liens covenant is useless without permission to incur the debt in the first place. For secured debt to be permitted, you need separate permissions in *both* covenants.

This independence creates opportunity for issuers—and traps for analysts who only check one covenant. It also means that answering a seemingly simple question—"What's this company's secured debt capacity?"—requires working through two parallel analyses and understanding how the pieces fit together.

---

## 9.2 The Dual-Track System: Ratio Debt vs. Permitted Debt

Modern debt covenants bifurcate capacity into two distinct channels:

### Ratio Debt

The first paragraph of most debt covenants permits unlimited debt incurrence provided a pro forma financial ratio is satisfied. In high yield bonds, this is typically a 2.0x Fixed Charge Coverage Ratio. In leveraged loans, it's often a leverage test (Total Net Leverage or Senior Secured Net Leverage).

Ratio Debt has no dollar cap. If you can meet the ratio after giving pro forma effect to the new debt, you can incur as much as mathematics allows.

### Permitted Debt (Baskets and Carveouts)

Below the ratio test sits a list of specific "baskets" that permit debt incurrence *regardless* of whether the ratio is satisfied. These include the Credit Facilities basket, General Debt basket, Acquisition Financing basket, Capital Lease/Purchase Money basket, and numerous others.

The critical point: **these baskets are cumulative to the Ratio Debt test, not alternative to it.**

If the ratio test is unavailable because pro forma leverage is too high, the borrower can still incur debt under any basket with remaining capacity. Conversely, if the borrower *can* meet the ratio test, it can choose to use Ratio Debt capacity to preserve its baskets for later.

### The "Ratio Disregard" Multiplier

Here's where it gets dangerous. In many documents, debt incurred under Permitted Debt baskets is *disregarded* when calculating the ratio for subsequent Ratio Debt incurrence.

The mechanic works like this:
1. Borrower incurs Ratio Debt up to maximum leverage limit (say, 4.0x)
2. Borrower then incurs Permitted Debt under various baskets
3. When calculating whether *more* Ratio Debt can be incurred, the Permitted Debt is excluded from the calculation
4. Result: actual leverage exceeds the headline ratio cap

This "no double counting" rule allows a borrower to incur Ratio Debt to the theoretical limit and *then* layer Permitted Debt on top, effectively blowing through any leverage ceiling the ratio appeared to impose.

---

## 9.3 The Major Permitted Debt Baskets

Understanding the major baskets is essential because each represents a potential source of additional leverage that can dilute or prime your position.

### The Credit Facilities Basket

This is typically the largest and most important carveout. It permits debt under a revolving credit facility, term loans, and related instruments up to a specified amount.

The sizing follows a familiar pattern:
- A fixed dollar amount (e.g., €200 million), *or*
- A percentage of Consolidated EBITDA (the "grower"), *or*
- Debt up to a specified Secured Leverage Ratio

The grower component means this basket expands as the company grows—and as EBITDA gets inflated through aggressive add-backs. A basket sized at "the greater of €200 million or 100% of EBITDA" could be €200 million on day one but €400 million three years later.

In bond documents, this basket is broadly drafted to include *any* debt facility—loans, bonds, commercial paper. It functions as a revolving bucket of secured capacity that refills as debt is repaid.

### The General Debt Basket

Most covenants include a catch-all basket permitting additional debt up to a capped amount, often with a grower alternative. Unlike the Credit Facilities basket, this is usually available for any purpose.

Whether this debt can be secured depends on the Liens covenant. Some documents include a parallel Permitted Liens carveout for the General Debt basket; others do not. Check both.

### The Acquisition Financing Basket

This permits debt incurred specifically to fund acquisitions, usually subject to a leverage test. The test typically requires that leverage not *increase* as a result of the acquisition—but with synergy add-backs and EBITDA credit for the target, this can be satisfied even when actual debt increases substantially.

### The Incremental Equivalent / "Side-Car" Basket

Bond-style loans often permit incurrence of debt *outside* the credit agreement that is economically equivalent to incremental debt under the agreement. This "side-car" capacity allows borrowers to raise term loans or other debt from third parties without going through the existing lender group.

### The Refinancing Indebtedness Carveout

This permits new debt to refinance existing debt, subject to conditions (principal amount limits, maturity requirements, ranking requirements). The trap: these conditions are often looser than they appear, and the carveout can be used to reshape the capital structure.

### The Non-Guarantor Debt Basket

Many covenants permit non-guarantor subsidiaries to incur debt up to a specified cap (or sometimes uncapped). This debt is *structurally senior* to your position—the subsidiary's creditors get paid from that subsidiary's assets before anything flows up to service your debt.

---

## 9.4 Incremental Facilities: The Accordion

The "Incremental Facility" or "Accordion" provisions allow borrowers to increase leverage within existing documentation without seeking full lender consent. This is leverage-on-demand.

### The Standard Accordion Structure

**The Freebie (Starter) Basket:** A fixed amount available immediately with no conditions—typically €50-100 million or a percentage of EBITDA.

**The Prepayment Basket:** Capacity that builds from voluntary prepayments or buybacks. If you prepay €50 million of term loans, that capacity can be "recycled" into new incremental debt.

**The Ratio-Based (Unlimited) Basket:** Unlimited capacity subject to compliance with a leverage test (First Lien, Senior Secured, or Total Net Leverage).

### The Maturity Erosion Problem

Historically, incremental debt was required to mature *no earlier* than the existing term loans (the "Inside Maturity" rule). This protected existing lenders from being subordinated in time.

This protection has eroded significantly. Modern documents include exceptions for:
- Bridge loans with short maturities
- Escrow debt
- "Customary" exclusions
- Specific capped baskets for inside maturity debt

The result: sponsors can layer in shorter-dated debt that effectively primes the original lenders in the maturity queue.

### The MFN Sunset

"Most Favored Nation" provisions historically required that incremental debt pricing not exceed existing debt pricing by more than a specified margin (typically 50 basis points). If the incremental debt was priced higher, existing debt spreads would step up to match.

MFN protections now routinely sunset after 6-12 months, and increasingly don't apply at all to debt incurred under separate "side-car" facilities. This removes pricing discipline for later tranches.

---

## 9.5 The Liens Covenant

The Liens covenant determines *how much* of the debt permitted by the Debt covenant can be *secured*—and on what assets, with what priority.

### Negative Pledge vs. True Liens Covenant

There are two fundamental architectures:

**Negative Pledge (Unsecured Bonds):** Does not limit how much debt can be secured. Instead, it provides that if other debt gets secured by collateral, the bonds must also be equally and ratably secured by the same collateral. The "Permitted Liens" definition carves out exceptions where the issuer can grant security *without* extending it to the bonds.

**True Liens Covenant (Secured Bonds/Loans):** Flatly prohibits the issuer from granting any liens except as permitted by the "Permitted Liens" (for non-collateral assets) and "Permitted Collateral Liens" (for collateral assets) definitions.

### The European Blended Approach

Most European secured high yield bonds use a blended structure:

- **For Collateral assets:** A true liens covenant applies. Liens on collateral are prohibited unless a "Permitted Collateral Liens" carveout permits them.

- **For Non-Collateral assets:** A negative pledge applies. Debt can be secured on non-collateral assets if a "Permitted Liens" carveout permits it, *or* if the bonds are equally and ratably secured.

This distinction matters enormously. European collateral packages are often limited to share pledges and certain bank accounts—meaning vast pools of operating assets sit *outside* the collateral package. The Permitted Liens definition determines who can grab those assets.

### The Major Permitted Liens Carveouts

**Credit Facilities Liens Basket:** Almost universally, debt incurred under the Credit Facilities debt basket can be secured. This is the primary channel for secured debt capacity.

**Leverage-Based Liens Carveout:** Many documents permit liens securing *any* debt (not just Credit Facilities debt) if a pro forma secured leverage test is satisfied.

**General Liens Basket:** A capped basket permitting liens on any assets securing any debt. This can be paired with any Debt covenant permission.

**Liens on Non-Guarantor/Foreign Sub Assets:** Permits these subsidiaries to pledge their assets to secure their own debt.

**Refinancing Liens:** Permits new liens that replace existing liens, subject to conditions that are often weaker than they appear.

---

## 9.6 The Secured Debt Capacity Analysis

Answering "What's this company's secured debt capacity?" requires working through both covenants systematically.

### The Mix-and-Match Principle

The Debt covenant permissions and Liens covenant permissions can be combined in multiple ways. You should not assume that the General Debt basket can only be secured under the General Liens basket, or that Ratio Debt can only be secured under a leverage-based liens carveout.

An issuer with Ratio Debt capacity could secure that debt using:
- The leverage-based liens carveout
- The General Liens basket
- Any other available Permitted Liens

This flexibility multiplies secured debt capacity beyond what any single basket would suggest.

### Why the Secured Leverage Test is NOT a Cap

This is the most common analytical error. A 4.0x Secured Leverage test in the liens covenant does *not* mean the company cannot exceed 4.0x secured leverage.

Here's why: each carveout is separate and independent. If the company cannot meet the 4.0x test, that specific carveout is unavailable—but the company can still incur secured debt under other Permitted Liens:
- The Credit Facilities basket (which may have its own size or ratio test)
- The General Liens basket
- Deal-specific carveouts

The leverage test is *one* source of liens capacity, not a ceiling on total secured debt.

### Worked Example

Consider a company with the following covenant structure:

*Debt Covenant:*
- Ratio Debt: Available at 2.0x FCCR
- Credit Facilities basket: Greater of €200M or Secured Leverage ≤ 4.0x
- General Debt basket: €50M

*Liens Covenant:*
- Credit Facilities basket debt may be secured
- Leverage-based liens: Any debt may be secured at Secured Leverage ≤ 4.5x
- General Liens basket: €75M

If current Secured Leverage is 4.2x:
- The Credit Facilities basket ratio prong is unavailable (4.2x > 4.0x)
- But the €200M fixed amount is still available
- The leverage-based liens carveout is also unavailable (4.2x > 4.5x)
- But the General Liens basket provides €75M of capacity

Secured debt capacity = €200M (Credit Facilities, fixed amount) + €75M (General Liens) + any capacity to incur *unsecured* debt that could be secured through creative structuring.

---

## 9.7 Getting Primed: The Priority Hierarchy

Understanding how debt achieves priority over your position is critical for distress analysis.

### Structural Subordination

Debt at non-guarantor subsidiaries is structurally senior to debt at the parent or guarantor level. The subsidiary's creditors get paid from that subsidiary's assets before anything flows up.

Sources of structurally senior debt capacity:
- Non-Guarantor Debt basket in the Debt covenant
- Investments into Unrestricted Subsidiaries (who can then incur unconstrained debt)
- Weak or non-existent guarantor coverage requirements

The interaction with Restricted Payments is important: a company can use RP capacity to invest in an Unrestricted Subsidiary, which then incurs debt secured by assets that were previously available (indirectly) to support your position.

### Lien Subordination: Super Senior Debt

In European structures, lien subordination is primarily contractual—set out in the Intercreditor Agreement.

The most common form is **Super Senior** debt: typically the revolving credit facility and hedging obligations. Super senior creditors share the *same* liens on the *same* collateral as term loan and bond holders—but the Intercreditor Agreement provides that on enforcement, proceeds go *first* to the super senior creditors.

Check the Permitted Collateral Liens definition: it specifies which debt can be secured on a super senior basis. This is usually limited to the Credit Facilities basket (or a portion of it) and hedging obligations—but the basket may be sized well above the day-one RCF, leaving room for additional super senior debt.

### Effective Subordination: Liens on Non-Collateral

In secured deals, debt secured on non-collateral assets is effectively senior to the bonds/loans with respect to those assets.

If the collateral package consists only of share pledges and certain bank accounts, operating assets like real estate, equipment, and receivables may be available to secure other debt. The Permitted Liens definition determines capacity for this effectively senior debt.

This is why European collateral analysis must go beyond "secured vs. unsecured." The relevant questions are:
1. What assets are actually pledged?
2. What assets are *outside* the collateral package?
3. Who can grab those non-collateral assets?

### The Priming Playbook

Distressed situations reveal the full priming toolkit:

**Inside Maturity Priming:** Layering shorter-dated debt that must be repaid first.

**Super Senior Priming:** Expanding the super senior tranche through covenant capacity.

**Structural Priming:** Moving assets to non-guarantor subsidiaries that incur local debt.

**Effective Priming:** Securing new debt on non-collateral assets, diluting the collateral pool's relative value.

**Double-Dip Structures:** Dropping assets to an Unrestricted Subsidiary, which issues secured debt, with proceeds lent back to the Restricted Group as a secured intercompany loan—giving new money creditors two recovery claims.

---

## Summary

The Debt and Liens covenants determine how much additional leverage can be stacked above or alongside the existing creditor position. Key principles:

1. **Two independent questions:** Can the borrower incur this debt? Can the borrower secure it? Both must be satisfied for secured debt.

2. **Ratio Debt and Permitted Debt are cumulative:** The ratio test is not a ceiling; baskets provide additional capacity.

3. **The mix-and-match principle:** Debt covenant permissions and Liens covenant permissions combine flexibly.

4. **Secured leverage tests are not caps:** They're one carveout among many.

5. **The blended European approach:** Collateral assets face true liens restrictions; non-collateral assets face a negative pledge with extensive carveouts.

6. **Multiple paths to priming:** Structural subordination, super senior debt, effective subordination, and inside maturity debt all dilute your recovery.

The best credit analysts map all sources of potential leverage—not just what's outstanding today, but what *could* be incurred tomorrow.

---

*Next: Chapter 10 covers the remaining key negative covenants—asset sales, merger restrictions, affiliate transactions, and change of control provisions.*
