# Workflow Reference

## Channel Quick Reference

All channels use `poll_cron.py register` with `--channel` and `--target` to specify the delivery channel.

### Feishu channel

```
Scenario A (text-to-image):        create → register(5/1800) → reply user → cron auto-delivers
Scenario B (image-to-image/bg):    transfer(--image-key) → create → register(3/1800) → reply user → cron auto-delivers
Scenario C (edit last generated):  cat last_result_feishu.json → create(--image-url) → register(5/1800) → reply user
Scenario D (text-to-video veo):    create(veo, text_to_video) → register(10/21600) → reply user
Scenario E (image-to-video veo):   transfer → create(veo, --first-frame-url) → register(10/21600) → reply user
Scenario J (multi-image blend):    check image_registry.json → create(Banana2, --image-urls) → register(5/1800) → reply user
Scenario K (seedance2 text-to-video): create(seedance2, text_to_video) → register(30/172800) → reply user
Scenario L (seedance2 image-to-video): transfer → create(seedance2, --first-frame-url) → register(30/172800) → reply user
```

### QQ Bot channel

```
Scenario F (text-to-image):        create → register(5/1800) → reply user → cron delivers <qqimg>
Scenario G (image-to-image):       cat last_result_qqbot.json → create(--image-url) → register(5/1800) → reply user
Scenario H (text-to-video veo):    create(veo, text_to_video) → register(10/21600) → reply user → cron delivers <qqvideo>
Scenario H2 (text-to-video seedance2): create(seedance2, text_to_video) → register(30/172800) → reply user
Scenario I (image-to-video veo):   transfer(--file) → create(veo, --first-frame-url) → register(10/21600) → reply user
Scenario I2 (image-to-video seedance2): transfer → create(seedance2, --first-frame-url) → register(30/172800) → reply user
```

### Telegram / other channels

Same as Feishu flow; `--target` format is `telegram:XXXXXXXXX`, image source is `~/.openclaw/media/inbound/`.

---

## cron Parameters Quick Reference

| Task type | --interval | --max-duration | Notes |
|----------|-----------|---------------|-------|
| Banana2 / BananaPro / seedream | `5` | `1800` | image, 30 min timeout |
| remove-bg / remove-watermark | `3` | `1800` | image processing, 30 min timeout |
| veo | `10` | `21600` | video, 6 hour timeout |
| seedance2 | `30` | `172800` | long video, 48 hour timeout |

---

## QQ Bot Detailed Examples

### Scenario F: Text-to-image

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category Banana2 \
  --prompt "user's image description"

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> \
  --channel qqbot \
  --target "qqbot:c2c:XXXX" \
  --interval 5 \
  --max-duration 1800
```

### Scenario G: Image-to-image

> Always read `last_result_qqbot.json` first; never guess the URL.

```bash
cat ~/.openclaw/media/plume/last_result_qqbot.json
# get result_url

python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category Banana2 \
  --image-url <result_url> \
  --prompt "cartoon style / Pixar style etc."

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> --channel qqbot --target "qqbot:c2c:XXXX" \
  --interval 5 --max-duration 1800
```

### Scenario H: Text-to-video (veo)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category veo --processing-mode text_to_video \
  --prompt "user's video description"

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> --channel qqbot --target "qqbot:c2c:XXXX" \
  --interval 10 --max-duration 21600
```

### Scenario H2: Text-to-video (seedance2)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category seedance2 --processing-mode text_to_video \
  --prompt "user's video description" --model "seedance2-5s" --aspect-ratio "9:16"

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> --channel qqbot --target "qqbot:c2c:XXXX" \
  --interval 30 --max-duration 172800
```

### Scenario I: Image-to-video (veo)

```bash
# option 1: user sent an image
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py transfer \
  --file ~/.openclaw/qqbot/downloads/<filename>

# option 2: use last result
cat ~/.openclaw/media/plume/last_result_qqbot.json  # get result_url

python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category veo --first-frame-url <url> --prompt "animate this image"

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> --channel qqbot --target "qqbot:c2c:XXXX" \
  --interval 10 --max-duration 21600
```

### Scenario I2: Image-to-video (seedance2)

```bash
# get image URL (same as Scenario I)

python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category seedance2 --first-frame-url <url> \
  --prompt "cinematic motion" --model "seedance2-5s"

python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <task_id> --channel qqbot --target "qqbot:c2c:XXXX" \
  --interval 30 --max-duration 172800
```

---

## Image Source Priority

> See SKILL.md "Multi-turn Dialog / Image-to-Image" section for full rules and context keyword list.

### Feishu
1. Message contains `image_key` (`img_v3_xxx`) → `transfer --image-key`
2. No image, user references "last image" → `cat last_result_feishu.json` get `result_url`
3. Neither → prompt user to send an image

### QQ Bot
1. User sent an image this turn (`~/.openclaw/qqbot/downloads/`) → `transfer --file`
2. No attachment, user references "this image / the one above" → `cat last_result_qqbot.json` get `result_url`
3. Not found → prompt user to send an image

### Telegram / Universal
1. User sent an attachment this turn (`~/.openclaw/media/inbound/`) → `transfer --file`
2. No attachment, user references "this image / just generated" → `cat last_result_telegram.json` get `result_url`
3. Not found → prompt user to send an image

---

## veo imageUrls Slot Description

`imageUrls` has fixed 3 slots, order is semantic:

| Parameter | Slot | Purpose |
|-----------|------|---------|
| `--first-frame-url` (or `--image-url`) | `[0]` | First frame (most common for image-to-video) |
| `--last-frame-url` | `[1]` | Last frame (first+last frame control) |
| `--reference-url` | `[2]` | Reference image (style blend) |

## seedance2 imageUrls Description

Pure URL array (not fixed slots), only pass non-empty URLs:
- `--first-frame-url` → processing_mode auto-set to `first_frame`
- `--first-frame-url` + `--last-frame-url` → `first_last_frame`
- `--reference-url` → `universal_reference`
