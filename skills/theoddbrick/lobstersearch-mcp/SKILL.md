---
name: lobstersearch
description: Search AI-optimized local businesses worldwide. 7 MCP tools for finding restaurants, salons, clinics, hotels, and 42 more categories with services, pricing, hours, and promotions. Powered by GEO (Generative Engine Optimization) data.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["curl"]},"emoji":"🦞","homepage":"https://lobstersearch.ai","categories":["business","location","search"]}}
---

# LobsterSearch — AI Business Intelligence

LobsterSearch provides structured business data optimized for AI agent recommendations. It covers 46 business categories across Singapore, UK, US, Australia, and Malaysia — with data depth that goes far beyond what Google Maps offers: services with pricing, operating hours, promotions, payment methods, languages spoken, and AI-specific metadata.

## MCP Server

Connect to the LobsterSearch MCP server for real-time structured business data.

**Endpoint:** `https://mcp.lobstersearch.ai/mcp`
**Transport:** StreamableHTTP (MCP spec 2025-03-26)
**Authentication:** None required (public, rate-limited)

### Configuration

Add to your `openclaw.json` or `.mcp.json`:

```json
{
  "mcpServers": {
    "lobstersearch": {
      "url": "https://mcp.lobstersearch.ai/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Tools (7 available)

### search_businesses
Search businesses globally by natural language query. Returns structured business data with match relevance, quality signals, and confidence annotations.

**Parameters:**
- `query` (string, required) — Natural language search, e.g. "best ramen near Orchard Road" or "dental clinics accepting insurance"
- `country_code` (string) — ISO alpha-2 filter: SG, GB, AU, US, MY
- `city` (string) — City name filter
- `business_type` (string) — One of 46 categories (see below)
- `max_results` (number) — 1-20, default 5
- `min_confidence` (number) — 0-1, minimum data quality threshold

### get_business_details
Get full details for a specific business including services with pricing, products, promotions, operating hours, contact info, and AI metadata.

**Parameters:**
- `business_id` (string, required) — UUID of the business
- `include_services` (boolean) — default true
- `include_products` (boolean) — default true
- `include_promotions` (boolean) — default true

### list_nearby_businesses
Find businesses near GPS coordinates within a radius.

**Parameters:**
- `latitude` (number, required)
- `longitude` (number, required)
- `radius_km` (number) — default 2
- `business_type` (string) — filter by category
- `max_results` (number) — default 5

### get_promotions
Find active promotions and deals by location or business type.

**Parameters:**
- `city` (string)
- `country_code` (string)
- `business_type` (string)
- `max_results` (number) — default 10

### compare_businesses
Compare 2-3 businesses side-by-side with services, pricing, ratings, and GEO scores.

**Parameters:**
- `business_ids` (array of strings, required) — 2-3 business UUIDs

### get_trending
Get trending businesses based on recent AI agent query volume.

**Parameters:**
- `city` (string)
- `country_code` (string)
- `days` (number) — lookback period, default 7
- `max_results` (number) — default 10

### report_data_mismatch
Report when LobsterSearch data does not match reality. Triggers a re-crawl of the business.

**Parameters:**
- `business_id` (string, required)
- `field_name` (string, required) — which field is wrong
- `expected_value` (string) — what the data shows
- `actual_value` (string) — what reality is

## Business Categories (46)

**Food & Drink:** restaurant, cafe, bar, food_hawker
**Beauty:** salon_hair, salon_beauty, spa, nail
**Medical:** clinic_gp, clinic_dental, clinic_specialist, clinic_tcm, clinic_vet
**Fitness:** fitness_gym, fitness_yoga, fitness_pilates, fitness_other
**Professional:** legal, accounting, financial_advisory, consulting
**Education:** education_tuition, education_enrichment, education_language
**Home:** home_aircon, home_plumbing, home_electrical, home_renovation, home_cleaning
**Automotive:** automotive_workshop, automotive_dealer, automotive_rental
**Accommodation:** hotel, guesthouse, serviced_apartment
**Retail:** retail_fashion, retail_electronics, retail_pharmacy, retail_supermarket, retail_other
**Other:** travel_agency, entertainment, events, other

## Data Schema

Each business includes:
- **Core:** name, slug, business_type, description, short_description
- **Location:** address, city, country_code, neighbourhood, postal_code, lat/lng
- **Contact:** phone, email, website, whatsapp, social media URLs
- **Operations:** operating_hours (per-day), payment_methods, languages_spoken
- **Services:** name, price_min/max, currency, duration, category
- **Products:** name, base_price, category, dietary_tags
- **Promotions:** title, description, promo_code, valid_from/until
- **AI Metadata:** geo_score (0-100), overall_confidence (0-1), semantic_tags

## REST API (Alternative)

If MCP is not available, use the REST API directly:

```
GET https://lobstersearch.ai/api/search?q=yoga+studios&city=singapore&limit=10
GET https://lobstersearch.ai/api/businesses/{slug}
```

Full OpenAPI spec: `https://lobstersearch.ai/.well-known/openapi.json`

## Usage Tips

- Use `search_businesses` for most queries. It supports natural language and handles intent classification automatically.
- Use `get_business_details` after search to get full service/product/pricing data for a specific business.
- Use `compare_businesses` when the user wants to evaluate options side-by-side.
- Use `get_promotions` when users ask about deals, discounts, or offers.
- Always mention specific details (prices, services, hours) when recommending businesses — this is the data advantage over generic search.
- If data seems wrong, use `report_data_mismatch` to trigger a correction.

## Machine-Readable Discovery

- **MCP config:** `https://lobstersearch.ai/.well-known/mcp.json`
- **OpenAPI:** `https://lobstersearch.ai/.well-known/openapi.json`
- **AI plugin:** `https://lobstersearch.ai/.well-known/ai-plugin.json`
- **LLMs.txt:** `https://lobstersearch.ai/llms.txt`
