# LinkedIn Series — "Credit Agreements Are Bundles of Options"

*Audience: junior LevFin / credit bankers · Tone: measured thought-leadership · CTA: soft, warming slightly at the close*

---

## How to run the series

**Cadence.** One post per week, seven weeks. Consistency matters more than frequency — the same slot each week trains your audience to expect it.

**Best posting window.** Tuesday–Thursday, 7:30–9:00am local. Avoid Mondays and Fridays for finance audiences.

**The arc.** Post 1 reframes (the hook). Posts 2–6 each take one option class and go deep — these are the credibility engine. Post 7 flips to the sponsor's side and synthesizes, with a slightly warmer call to action once seven posts of value are on the record.

**Working the comments.** Every post ends with a soft prompt. When someone engages substantively, reply in-thread first (the algorithm rewards it), then move the real conversation to DMs. That DM is where a 1-on-1 session gets discussed — never in the post itself.

**Continuity.** Each post names its place in the series ("Part 3 of 7") and ends pointing at the next. Returning readers should feel they're following something, not catching scattered posts.

---

## POST 1 — The Launch *(already published)*

Most of us in leveraged finance learn to read a credit agreement as a checklist: incurrence tests, baskets, carve-outs, events of default. Tick, tick, tick.

I've come to read it as something else — a portfolio of options.

I spend my time in two areas that rarely talk to each other: options pricing, and leveraged finance documentation. Put them side by side and the same structure keeps showing up on both.

A leveraged loan is not a loan with covenants attached. The lender holds a near-riskless bond, is short a put on enterprise value — the credit-risk put, in the Merton sense — and is short a whole further bundle of options written to the borrower. The yield is not the price of the credit. The yield is the residual: what is left after subtracting the cost of every option the lender has written.

Seen this way, the covenant package becomes precise instead of vague:

— A make-whole call is a Bermudan call on a defaultable bond.
— An equity cure is a Bermudan put the lender writes to the sponsor.
— A builder basket is an Asian option on cumulative net income.
— Portability is a knock-out on the change-of-control put.

None of this is exotic. It is Black-Scholes, Merton, binomial trees — the toolkit options desks have used for fifty years. What is missing is simply the bridge between that toolkit and the 200-page credit agreement.

For anyone early in a LevFin or credit career, that bridge is a real edge. Two loans can print at the same spread and still differ by 150-200 bps of embedded optionality. Whoever can decompose that sees what the market has compressed into a single number.

I have been writing this framework up properly — the lender's side and the sponsor's side both. Over the next few weeks I'll take it one option class at a time. If it's the kind of thing you'd want to work through in depth, leave a comment or send me a message.

---

## POST 2 — Call Protection *(Part 2 of 7)*

Last week I argued a credit agreement is a portfolio of options. This week, the one almost everyone half-prices and nobody decomposes: call protection.

A high yield bond's call schedule looks like a table — NC3, then 105, 102.5, par. Most analysts treat it as a redemption calendar. It isn't a calendar. It's a Bermudan call the bondholder has written to the issuer.

Break it into its parts:

— The non-call period is an exercise restriction — the option exists but cannot be exercised yet.
— The fixed call schedule is a Bermudan call with declining strikes — one exercise date per year, each at a lower price.
— The make-whole that bridges the non-call period is, in substance, a spread option: the issuer's right to refinance, struck at a fixed make-whole spread set on day one.

That last point is where the money hides. The make-whole spread — T+50, say — is locked at issuance. If the issuer's credit spread later tightens by more than that, refinancing is profitable and the bondholder is short exactly that move. The bondholder isn't protected; they're short a spread option with a fixed strike.

In the loan market the equivalent — the 101 soft call — is far weaker: a flat 1% premium for six months, then nothing. Administratively simple, and not coincidentally far less valuable to the lender.

Why this matters if you're early in the seat: when you next see "NC3," don't write "callable from year 4." Write "three-year exercise restriction on a Bermudan call, plus a fixed-strike spread option in between." Then estimate it. For a moderately stressed credit the call protection the lender has written is worth roughly 50-150 bps of running spread — and it never shows up as a line item.

What's the widest make-whole spread you've seen on a recent deal? Genuinely curious — drop it in the comments.

