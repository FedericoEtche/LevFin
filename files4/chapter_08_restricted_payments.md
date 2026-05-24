# CHAPTER 8
## Restricted Payments — The Heart of the Fight

---

### Why This Chapter Matters

If you learn nothing else from this book, learn this chapter.

The Restricted Payments covenant is where the real battle between sponsors and lenders is fought. It's where value leaves the credit box. It's where sponsors extract returns, fund dividends, and — if the documentation is weak — strip assets while lenders watch helplessly.

Every major creditor-on-creditor fight of the past decade traces back to RP capacity: J.Crew, Serta, Chewy, Pluralsight. The sponsors didn't break the rules. They found ways to use the RP covenant — or bypass it — that lenders never anticipated when they signed the documents.

This chapter will teach you how the RP covenant actually works, where it fails, and what to look for in every deal you touch.

---

### 8.1 The Credit Box Concept

Before diving into mechanics, understand what we're protecting.

The "credit box" is the ring-fenced group of entities that secure the lenders' debt. When you make a loan to a leveraged borrower, you're lending to a corporate structure — a parent company, its subsidiaries, their assets, and their cash flows. The credit box is supposed to keep all of that value inside, available to service and repay your debt.

The Restricted Payments covenant is the wall around that box. It limits the borrower's ability to:

- **Pay dividends** to equity holders
- **Make distributions** to parent companies
- **Repurchase equity** or subordinated debt
- **Make investments** in unrestricted subsidiaries

Every dollar that leaves the credit box through one of these channels is a dollar that's no longer available to repay lenders. The RP covenant exists to control that leakage.

The problem: sponsors are very, very good at finding holes in the wall.

---

### 8.2 The Builder Basket: How Capacity Accumulates

The most important concept in the RP covenant is the "builder basket" — a cumulative pool of capacity that grows (or shrinks) over time based on the borrower's financial performance.

#### The Basic Mechanics

The builder basket typically starts at a fixed amount (often $1 or zero) and grows based on Consolidated Net Income (CNI). The standard formulation:

**50% of cumulative CNI** (if positive) is added to the basket.

But here's the trap that catches most junior bankers: losses hit the basket at 100%, not 50%.

This asymmetry is brutal. A company that earns $100 million one year adds $50 million to the basket. But if it loses $100 million the next year, the entire $100 million is deducted. Two years of performance, net zero profit, and the basket is *negative* $50 million.

This is the "dinging the builder" problem, and it's one of the most important concepts in RP analysis.

#### Positive Adjustments

The basket doesn't just grow from CNI. Most documentation includes "positive adjustments" that add capacity:

- **Equity contributions** — fresh equity invested in the borrower
- **Asset sale proceeds** — money received from selling assets (subject to reinvestment requirements)
- **Debt-to-equity conversions** — when subordinated debt is converted to equity
- **Returns on investments** — dividends or proceeds from investments in unrestricted subsidiaries

These adjustments can dramatically increase RP capacity beyond what CNI alone would suggest. In some deals, the positive adjustments dwarf the CNI component.

#### The Ratio Governors

Even if the builder basket has capacity, most deals require the borrower to meet a financial test before using it. These are the "ratio governors":

- **Fixed Charge Coverage Ratio (FCCR)** — typically must be at least 2.0x
- **Leverage test** — often must be below a specified multiple (e.g., inside leverage)

The ratio governor acts as a gate. You can have all the builder basket capacity in the world, but if you can't meet the ratio test on a pro forma basis, you can't use it.

---

### 8.3 The Permitted Baskets

Beyond the builder basket, RP covenants include a menu of "permitted" restricted payments — fixed-dollar or ratio-based carveouts that allow specific types of distributions regardless of builder basket capacity.

#### Fixed-Dollar Baskets

These are straightforward: a set amount (e.g., "$25 million per year" or "$50 million in aggregate") available for restricted payments without any ratio test.

Common fixed baskets include:

- **General RP basket** — catch-all capacity for dividends and distributions
- **Management equity repurchases** — buying back stock from departing executives
- **Tax distributions** — allowing pass-through entities to fund owners' tax obligations

#### Ratio-Based Carveouts

More aggressive deals include ratio-based RP capacity that exists outside the builder basket entirely. If the borrower can meet a specified leverage test (e.g., Total Leverage < 4.0x), it may have unlimited RP capacity.

This is a major documentation fight. Lenders want RP capacity tied to the builder basket, which tracks actual performance. Sponsors want ratio-based capacity, which can be manufactured through EBITDA add-backs and favorable definitions.

