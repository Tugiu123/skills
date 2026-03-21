# Vidu Speech Generate API Reference

语音合成与声音复刻 API 参考，包含TTS和声音复刻功能。

## Base URL

```
https://api.vidu.cn/ent/v2
```

**域名选择规则**：
- **简体中文用户**：使用 `api.vidu.cn`
- **非简体中文用户**：使用 `api.vidu.com`

根据用户交流语言自动切换域名。

## Authentication

```
Authorization: Token YOUR_API_KEY
```

---

## 音频生成 API

### 1. TTS 语音合成

**POST** `/audio-tts`

```json
{
  "text": "要配音的文本",
  "voice_setting_voice_id": "female-shaonv",
  "voice_setting_speed": 1.0,
  "voice_setting_volume": 0,
  "voice_setting_pitch": 0,
  "voice_setting_emotion": "calm"
}
```

**参数说明**：
| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| text | string | - | 要合成的文本 |
| voice_setting_voice_id | string | - | 音色ID，见 voice_id_list.md |
| voice_setting_speed | float | 0.5-2.0 | 语速，默认1.0 |
| voice_setting_volume | int | 0-10 | 音量，默认0 |
| voice_setting_pitch | int | -12~12 | 语调，默认0 |
| voice_setting_emotion | string | - | 情绪：happy/sad/angry/fearful/disgusted/surprised/calm |

**返回**：同步返回音频URL

**停顿控制**：
使用 `<#x#>` 标记控制停顿（x为秒数）：

```json
{
  "text": "你好<#2#>我是vidu<#1#>很高兴见到你",
  "voice_setting_voice_id": "female-shaonv"
}
```

**热门音色**：
| 音色类型 | Voice ID | 适用场景 |
|---------|---------|---------|
| 少女音色 | `female-shaonv` | 小红书/短视频 |
| 精英青年 | `male-qn-jingying` | 小红书/短视频（男） |
| 播报男声 | `Chinese (Mandarin)_Male_Announcer` | 教程/科普 |
| 御姐音色 | `female-yujie` | 情感/故事 |
| 温暖少女 | `Chinese (Mandarin)_Warm_Girl` | 温馨/治愈 |

---

### 2. 声音复刻

**POST** `/audio-clone`

```json
{
  "audio_url": "源音频URL",
  "voice_id": "自定义音色ID",
  "text": "试听文本",
  "prompt_audio_url": "参考音频URL（可选）",
  "prompt_text": "参考音频对应文本（可选）"
}
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audio_url | string | ✅ | 源音频URL（10秒-5分钟） |
| voice_id | string | ✅ | 自定义音色ID |
| text | string | ✅ | 试听文本 |
| prompt_audio_url | string | ❌ | 参考音频URL |
| prompt_text | string | ❌ | 参考音频对应文本 |

**要求**：
- 源音频时长：10秒-5分钟
- 音频清晰，无背景噪音
- 复刻音色7天内需使用才能保留

**返回**：复刻音色ID

---

## 响应格式

### TTS 响应

```json
{
  "state": "success",
  "file_url": "https://...",
  "duration": 10.5
}
```

### 声音复刻响应

```json
{
  "state": "success",
  "voice_id": "my_voice_001",
  "demo_url": "https://..."
}
```

---

## 错误码

| 错误 | 说明 |
|------|------|
| Invalid API key | API 密钥错误 |
| Voice ID not found | 音色不存在 |
| Audio too long | 音频过长（超过5分钟） |
| Audio too short | 音频过短（少于10秒） |
| Task failed | 生成失败 |

---

## 使用注意事项

### TTS 使用

1. **文本长度**：超过30字符建议使用 `--text-file` 参数
2. **音色选择**：根据场景自动推荐音色
3. **停顿控制**：使用 `<#x#>` 标记
4. **情绪设置**：可选 happy/sad/angry/fearful/disgusted/surprised/calm

### 声音复刻

1. **音频质量**：必须清晰，无背景噪音
2. **音频时长**：10秒-5分钟
3. **音色保留**：7天内需使用，否则删除
4. **音色ID**：自定义，建议使用有意义的前缀

---

## 参数速查

### TTS参数

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| speed | 0.5-2.0 | 1.0 |
| volume | 0-10 | 0 |
| pitch | -12~12 | 0 |
| emotion | happy/sad/angry/fearful/disgusted/surprised/calm | calm |

### 音色列表

**完整音色列表**: 见 `voice_id_list.md` (303个音色)

包含：
- 中文音色（少女、御姐、精英、播报等）
- 英文音色（男声、女声）
- 日文音色（男声、女声）
- 韩文音色（男声、女声）
- 特色音色（萌系、搞笑、温馨等）
