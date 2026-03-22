---
name: amazon-supplier-sourcing
description: "Amazon supplier sourcing and development agent. Find manufacturers on Alibaba/1688, evaluate supplier quality, generate RFQ inquiry templates, negotiate MOQ and pricing, and create quality control checklists for your Amazon FBA products. Triggers: supplier sourcing, alibaba sourcing, find manufacturer, rfq template, supplier evaluation, moq negotiation, alibaba supplier, product sourcing, china manufacturer, supplier inquiry, quality control, factory audit, sourcing agent, private label sourcing, fba sourcing"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/amazon-supplier-sourcing
---

# Amazon Supplier Sourcing Agent

Find the right manufacturer, send professional inquiries, negotiate smart, and protect your quality. From first contact to first shipment — your sourcing co-pilot.

## Commands

```
sourcing find [product]         # generate supplier search strategy
sourcing rfq [product]          # generate professional RFQ template
sourcing evaluate [supplier]    # supplier evaluation scorecard
sourcing negotiate [details]    # MOQ and pricing negotiation script
sourcing qc [product]           # quality control checklist
sourcing questions              # 20 must-ask supplier questions
sourcing red flags               # supplier red flag checklist
sourcing compare [s1] [s2]      # compare two supplier profiles
sourcing timeline               # sourcing timeline planner
sourcing save [supplier]        # save supplier profile
```

## What Data to Provide

- **Product description** — what you want to source
- **Target price** — your maximum COGS budget
- **Target quantity** — units per order (MOQ expectations)
- **Quality requirements** — materials, certifications, specifications
- **Supplier details** — paste Alibaba/1688 profile info for evaluation

## Supplier Search Strategy

### Where to Find Suppliers

| Platform | Best For | Notes |
|----------|----------|-------|
| Alibaba.com | English-speaking factories, export experience | Higher price, more reliable |
| 1688.com | Lower price, domestic China market | Need sourcing agent or Chinese |
| Global Sources | Electronics, tech products | Trade show quality suppliers |
| Made-in-China.com | Industrial products | Less competitive than Alibaba |
| Canton Fair | Best-in-class manufacturers | Twice yearly, April & October |

### Search Keywords Strategy
- Search in Chinese (translate your product) for 1688
- Use both generic and specific terms: "yoga mat" AND "TPE yoga mat manufacturer"
- Add: OEM / ODM / private label to filter for customization capability
- Avoid: trading companies if you want factory-direct pricing

### Supplier Tiers
| Tier | Type | Pros | Cons |
|------|------|------|------|
| Tier 1 | Large factory (500+ workers) | Consistent quality, certifications | High MOQ, less flexible |
| Tier 2 | Mid factory (50–500 workers) | Balance of flexibility and quality | Variable quality control |
| Tier 3 | Small factory / workshop | Low MOQ, highly flexible | Quality consistency risk |
| Trading Co. | Middleman | Easy communication | Markup 15–30%, less control |

## RFQ Template (Professional Inquiry)

```
Subject: OEM Inquiry — [Product Name] — [Your Company Name]

Dear [Supplier Name],

I am [Name] from [Company], an Amazon FBA seller based in [Country].
I am interested in sourcing [Product] for the US/UK/EU market.

PRODUCT SPECIFICATIONS:
- Product: [detailed description]
- Material: [material requirements]
- Dimensions: [L × W × H cm] / Weight: [grams]
- Color options: [colors needed]
- Certifications required: [CE / FCC / ROHS / etc.]
- Custom branding: Logo on product / custom packaging (Yes/No)

QUANTITY & TIMELINE:
- Sample order: [X units] for quality evaluation
- Initial order: [X units] (if samples approved)
- Future orders: [X units/month] estimated
- Delivery timeline required: [X weeks from order]

QUESTIONS:
1. What is your MOQ for this product?
2. What is the unit price at [500 / 1000 / 2000 / 5000] units?
3. Can you provide OEM/private label with our logo?
4. What certifications does this product have?
5. What is the sample cost and lead time?
6. Do you offer DDP (Delivered Duty Paid) shipping to [country]?
7. What is your factory inspection policy?

Please send: product catalog, price list, and factory certification documents.

Best regards,
[Your Name]
[Company] | [Email] | [WhatsApp/WeChat]
```

