# LinkedIn Post — Credit Agreements as Bundles of Options

*Audience: junior LevFin / credit bankers · Tone: measured thought-leadership · CTA: soft*

---

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

I have been writing this framework up properly — the lender's side and the sponsor's side both. If it is something you would want to work through in depth, leave a comment or send me a message. Always glad to talk credit and options with people building this muscle early.
