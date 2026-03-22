# Social Content Pro 📱

> AI-powered viral content generator for TikTok, Instagram, Twitter, LinkedIn, and Xiaohongshu.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)

## 🎯 What It Does

Social Content Pro helps creators and marketers:

- **Multi-Platform Content** - Generate posts for TikTok, Instagram, Twitter, LinkedIn, Xiaohongshu
- **Viral Hooks** - Access proven viral hook templates
- **Smart Hashtags** - Get optimal hashtags for each platform
- **Content Calendar** - Plan 30 days of content in minutes
- **Competitor Analysis** - Learn from top performers in your niche
- **Auto-Scheduling** - Post at optimal times automatically

## 📦 Installation

```bash
# Install via ClawHub
npx clawhub@latest install social-content-pro

# Or clone manually
git clone https://github.com/openclaw/skills/social-content-pro
cd social-content-pro
npm install
```

## 🚀 Quick Start

```javascript
const { SocialContentPro } = require('social-content-pro');

const creator = new SocialContentPro({
  apiKey: 'your-api-key',
  niche: 'crypto trading',
  platforms: ['tiktok', 'twitter', 'xiaohongshu'],
  tone: 'professional'
});

// Generate content ideas
const ideas = await creator.generateIdeas({ count: 10 });
console.log(ideas);

// Create platform-specific post
const post = await creator.createPost({
  topic: 'Bitcoin halving explained',
  platform: 'twitter',
  format: 'thread'
});
console.log(post);

// Get viral hashtags
const hashtags = await creator.getHashtags({
  niche: 'crypto',
  platform: 'instagram',
  count: 30
});
console.log(hashtags);
```

## 📊 Key Features

### Platform Support
- **TikTok** - Short video scripts, hooks, captions
- **Instagram** - Posts, Stories, Reels captions
- **Twitter/X** - Threads, tweets, engagement hooks
- **LinkedIn** - Professional posts, articles
- **Xiaohongshu** - 小红书笔记 (Chinese market)

### Content Generation
- AI-powered idea generation
- Viral hook library (10+ proven templates)
- Platform-specific optimization
- Auto-hashtag generation
- Content calendar planning

### Analytics (Pro)
- Engagement rate tracking
- Follower growth analysis
- Best performing content types
- Competitor benchmarking

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $39 | Content generation, hashtag engine, calendar planning |
| **Pro** | $79 | + Analytics, auto-posting, competitor analysis, A/B testing |

## ⚠️ Disclaimer

This tool is for content creation assistance only. Results may vary. Always create authentic, valuable content for your audience.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Support

- **GitHub**: https://github.com/openclaw/skills/social-content-pro
- **Discord**: OpenClaw Community
- **Email**: support@openclaw.ai

---

*Built with ❤️ by OpenClaw Agent*
