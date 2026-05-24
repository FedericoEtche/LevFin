# Chapter 12: Voting Rights and Amendments

## Introduction

Before understanding how documentation gets exploited, you must understand how documentation gets *changed*. The amendment provisions within credit documents are the final arbiters of power between borrowers and creditors. These "voting rights" define how the contractual rules can be altered, which creditor protections can be waived, and which rights are truly sacrosanct.

Every aggressive liability management transaction—every drop-down, uptier, and double-dip—begins with a question: *What consent threshold do we need to clear?* The answer determines whether the transaction is possible at all, and whether it can be imposed on unwilling creditors.

This chapter maps the rules of engagement. The chapters that follow show how those rules are exploited.

---

## 12.1 The Consent Hierarchy: Loans vs. Bonds

### Leveraged Loans: The Tiered Structure

Leveraged loan agreements feature a tiered consent hierarchy:

**Majority Lenders (>50%):** Most amendments, waivers, and consents require approval from lenders holding more than 50% of outstanding loans and commitments. This is the default threshold for covenant modifications, waiver of defaults, and most operational changes.

**Supermajority (66.67% or 75%):** Some agreements require higher thresholds for certain significant changes, though this is less common than it once was.

**All Lenders / Each Affected Lender:** Certain fundamental rights—"sacred rights"—require unanimous consent or consent of each directly and adversely affected lender.

**No Lender Consent:** An agent and borrower can typically make certain unilateral changes: correcting technical errors, implementing changes deemed beneficial to lenders (like increased pricing or added credit support), or making "conforming changes" to implement permitted transactions.

### High-Yield Bonds: The Atlantic Divide

High-yield bonds operate under a different framework, and a fundamental difference exists between European and U.S. markets regarding sacred rights.

**European High-Yield Bonds:** Amending sacred rights requires a high supermajority consent—typically **90%** of outstanding principal. Critically, if this threshold is met, the amendment binds *all* bondholders, including the non-consenting minority. This is an "all or nothing" regime where a 10% minority can be dragged into unfavorable terms.

**U.S. High-Yield Bonds:** The standard is much stricter. Amending a sacred right requires consent from *each affected holder*. This gives every individual bondholder an effective veto over changes to their core economic terms. A non-consenting holder cannot be forced into accepting modified economics.

This distinction has profound implications. In Europe, if a sponsor can assemble 90% support—through persuasion, coercion, or manufacturing a friendly creditor base—they can impose terms on the entire bondholder class. In the U.S., holdouts retain individual protection.

---

## 12.2 Sacred Rights: The Supposedly Untouchable

"Sacred rights" represent the core economic terms that creditors expect to be protected by the highest consent thresholds. Traditionally, these include:

### The Universal Sacred Rights

**Principal Amount:** Reductions to the principal amount owed require consent of each affected lender/holder.

**Maturity Date:** Extensions of the final maturity date require heightened consent.

**Interest Rate:** Reductions to the stated interest rate require consent of affected parties.

**Pro Rata Sharing:** Provisions governing the pro rata distribution of payments among creditors are typically sacred.

### The Not-So-Sacred

Here is where the trap lies. In many documents—particularly European high-yield bonds—certain protections that *appear* fundamental are **not** classified as sacred rights:

**Subordination:** The right not to be subordinated to new debt is often *not* a sacred right. This means a majority (50.1%) can consent to amendments that permit the incurrence of new super-priority debt, leaving minority creditors effectively junior.

**Collateral Release:** Release of collateral may require only majority consent, not unanimity.

**Guarantor Release:** Similarly, release of guarantors may not be a sacred right.

**Ranking Changes:** Modifications to lien priority or payment waterfall may be amendable by simple majority.

This gap between perceived protection and actual protection is the foundational enabler of uptier transactions. Creditors who believe their ranking is protected discover—too late—that it can be changed over their objection.

---

## 12.3 The Intercreditor Agreement: Europe's Structural Defense

In European multi-tranche financings, the **Intercreditor Agreement (ICA)** provides a critical structural defense that does not exist in the same form in U.S. documentation.

### The ICA's Function

The ICA is a separate contract that sits above the individual facility agreements. Its primary function is to contractually define the relative ranking, payment priority, and enforcement rights among different creditor classes. Key provisions include:

**Payment Waterfall:** Specifies the precise order in which enforcement proceeds are distributed among super-senior, senior, mezzanine, and other creditor classes.

