---
name: api-video-image
description: AI Media Generation via API | 通过API生成图片和视频。【触发词】帮我生成图片/画个图/做个视频/生成视频/文生图/图生图/AI图片/AI视频/用Sora生成/用Gemini画。使用 Gemini 生成图片（文生图、图生图），使用 Sora/veo 生成视频（文生视频）。支持 Prompt 优化建议、错误重试机制、异步任务轮询。
version: 1.4.0
author: lrs
tags:
  - image-generation
  - video-generation
  - gemini
  - sora
  - ai-media
  - api
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins:
        - python3
---

# API Video & Image Generation
# AI 图片与视频生成

## 0. Trigger Words | 触发词

**激活本技能的场景：**
- "帮我生成一张图片" / "画个图"
- "做个视频" / "生成视频"
- "文生图" / "图生图"
- "AI生成" / "用Sora生成" / "用Gemini画"

---

## 决策树

```
收到生成请求
  ↓
1. 检查 USER.md 中 中转站地址，API端点，API 配置
  ├─ 配置正确 → 使用配置
  └─ 配置缺失/错误 → 要求用户提供 → 自动修复 USER.md 配置
  ↓
2. 判断类型
  ├─ 图片生成（文生图/图生图）→ 默认Gemini API → 错误 → 要求用户指定模型
  └─ 视频生成 → 默认Sora/veo API → 错误 → 要求用户指定模型
  ↓
3. 执行生成 → 异步轮询 → 返回结果
```

## ⚙️ 配置要求 | Configuration

### 正确格式（脚本能识别的格式）：

```markdown
## 中转站AI生成配置

### 图片生成
- 中转站API 地址: https://jeniya.cn/v1beta/models/gemini-3-pro-image-preview:generateContent
- 模型选择: models/gemini-3-pro-image-preview:generateContent
- API Key: sk-aeXk你的Key

### 视频生成
- 中转站API 地址: https://jeniya.cn/v1/v1/video/create
- 模型选择: models/sora-2-pro-all/veo_3_1-4K
- API Key: sk-0PzKg你的Key
```

---

## 🚀 Quick Start | 快速上手

**用户说：** "帮我画一张科幻风格的未来城市"

**AI 执行：**
1. ✅ 检查配置（USER.md）
2. ✅ 优化 Prompt（结构化）
3. ✅ 执行：`python3 scripts/gen_image.py "prompt"`
4. ✅ 输出：`MEDIA:<绝对路径>` 让 OC 自动附件

---

## 1. 执行检查清单 | Execution Checklist

**每次生成前必须确认：**
- [ ] Step 0：USER.md 配置正确，脚本能读取到 URL 和 Key
- [ ] Step 1：已理解用户需求（图片/视频/风格/场景）
- [ ] Step 2：Prompt 已优化（结构化、有细节）
- [ ] Step 3：输出路径已确认（~/Desktop/）
- [ ] 生成完成后：输出 `MEDIA:<绝对路径>` 让 OC 自动附件

---

## 2. 工作流程

```
Step 0: 检查配置 → Step 1: 理解需求 → Step 2: Prompt优化 → Step 3: 执行生成 → Step 4: 交付用户
```

### Step 0: 检查并修复配置

**首次使用时必须执行此步骤：**

1. 读取 `~/.openclaw/workspace/USER.md` 中的中转站AI生成配置
2. 检查是否包含正确的"图片生成"和"视频生成"区块
3. 检查是否有"中转站API 地址"和"API Key"字段
4. 如果格式不对或缺少配置 → **AI 帮您更新 USER.md 为正确格式**

### Step 1: 理解需求

用户说"帮我生成一张图"或"做个视频"时：
1. 询问具体内容/场景/风格
2. 判断是文生图、图生图、还是视频
3. 整理成结构化 Prompt

### Step 2: Prompt 优化

**Prompt 结构 | Prompt Structure：**

| 组成部分 | 说明 | 示例 |
|---------|------|------|
| Subject | 主体 | 一只猫、未来城市 |
| Style | 风格 | 赛博朋克、宫崎骏、水墨画 |
| Lighting | 光线 | 逆光、柔光、日落 |
| Composition | 构图 | 全身、半身、特写 |
| Details | 细节 | 表情、服装、环境 |
| Quality | 质量 | 4K、高清、电影感 |

