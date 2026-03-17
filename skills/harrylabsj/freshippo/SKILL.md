---
name: freshippo
description: "Shop Freshippo (盒马鲜生) with smart grocery guidance, fresh produce selection tips, delivery timing optimization, membership benefits, and weekly meal planning. Use when the user wants help shopping on 盒马鲜生, choosing fresh groceries, planning family meals, understanding X会员 benefits, or optimizing delivery slots. NOT for: placing real orders, handling payments, or scraping live account data."
metadata:
  clawdbot:
    emoji: "🦛"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Freshippo (盒马鲜生)

## Overview

Use this skill to help users shop smartly on Freshippo (盒马鲜生), Alibaba's premium fresh grocery platform. Get guidance on fresh produce selection, delivery timing, membership benefits, and weekly meal planning.

## Scope

Keep this skill guidance-only unless live shopping tools are explicitly available and verified.

- Give shopping strategy, selection tips, delivery timing advice, and meal-planning help.
- Do not claim to browse a live Freshippo account, place orders, or confirm exact inventory unless the required tools are actually available.
- When the user wants a reusable shopping list or meal plan, provide it directly in the reply unless a separate first-class tool is available.

## Workflow

1. Determine the user's goal:
   - browse categories and get product recommendations
   - plan weekly meals and build shopping lists
   - understand delivery slots and timing strategies
   - learn about X会员 membership benefits
   - get fresh produce selection tips
   - review or clear local shopping lists/history/privacy data
2. Ask for only the missing essentials, such as dietary preferences, family size, or delivery preferences.
3. Give the most practical answer first.
4. If exact prices or availability cannot be confirmed, provide cautious estimates and state assumptions.
5. If exact prices, availability, or store coverage cannot be verified, say so clearly and give cautious, practical guidance instead.
6. Do not claim to complete real purchase actions unless live tools are available and confirmed.

## Quick Reference

| Topic | Description |
|-------|-------------|
| Fresh Produce | 生鲜蔬果选购指南 |
| Delivery Slots | 配送时段优化建议 |
| X会员 Benefits | 盒马X会员权益详解 |
| Weekly Planning | 一周买菜规划 |
| Shopping Lists | 购物清单管理 |

## Core Rules

### 1. Delivery Slot Timing

Freshippo operates on **30-minute delivery slots** (30分钟送达):

| Time Slot | Best For | Notes |
|-----------|----------|-------|
| 8:00 - 10:00 AM | Fresh produce, bakery | Best selection, morning delivery |
| 10:00 - 12:00 PM | Daily essentials | Good availability |
| 14:00 - 16:00 PM | Afternoon shopping | Moderate availability |
| 16:00 - 18:00 PM | Dinner prep | High demand, book early |
| 18:00 - 22:00 PM | Evening restock | Limited fresh selection |

**Strategy:**
- Book 8-10 AM slots for freshest produce
- Peak dinner prep slots (17:00-19:00) fill up fast
- Same-day delivery available if ordered before 21:00
- Rainy days may have delayed slots

### 2. Fresh Produce Selection

Freshippo's strength is **fresh food and quality groceries**:

| Category | Best Time to Buy | Quality Indicators |
|----------|------------------|-------------------|
| Vegetables | Morning 8-10 AM | Harvest date, origin label |
| Fruits | Morning 8-10 AM | Ripeness indicator, origin |
| Meat | Morning 8-10 AM | Slaughter date, grade |
| Seafood | Morning 8-10 AM | Catch/delivery date, live tanks |
| Bakery | Morning 8-10 AM | Bake time stamp |
| Dairy | Any time | Expiration dates |

**Pro Tips:**
- 盒马日日鲜 (Daily Fresh) = same-day packaged, best quality
- 产地直采 (Direct sourcing) = fresher, traceable
- 鲜活 (Live) seafood = premium quality, cook same day
- Check 溯源码 (traceability code) for origin info

### 3. X会员 Membership Benefits

**Membership Tiers:**

| Tier | Annual Fee | Key Benefits |
|------|------------|--------------|
| Regular | Free | Basic shopping, standard delivery |
| X会员 | ¥258/year | Free delivery, member prices, daily deals |
| X会员·黄金 | ¥658/year | All above + premium services |

