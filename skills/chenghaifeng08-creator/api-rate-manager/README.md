# API Rate Manager 🚦

**Smart API rate limit management with automatic retry, queuing, and cost optimization.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/api-rate-manager)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-available-orange.svg)](https://clawhub.com)

---

## 🎯 What It Solves

Tired of hitting API rate limits?

```
❌ Rate limit exceeded (retry in 60s, remaining: 0/120)
❌ Error 429: Too Many Requests
❌ This request requires more credits
```

**API Rate Manager** automatically handles all of that for you!

---

## ✨ Features

- 🔄 **Auto-Retry** - Automatically retries when rate limit hit
- 📦 **Request Queue** - Queues requests and processes when limit resets
- 📊 **Usage Stats** - Track API usage and optimize costs
- 🚦 **Smart Timing** - Schedules requests optimally
- 🔌 **Multi-API** - Works with any REST API

---

## 📦 Installation

```bash
clawhub install api-rate-manager
```

---

## 🚀 Quick Start

```javascript
const { RateManager } = require('api-rate-manager');

const manager = new RateManager({
  apiName: 'clawhub',
  limit: 120,        // requests per minute
  windowMs: 60000,   // 1 minute window
  retry: true        // auto-retry on limit
});

// Make API calls
await manager.call(() => {
  return clawhub.install('my-skill');
});
```

---

## 📖 Documentation

See [SKILL.md](SKILL.md) for full documentation.

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $19 | Core rate limiting, retry, queue |
| **Pro** | $49 | + Analytics, alerts, multi-API |

---

## 📝 Changelog

### v1.0.0 (2026-03-18)
- Initial release
- Auto-retry on rate limit
- Request queuing
- Multi-API support
- Usage statistics

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Support

- GitHub: https://github.com/openclaw/skills/api-rate-manager
- Discord: OpenClaw Community

---

*Built with ❤️ by OpenClaw Agent*
