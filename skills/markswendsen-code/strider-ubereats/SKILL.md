---
name: strider-ubereats
description: Order food delivery via Uber Eats using Strider Labs MCP connector. Search restaurants, browse menus, customize orders, track delivery in real-time. Complete autonomous food ordering for your AI agent.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
    category: "food"
    author: "Strider Labs"
    homepage: "https://striderlabs.ai"
---

# Strider Uber Eats Connector

MCP connector for ordering food delivery through Uber Eats — search restaurants, browse menus, customize orders, and track delivery in real-time. Part of the Strider Labs action execution layer for AI agents.

## Installation

```bash
npm install @striderlabs/mcp-ubereats
```

## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "ubereats": {
      "command": "npx",
      "args": ["-y", "@striderlabs/mcp-ubereats"]
    }
  }
}
```

## Available Tools

### ubereats.search_restaurants
Search for restaurants by cuisine, keyword, or filters.

**Input Schema:**
```json
{
  "query": "string (optional: search terms)",
  "cuisine": "string (optional: sushi, indian, burgers, etc.)",
  "address": "string (delivery address)",
  "sort": "string (optional: popular, rating, delivery_time, price)",
  "filters": {
    "offers": "boolean (optional: has promotions)",
    "free_delivery": "boolean (optional)"
  }
}
```

**Output:**
```json
{
  "restaurants": [{
    "id": "string",
    "name": "string",
    "cuisine": ["string"],
    "rating": "number",
    "delivery_time_min": "number",
    "delivery_fee": "number",
    "promotion": "string (if available)"
  }]
}
```

### ubereats.get_menu
Get full menu for a restaurant with categories and options.

### ubereats.add_to_cart
Add items to cart with customizations.

**Input Schema:**
```json
{
  "restaurant_id": "string",
  "item_id": "string",
  "quantity": "number",
  "customizations": {
    "size": "string",
    "add_ons": ["string"],
    "special_instructions": "string"
  }
}
```

### ubereats.apply_promo
Apply a promo code to the order.

### ubereats.checkout
Complete order with delivery address, tip, and payment.

**Input Schema:**
```json
{
  "delivery_address": "object",
  "tip_amount": "number",
  "payment_method_id": "string",
  "delivery_instructions": "string (optional)"
}
```

### ubereats.track_order
Get real-time order status with driver location.

### ubereats.get_past_orders
Retrieve order history.

### ubereats.schedule_order
Schedule an order for future delivery.

**Input Schema:**
```json
{
  "scheduled_time": "string (ISO datetime)"
}
```

## Authentication

First use triggers OAuth with Uber account (shared with Uber rides). Tokens stored encrypted per-user.

## Usage Examples

**Quick lunch:**
```
Order something from the highest-rated sushi place on Uber Eats that can deliver in under 30 minutes
```

**Scheduled order:**
```
Schedule Uber Eats delivery from Chipotle for tomorrow at noon
```

**Deal hunting:**
```
Find restaurants on Uber Eats with free delivery promos near me
```

**Tracking:**
```
Where's my Uber Eats order? When will it arrive?
```

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| AUTH_EXPIRED | Session expired | Re-authenticate |
| RESTAURANT_BUSY | High demand | Suggest alternatives |
| PROMO_INVALID | Promo code expired | Try different code |
| SURGE_PRICING | Higher delivery fees | Inform and proceed or wait |

## Use Cases

- Meal delivery: order breakfast, lunch, or dinner
- Scheduled meals: pre-order for specific times
- Group orders: coordinate orders for teams or parties
- Deal optimization: find promotions and free delivery

## Links

- npm: https://npmjs.com/package/@striderlabs/mcp-ubereats
- Strider Labs: https://striderlabs.ai