#### Tax Distributions

Almost every deal allows distributions to fund tax obligations of parent entities in structures where the borrower is a pass-through for tax purposes. These are usually uncapped and not subject to ratio tests.

Watch the definition carefully. Aggressive sponsors have used "tax distribution" baskets to move significant value outside the credit box by inflating the deemed tax liability.

---

### 8.4 The "Dinging" Trap — Where Deals Go Wrong

This is where most junior bankers get lost, and where most lenders get hurt.

#### The Interaction Problem

RP covenants don't exist in isolation. They interact with:

- The **Debt covenant** (what debt can be incurred)
- The **Liens covenant** (what collateral can be pledged)
- The **Asset Sale covenant** (what happens to sale proceeds)
- The **Investment covenant** (what investments can be made)

The builder basket in the RP covenant is often *shared* with these other covenants. Use capacity for one purpose, and it's no longer available for another.

But here's the critical issue: **not all uses "ding" the basket equally**.

#### The Leverage-Based RP Problem

Consider a borrower with $100 million of builder basket capacity and a leverage-based RP test requiring Total Leverage below 4.0x.

The borrower is at 3.5x leverage. It has both (a) builder capacity and (b) ratio compliance. So it pays a $50 million dividend.

What happens?

The $50 million leaves the credit box. That's $50 million less cash on the balance sheet. Net debt goes up. EBITDA stays the same. Leverage is now higher — maybe 3.8x.

The borrower still has $50 million of builder capacity left. And it still meets the 4.0x ratio test. So it pays another dividend...

This is how RP covenants can be "run" — used repeatedly until the builder basket is exhausted or the ratio test finally binds. And by that point, significant value has left the credit box.

#### What to Check in Every Deal

When analyzing an RP covenant, ask:

1. **What's the starting basket?** Zero is safer than a large fixed amount.
2. **How does CNI accumulate?** 50% up / 100% down is standard. Watch for more aggressive formulations.
3. **What are the positive adjustments?** Large equity contribution add-backs can inflate capacity.
4. **What's the ratio governor?** Higher tests (2.25x FCCR vs 2.0x) are more protective.
5. **Are there uncapped ratio-based carveouts?** These can bypass the builder basket entirely.
6. **How do the baskets interact?** Shared capacity across covenants is more protective than separate baskets.

---

### 8.5 The Dividend-to-Debt Toggle

One of the most structurally destructive developments in leveraged finance documentation is the "dividend-to-debt toggle" — the ability to redesignate RP capacity as debt incurrence capacity.

#### How It Works

Imagine a borrower has $100 million of unused RP capacity. Instead of paying a dividend (which would reduce equity), it can:

1. Use the RP capacity to make a "permitted investment" in an unrestricted subsidiary
2. The unrestricted subsidiary incurs new debt
3. The proceeds flow back up as a dividend

The result: the same $100 million leaves the credit box, but now there's *additional debt* at the unrestricted subsidiary level. The sponsor got its dividend, AND the overall enterprise has more leverage.

This is the "dividend-to-debt toggle" in action. It converts shareholder-friendly capacity into creditor-unfriendly outcomes.

#### Why This Matters

The toggle isn't a bug — it's a feature. Sponsors negotiate for flexibility, and the interaction between RP capacity and investment capacity creates this optionality.

From a lender's perspective, this is structurally problematic. You sized the debt based on certain leverage levels. The toggle allows the sponsor to increase enterprise leverage while extracting value, without technically breaching any covenant.

---

### 8.6 The J.Crew Trap Door

No discussion of RP covenants is complete without J.Crew.

#### What Happened

In 2016-2017, J.Crew — struggling with operational challenges — executed a series of transactions that moved valuable intellectual property (its brand trademarks) outside the credit box and used them to raise new debt that effectively primed existing lenders.

The mechanics:

1. J.Crew had RP capacity under its builder basket
2. It used this capacity to make an "investment" — transferring IP to an unrestricted subsidiary
3. The unrestricted subsidiary was outside the lender collateral package
4. That subsidiary then borrowed money against the IP
5. The proceeds went back to the company, but the IP was gone

Lenders were left with claims against a borrower whose most valuable asset — the brand — was no longer available to satisfy their debt.

#### The Two-Step Pass-Through

The J.Crew structure worked because of how the RP covenant interacted with the Investment covenant:

**Step 1:** Use RP capacity to make an investment in an unrestricted subsidiary (permitted under the Investment covenant)

**Step 2:** The unrestricted subsidiary is, by definition, outside the credit box — so it can do whatever it wants, including pledging assets to new lenders

