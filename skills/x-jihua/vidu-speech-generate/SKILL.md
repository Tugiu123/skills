---
name: vidu-speech-generate
version: 1.0.0
description: "Vidu AI 语音合成与声音复刻。支持303个音色TTS语音合成、声音复刻功能。对话式调用，自动推荐音色。"
---

# Vidu Speech Generate 🔊

Vidu AI 语音合成与声音复刻工具，专注于音频生成功能。

## 环境说明

**变量说明**：
- `{baseDir}` - 运行时自动替换为本 skill 目录的绝对路径
  - 实际路径：`~/.openclaw/workspace/skills/vidu-speech-generate/`

**环境变量**：
- `VIDU_API_KEY` - Vidu API 密钥（必需）

## 快速开始

直接告诉我你想生成什么语音，我会自动选择合适的音色：

```
"用少女音配音这段话：大家好，欢迎来到我的频道"
"用播报男声朗读这段教程内容"
"帮我复刻这个音频的声音"
```

## 支持的音频类型

| 类型 | 触发条件 | 说明 |
|------|----------|------|
| TTS语音合成 | "配音"、"朗读"、语音描述 | 文字转语音 |
| 声音复刻 | "复刻声音"、"克隆音色" | 根据音频复刻音色 |

## 自动识别规则

```
用户输入 → 意图识别
─────────────────────────────
"配音" + 文本 → TTS语音合成
"复刻声音" + 音频 → 声音复刻
```

## TTS 语音合成

### 自动音色推荐

根据内容场景自动选择合适音色：

| 场景 | 推荐音色 | Voice ID |
|------|----------|----------|
| 小红书/短视频（女） | 少女音色 | `female-shaonv` |
| 小红书/短视频（男） | 精英青年 | `male-qn-jingying` |
| 教程/科普 | 播报男声 | `Chinese (Mandarin)_Male_Announcer` |
| 情感/故事 | 御姐音色 | `female-yujie` |
| 商务/产品 | 沉稳高管 | `Chinese (Mandarin)_Reliable_Executive` |
| 可爱/萌系 | 萌萌女童 | `lovely_girl` |
| 搞笑/轻松 | 搞笑大爷 | `Chinese (Mandarin)_Humorous_Elder` |
| 温馨/治愈 | 温暖少女 | `Chinese (Mandarin)_Warm_Girl` |
| 甜美风格 | 甜美女声 | `Chinese (Mandarin)_Sweet_Lady` |
| 专业主持 | 新闻女声 | `Chinese (Mandarin)_News_Anchor` |
| 英文内容 | 男声 | `English_Trustworthy_Man` |
| 英文内容 | 女声 | `English_Graceful_Lady` |
| 日文内容 | 男声 | `Japanese_GentleButler` |
| 日文内容 | 女声 | `Japanese_KindLady` |
| 韩文内容 | 女声 | `Korean_SweetGirl` |
| 韩文内容 | 男声 | `Korean_CheerfulBoyfriend` |

### 使用示例

```
用户: 用少女音配音这段话：大家好，欢迎来到我的频道
→ 自动选择 female-shaonv
→ 生成音频文件

用户: 用播报男声朗读这段教程内容
→ 自动选择 Chinese (Mandarin)_Male_Announcer

用户: 英文配音：Hello, welcome to my channel
→ 自动选择 English_Trustworthy_Man
```

### 停顿控制

使用 `<#x#>` 标记控制停顿（x为秒数）：

```
你好<#2#>我是vidu<#1#>很高兴见到你
```

### 参数说明

| 参数 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| speed | 0.5-2.0 | 1.0 | 语速 |
| volume | 0-10 | 0 | 音量 |
| pitch | -12~12 | 0 | 语调 |
| emotion | happy/sad/angry/fearful/disgusted/surprised/calm | - | 情绪 |

## 声音复刻

根据音频样本复刻音色，用于后续TTS。

### 使用示例

```
用户: 帮我复刻这个音频的声音
[发送音频文件]
→ 创建自定义音色
→ 返回 voice_id 供后续使用
```

### 要求

- 原音频时长：10秒-5分钟
- 音频清晰，无背景噪音
- 复刻音色为临时音色，7天内需在TTS中调用才能永久保留

### API 调用

```bash
python3 {baseDir}/scripts/vidu_cli.py voice-clone \
  --audio-url sample.mp3 \
  --voice-id my_voice_001 \
  --text "这是复刻的声音样例"
```

## API 调用

内部使用 Python CLI 工具：

```bash
# TTS语音合成
python3 {baseDir}/scripts/vidu_cli.py tts \
  --text "配音文本" \
  --voice-id "female-shaonv"

# 长文本TTS（避免shell引号问题）
python3 {baseDir}/scripts/vidu_cli.py tts \
  --text-file long_text.txt \
  --voice-id "female-shaonv"

# 声音复刻
python3 {baseDir}/scripts/vidu_cli.py voice-clone \
  --audio-url sample.mp3 \
  --voice-id my_voice \
  --text "这是复刻的声音样例"
```

## 输出规范

1. **下载目录**: `{baseDir}/uploads/`
2. **返回格式**: Markdown 格式引用文件
3. **音频链接**: 必须返回音频 URL 让用户直接访问

## 环境配置

必需环境变量：

```bash
VIDU_API_KEY=your_api_key_here
```

获取 API Key：
- Vidu 官方开放平台：https://platform.vidu.cn 或 https://platform.vidu.com
- 注册账号后在「API Keys」页面创建

## API 域名选择

**重要规则**：根据用户语言自动选择 API 域名

| 用户语言 | API 域名 | 说明 |
|---------|---------|------|
| 简体中文 | `api.vidu.cn` | 国内用户（默认） |
| 其他语言 | `api.vidu.com` | 海外用户 |

**Base URL 配置**：
```python
# 简体中文用户
BASE_URL = "https://api.vidu.cn/ent/v2"

# 非简体中文用户（英文、日文、韩文等）
BASE_URL = "https://api.vidu.com/ent/v2"
```

**判断逻辑**：
- 用户使用简体中文 → 使用 `api.vidu.cn`
- 用户使用其他语言（英文、日文、韩文等） → 使用 `api.vidu.com`

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Invalid API key | API密钥错误 | 检查 VIDU_API_KEY 环境变量 |
| Voice ID not found | 音色不存在 | 检查音色列表或重新复刻 |
| Task failed | 生成失败 | 查看 error 信息重试 |
| Audio too long | 音频过长 | 音频需在10秒-5分钟之间 |

## References

- [音色列表](references/voice_id_list.md) - 303个可用音色
- [API参考文档](references/api_reference.md) - 所有API详细参数

## Rules

1. **API Key 检查**: 调用前确认 `VIDU_API_KEY` 已设置
2. **TTS同步**: TTS 为同步接口，立即返回音频URL
3. **长文本处理**: 文本超过30字符必须使用 `--text-file` 参数
4. **音色保留**: 复刻音色7天内需使用否则删除
5. **返回音频链接**: 必须返回音频 URL 让用户直接访问
