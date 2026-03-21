---
name: amazon-listing-health-monitor
description: "Amazon listing health audit agent. Checks title and bullet completeness, keyword coverage, image count, BSR trends, Buy Box eligibility, suppression risk, and hijacker signals. Scores each listing and delivers a prioritized fix list. Triggers: listing audit, amazon listing, listing health, listing score, buy box, listing optimization, listing checker, product listing, amazon seo, backend keywords, listing suppression, hijacker, listing quality"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/amazon-listing-health-monitor
---

# Amazon Listing Health Monitor

AI-powered Amazon listing audit agent — scores your listing across content, keywords, images, and account health signals, then tells you exactly what to fix first.

Paste your listing details, describe your ASIN, or provide a bulk export. The agent audits every dimension and returns a prioritized action plan.

## Commands

```
listing audit                      # full health audit (paste listing content or describe ASIN)
listing score                      # get numeric health score with dimension breakdown
bsr track                          # log and analyze BSR trend for a product
buy box check                      # assess Buy Box eligibility and loss signals
keyword audit                      # evaluate keyword coverage in title, bullets, description
image audit                        # check image count, types, and compliance
listing compare                    # compare two listing versions side by side
listing save <asin>                # save listing snapshot to workspace
```

## What Data to Provide

The agent works with:
- **Listing content** — paste title, bullet points, description, backend keywords
- **ASIN description** — "ASIN B08XYZ, baby monitor, 3.8 stars, 1200 reviews, BSR 450 in Baby"
- **Seller Central export** — paste Flat File or Inventory report rows
- **Screenshots** — listing page, Seller Central listing quality dashboard
- **Metrics** — "title is 95 chars, 4 bullets, 5 images, lost Buy Box 3 days ago"

No API keys needed. No tools required.

## Workspace

Creates `~/amazon-listings/` containing:
- `memory.md` — saved ASIN profiles and audit history
- `reports/` — past audit reports (markdown)
- `bsr-log.md` — BSR snapshots for trend tracking

## Analysis Framework

### 1. Content Completeness Audit

#### Title
| Signal | Benchmark |
|--------|-----------|
| Character length | 150–200 chars (category-dependent) |
| Primary keyword | In first 80 characters |
| Brand name | Present |
| Key attributes | Size, color, quantity, material |
| Forbidden elements | No promotional claims, no symbols like !, $ |

#### Bullet Points
- Count: 5 bullets (maximum allowed, all should be used)
- Each bullet: 150–250 characters (enough detail, not truncated in mobile)
- Top-3 bullets: lead with benefit, not feature
- Keyword integration: secondary and LSI keywords distributed across bullets
- Forbidden: shipping claims, seller-specific info, subjective claims without context

#### Product Description / A+ Content
- A+ Content preferred over plain description for brand-registered sellers
- Plain description: 2000 character limit, HTML formatting supported
- A+ Content: check for comparison chart module (drives conversion)

### 2. Keyword Coverage Check
- **Title keywords**: primary high-volume keyword must appear in title
- **Bullet keywords**: secondary keywords distributed (not keyword stuffed)
- **Backend search terms**: 250 bytes (not characters) total, no repetition, no brand names of competitors
- **Subject Matter fields**: used for additional indexing (intended use, target audience, material)
- Red flag: primary keyword absent from both title and backend = indexing gap

### 3. Image Audit
| Requirement | Standard |
|-------------|----------|
| Minimum images | 4 (7+ strongly recommended) |
| Main image | Pure white background, product fills 85%+ of frame |
| Lifestyle images | At least 2 showing product in use |
| Infographic | At least 1 with key specs/benefits called out |
| Size chart | Required for apparel, recommended for any sized product |
| Video | Strongly recommended — increases conversion rate |

### 4. BSR Benchmarks by Category
| BSR Range | Category Signal |
|-----------|----------------|
| Top 100 | Bestseller in category |
| Top 1,000 | Strong seller |
| Top 10,000 | Established, moderate velocity |
| Top 100,000 | Low velocity, optimization needed |
| > 100,000 | Low sales, investigate listing issues |

BSR drops > 20% in 7 days = investigate: stock-out, price change, competitor surge, listing suppression.

### 5. Buy Box Eligibility Signals
Factors Amazon weighs for Buy Box:
- **Price competitiveness**: within ~2% of lowest FBA price
- **Fulfillment method**: FBA preferred over FBM
- **Order defect rate (ODR)**: must be < 1%
- **Late shipment rate**: < 4%
- **Seller feedback score**: > 95% positive (trailing 12 months)
- **In-stock rate**: consistent stock, no stockouts
- **Account health**: no active policy violations

Buy Box loss signals: price undercut by competitor, new FBA seller entered, account metric dip.

### 6. Suppression Trigger Checklist
Common suppression causes:
- Main image does not meet white background requirement
- Title exceeds character limit for category
- Missing required attributes (e.g., material, size for apparel)
- Listing flagged for prohibited content (health claims, offensive language)
- Pricing error (price too high or too low vs. reference price)
- ASIN merged/split issue creating content conflict

### 7. Hijacker Detection Signals
- Buy Box seller is not your brand
- Product reviews mention a different product than yours
- Main image has changed without your action
- Listing title or bullets contain unfamiliar text
- Sudden BSR drop with no change in your ad spend or pricing

## Listing Health Score

Score each dimension 1–10. Overall Health Score = weighted average:

| Dimension | Weight |
|-----------|--------|
| Title quality | 20% |
| Bullet quality | 20% |
| Image completeness | 20% |
| Keyword coverage | 20% |
| Buy Box status | 10% |
| Suppression risk | 10% |

Score interpretation: 8–10 = Healthy, 6–7 = Needs work, < 6 = Critical issues present.

## Output Format

Every audit outputs:
1. **Health Score** — numeric score with per-dimension breakdown
2. **Critical Issues** — suppression risks, Buy Box loss signals, hijacker alerts (fix immediately)
3. **Content Gaps** — missing images, thin bullets, title issues (fix this week)
4. **Keyword Opportunities** — indexing gaps and backend keyword improvements
5. **Prioritized Action List** — ranked by impact, with specific copy suggestions where possible

## Rules

1. Always ask for the product category before auditing — title length limits and required attributes vary by category
2. Flag suppression risks before any other finding — suppression means zero sales
3. Never suggest keyword stuffing — penalization risk outweighs any indexing gain
4. Distinguish between brand-registered and non-registered listings — A+ Content and Brand Story only available to registered brands
5. When Buy Box is lost, investigate pricing and fulfillment method first — these are the two most common causes
6. Note when BSR data is a single snapshot vs. trend — single point is insufficient for meaningful analysis
7. Save listing snapshots to `~/amazon-listings/` when listing save command is used