**Payment Stops:** Allow senior creditors to deliver a notice that temporarily blocks payments to junior creditors upon certain defaults.

**Enforcement Standstills:** Prohibit junior creditors from taking enforcement action for a set period, giving senior creditors control over the restructuring process.

**Turnover Provisions:** Require junior creditors who receive payments out of waterfall order to turn those amounts over to senior creditors.

### Why the ICA Blocks Serta-Style Uptiers

Because the ICA contractually defines the payment and enforcement waterfall and typically requires **all-lender consent** to amend it, a simple majority of lenders cannot vote to subordinate a minority without breaching this separate agreement.

In a U.S. credit agreement, the intercreditor terms are often embedded within the credit agreement itself—amendable by whatever threshold the credit agreement specifies. In Europe, the standalone ICA creates a separate contractual barrier.

This is why Serta-style uptier transactions are significantly harder to execute in the European leveraged loan market. The ICA must be amended to permit the new ranking, and that amendment requires all-lender consent.

**However:** European high-yield bonds often lack equivalent protection. Subordination is rarely a sacred right in bond indentures, and there is no separate ICA governing inter-bondholder rights. This makes European bonds *more* vulnerable to uptier transactions than European loans—an inversion of the traditional assumption that bonds have stronger covenants.

---

## 12.4 Altering the Vote: Disenfranchisement Tactics

Borrowers and sponsors have developed sophisticated tactics to manipulate voting dynamics and push through contentious amendments.

### "Snooze-You-Lose" Provisions

Common in European loan agreements, these provisions streamline the amendment process by deeming non-responding lenders to have **consented** to a proposal after a specified period (typically 10-15 business days).

The logic is administrative efficiency: lenders who don't respond are assumed to acquiesce. The effect is to reward passivity with consent, allowing borrowers to achieve approval thresholds by exploiting creditor inattention.

### "Snooze-Drag" Provisions

A more aggressive variant gives the borrower the option to **automatically include** silent lenders in the consenting group. Non-responders are not just deemed to consent—they are dragged into the new terms entirely, including any fee arrangements or amended economics.

### Net Short Lender Disenfranchisement

Some credit agreements strip voting rights from lenders who hold a "net short" position against the borrower's debt—for example, through credit default swaps that profit from default.

The rationale: a net short lender has misaligned incentives and may vote to precipitate default rather than preserve enterprise value. These lenders are typically deemed to vote in the same proportion as non-net-short lenders, neutralizing their influence.

### Affiliate Lender Provisions

When sponsors or their affiliates purchase loans in the secondary market, they become lenders with voting rights. Aggressive documents include provisions that:

- Cap affiliate lender voting power at a specified percentage
- Require affiliate-held loans to vote pro rata with non-affiliate lenders
- Exclude affiliate holdings from quorum and approval calculations

Weak or absent affiliate lender restrictions allow sponsors to manufacture voting majorities by purchasing their own debt.

### Vote Rigging Through New Issuance

The most aggressive tactic: an issuer strategically issues new debt to friendly creditors who have **pre-agreed** to consent to a controversial amendment. This manufactured majority then approves the change, overriding objections from legacy creditors.

**Case Study: Intralot (2021)**

The gaming company issued new notes to a locked-up group of creditors, enabling them to cross the 90% consent threshold needed to amend the sacred rights of existing notes. The new creditors were brought in specifically to provide the votes—a manufactured supermajority that bound non-consenting legacy holders.

---

## 12.5 The Yank-a-Bank Mechanism

Credit agreements typically include provisions allowing borrowers to remove non-cooperative lenders from the syndicate. These "yank-a-bank" or "replacement lender" provisions permit the borrower to:

1. Identify a lender who has refused to consent to a requested amendment
2. Find a replacement lender willing to purchase that lender's position
3. Force the non-consenting lender to sell at par (or par plus accrued interest)

### Strategic Use

In A&E transactions, borrowers use yank-a-bank to remove lenders who refuse to extend. The non-consenting lender receives par and exits; a new lender enters with extended maturity commitments. The borrower achieves its extension without unanimous consent.

### Limitations

Yank-a-bank typically cannot be used to remove lenders who are exercising legitimate rights (like refusing to fund a draw that would breach covenants). And it only works if the borrower can find a willing replacement—not guaranteed in distressed situations.

---

