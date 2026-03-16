# Usage Examples

Real conversation examples showing each LobsterSearch MCP tool in action.

---

## search_businesses

> "Find me a hair salon near Tiong Bahru that's open on Sundays"

**Tool call:**
```json
{
  "tool": "search_businesses",
  "arguments": {
    "query": "hair salon near Tiong Bahru open on Sundays",
    "country_code": "SG"
  }
}
```

**Response (truncated):**
```json
{
  "results": [
    {
      "business_id": "a1b2c3d4-...",
      "name": "Hue Salon",
      "business_type": "salon_hair",
      "neighbourhood": "Tiong Bahru",
      "overall_confidence": 0.92,
      "operating_hours": {
        "sunday": { "open": "10:00", "close": "18:00" }
      },
      "match_explanation": "Hair salon in Tiong Bahru, confirmed open Sundays 10am-6pm"
    }
  ],
  "answer_quality_score": 0.88,
  "total_results": 3
}
```

---

## get_business_details

> "Tell me more about that salon — what services do they offer and how much do they cost?"

**Tool call:**
```json
{
  "tool": "get_business_details",
  "arguments": {
    "business_id": "a1b2c3d4-...",
    "include_services": true,
    "include_promotions": true
  }
}
```

**Response (truncated):**
```json
{
  "name": "Hue Salon",
  "address": "71 Seng Poh Rd, #01-35, Singapore 160071",
  "phone": "+65 6222 0088",
  "website": "https://huesalon.sg",
  "services": [
    {
      "name": "Women's Haircut & Blow Dry",
      "price_min": 55,
      "price_max": 75,
      "currency": "SGD",
      "duration": "60 min"
    },
    {
      "name": "Full Hair Colouring",
      "price_min": 120,
      "price_max": 180,
      "currency": "SGD",
      "duration": "120 min"
    }
  ],
  "payment_methods": ["cash", "visa", "mastercard", "paynow"],
  "languages_spoken": ["en", "zh"]
}
```

---

## list_nearby_businesses

> "Are there any restaurants within 1km of Raffles Place?"

**Tool call:**
```json
{
  "tool": "list_nearby_businesses",
  "arguments": {
    "latitude": 1.2840,
    "longitude": 103.8515,
    "radius_km": 1,
    "business_type": "restaurant",
    "max_results": 5
  }
}
```

**Response (truncated):**
```json
{
  "results": [
    {
      "name": "Keisuke Ramen",
      "distance_km": 0.3,
      "business_type": "restaurant",
      "neighbourhood": "Tanjong Pagar",
      "overall_confidence": 0.95
    },
    {
      "name": "Lolla",
      "distance_km": 0.5,
      "business_type": "restaurant",
      "neighbourhood": "Ann Siang Hill",
      "overall_confidence": 0.91
    }
  ],
  "total_results": 5
}
```

---

## get_promotions

> "What promotions are running in Singapore right now?"

**Tool call:**
```json
{
  "tool": "get_promotions",
  "arguments": {
    "country_code": "SG"
  }
}
```

**Response (truncated):**
```json
{
  "promotions": [
    {
      "business_name": "The Nail Social",
      "title": "20% Off Classic Manicure",
      "description": "Valid for first-time customers",
      "promo_code": "NAILNEW20",
      "valid_until": "2026-04-30"
    },
    {
      "business_name": "ActiveSG Gym",
      "title": "Free Trial Week",
      "description": "7-day unlimited access for new members",
      "valid_until": "2026-03-31"
    }
  ],
  "total_results": 8
}
```

---

## compare_businesses

> "Compare Hue Salon and The Nail Social side by side"

**Tool call:**
```json
{
  "tool": "compare_businesses",
  "arguments": {
    "business_ids": ["a1b2c3d4-...", "e5f6g7h8-..."]
  }
}
```

**Response (truncated):**
```json
{
  "businesses": [
    {
      "name": "Hue Salon",
      "business_type": "salon_hair",
      "geo_score": 78,
      "overall_confidence": 0.92,
      "service_count": 12,
      "price_range": "$55 - $180 SGD",
      "neighbourhood": "Tiong Bahru"
    },
    {
      "name": "The Nail Social",
      "business_type": "nail",
      "geo_score": 72,
      "overall_confidence": 0.88,
      "service_count": 8,
      "price_range": "$28 - $65 SGD",
      "neighbourhood": "Haji Lane"
    }
  ]
}
```

---

## get_trending

> "What businesses are trending this week in Singapore?"

**Tool call:**
```json
{
  "tool": "get_trending",
  "arguments": {
    "country_code": "SG",
    "days": 7,
    "max_results": 5
  }
}
```

**Response (truncated):**
```json
{
  "trending": [
    {
      "name": "Keisuke Ramen",
      "business_type": "restaurant",
      "query_count": 42,
      "geo_score": 85,
      "trend": "rising"
    },
    {
      "name": "Hue Salon",
      "business_type": "salon_hair",
      "query_count": 28,
      "geo_score": 78,
      "trend": "stable"
    }
  ],
  "period": "2026-03-06 to 2026-03-13"
}
```

---

## report_data_mismatch

> "The phone number for Hue Salon is wrong — it should be +65 9123 4567"

**Tool call:**
```json
{
  "tool": "report_data_mismatch",
  "arguments": {
    "business_id": "a1b2c3d4-...",
    "field_name": "phone",
    "expected_value": "+65 6222 0088",
    "actual_value": "+65 9123 4567"
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "message": "Data mismatch report received. A priority re-crawl has been queued for this business.",
  "business_id": "a1b2c3d4-..."
}
```
