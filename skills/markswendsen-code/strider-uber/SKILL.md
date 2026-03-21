---
name: strider-uber
description: Request Uber rides via Strider Labs MCP connector. Get fare estimates, request pickups, track drivers, and manage ride history.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
    category: "transportation"
    author: "Strider Labs"
    homepage: "https://striderlabs.ai"
---

# Strider Uber Connector

MCP connector for requesting Uber rides and managing ride-related actions. Part of the Strider Labs action execution layer for AI agents.

## Installation

```bash
npm install @striderlabs/mcp-uber
```

## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "uber": {
      "command": "npx",
      "args": ["-y", "@striderlabs/mcp-uber"]
    }
  }
}
```

## Available Tools

### uber.request_ride
Request an Uber ride with pickup and dropoff locations.

**Input Schema:**
```json
{
  "pickup": "string (address or place name)",
  "dropoff": "string (address or place name)",
  "ride_type": "UberX | UberXL | Comfort | Black (optional)"
}
```

**Output:**
```json
{
  "ride_id": "string",
  "driver": {
    "name": "string",
    "rating": "number",
    "vehicle": "string"
  },
  "eta_minutes": "number",
  "fare_estimate": "string"
}
```

### uber.get_fare_estimate
Get fare estimates for a route without booking.

**Input:**
```json
{
  "pickup": "string",
  "dropoff": "string"
}
```

### uber.cancel_ride
Cancel an active ride request.

### uber.get_ride_status
Check the status of an active or recent ride.

## Authentication

First use triggers OAuth authorization flow:
1. User is redirected to Uber to authorize
2. Tokens are stored encrypted per-user
3. Automatic refresh handles token expiration

No API key required — connector manages OAuth flow.

## Usage Examples

**Request a basic ride:**
```
Get me an Uber from 123 Main St to SFO Airport
```

**Compare ride options:**
```
What's the fare estimate for an UberX vs Uber Black from downtown to the airport?
```

**Schedule ahead:**
```
Request an Uber to pick me up at my house tomorrow at 7am going to the train station
```

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| AUTH_EXPIRED | Session expired | Re-authenticate |
| AUTH_MFA_REQUIRED | Verification needed | Notify user |
| RATE_LIMITED | Too many requests | Retry after delay |
| SERVICE_UNAVAILABLE | Uber unavailable | Retry with backoff |

## Use Cases

- Airport transfers: get to/from the airport reliably
- Commuting: request rides when car is unavailable
- Night out: safe rides home without driving
- Business travel: expense-trackable rides in new cities

## Links

- npm: https://npmjs.com/package/@striderlabs/mcp-uber
- Strider Labs: https://striderlabs.ai
- MCP Registry: https://registry.modelcontextprotocol.io
