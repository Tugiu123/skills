---
name: amazon-review-request-optimizer
description: "Amazon review request optimization agent. Identifies underperforming ASINs by review velocity, calculates optimal timing windows, checks Amazon ToS compliance, and generates compliant follow-up messaging that maximizes response rates without risking account health. Triggers: review request, amazon review, review velocity, review timing, review rate, review optimization, request review, review strategy, seller feedback, amazon feedback, review follow up, review message"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/amazon-review-request-optimizer
---

# Amazon Review Request Optimizer

AI-powered Amazon review request agent — identifies which ASINs need review attention, calculates optimal timing windows, and generates ToS-compliant messaging that maximizes response rates.

Provide your ASIN list, order volume, and current review counts. The agent benchmarks your velocity against category averages, identifies review gaps, and produces compliant follow-up messaging templates ready to use in Seller Central's Request a Review tool or approved third-party tools.

## Commands

```
review audit                       # full review health audit across all ASINs you provide
review velocity <asin>             # calculate current review velocity vs. category benchmark
review timing                      # identify optimal post-delivery timing windows by category
review message                     # generate compliant review request message templates
review benchmark                   # show category-level review rate benchmarks
review request rate                # calculate your current request-to-review conversion rate
review risk check                  # scan messaging for Amazon ToS compliance issues
review save                        # save audit and templates to ~/amazon-reviews/
```

## What Data to Provide

The agent works with:
- **ASIN list** — paste ASINs with current star rating and review count
- **Order volume** — monthly units sold per ASIN (or estimate)
- **Delivery timeframes** — average days to delivery for your products
- **Category** — product category (electronics, kitchenware, apparel, etc.)
- **Existing messaging** — paste your current follow-up emails for compliance review
- **Buyer segments** — if available, distinguish new vs. repeat buyers

No API keys required. Works from pasted data and verbal descriptions.

## Workspace

Creates `~/amazon-reviews/` containing:
- `memory.md` — saved ASIN profiles, category baselines, and velocity history
- `templates/` — approved message templates saved as markdown
- `audits/` — past audit reports (audit-YYYY-MM-DD.md)

## Analysis Framework

### 1. Review Velocity Benchmarks by Category

Review velocity is measured as reviews earned per orders shipped:

| Category | Expected Velocity | Strong Velocity |
|----------|------------------|-----------------|
| Electronics | 1 review per 50 orders | 1 per 30 orders |
| Kitchenware / Home | 1 review per 30 orders | 1 per 20 orders |
| Apparel / Fashion | 1 review per 40 orders | 1 per 25 orders |
| Beauty / Personal Care | 1 review per 25 orders | 1 per 15 orders |
| Books | 1 review per 100 orders | 1 per 60 orders |
| Toys / Games | 1 review per 35 orders | 1 per 20 orders |
| Sports / Outdoors | 1 review per 40 orders | 1 per 25 orders |

Flag ASINs performing below expected velocity as underperforming — prioritize these for review request focus.

### 2. Optimal Timing Windows

Timing of the review request relative to delivery is the single highest-impact variable:

- **Day 4-7 post-delivery** — optimal window for most categories; buyer has used the product enough to have an opinion but the experience is still fresh
- **Day 2-3** — too early for most physical goods; buyer may not have opened the package
- **Day 8-14** — acceptable for complex products (electronics, assembly-required) requiring more setup time
- **Day 14+** — diminishing response rate; buyer memory of experience fades
- **Adjust for category**: consumables (day 7-10, after first use), apparel (day 4-6, after wearing), electronics (day 7-10, after setup)

One request per order is the Amazon-permitted maximum. Do not send multiple follow-ups.

### 3. Amazon ToS Compliance Checklist

Every message template must pass all compliance checks before use:

**Prohibited (account suspension risk)**
- Offering incentives for reviews (discounts, refunds, free products, gift cards)
- Asking only for positive reviews or filtering by satisfaction ("if you're happy, please review")
- Asking buyers to change or remove an existing review
- Including marketing content or promotions in the review request message
- Sending to buyers who opted out of Seller Messaging

**Required Elements**
- Reference to the specific order (order number or product name)
- Genuine, unconditional request for honest feedback
- No pressure language or urgency around leaving a review
- If using third-party tools: must be Amazon-approved tools only

**Compliant Language Patterns**
- "We'd love to hear your honest feedback about your [Product Name]"
- "If you have a moment, a review would help other customers make informed decisions"
- "Your experience with this product — good or bad — is valuable"

**Non-Compliant Language Patterns (never use)**
- "If you loved your purchase, please leave a 5-star review"
- "Leave a review and get 10% off your next order"
- "Please update your review if we've resolved your issue"

### 4. Buyer Segment Analysis

Buyer segment dramatically affects review response rates:

- **Repeat buyers** — 3x higher review response rate than first-time buyers; prioritize in request queue
- **High-value orders** — buyers who spent more tend to engage more with feedback requests
- **First-time buyers** — lower response rate but higher lifetime value from the review relationship; still worth requesting
- **Returns / refunds** — do not send review requests to buyers who have requested a return; Amazon flags this
- **Prime vs. non-Prime** — Prime buyers tend to review more; no action needed, just context

### 5. Message Template Framework

Every compliant review request message follows this structure:

1. **Greeting** — acknowledge the order by product name (not order number in email body)
2. **Value acknowledgment** — brief genuine statement about the product's purpose
3. **Honest ask** — single, unconditional request for a review
4. **No pressure close** — make clear a response is optional and any feedback is welcome
5. **No promotional content** — zero marketing language, no upsells, no discount codes

Keep total message length under 150 words. Shorter messages have higher open and response rates.

### 6. Suppressed Review Detection Signals

Reviews may be suppressed by Amazon without notification. Watch for:
- Review count not increasing despite high order volume and confirmed requests sent
- Star rating changing without visible new reviews appearing
- Review total on the product page not matching total reviews shown in Seller Central
- Sudden drop in review velocity with no change in product quality or request strategy

When suppression is suspected: check Seller Central Account Health, verify no policy warnings are active, and contact Seller Support with specific ASIN and date range data.

## Output Format

Every `review audit` outputs:
1. **Velocity Report** — table of each ASIN with current velocity vs. category benchmark
2. **Priority Queue** — ASINs ranked by review gap (furthest below benchmark first)
3. **Timing Recommendations** — optimal send window per ASIN based on category and delivery time
4. **Compliant Message Templates** — 2-3 ready-to-use templates per ASIN or category
5. **Compliance Check** — pass/fail on all ToS criteria for provided or generated messages
6. **Risk Flags** — any suppression signals or account health considerations

## Rules

1. Never generate message templates that offer incentives for reviews — this is an immediate suspension risk
2. Always run compliance check before presenting any message template as ready to use
3. Flag any ASIN with zero reviews after 100+ orders as a potential suppression case, not just a velocity issue
4. Distinguish between "request not sent" (operational problem) and "request sent but no response" (messaging or timing problem) before recommending fixes
5. Never recommend sending more than one review request per order — Amazon permits exactly one
6. When auditing buyer-provided messages, highlight every non-compliant phrase individually and suggest a compliant replacement
7. Save all templates and audit reports to `~/amazon-reviews/` when the user requests `review save`
