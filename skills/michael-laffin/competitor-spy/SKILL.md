# Competitor Spy

Analyze any website or business and extract competitive intelligence in seconds.

---

## When to Use

Trigger when the user says:
- "spy on [website/domain]"
- "analyze competitor [name]"
- "competitor research [url]"
- "what are [competitor]'s tech stack"
- "reverse engineer [website]"

## How It Works

1. User provides a domain, URL, or business name
2. Agent scrapes the target website
3. Extracts: tech stack, pricing, features, SEO keywords, content strategy, social proof
4. Generates a competitive intelligence report

## Commands

### Primary: Full Spy Report

User says: "spy on example.com"

Agent workflow:
1. Use `web_fetch` to grab the homepage
2. Use `web_fetch` on /pricing, /about, /features, /blog
3. Extract and analyze:
   - **Tech Stack:** Check for common frameworks (Next.js, React, WordPress, etc.), hosting (Vercel, Netlify, AWS), analytics (GA4, PostHog), fonts, CDNs
   - **Pricing:** Extract all pricing tiers, features per tier, free trial info
   - **Features:** Main product features, unique selling points
   - **SEO:** Meta tags, headings, schema markup, sitemap
   - **Content Strategy:** Blog topics, content frequency, tone
   - **Social Proof:** Testimonials, logos, case studies, review counts
   - **Monetization:** Revenue model (SaaS, freemium, ads, marketplace)
   - **Weaknesses:** Missing features, poor UX, slow pages, thin content
4. Output a structured markdown report

### Secondary: Quick Tech Stack Check

User says: "tech stack of example.com"

Agent workflow:
1. Use `web_fetch` on the homepage
2. Look for framework signatures, CDN headers, meta generators
3. Output a compact tech stack summary

### Tertiary: Pricing Comparison

User says: "compare pricing for example.com and competitor.com"

Agent workflow:
1. Fetch /pricing from both sites
2. Extract all tiers and features
3. Create side-by-side comparison table
4. Highlight gaps and opportunities

## Report Format

```markdown
# 🔍 Competitor Spy Report: [domain]

## 🏢 Business Overview
- **Name:** [extracted]
- **Tagline:** [extracted]
- **Industry:** [inferred]

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Framework | [detected] |
| Hosting | [detected] |
| Analytics | [detected] |
| CDN | [detected] |
| Fonts | [detected] |

## 💰 Pricing
| Tier | Price | Key Features |
|------|-------|-------------|
| ... | ... | ... |

## ✅ Strengths
- ...

## ❌ Weaknesses & Opportunities
- ...

## 📈 SEO Score
| Metric | Value |
|--------|-------|
| Title tag | ... |
| Meta description | ... |
| H1 tag | ... |
| Schema markup | ... |
| Sitemap | ... |
| Robots.txt | ... |

## 💡 Recommendations
- ...
```

## Tips

- If the site blocks scraping, try the Google cache version
- Check LinkedIn/Twitter for additional business info
- Use `web_search` to find reviews and mentions
- Cross-reference with SimilarWeb/Alexa if needed
- Always cite sources for claims

## Limitations

- Cannot access paywalled content
- JavaScript-heavy SPAs may need browser automation
- Pricing pages behind login walls are inaccessible
- Results depend on site structure and accessibility
