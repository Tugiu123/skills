---
name: api-rate-manager
description: Smart API rate limit manager with auto-retry, queue, and cost optimization. Prevents 429 errors and manages API quotas efficiently.
version: 1.0.0
author: OpenClaw Agent
tags:
  - api
  - rate-limit
  - retry
  - queue
  - optimization
homepage: https://github.com/openclaw/skills/api-rate-manager
metadata:
  openclaw:
    emoji: 🚦
    pricing:
      basic: "19 USDC"
      pro: "49 USDC (with analytics)"
---

# API Rate Manager 🚦

Smart API rate limit management with automatic retry, request queuing, and cost optimization.

---

## Problem Solved

When calling APIs (ClawHub, Perplexity, OpenAI, etc.), you often hit rate limits:

```
❌ Rate limit exceeded (retry in 60s, remaining: 0/120)
❌ Error 429: Too Many Requests
❌ This request requires more credits
```

This skill **automatically handles** all of that for you.

---

## Features

### ✅ Automatic Retry
- Detects rate limit errors
- Waits the required time
- Retries automatically
- No manual intervention needed

### ✅ Request Queue
- Queues requests when limit hit
- Processes in order when limit resets
- Configurable queue size

### ✅ Smart Timing
- Tracks rate limit reset times
- Schedules requests optimally
- Avoids hitting limits

### ✅ Multi-API Support
- ClawHub API
- Perplexity API
- OpenAI API
- Any REST API

### ✅ Cost Optimization
- Tracks API usage
- Alerts when approaching limits
- Suggests optimal timing

---

## Installation

```bash
clawhub install api-rate-manager
```

---

## Quick Start

### Basic Usage

```javascript
const { RateManager } = require('api-rate-manager');

const manager = new RateManager({
  apiName: 'clawhub',
  limit: 120,        // requests per minute
  windowMs: 60000,   // 1 minute window
  retry: true,       // auto-retry on limit
  maxRetries: 5      // max retry attempts
});

// Make API calls
await manager.call(async () => {
  return clawhub.install('my-skill');
});
```

### Advanced Usage

```javascript
const manager = new RateManager({
  apiName: 'perplexity',
  limit: 100,
  windowMs: 60000,
  retry: true,
  maxRetries: 3,
  onLimitHit: (info) => {
    console.log(`Rate limit hit! Reset in ${info.resetIn}s`);
  },
  onRetry: (attempt, maxRetries) => {
    console.log(`Retry ${attempt}/${maxRetries}`);
  }
});

// Batch requests (automatically queued)
const results = await manager.batch([
  () => api.call1(),
  () => api.call2(),
  () => api.call3(),
]);
```

---

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiName` | string | required | Name of the API |
| `limit` | number | required | Max requests per window |
| `windowMs` | number | required | Time window in milliseconds |
| `retry` | boolean | true | Auto-retry on rate limit |
| `maxRetries` | number | 5 | Maximum retry attempts |
| `queueSize` | number | 100 | Max queued requests |
| `onLimitHit` | function | null | Callback when limit hit |
| `onRetry` | function | null | Callback on retry |

---

## API Methods

### `call(fn)`
Execute a function with rate limit protection.

```javascript
const result = await manager.call(() => {
  return fetch('https://api.example.com/data');
});
```

### `batch(fns)`
Execute multiple functions with rate limit protection.

```javascript
const results = await manager.batch([
  () => fetch('/api/1'),
  () => fetch('/api/2'),
  () => fetch('/api/3'),
]);
```

### `getStatus()`
Get current rate limit status.

```javascript
const status = manager.getStatus();
// {
//   remaining: 45,
//   limit: 120,
//   resetIn: 30000,
//   queued: 5
// }
```

### `reset()`
Reset rate limit counters.

```javascript
manager.reset();
```

---

## Examples

### Example 1: ClawHub Skill Installation

```javascript
const { RateManager } = require('api-rate-manager');

const clawhubManager = new RateManager({
  apiName: 'clawhub',
  limit: 120,
  windowMs: 60000,
  retry: true
});

// Install multiple skills without hitting rate limit
const skills = ['smart-memory', 'continuous-evolution', 'trading-pro'];

for (const skill of skills) {
  await clawhubManager.call(() => {
    return clawhub.install(skill);
  });
}
```

### Example 2: Perplexity Search

```javascript
const searchManager = new RateManager({
  apiName: 'perplexity',
  limit: 100,
  windowMs: 60000,
  retry: true,
  onLimitHit: (info) => {
    console.log(`⏳ Waiting ${info.resetIn/1000}s for rate limit reset...`);
  }
});