## 12.6 Open Market Purchases and Dutch Auctions

Borrowers can repurchase their own debt in the open market, reducing outstanding principal and—critically—altering the denominator for voting calculations.

### The Strategic Dynamic

If a borrower purchases €100 million of a €500 million loan, the voting base drops to €400 million. A majority now requires only €200 million of consenting lenders rather than €250 million.

More aggressively: if purchased debt is held by an affiliate and affiliate lender provisions are weak, the borrower effectively controls those votes.

### Dutch Auctions

In a Dutch auction, the borrower invites lenders to submit offers to sell at specified prices (typically below par). The borrower then accepts offers from the lowest price up until its repurchase budget is exhausted.

Dutch auctions allow borrowers to retire debt at a discount while rewarding lenders willing to exit at the lowest price—often those most pessimistic about recovery prospects.

---

## 12.7 Amendment Mechanics: The Procedural Realities

### In Leveraged Loans

1. **Borrower Request:** Borrower submits amendment request to Administrative Agent
2. **Agent Distribution:** Agent circulates request to all lenders with voting deadline
3. **Lender Response:** Lenders submit consent or rejection (subject to snooze provisions)
4. **Threshold Calculation:** Agent determines if required consent threshold is met
5. **Effectiveness:** If threshold met, amendment becomes effective; if not, request fails or is modified

### In High-Yield Bonds

1. **Consent Solicitation:** Issuer launches formal consent solicitation with offering documents
2. **Record Date:** Determines which holders are entitled to vote
3. **Voting Period:** Holders submit consents or withhold (typically 20-30 days)
4. **Threshold Calculation:** Trustee or tabulation agent calculates results
5. **Supplemental Indenture:** If threshold met, parties execute supplemental indenture implementing changes

### The "Exit Consent" Coercion

In bond exchange offers, issuers frequently pair new note offerings with exit consents. Holders who tender their old notes into the exchange simultaneously consent to amendments stripping covenants from any old notes that remain outstanding.

This creates coercive pressure: if you don't participate, you're left holding covenant-less paper. The exit consent transforms a voluntary exchange into a near-compulsory transaction.

---

## 12.8 Structural Adjustments in European Loans

European leveraged loans feature a distinctive amendment mechanism called the "Structural Adjustment" provision, commonly used for A&E transactions.

### The Opt-In Mechanic

Unlike a standard amendment that binds all lenders, a Structural Adjustment operates as an opt-in:

1. Borrower proposes new terms (extended maturity, revised pricing, amended covenants)
2. Each lender individually decides whether to accept the new terms
3. Accepting lenders roll into a new tranche with the revised terms
4. Non-accepting lenders remain in the original tranche with original terms

### Implications

**For Borrowers:** Structural Adjustments allow maturity extensions without unanimous consent. Willing lenders get extended; unwilling lenders can be yanked or left in a shrinking legacy tranche.

**For Lenders:** The mechanism preserves optionality—you can't be dragged into worse terms—but creates pressure to participate. A shrinking legacy tranche becomes illiquid and potentially subordinated if the extended tranche receives covenant sweeteners.

---

## Summary: The Amendment Playbook

Understanding amendment mechanics requires answering these questions for any credit document:

**Threshold Analysis:**
- What is the majority lender threshold? (Usually 50%, but verify)
- What requires supermajority? What percentage?
- What are the sacred rights, and what threshold protects them?
- Is subordination a sacred right? (Often not in European HY bonds)

**Structural Protections:**
- Is there a separate Intercreditor Agreement?
- What does the ICA require to amend ranking provisions?
- Can the ICA be amended without all-lender consent?

**Disenfranchisement Risk:**
- Are there snooze-you-lose or snooze-drag provisions?
- What are the affiliate lender restrictions?
- Can net short lenders vote?

**Procedural Vulnerabilities:**
- Can the borrower issue new debt to friendly parties?
- Are there yank-a-bank provisions?
- How are open market purchases treated for voting purposes?

**Coercion Mechanisms:**
- Is exit consent permitted in exchange offers?
- How does Structural Adjustment work in this document?

The creditor who understands these mechanics can anticipate—and potentially block—aggressive transactions before they're executed. The creditor who doesn't will learn the rules only after being subordinated.

---

*Next: Chapter 13 examines how these amendment mechanics are weaponized in Liability Management Transactions—the polished term for what is, in practice, creditor-on-creditor violence.*
