---
name: video-quick-gen
description: | 
  Quick-generate a marketing video via the local content-marketing-dashboard (dashboard-console) Video module: first call POST /video/script/gen to create a video script from a user requirement, then call POST /video/task/create to start video generation, poll GET /video/task/state until completion, and return the final video_url (optionally download mp4). Use when the user says “快速生成视频/生成一个视频/做个视频/把这个需求直接生成视频” and they expect the result produced by the dashboard API (not manual writing).
---

# video-quick-gen

Generate a video end-to-end via dashboard-console.

## Prereqs

- Service base: `https://xiaonian.cc`
- API prefix: `https://xiaonian.cc/employee-console/dashboard/v2/api`
- Auth: built-in token, no configuration needed.

## Workflow

1) Generate script
- `POST /video/script/gen` → returns `script`

2) Create video task
- `POST /video/task/create` → returns `task_id`

3) Poll until done
- `GET /video/task/state?task_id=...` → returns `status/progress/video_url`

## Quick start

```bash
python3 skills/local/video-quick-gen/scripts/video_quick_gen.py \
  --request "<用户需求，尽量原样保留>" \
  --video-type AUTO \
  --duration 15 \
  --orientation portrait \
  --hd \
  --out /tmp/video.mp4
```

Optional:
- Provide reference image URL: `--image-url "<bos_url>"`
- Disable subtitles: `--no-subtitle`

## Output

JSON returned to the agent (always present):
- `state` — `"SUCCESS"`
- `task_id`
- `script` — the generated video script text (agent should read and summarize this to the user)
- `video_url` — final video URL
- `downloaded_to` — local path (only when `--out` is provided)

After the script runs, summarize both the script content and the video URL to the user.

## Troubleshooting

- status=failed:
  - Check `failed_reason` and backend logs.