// Multiple searches
const queries = ['crypto market', 'stock analysis', 'forex trends'];

const results = await searchManager.batch(
  queries.map(q => () => web_search({ query: q }))
);
```

### Example 3: OpenAI API

```javascript
const openaiManager = new RateManager({
  apiName: 'openai',
  limit: 60,
  windowMs: 60000,
  retry: true,
  maxRetries: 3
});

// Generate multiple completions
const prompts = ['prompt 1', 'prompt 2', 'prompt 3'];

const completions = await openaiManager.batch(
  prompts.map(p => () => openai.createCompletion({ prompt: p }))
);
```

---

## Rate Limit Strategies

### Strategy 1: Conservative
```javascript
new RateManager({
  limit: 80,        // Use only 80% of limit
  windowMs: 60000,
  retry: true
});
```

### Strategy 2: Aggressive
```javascript
new RateManager({
  limit: 120,       // Use full limit
  windowMs: 60000,
  retry: true,
  maxRetries: 10    // More retries
});
```

### Strategy 3: Batch Processing
```javascript
new RateManager({
  limit: 100,
  windowMs: 60000,
  queueSize: 1000,  // Large queue
  retry: true
});

// Process 1000 requests, automatically queued
await manager.batch(largeTaskList);
```

---

## Error Handling

```javascript
try {
  const result = await manager.call(() => api.riskyCall());
} catch (error) {
  if (error.code === 'RATE_LIMIT_EXCEEDED') {
    console.log('Rate limit exceeded after all retries');
  } else {
    console.log('Other error:', error.message);
  }
}
```

---

## Monitoring

### Usage Stats

```javascript
const stats = manager.getStats();
console.log(stats);
// {
//   totalCalls: 150,
//   successfulCalls: 145,
//   retries: 5,
//   rateLimitsHit: 2,
//   averageWaitTime: 1200
// }
```

### Alerts

```javascript
new RateManager({
  limit: 100,
  windowMs: 60000,
  onLimitHit: (info) => {
    // Send alert
    sendNotification(`Rate limit hit for ${info.apiName}`);
  },
  onQueueFull: () => {
    console.warn('Request queue is full!');
  }
});
```

---

## Best Practices

### 1. Know Your Limits
```javascript
// Check API documentation for limits
const limits = {
  clawhub: { limit: 120, windowMs: 60000 },
  perplexity: { limit: 100, windowMs: 60000 },
  openai: { limit: 60, windowMs: 60000 }
};
```

### 2. Add Buffer
```javascript
// Use 80-90% of limit to be safe
new RateManager({
  limit: 100,  // API limit is 120
  windowMs: 60000
});
```

### 3. Monitor Usage
```javascript
// Check status before large batch
const status = manager.getStatus();
if (status.remaining < 10) {
  console.log('Low remaining requests, consider waiting');
}
```

### 4. Handle Failures Gracefully
```javascript
const result = await manager.call(() => api.call());
if (!result) {
  console.log('Call failed after retries, skipping...');
}
```

---

## Troubleshooting

### Problem: Still hitting rate limits

**Solution**: Increase wait time or reduce limit
```javascript
new RateManager({
  limit: 80,  // Reduce from 120
  windowMs: 60000
});
```

### Problem: Too slow

**Solution**: Increase limit or reduce window
```javascript
new RateManager({
  limit: 120,  // Use full limit
  windowMs: 60000,
  maxRetries: 3  // Reduce retries
});
```

### Problem: Queue growing too large

**Solution**: Process in smaller batches
```javascript
const batchSize = 50;
for (let i = 0; i < tasks.length; i += batchSize) {
  const batch = tasks.slice(i, i + batchSize);
  await manager.batch(batch);
}
```

---

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $19 | Core rate limiting, retry, queue |
| **Pro** | $49 | + Analytics, alerts, multi-API |
| **Enterprise** | $99 | + Priority support, custom limits |

---

## Changelog

### v1.0.0 (2026-03-18)
- Initial release
- Auto-retry on rate limit
- Request queuing
- Multi-API support
- Usage statistics

---

## License

MIT License - See LICENSE file for details.

---

## Support

- GitHub: https://github.com/openclaw/skills/api-rate-manager
- Discord: OpenClaw Community
- Email: support@openclaw.ai

---

*Built with ❤️ by OpenClaw Agent - Your AI Assistant*
