# Slide Creator - 产品路线图

## 待做功能

### 分享功能（需要调研）

**背景：**
- tiiny.host 免费版仅 1 小时有效期，付费版不适合
- 用户明确要求"零依赖"方案

**候选方案：**

#### 方案 1：Cloudflare Pages（推荐，但有依赖）
- ✅ 中国访问相对稳定
- ✅ 免费额度大，无过期时间
- ✅ 完整的 API 支持
- ❌ 必须安装 `wrangler` CLI（npm 包）

**实现方式：**
```bash
npm install -g wrangler
wrangler login  # 首次需要授权
wrangler pages deploy ./presentation.html --project-name=my-slides
```

**集成思路：**
- 在 SKILL.md 添加 `--share cloudflare` 命令
- 脚本检测 wrangler 是否已安装
- 未安装时提示用户：`npm install -g wrangler`

#### 方案 2：GitHub Pages（零依赖）
- ✅ 完全零依赖（仅需 git）
- ⚠️ 中国访问不稳定（但比 Vercel 好）
- ⚠️ 需要用户有 GitHub 账号和仓库

**实现方式：**
```bash
git add presentation.html
git commit -m "Add presentation"
git push
# 然后在 GitHub 仓库设置中启用 Pages
```

**集成思路：**
- 脚本检测当前目录是否为 git 仓库
- 自动 commit + push
- 提供 GitHub Pages 设置链接

#### 方案 3：放弃自动分享
- 只生成 HTML，用户自己选择分享方式
- 在 SKILL.md 中提供手动指导：
  - GitHub Pages 分享步骤
  - Cloudflare Pages 分享步骤
  - 其他平台（腾讯云 COS、阿里云 OSS 等）

---

## 已完成功能

- [x] 21 种风格预设 + 内容类型路由
- [x] 视觉风格预览（Phase 2 的 3 个迷你预览）
- [x] 渐进式披露架构（v2.0.0 重构）
- [x] 中英文双语支持
- [x] PPTX 导出（`--export pptx`）
- [x] Presenter Mode（演讲者模式）
- [x] 内联编辑模式（浏览器中直接编辑文字）