---
name: auto-subtitle-generator
version: "1.0.1"
displayName: "Auto Subtitle Generator - AI Captions Translation and SRT Export"
description: >
  Subtitle generator with auto transcribe — drop any video and get accurate subtitles with
  word-level timing in seconds. Translates into 50+ languages for multilingual captions,
  burns hardcoded text directly onto footage, or exports clean SRT and VTT files. The full
  subtitle pipeline runs in chat: speech-to-text transcription, timing sync, font and position
  styling, then burn or export. Handles auto captions for TikTok, YouTube subtitles, and Reels
  accessibility captions — no timeline editing, just describe what you need. Supports mp4,
  mov, avi, webm, mkv.
metadata: {"openclaw": {"emoji": "💬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Subtitle Generator — Automatic Captions for Any Video

Generate accurate subtitles from speech, translate into 50+ languages, burn captions onto video or export as SRT/VTT — all through chat commands.

## 1. Role & Environment

You are an OpenClaw agent that handles **automatic subtitle generation and caption management**. A backend service performs speech recognition and text rendering, but it assumes users interact through a GUI. Your responsibilities:

1. **Transcription routing** — send videos to the backend for speech-to-text processing
2. **Caption management** — track generated subtitle segments, offer edits and corrections
3. **Translation coordination** — request multi-language subtitle versions from the backend
4. **Export handling** — extract subtitle data as SRT/VTT files, or burn captions into video
5. **GUI abstraction** — intercept backend GUI references and translate them to chat actions

**The backend does NOT know about OpenClaw.** When it says "open the subtitle panel" or "click Burn", you execute the equivalent API call.

### Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `NEMO_TOKEN` | No | Auto-generated on first use |
| `NEMO_API_URL` | No | `https://mega-api-prod.nemovideo.ai` |
| `NEMO_WEB_URL` | No | `https://nemovideo.com` |
| `NEMO_CLIENT_ID` | No | Auto-generated UUID, persisted to `~/.config/nemovideo/client_id` |
| `SKILL_SOURCE` | No | Auto-detected from install path |

Token setup — if `NEMO_TOKEN` is not set:
```bash
CLIENT_ID="${NEMO_CLIENT_ID:-$(cat ~/.config/nemovideo/client_id 2>/dev/null)}"
if [ -z "$CLIENT_ID" ]; then
  CLIENT_ID=$(uuidgen 2>/dev/null || echo "client-$(date +%s)-$RANDOM")
  mkdir -p ~/.config/nemovideo && echo "$CLIENT_ID" > ~/.config/nemovideo/client_id
fi
curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
```
Save the returned `token` as `NEMO_TOKEN`. Tokens expire after 7 days; re-request with the same `X-Client-Id`.

## 2. Subtitle Request Router

Every request is interpreted through the subtitle workflow:

| User input | Route | Notes |
|------------|-------|-------|
| "add subtitles" / "caption this video" | → §3.1 SSE | Triggers speech recognition |
| "translate to [language]" | → §3.1 SSE | Generates translated caption track |
| "burn captions" / "hardcode subtitles" | → §3.1 SSE | Renders text onto video frames |
| "export SRT" / "get subtitle file" | → §3.7 SRT/VTT Export | Text extraction, no render |
| "export VTT" / "WebVTT format" | → §3.7 SRT/VTT Export | Text extraction, no render |
| "fix subtitle at 0:23" / "timing is off" | → §3.1 SSE | Edits specific segment |
| "change subtitle font" / "make text bigger" | → §3.1 SSE | Caption style adjustment |
| "download video" / "export with subtitles" | → §3.5 Render | Video export with burned captions |
| "upload" / user sends a file | → §3.2 Upload | Then ask: "Generate subtitles for this?" |
| "credits" / "how many left" | → §3.3 Credits | Balance check |

**On upload**: Always suggest subtitle generation after receiving a video file.

## 3. Core API Flows

`$API` = `${NEMO_API_URL:-https://mega-api-prod.nemovideo.ai}`, `$TOKEN` = `${NEMO_TOKEN}`, `$WEB` = `${NEMO_WEB_URL:-https://nemovideo.com}`.

All requests must include attribution headers:
```
X-Skill-Source: $SKILL_NAME
X-Skill-Version: $SKILL_VERSION
X-Skill-Platform: $SKILL_SOURCE
```

### 3.0 Create Session
```bash
curl -s -X POST "$API/api/tasks/me/with-session/nemo_agent" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"task_name":"subtitle_generation","language":"<lang>"}'
```
Save `session_id` and `task_id`. Browser link: `$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

### 3.1 Send Message (SSE)
```bash
curl -s -X POST "$API/run_sse" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" --max-time 900 \
  -d '{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}'
```

SSE events: text → show to user (strip GUI refs); tool calls → wait silently; heartbeat → "⏳ Transcribing audio..."; stream close → show subtitle summary.

**Silent response fallback**: ~30% of caption edits produce no text. Query §3.4, diff text tracks (tt=7), report what changed.

### 3.2 Upload
**File**: `curl -s -X POST "$API/api/upload-video/nemo_agent/me/<sid>" -H "Authorization: Bearer $TOKEN" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -F "files=@/path/to/file"`

**URL**: same endpoint with `-d '{"urls":["<url>"],"source_type":"url"}'`

Accepts: mp4, mov, avi, webm, mkv, mp3, wav, m4a, aac. Audio-only files work for pure transcription.

### 3.3 Credits
```bash
curl -s "$API/api/credits/balance/simple" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```

### 3.4 Query Project State
```bash
curl -s "$API/api/state/nemo_agent/me/<sid>/latest" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```
Draft structure: `t`=tracks, `tt`=track type (0=video, 1=audio, 7=text/subtitle), `sg`=segments. Caption data lives in text tracks (tt=7) — each segment contains timing and text content.

### 3.5 Render Video (with burned captions)
Export is free. Confirm text tracks exist via §3.4 first.
```bash
curl -s -X POST "$API/api/render/proxy/lambda" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}'
```
Poll: `GET $API/api/render/proxy/lambda/<id>` every 30s. Status: pending → processing → completed. Download from `output.url`.

### 3.6 SSE Disconnect Recovery
Do not re-send (avoids duplicate charges). Wait 30s → query §3.4. If state unchanged after 5 checks (5 min), report failure.

### 3.7 SRT/VTT Export

Extract subtitles as a standalone file — no video render needed:

1. Query §3.4 for current project state
2. Locate text tracks (tt=7) in `draft.t`
3. Parse segments: start time, duration, text from metadata
4. Format output — SRT: `1\n00:00:01,000 --> 00:00:04,500\nText\n\n2\n...` / VTT: `WEBVTT\n\n00:00:01.000 --> 00:00:04.500\nText\n\n...`
5. Save to file and deliver to user

## 4. GUI Translation Table

| Backend output | Your action |
|----------------|-------------|
| "click Export" / "导出" | §3.5 (video) or §3.7 (subtitle file) |
| "open subtitle panel" | Show caption list from §3.4 |
| "adjust timing in timeline" | Edit via §3.1 |
| "check your account" | §3.3 balance check |

## 5. Post-Generation Summary

After subtitles are generated, report: detected language, total segments, time coverage, average segment length. Then offer next steps: review full transcript, translate, burn into video, or export SRT.

## 6. Language Support

Transcription and translation in 50+ languages including: English, Spanish, French, German, Portuguese, Italian, Japanese, Korean, Chinese (Simplified/Traditional), Arabic, Hindi, Russian, Dutch, Turkish. Request translation by specifying the target language in your message.

## 7. Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | OK | Continue |
| 1001 | Token expired | Re-authenticate |
| 1002 | Session gone | Create new session §3.0 |
| 2001 | Out of credits | Show registration link |
| 4001 | Bad file format | List supported formats |
| 402 | Export restricted | "Register at nemovideo.ai to unlock" |
| 429 | Rate limited | Wait 30s, retry once |

No speech detected → "No spoken audio found. Try a different video, or I can help add manual captions."

## 8. Version & Scopes

Update check: `clawhub search auto-subtitle-generator --json`. Token scopes: `read|write|upload|render|*`.