**图片 Prompt 示例：**
> 原始："一只猫"
> 结构化："橘色英国短毛猫，阳光下慵懒姿态，写实风格，高清摄影，暖色调"

**视频 Prompt 示例：**
> 原始："日出"
> 结构化："清晨日出，太阳缓缓升起，金色阳光穿透薄雾，城市天际线，云层缓慢流动，航拍视角，4K"

### Step 3: 执行生成

**图片生成：**
```bash
python3 scripts/gen_image.py "优化后的prompt" [output_path] [ref_image_path]
```

**视频生成：**
```bash
python3 scripts/gen_video.py "优化后的prompt" [model] [size] [output_path]
```

---

## 3. 图片生成

### 使用方法

```bash
python3 scripts/gen_image.py "prompt" [output_path] [ref_image_path]
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | ✅ | - | 图片描述/提示词 |
| output_path | ❌ | ~/Desktop/img_*.png | 保存路径 |
| ref_image_path | ❌ | None | 参考图片路径，传参则图生图 |

### 输出

- 成功：输出 `MEDIA:<绝对路径>` 让 OC 自动附件
- 失败：返回错误信息，需要重试

### 重试机制

图片生成失败时，自动重试最多3次

---

## 4. 视频生成

### 使用方法

```bash
python3 scripts/gen_video.py "prompt" [model] [size] [output_path]
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | ✅ | - | 视频场景描述 |
| model | ❌ | sora-2-pro-all | 生成模型 |
| size | ❌ | 16:9 | 画面比例 |
| output_path | ❌ | ~/Desktop/vid_*.mp4 | 保存路径 |

### 模型选项

| 模型 | 特点 |
|------|------|
| sora-2-pro-all | Sora 2，视频生成首选 |
| veo_3_1-4K | Veo 3.1，4K高清 |

### 画面比例

| 比例 | 用途 |
|------|------|
| 16:9 | 横版视频（默认） |
| 9:16 | 竖版视频（短视频） |

### 异步处理

视频生成是异步的：
1. 发起请求 → 获取 task_id
2. 轮询查询状态（每5秒）
3. 任务完成 → 下载视频
4. 超时时间：300秒

### 重试机制

视频生成可能失败：
- 网络问题 → 重试
- API限流 → 等待10秒后重试
- 超时 → 提示用户

---

## 5. 交付用户 | Delivery

**生成完成后必须输出：**
```
MEDIA:/Users/lrs/Desktop/xxx.png
MEDIA:/Users/lrs/Desktop/xxx.mp4
```

OC 会自动附件文件到消息中。

---

## 6. 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| API Key无效 | 检查 USER.md 配置 |
| 网络超时 | 重试3次 |
| 内容审核拒绝 | 提示用户修改 Prompt |
| 任务超时 | 提示用户，重新生成 |

---

## 7. 安全注意 | Security

**Shell 路径清理：**
- 输出文件时确保路径只包含 `A-Za-z0-9._-`
- 使用 `tr -cd 'A-Za-z0-9._-'` 清理特殊字符
- 禁止将未清理的路径传给 shell

---

## 8. 文件结构 | File Structure

```
api-video-image/
├── SKILL.md                      # 技能核心定义（工作流程、规则、触发词）
└── scripts/
    ├── gen_image.py              # 图片生成脚本（文生图/图生图）
    └── gen_video.py             # 视频生成脚本（异步任务+轮询）
```

---

## 9. 边界 | Boundaries

- 本技能只负责生成图片/视频
- 不负责发送消息（由 OC 自动附件）
- 不负责内容审核（用户对内容负责）
- 不记录用户生成的图片/视频

---

## 10. 更新日志

- v1.4.0: 增加执行检查清单、Prompt结构表、MEDIA自动附件、安全注释
- v1.3.0: 配置改为从 USER.md 读取中转地址和密钥
- v1.2.0: 增加触发词、Quick Start
- v1.1.0: 增加Prompt优化、错误处理，重试机制
- v1.0.0: 初版发布
