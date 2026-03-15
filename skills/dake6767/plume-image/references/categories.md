# AI Service Category Reference

## Available categories

### Banana2 — Gemini Image Generation (Default)

**Text-to-image (text_to_image)**
```json
{
  "processing_mode": "text_to_image",
  "prompt": "a beautiful sunset over the ocean, photorealistic, 4k",
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "image_size": "1K"
    }
  }
}
```

**Image-to-image (image_to_image)**
```json
{
  "processing_mode": "image_to_image",
  "prompt": "transform into oil painting style",
  "imageUrls": ["https://r2.example.com/uploaded-image.jpg"],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "image_size": "1K"
    }
  }
}
```

**Multi-image blend (multi_image_blend)**
```json
{
  "processing_mode": "multi_image_blend",
  "prompt": "blend these images into a cohesive scene",
  "imageUrls": ["https://r2.../img1.jpg", "https://r2.../img2.jpg"],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "image_size": "1K"
    }
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| processing_mode | string | yes | `text_to_image` / `image_to_image` / `multi_image_blend` |
| prompt | string | yes | English description prompt |
| imageUrls | string[] | required for image-to-image/multi-blend | Reference image URLs (must be R2 URLs) |
| generationConfig.responseModalities | string[] | yes | Fixed `["IMAGE"]` |
| generationConfig.imageConfig.image_size | string | no | `1K` (default) / `2K` / `4K`, affects credits multiplier |
| generationConfig.imageConfig.aspectRatio | string | no | e.g. `1:1` / `16:9` / `9:16` / `4:3` / `3:4` |

Credits: text_to_image=10, image_to_image=15, multi_image_blend=20 (1K baseline)
Estimated time: 10–30 seconds

---

### remove-bg — Background Removal

```json
{
  "imageUrls": ["https://r2.example.com/photo.jpg"]
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| imageUrls | string[] | yes | Image URL to remove background from |

No processing_mode or prompt needed. Credits: 5
Estimated time: 5–10 seconds

---

### remove-watermark — Watermark Removal

```json
{
  "imageUrls": ["https://r2.example.com/photo.jpg"]
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| imageUrls | string[] | yes | Image URL to remove watermark from |

No processing_mode or prompt needed. Credits: 5
Estimated time: 5–10 seconds

---

### seedream — Doubao Seedream Image Generation

**Text-to-image**
```json
{
  "processing_mode": "text_to_image",
  "prompt": "一只可爱的橘猫坐在窗台上",
  "generationConfig": {
    "imageConfig": {
      "image_size": "2K"
    }
  }
}
```

**Image-to-image**
```json
{
  "processing_mode": "image_to_image",
  "prompt": "改成水彩画风格",
  "imageUrls": ["https://r2.example.com/photo.jpg"],
  "generationConfig": {
    "imageConfig": {
      "image_size": "2K"
    }
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| processing_mode | string | yes | `text_to_image` / `image_to_image` |
| prompt | string | yes | Description prompt (**supports Chinese**) |
| imageUrls | string[] | required for image-to-image | Reference image URL |
| generationConfig.imageConfig.image_size | string | no | Default `2K` |

Credits: text_to_image=15, image_to_image=20
Estimated time: 10–30 seconds

---

### veo — Veo Video Generation

**Text-to-video (text_to_video)**
```json
{
  "processing_mode": "text_to_video",
  "prompt": "a cat walking on the beach, cinematic, 4k",
  "videoConfig": {
    "aspectRatio": "16:9",
    "durationSeconds": 6
  }
}
```

**Image-to-video (image_to_video)**
```json
{
  "processing_mode": "image_to_video",
  "prompt": "animate this image with gentle motion",
  "imageUrls": ["https://r2.example.com/uploaded-image.jpg"],
  "videoConfig": {
    "aspectRatio": "16:9",
    "durationSeconds": 6
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| processing_mode | string | yes | `text_to_video` / `image_to_video` (note: not text_to_image) |
| prompt | string | yes | English description prompt |
| imageUrls | string[] | required for image-to-video | Reference image URL (must be R2 URL) |
| videoConfig.aspectRatio | string | no | `16:9` (default) / `9:16` |
| videoConfig.durationSeconds | int | no | Video duration, default 6 seconds |

**Note**: veo does not use `generationConfig`, uses `videoConfig` instead
Estimated time: 1–10 minutes (long task, async cron polling recommended)

---

### seedance2 — Seedance2 Video Generation

**Text-to-video (text_to_video)**
```json
{
  "processing_mode": "text_to_video",
  "prompt": "a cat walking on the beach, cinematic, 4k",
  "videoConfig": {
    "model": "seedance2-5s",
    "aspectRatio": "16:9"
  }
}
```

**Image-to-video - first frame control (first_frame)**
```json
{
  "processing_mode": "first_frame",
  "prompt": "animate this image with gentle motion",
  "imageUrls": ["https://r2.example.com/uploaded-image.jpg"],
  "videoConfig": {
    "model": "seedance2-5s",
    "aspectRatio": "16:9"
  }
}
```

**Image-to-video - first and last frame control (first_last_frame)**
```json
{
  "processing_mode": "first_last_frame",
  "prompt": "smooth transition between frames",
  "imageUrls": ["https://r2.../first.jpg", "https://r2.../last.jpg"],
  "videoConfig": {
    "model": "seedance2-5s"
  }
}
```

**Universal reference (universal_reference)**
```json
{
  "processing_mode": "universal_reference",
  "prompt": "generate video in this style",
  "imageUrls": ["https://r2.../reference.jpg"],
  "videoConfig": {
    "model": "seedance2-5s",
    "aspectRatio": "9:16"
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| processing_mode | string | yes | `text_to_video` / `first_frame` / `first_last_frame` / `universal_reference` |
| prompt | string | yes | English description prompt |
| imageUrls | string[] | required for image-to-video | Image URLs (must be R2 URLs), first frame/last frame/reference |
| videoConfig.model | string | no | `seedance2-5s` (default) / `seedance2-10s` / `seedance2-15s`, determines video duration |
| videoConfig.aspectRatio | string | no | `16:9` (default) / `9:16` / `1:1` etc. |

**Notes**:
- seedance2 does not use `generationConfig`, uses `videoConfig` instead
- Images are passed via URL (not Base64), imageUrls contains only non-empty URLs (not fixed 3 slots)
- Do not pass aspectRatio for first_frame/first_last_frame modes (API infers from image dimensions)
- Model name determines video duration: seedance2-5s=5s, seedance2-10s=10s, seedance2-15s=15s
- Due to high demand for Seedance2, generation may take minutes to hours
- Credits: 5s=40, 10s=72(40×1.8), 15s=100(40×2.5)
Estimated time: minutes to hours (very long task, cron interval 30s, max-duration 86400s recommended)

---

## Image Size Reference

| image_size | Credits multiplier | Description |
|-----------|-------------------|-------------|
| `1K` | x1.0 | Standard resolution (default) |
| `2K` | x1.5 | High definition |
| `4K` | x2.0 | Ultra high definition |

## Category Selection Guide

| User request | Recommended category | Reason |
|-------------|---------------------|--------|
| High-quality realistic photo | `Banana2` | Gemini excels at realism |
| Chinese text prompt | `seedream` | Doubao natively supports Chinese |
| Remove background / cutout | `remove-bg` | Dedicated model, best results |
| Remove watermark | `remove-watermark` | Dedicated watermark removal model |
| Modify an existing image | `Banana2` (image_to_image) | Stable image-to-image results |
| Blend multiple images | `Banana2` (multi_image_blend) | Supports multiple image inputs |
| Generate video | `veo` | Supports text-to-video and image-to-video |
| Generate video (Seedance2) | `seedance2` | First/last frame control, use when user explicitly requests |
