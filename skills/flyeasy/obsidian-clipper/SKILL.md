---
name: obsidian-clipper
description: >
  Save web content (articles, videos, notes) to Obsidian vault with automatic classification,
  intelligent naming, and content extraction. Supports: 小红书 (Xiaohongshu), YouTube, 知乎,
  WeChat articles, and general web pages. Auto-categorizes into AI tools, hobbies, or tutorials.
  Trigger words: 收藏, 保存到obsidian, 归档, clip, save to obsidian. Use when user sends links
  or asks to save content to Obsidian.
version: 1.0.0
author: Lucien L
license: MIT
tags: [obsidian, clipper, web-scraping, content-management, 小红书, youtube, 知乎]
---

# Obsidian Clipper

将网页、文章、视频、小红书笔记等内容收藏到主人的 Obsidian vault。

## 存储路径

**主目录**: `~/Documents/Obsidian/Lzz_Vault/收藏文档/`

**分类子目录**:
- `AI工具/` - AI工具评测、AI产品、机器学习相关
- `兴趣爱好/` - 路亚、户外、游戏、音乐等个人兴趣
- `技术教程/` - 编程教程、技术文档、开发指南

## 文件命名规范

**格式**: `「来源类型」主题-YYYY.MM.DD.md`

**来源类型**:
- `「小红书」` - 小红书笔记
- `「Youtube视频」` - YouTube 视频
- `「知乎文章」` - 知乎文章
- `「网页」` - 普通网页
- `「公众号」` - 微信公众号文章
- `「技术文档」` - 官方文档、技术博客

**示例**:
- `「小红书」AI转3D工具评测-2026.03.12.md`
- `「Youtube视频」Andrej Karpathy谈LLM-2026.03.12.md`
- `「网页」OpenClaw配置指南-2026.03.12.md`

## 工作流程

### 1. 接收输入

用户可能提供：
- 直接链接（小红书、YouTube、知乎等）
- 内容描述 + 要求收藏
- 多个链接批量处理

### 2. 获取内容

根据来源类型选择方法：

**小红书链接** (`xhslink.com`):
- 无法直接抓取，使用网络搜索获取相关内容
- 搜索关键词：标题 + 主题
- 整合多个来源补充内容

**普通网页**:
- 使用 `web_fetch` 抓取内容
- 提取标题、正文、关键信息

**YouTube 视频**:
- 使用 `web_search` 搜索视频标题 + 内容
- 整合搜索结果整理要点

### 3. 自动分类

根据内容关键词判断类别：

| 关键词 | 分类 |
|--------|------|
| AI、机器学习、LLM、GPT、Claude、工具评测 | AI工具/ |
| 路亚、钓鱼、户外、游戏、音乐、运动 | 兴趣爱好/ |
| 编程、代码、教程、开发、配置、部署 | 技术教程/ |

**不确定时询问用户**

### 4. 生成文档

**Markdown 结构**:

```markdown
# {标题}

**来源**: {来源链接或描述}
**保存日期**: {YYYY.MM.DD}
**类别**: {分类路径}

---

## 摘要

{简短摘要，1-3句话}

---

## 正文内容

{整理后的内容}

---

## 关键要点

- {要点1}
- {要点2}
- {要点3}

---

## 相关链接

- {原始链接}
- {其他参考}

---

*收藏人: 万茜*
```

### 5. 保存文件

1. 确定分类目录
2. 生成文件名
3. 使用 `write` 工具保存
4. 向用户确认保存路径

## 使用示例

**用户**: "收藏这个小红书链接 http://xhslink.com/xxx"

**处理流程**:
1. 识别来源：小红书
2. 搜索相关内容
3. 判断分类（如 AI工具/）
4. 生成文件名：`「小红书」AI转3D工具评测-2026.03.12.md`
5. 保存到：`~/Documents/Obsidian/Lzz_Vault/收藏文档/AI工具/`
6. 回复：✅ 已保存到 Obsidian

## 注意事项

1. **小红书链接**：无法直接访问，需通过网络搜索补充
2. **分类不确定**：主动询问用户
3. **批量处理**：逐个处理，统一回复
4. **内容过长**：提取核心要点，避免冗余
5. **日期格式**：统一使用 `YYYY.MM.DD`

## 批量收藏

用户一次发送多个链接时：

1. 逐个处理每个链接
2. 记录所有保存路径
3. 统一回复所有结果

示例回复：
```
✅ 已保存 3 篇到 Obsidian

1. 「小红书」AI转3D工具 → 收藏文档/AI工具/
2. 「小红书」路亚教程 → 收藏文档/兴趣爱好/
3. 「小红书」OpenClaw优化 → 收藏文档/AI工具/
```
