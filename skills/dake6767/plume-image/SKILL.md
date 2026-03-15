---
name: plume-image
description: |
  Plume AI image generation and editing service. Auto-triggers when users send images or describe image needs.
  Supports: text-to-image, image-to-image, background removal, watermark removal, style transfer, text-to-video, image-to-video.
  Activate when user mentions: generate image, edit image, remove background, change background, remove watermark,
  text-to-image, image-to-image, AI art, style transfer, generate poster, photo editing, generate video, AI video,
  animate this image, make it move, image-to-video, make image into video, seedance2, seedance.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*), Bash(cat ~/.openclaw/media/plume/*)
---

# Plume AI Image Service

Help users complete AI image generation and editing through natural language.

## 🚨 Critical Workflow Rules (Must Follow)

**All tasks must use: `create` → `poll_cron.py register` → reply to user immediately → end**

**Strictly prohibited:**
- ❌ Do NOT use `process_image.py poll` command
- ❌ Do NOT run check after register
- ❌ Do NOT use sleep to wait before polling
- ❌ Do NOT ask users to paste API Key in chat
- ❌ **Do NOT auto-create tasks when user sends only an image without text instructions** — the user may just be preparing a reference image; wait for explicit text instructions before acting

**Correct approach:**
- ✅ Call `poll_cron.py register` immediately after creating a task
- ✅ Reply to user right after register succeeds, informing them that processing has started
- ✅ End the current session; background process polls automatically and delivers result
- ✅ **When receiving a pure image (no text), just reply "Got your image. What would you like to do with it?" and wait for the user's next message**

## ⚠️ Mandatory Pre-check (Run Before Every Use)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_config.py
```

- Output `CONFIGURED`: proceed with subsequent operations
- Output `NOT_CONFIGURED`: **stop immediately**, prompt user to configure as follows (do NOT ask for the key in chat):

> To use the Plume AI image service, you need to configure your API Key first:
> 1. Visit [Plume Platform](https://design.useplume.app/openclaw-skill) to register and obtain an API Key
> 2. Edit `~/.openclaw/openclaw.json`, add to `skills.entries`:
>    ```json
>    "plume-image": { "env": { "PLUME_API_KEY": "your-key" } }
>    ```
>    Or add `PLUME_API_KEY=your-key` to the `~/.openclaw/.env` file
> 3. Enter `/restart` to apply changes

## Background Polling Behavior

This skill starts a background Python process via `poll_cron.py register` to poll task status. Results are delivered via `openclaw message send` when the task completes.

- Poll interval: images 3–5s, videos 10–30s
- Default timeout: 30 minutes (adjustable by category)
- Max concurrency: 5 active polling tasks
- Process exits automatically and cleans up metadata after task completes, fails, or times out
- Results delivered via `openclaw message send`, no direct channel API calls

## Supported categories (fixed enum, do not invent)

| category | Alias | Use case | Default |
|----------|-------|----------|---------|
| `Banana2` | 香蕉 | text-to-image / image-to-image / style transfer | ✅ default for images |
| `BananaPro` | 香蕉Pro | text-to-image / image-to-image (user explicitly requested) | |
| `remove-bg` | | background removal | |
| `remove-watermark` | | watermark removal | |
| `seedream` | 即梦/豆包即梦 | Doubao Seedream image generation | |
| `veo` | | text-to-video / image-to-video | ✅ default for videos |
| `seedance2` | | Seedance2 video (user explicitly requested) | |

**Style transfer (cartoon, Pixar, watercolor, etc.) defaults to `Banana2` + `--prompt` describing the style, unless user explicitly requests BananaPro. Do not invent new categories.**

## Image/Video Specs

- Default: `2K`, `9:16` (portrait)
- Resolution: `1K` / `2K`
- Aspect ratio: `21:9` / `16:9` / `4:3` / `3:2` / `1:1` / `9:16` / `3:4` / `2:3` / `5:4` / `4:5`
- **Only adjust aspect ratio based on keywords the user explicitly states; do NOT infer from image content**

## Multi-turn Dialog / Image-to-Image

When the user requests modifications to an existing image (style transfer, background removal, image-to-video, etc.), first determine the image source:

### Determine image source (priority: highest to lowest)

1. **User sent both image and text instructions in the current turn** → `transfer --file <attachment path>` to upload to R2, get `image_url`, process per text instructions
2. **User sent only an image in the current turn, no text** → **do not create a task**, reply "Got your image. What would you like to do with it?" and wait for next message
3. **User sent an image in the previous turn, text instructions in the current turn** → `transfer` upload the previous turn's image, process per current text instructions
4. **User references "last/this/just generated" image** → read `last_result_{channel}.json` to get `result_url`
5. **None of the above** → prompt user to send an image

### Read last result

Files are isolated by channel to prevent cross-channel mix-up:

```bash
# {channel} = current channel: feishu / qqbot / telegram
cat ~/.openclaw/media/plume/last_result_{channel}.json
```

Returns JSON:
```json
{"task_id": "xxx", "result_url": "https://pics.useplume.app/...", "local_file": "...", "media_type": "image", "created_at": ...}
```

**Must use `result_url` (remote URL) as `--image-url`; do NOT use `local_file`.**

### Image-to-image example

```bash
# 1. Read last result (using QQ Bot channel as example)
cat ~/.openclaw/media/plume/last_result_qqbot.json
# get result_url = https://pics.useplume.app/xxx.png

# 2. Create image-to-image task (processing_mode auto-detected as image_to_image)
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category Banana2 \
  --image-url "https://pics.useplume.app/xxx.png" \
  --prompt "transform into Pixar 3D animation style"

# 3. Register polling (same as standard flow)
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <id> --channel qqbot --target "qqbot:c2c:XXXX" --interval 5 --max-duration 1800
```

### Context keywords

When the user says any of the following, read last_result_{channel}.json for image-to-image:
- Style-related: change to XX style, make it XX, convert to XX, Pixar, cartoon, watercolor, oil painting, sketch
- Referencing previous: this image, the last one, the one just now, edit it, tweak it
- Operations: remove background, remove watermark, animate it (image-to-video)

## Unified Workflow

All tasks: `create` → `poll_cron.py register` → reply to user immediately → end

### Create task

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category <category> \
  --prompt "<English prompt>" \
  [--processing-mode text_to_image|image_to_image|text_to_video] \
  [--image-url <r2_url>] \
  [--first-frame-url <url>] \
  [--image-size 2K] \
  [--aspect-ratio 9:16]
```

**Output format:** JSON, always check the `success` field
- `{"success": true, "task_id": "xxx", ...}` → proceed to register
- `{"success": false, ...}` → **must inform user of the specific error reason**, classify by `code` field:

| code | User message |
|------|-------------|
| `INSUFFICIENT_CREDITS` | Inform user that Plume account credits are insufficient, guide them to [Plume Platform](https://design.useplume.app) to top up and retry |
| `CREDITS_ACCOUNT_NOT_FOUND` | Inform user that credits account has not been created, guide them to [Plume Platform](https://design.useplume.app) to register |
| `UNAUTHORIZED` | Inform user that API Key is invalid, guide them to re-obtain and configure |
| `VALIDATION_ERROR` | Inform user of invalid parameters, show the specific message in the `error` field |
| other | Show the `error` field content directly to user |

**Important: when task creation fails, clearly explain the failure reason and resolution to the user; do not skip the error.**

### Register cron polling

Use the unified script with `--channel` and `--target` to specify delivery channel and target:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <id> \
  --channel <channel> \
  --target <target> \
  [--interval <seconds>] \
  [--max-duration <seconds>]
```

**Determining channel and target:**

| Context clue | --channel | --target |
|-------------|-----------|----------|
| sender_id with `ou_` prefix | `feishu` | `ou_xxx` (DM) or `oc_xxx` (group) |
| Contains "You are chatting via QQ" | `qqbot` | full delivery target (e.g. `qqbot:c2c:XXXX`) |
| Contains Telegram or target starts with `telegram:` | `telegram` | full delivery target (e.g. `telegram:6986707981`) |
| Other | infer from context | infer from context |

**Poll parameters by category:**

| Category | --interval | --max-duration | Notes |
|----------|-----------|---------------|-------|
| Banana2 / BananaPro / seedream | 5 | 1800 | image, 30 min timeout |
| remove-bg / remove-watermark | 3 | 1800 | image processing, 30 min timeout |
| veo | 10 | 21600 | video, 6 hour timeout |
| seedance2 | 30 | 172800 | long video, 48 hour timeout |

**Examples:**

```bash
# Feishu DM
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel feishu --target ou_xxx --interval 5 --max-duration 1800

# Feishu group
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel feishu --target oc_xxx --interval 5 --max-duration 1800

# Telegram
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel telegram --target "telegram:6986707981" --interval 10 --max-duration 21600

# QQ Bot
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel qqbot --target "qqbot:c2c:XXXX" --interval 5 --max-duration 1800
```

### Image source

> See the "Multi-turn Dialog / Image-to-Image" section above for full image source priority rules.

Upload user image to R2:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py transfer \
  --file "/path/to/image.jpg"
```

## Prohibited Actions

- Do NOT fabricate task_id (only use values returned from create)
- Do NOT fabricate image URLs (only use `result_url` or `r2_url` returned by `transfer`; domain must be `pics.useplume.app`)
- Do NOT invent categories (only the 7 values in the table above are allowed)
- Do NOT run check after register
- Do NOT use curl/wget to download images
- Do NOT use the /tmp directory
- Do NOT ask users to paste API Key in chat

## Reference Docs

- Detailed workflow examples: [references/workflows.md](references/workflows.md)
- Category parameter reference: [references/categories.md](references/categories.md)
- Error code reference: [references/error-codes.md](references/error-codes.md)