This "two-step pass-through" is now the template for sponsor value extraction. Every sophisticated sponsor knows this playbook.

#### Why It Matters for Every Deal Since

J.Crew wasn't just one bad deal. It revealed a structural flaw in standard documentation: the interaction between RP capacity, investment baskets, and unrestricted subsidiary designations creates a path for asset stripping that lenders didn't adequately price.

After J.Crew, every sophisticated lender asks: **"Can this happen to us?"**

---

### 8.7 Fighting Back: Blockers and Hardening

Post-J.Crew, lenders have developed defensive documentation provisions — "blockers" designed to prevent the most aggressive uses of RP and investment capacity.

#### J.Crew Blockers

The first generation of defensive provisions focused specifically on the J.Crew structure:

- **IP transfer restrictions** — limiting the ability to move intellectual property to unrestricted subsidiaries
- **Material asset restrictions** — requiring that "material" assets remain within the credit box
- **Designation limitations** — tightening the conditions for designating subsidiaries as "unrestricted"

These blockers appear in most post-2017 deals, but their effectiveness varies. The definitions matter: what counts as "intellectual property"? What makes an asset "material"? Aggressive sponsors negotiate carveouts that can swallow the protection.

#### Pluralsight Blockers

The Pluralsight situation (2020) revealed another gap. Even with J.Crew blockers in place, sponsors found ways to:

- Transfer value through intercompany transactions at less-than-arm's-length terms
- Use permitted investments to fund unrestricted subsidiaries that then competed for assets in a restructuring

"Pluralsight blockers" attempt to address these issues by:

- Requiring arm's-length terms for intercompany transactions
- Limiting the ability of unrestricted subsidiaries to acquire debt or assets of the restricted group
- Adding creditor protections in "trap door" scenarios

#### Post-LME Covenant Hardening

The wave of liability management exercises (Serta, TriMark, Envision) in 2020-2022 led to broader covenant hardening:

- **Anti-priming provisions** — limiting the ability to subordinate existing debt
- **Pro-rata sharing requirements** — ensuring all lenders are treated equally in any restructuring transaction
- **Voting right protections** — preventing "strip and flip" transactions that concentrate control

These provisions go beyond RP-specific blockers to address the broader documentation weaknesses that LMEs exploit.

---

### 8.8 What 20 Years Teaches You About RPs

[FEDERICO — THIS SECTION IS FOR YOU]

This is where the chapter becomes yours. The material above is mechanics — important, but available to anyone who reads the documentation carefully.

This section is different. It's what you know that isn't written down anywhere. Some prompts:

**What do you look for first?**
When you open an RP covenant for the first time, what's your pattern? What jumps out to you after 20 years that a junior banker would miss?

**What's the biggest RP disaster you've seen?**
Not the famous cases — J.Crew, Serta — but something you lived through. What happened? What did you learn?

**When do you know a deal is in trouble?**
Are there early warning signs in how borrowers use their RP capacity that signal problems ahead?

**What advice would you give your 25-year-old self?**
If you could go back to your first LevFin role, what would you tell yourself about RP covenants specifically?

**What do sponsors know that lenders don't?**
After 20 years on the bank side, watching sponsors operate — what have you learned about how they think about RP capacity?

---

### Chapter Summary

The Restricted Payments covenant is the heart of the leveraged finance documentation fight. It controls how value leaves the credit box and — when well drafted — protects lenders from the most aggressive forms of sponsor value extraction.

Key takeaways:

1. **The builder basket is asymmetric** — 50% of gains, 100% of losses. This "dinging" dynamic is critical.

2. **Ratio governors are gates** — capacity means nothing if you can't meet the test.

3. **Baskets interact** — RP, Debt, Liens, and Investments are connected. Understand the linkages.

4. **The dividend-to-debt toggle is real** — sponsors can convert RP capacity into additional leverage.

5. **J.Crew changed everything** — the two-step pass-through to unrestricted subsidiaries is now standard playbook.

6. **Blockers help but aren't perfect** — J.Crew blockers, Pluralsight blockers, and post-LME hardening are necessary but not sufficient.

The best protection is understanding. Know how these provisions work, know how they fail, and know what questions to ask before you sign.

---

*[Chapter word count: ~2,400 words — target for book chapter: 4,000-6,000 words]*

*[Sources: Restricted Payments Covenant Compendium, European Sponsor Playbook: Capacity Reallocation, Plain English Translations: Zero Floor, Carry Forward/Carry Back]*