## Supplier Evaluation Scorecard (100 points)

| Criteria | Weight | How to Score |
|----------|--------|-------------|
| Response speed | 10 | <24h=10, <48h=7, >48h=3 |
| Communication quality | 15 | Clear, professional, detailed |
| Factory verification | 15 | Verified badge, audit report, video tour |
| Years in business | 10 | >5yr=10, 3-5yr=7, <3yr=3 |
| Certifications | 15 | CE/FCC/ROHS/ISO as needed |
| Sample quality | 20 | Rate after receiving samples |
| Price competitiveness | 10 | Within target COGS budget |
| References/reviews | 5 | Past buyer feedback |

**Score 80+** = Preferred supplier
**Score 60–79** = Proceed with caution
**Score <60** = Find alternative

## MOQ Negotiation Scripts

**Opening ask (too high MOQ):**
> "Your MOQ is [X] units, but for our initial order we'd like to start with [lower amount] to validate the market. We can commit to [X] units per quarter if quality meets expectations. Can you accommodate a smaller first order at a slightly higher unit price?"

**Price negotiation:**
> "We've received quotes from 3 suppliers in the [price range]. To move forward with you, we need to be at [target price]. What can we do to reach that number — material adjustment, packaging simplification, or payment terms?"

**Certification leverage:**
> "We require [certification] for our market. Can you share the test report? If you don't have it, we can arrange third-party testing and split the cost."

## Quality Control Checklist

### Pre-Production
- [ ] Material specifications confirmed in writing
- [ ] Approved sample on file (golden sample)
- [ ] Packaging artwork approved
- [ ] Barcode/FNSKU placement confirmed
- [ ] Certification requirements documented

### During Production (if 3rd party inspection)
- [ ] Raw material check
- [ ] In-line production inspection (30% completion)
- [ ] Final random inspection (AQL 2.5 standard)

### Pre-Shipment
- [ ] AQL inspection passed (hire SGS/Bureau Veritas/QIMA)
- [ ] Carton drop test passed
- [ ] Weight and dimensions match spec
- [ ] Barcodes scan correctly
- [ ] All units in carton match quantity

## 20 Must-Ask Supplier Questions

1. Can I visit your factory? (Red flag if no)
2. Who else do you supply? (Reference check)
3. What is your reject rate?
4. How do you handle defective units?
5. Do you have product liability insurance?
6. What payment terms do you offer? (30/70 is standard)
7. Can I get a factory audit report?
8. What is your capacity per month?
9. How do you handle IP/design confidentiality?
10. What happens if my shipment is delayed?
11. Do you use child labor? (Compliance)
12. What raw materials do you use and where from?
13. Can you do custom packaging?
14. What shipping methods do you use?
15. Do you work with freight forwarders?
16. What is your sample lead time?
17. Can you provide references from current customers?
18. Do you have experience with Amazon FBA requirements?
19. What certifications can you provide?
20. What is your policy on NDA/confidentiality agreements?

## Red Flags — Walk Away If:

- Refuses factory visit or video call
- No verifiable business registration
- Price dramatically below market (too good to be true)
- Pushes for full payment upfront
- Cannot provide certifications for regulated categories
- Copies competitor products without hesitation
- Poor sample quality with excuses ("production will be better")
- Communication disappears after initial inquiry

## Output Format

1. **Supplier Search Plan** — where to look, what keywords to use
2. **RFQ Draft** — ready to send inquiry template
3. **Evaluation Scorecard** — fill-in assessment for each supplier
4. **Negotiation Script** — specific language for price/MOQ discussion
5. **QC Checklist** — pre-production through delivery checkpoints