Next week, Part 3: the builder basket — the most valuable option in the whole agreement, hiding inside a definition.

---

## POST 3 — The Builder Basket *(Part 3 of 7)*

Part 3 of the series. If I had to name the single most valuable piece of optionality in a modern credit agreement, it wouldn't be the call schedule or the change-of-control put. It would be the builder basket — and it hides in plain sight, inside a definition.

The builder basket lets the borrower accumulate restricted-payments capacity over the life of the deal: typically 50% of cumulative Consolidated Net Income since closing. Most people read it as a running total. In options terms it is something specific — an Asian option on cumulative net income.

Two features make that the right label, and both matter:

— It is path-dependent. The payoff depends on the sum of the earnings path, not where earnings end up. Standard option intuition — strike, spot, expiry — doesn't capture it. You have to price the path.

— It is sticky. A strong year unlocks distribution capacity that, in most modern drafting, never gives back on a weak year. The exposure the lender has written only ratchets one way.

And there is a second option stacked on top: the add-back rules. Every add-back category — synergies, run-rate, restructuring, transaction costs — is a real option on how management characterizes the income statement. Aggressive add-back drafting inflates CNI, which inflates the builder. You are pricing optionality on top of optionality.

Why it matters for a junior banker: when you see "50% of CNI builder, uncapped synergies," you should not see a basket. You should see an Asian option on cumulative net income with an embedded characterization option — and you should be able to size it. On a typical mid-cap deal that basket is worth €60-120m of distribution capacity over the hold. That is not a footnote. That is the dividend recap.

If you want the rough math behind that range, say so in the comments and I'll walk through it.

Next week, Part 4: portability — why change-of-control protection often looks strong and is nearly worthless.

---

## POST 4 — Portability and the Change-of-Control Put *(Part 4 of 7)*

Part 4. This week, a provision that looks like solid investor protection and frequently is not: the change-of-control put — and the thing that quietly guts it, portability.

Start with the put. A change-of-control covenant gives bondholders the right to sell back at 101 if control changes hands. In options terms it is a contingent put: a binary trigger (the change of control) multiplied by a put struck at 101. Clean enough.

Now portability. Portability says the put does not fire if pro forma leverage sits below a threshold at the time of the change of control. That is not a tweak. That is a knock-out barrier written onto the bondholder's put. Cross the leverage barrier downward and the protection you thought you held simply disappears.

And there is a quieter version — what I'd call disguised portability. Even with no formal portability clause, a broad "Permitted Holders" definition shrinks the set of transactions that count as a change of control at all. Widen Permitted Holders far enough and you are not knocking out the put — you are reducing the probability it is ever triggered. Same destination, different mechanism.

Put the two together and the picture is stark. A change-of-control put with leverage-conditioned portability and a broad Permitted Holders definition can lose 40-70% of its value relative to the headline protection. The covenant reads strong. The economics are thin.

Why it matters early in your career: when you see "portable at 4.5x," do not write "change-of-control protection: yes." Write "knock-out barrier on the CoC put at 4.5x leverage" — then ask what fraction of the put actually survives. The honest answer is usually: less than the marketing suggests.

Have you seen a Permitted Holders definition so broad it covered the whole plausible buyer universe? I've seen a few. Curious what's out there.

Next week, Part 5: the equity cure — the option that rewrites a credit's entire tail risk.

---

## POST 5 — The Equity Cure *(Part 5 of 7)*

Part 5. This one is small in the document and large in its consequences: the equity cure.

An equity cure lets the sponsor inject fresh equity to cure a financial-covenant breach — the injection is treated as additional EBITDA for the recalculation. Most cure rights are limited: five uses over the life of the loan, often with a "three-of-four consecutive quarters" cap.

In options terms it is a Bermudan put — written by the lender, held by the sponsor. The exercise dates are the quarterly covenant tests. The strike is endogenous: whatever equity it takes to clear the breach given that quarter's EBITDA. Each exercise decrements the remaining count.

That much is mechanical. The deeper point is what the option does to the shape of the credit.

Without an equity cure, a covenant breach is a hard event — it brings lenders to the table early, while there is still enterprise value to protect. With an equity cure, the sponsor can convert that hard default into a small equity contribution and push the reckoning out a year, sometimes three. A clean early restructuring at high recovery becomes a delayed restructuring at lower recovery.