**Member-Exclusive Features:**
- 免费配送 (Free delivery): No minimum order for X会员
- 会员价 (Member prices): 5-15% off regular prices
- 会员日 (Member day): Tuesday extra discounts
- 专享商品 (Member-only products): Premium selections
- 优先配送 (Priority delivery): Peak slots reserved

**Break-Even Analysis:**
- Shop >¥300/month → membership pays for itself
- Frequent fresh grocery buyers → highly recommended
- Free delivery saves ¥6-15 per order

### 4. Category Highlights

**盒马特色 (Freshippo Specialties):**

| Category | Highlights | Tips |
|----------|------------|------|
| 盒马工坊 | Ready-to-cook meals | Fresh, restaurant-quality |
| 海鲜水产 | Live seafood tanks | Cook in-store or home delivery |
| 日日鲜 | Daily fresh produce | Same-day packaging |
| 烘焙 | In-store bakery | Fresh daily, limited quantities |
| 进口食品 | International imports | Premium selection |
| 有机蔬菜 | Organic produce | Certified, higher price |

### 5. Smart Shopping Strategies

**Timing Strategies:**
1. **Morning Shopping (8-10 AM):** Best selection of fresh items
2. **Tuesday Member Day:** Extra discounts for X会员
3. **Evening Clearance (after 20:00):** Discounted bakery and ready meals
4. **Weekend Prep:** Plan ahead for busy slots

**Category Bundling:**
- Fresh + Pantry = Free delivery threshold easier to reach
- Ready meals + Fresh = Complete dinner solution
- Bulk buying on staples = Lower unit cost

**Payment Optimization:**
- 盒马钱包: Occasional extra discounts
- Alipay: Seamless integration
- Credit card partnerships: Check for cashback
- First-order: Usually has welcome discount

### 6. Delivery & Pickup

| Aspect | Details |
|--------|---------|
| Standard Delivery | 30-minute slots, 8:00 AM - 22:00 PM |
| Delivery Radius | ~3-5km from store |
| Free Shipping Threshold | ¥39 for non-members, free for X会员 |
| In-Store Shopping | Live seafood cooking, fresh bakery |
| Self-Pickup | Available at some locations |

**Delivery Optimization:**
- Choose morning slots for freshest produce
- Evening slots have limited fresh selection
- Combine orders to hit free shipping threshold
- Cold chain items delivered in insulated packaging

### 7. Weekly Meal Planning

**Family Shopping Guide:**

| Day | Focus | Suggested Items |
|-----|-------|-----------------|
| Monday | Fresh start | Vegetables, fruits, dairy |
| Tuesday | Member Day deals | Stock up on staples |
| Wednesday | Mid-week refresh | Meat, seafood |
| Thursday | Prep for weekend | Party foods, snacks |
| Friday | Weekend treats | Premium items, bakery |
| Saturday | Family cooking | Bulk fresh produce |
| Sunday | Meal prep | Ready meals, leftovers |

**Weekly Budget Guide:**
- Small family (2-3 people): ¥300-500/week
- Medium family (4-5 people): ¥500-800/week
- Large family (6+ people): ¥800-1200/week

## Common Traps

- **Overbuying perishables** → Fresh items have limited shelf life
- **Missing delivery slots** → Peak times fill up quickly
- **Ignoring member benefits** → Non-members pay delivery fees
- **Flash sale FOMO** → Compare with regular prices
- **Not checking expiration** → Especially on dairy and ready meals
- **Ordering during rush hour** → Limited slot availability

## Freshippo-Specific Features to Leverage

### 1. 盒马工坊 (Freshippo Kitchen)
- Ready-to-cook meals
- Restaurant-quality ingredients prepped
- Great for busy weeknights

### 2. 鲜活海鲜 (Live Seafood)
- Live tanks in store
- Cook in-store or take home
- Premium quality guarantee

### 3. 日日鲜 (Daily Fresh)
- Same-day packaged produce
- Clear harvest/pack dates
- Best quality indicator

### 4. 会员日 (Member Day)
- Tuesday exclusive deals
- Extra discounts for X 会员
- Limited-time promotions

### 5. 盒马村 (Freshippo Village)
- Direct farm sourcing
- Traceable origin products
- Seasonal specialties

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `home-food-planner` — family meal planning and nutrition
- `yhd` — YHD.com grocery shopping

## Feedback

- If useful: `clawhub star freshippo`
- Stay updated: `clawhub sync`
