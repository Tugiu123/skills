---
name: wechat-article-assistant
description: 本地微信公众号文章同步服务助手。用于搜索公众号、添加或删除公众号、获取最新文章、通过 aid 或 mp.weixin.qq.com 链接获取单篇文章详情、触发同步任务以及检查登录状态。
---

# 微信公众号文章助手

本 Skill 通过 Python CLI 工具与本地服务 `http://localhost:3010/api/public/v1` 通信：

```bash
python3 scripts/wechat_article_skill.py
```

## 功能

- 通过关键词搜索公众号
- 列出本地已添加的公众号
- 列出同步配置中的公众号
- 添加或删除公众号
- 当搜索结果唯一且完全匹配时，直接通过关键词添加公众号
- 获取最新文章列表
- 通过 `aid` 或公众号文章 URL 获取单篇文章详情
- 触发单个或全部公众号的同步任务
- 查看同步日志
- 启动登录流程并检查登录状态

## 服务检查

如果本地服务在端口 `3010` 不可用，请先从本仓库启动或刷新服务。

快速健康检查：

```bash
python3 scripts/wechat_article_skill.py recent --hours 24 --limit 1 --json
```

## 常用命令

搜索公众号：

```bash
python3 scripts/wechat_article_skill.py search "腾讯" --json
```

通过关键词添加公众号：

```bash
python3 scripts/wechat_article_skill.py add-account-by-keyword "四川省图书馆" --json
```

获取最新文章：

```bash
python3 scripts/wechat_article_skill.py recent --hours 24 --limit 10 --json
```

列出本地已添加的公众号：

```bash
python3 scripts/wechat_article_skill.py list-accounts --json
```

列出同步配置中的公众号：

```bash
python3 scripts/wechat_article_skill.py list-sync-accounts --json
```

通过 URL 获取文章详情：

```bash
python3 scripts/wechat_article_skill.py article \
  --link "https://mp.weixin.qq.com/s/example" \
  --json
```

通过 aid 获取文章详情：

```bash
python3 scripts/wechat_article_skill.py article --aid 2247493916_1 --json
```

触发同步任务：

```bash
python3 scripts/wechat_article_skill.py sync --fakeid "MzA4NTMxODEzOQ==" --json
```

检查登录状态：

```bash
python3 scripts/wechat_article_skill.py login-info --json
```

## 注意事项

- 文章详情接口使用 `/sync?action=article` 路径。
- `addAccountByKeyword` 会先搜索公众号，仅当存在唯一的完全匹配昵称、唯一的完全匹配别名，或搜索结果只有一条时，才会自动添加。
- 如果找到多个候选结果且没有完全匹配项，`addAccountByKeyword` 会返回候选列表而不是猜测添加。
- 当提供 `--link` 参数时，服务可以直接从 URL 解析公众号文章，无需预先缓存的文章。
- 请保持本 Skill 目录中的 JSON 清单与 CLI 工具一致，因为 Trae 可能会依赖这些元数据来发现工具。