So the equity cure does not just cost the lender a few basis points of running spread. It transfers something larger — it reshapes the entire default distribution, trading early intervention for late. The economic value that moves from lender to sponsor is far bigger than the spread line would suggest.

Why it matters for anyone learning credit: when you see "5 equity cures, 3-of-4," do not file it as a minor cure mechanic. See a Bermudan put with a use cap — and understand that what it really changes is the tail. Two credits with identical leverage and identical spreads are not the same credit if one has five unused cures and the other has none.

Next week, Part 6: liability management — Serta, J.Crew, and a class of options written not on the company but on the document itself.

---

## POST 6 — Liability Management *(Part 6 of 7)*

Part 6, and the one I could talk about all day. The most important development in credit over the last decade is not a covenant. It is a class of options written on the documentation itself.

Uptier exchanges (Serta) and drop-down financings (J.Crew) do not price with Black-Scholes. Their underlying is not enterprise value, not EBITDA, not leverage. Their underlying is the set of gaps, ambiguities and undefined terms in the credit agreement — and the right tool is game theory, not the Greeks.

Take the uptier. A majority lender group agrees to move itself to super-priority, subordinating the non-participating minority. Each individual lender, offered the exchange, faces a prisoner's dilemma: join the majority and be promoted, or refuse and be primed. Rational play almost guarantees the exchange succeeds once a majority forms — and the collective best outcome, where everyone refuses, is unreachable through individual choice. That is not an accident of any one deal. It is the structure of the game.

Two consequences worth carrying with you.

First, the LME bundle is a max function, not an average. It is dominated by the single weakest provision in the document. A covenant package can be immaculate everywhere else and still be wide open if one definition — Investment-versus-RP capacity, sacred-rights drafting — leaves a door ajar.

Second, the defenses are themselves options. A cooperation agreement is an anti-option: it removes the coordination failure the uptier depends on. Anti-Serta and anti-J.Crew language are the same idea — written protection against a written exploit.

Why it matters if you are early in credit: this is the most topical subject on any desk right now. If you can frame an uptier as a coercive coordination game rather than just "the Serta thing," you are already thinking about it more clearly than most of the room.

What is your read — is LME a permanent feature of the market now, or a cycle that tightens back? Genuinely interested in where people land.

Next week, the finale: flip the whole framework around — to the borrower's side.

---

## POST 7 — The Sponsor's Side *(Part 7 of 7)*

The finale. Six weeks ago I argued a credit agreement is a portfolio of options the lender has written. Here is the turn: every option the lender is short, the borrower is long. Flip the framework, and a different — and for many readers more useful — discipline appears.

For the lender, optionality is a pricing problem: what spread compensates me for what I have written? For the sponsor or the borrower, it is not a pricing problem at all. It is portfolio construction. Given a finite budget of spread you are willing to pay for flexibility, which options do you negotiate hard for, and which do you concede?

The organizing number is an efficiency ratio: the strategic value of a feature, times the probability your actual plan uses it, divided by what the lender charges for it. Rank every negotiable feature by that ratio. The top of the list is where you spend. The bottom is where you stop fighting. And there is a tier below that — features the lender will pay you to concede, because in your base case you will never use them.

The edge sits in one fact. The lender prices optionality assuming an average borrower with an average plan. You are not average. You know your playbook — buy-and-build, turnaround, dividend recap, the specific exit. Pay for the flexibility your plan actually relies on; give back the flexibility it never will. The gap between the lender's average price and your plan-specific value is, quite literally, your negotiation surplus.

That is the whole series in one line: the same options theory, read from two sides of the table.

I have now written this up in full — the lender's framework and the sponsor's playbook, with the models behind both. I run a small number of 1-on-1 sessions for people who want to work through it properly: how to decompose a covenant package, price each piece, and read a credit agreement the way an options desk reads a term sheet. If that is something you want to build early in your career, leave a comment or send me a message and we can talk about what it would look like.

Thanks for following the series. The reframe is simple, but it does not leave you — once a credit agreement looks like a bundle of options, it never looks like a checklist again.
