# Plume Image Skill Usage Examples

## Text-to-image (most common)

```bash
# 1. Create text-to-image task
python3 scripts/process_image.py create \
  --category "banana" \
  --prompt "a cute orange cat sitting on a windowsill, afternoon sunlight, photorealistic" \
  --processing-mode "text_to_image" \
  --image-size "1K" \
  --aspect-ratio "1:1"

# Output: {"success": true, "task_id": 123, "status": 1, "credits_cost": 10}

# 2. Poll for result
python3 scripts/process_image.py poll --task-id 123

# Output: {"success": true, "status": 3, "result_url": "https://r2.../result.jpg", ...}

# 3. Deliver via Feishu
python3 scripts/process_image.py deliver \
  --result-url "https://r2.../result.jpg" \
  --chat-id "oc_xxxxx" \
  --chat-type "group"
```

## Image-to-image (user sent a reference image)

```bash
# 1. Relay Feishu image to R2
python3 scripts/process_image.py transfer \
  --image-key "img_v3_xxx"

# Output: {"success": true, "image_url": "https://r2.../transferred.jpg", ...}

# 2. Create image-to-image task
python3 scripts/process_image.py create \
  --category "banana" \
  --prompt "transform into watercolor painting style" \
  --image-url "https://r2.../transferred.jpg" \
  --processing-mode "image_to_image"

# 3. Poll + deliver (same as text-to-image)
```

## Background removal

```bash
# 1. Relay image (if from Feishu)
python3 scripts/process_image.py transfer --image-key "img_v3_xxx"

# 2. Create background removal task (no processing-mode or prompt needed)
python3 scripts/process_image.py create \
  --category "remove-bg" \
  --image-url "https://r2.../photo.jpg"

# 3. Poll + deliver
```

## Using Doubao Seedream (supports Chinese prompt)

```bash
python3 scripts/process_image.py create \
  --category "seedream" \
  --prompt "一只可爱的柴犬穿着宇航服在月球上散步" \
  --processing-mode "text_to_image" \
  --image-size "2K"
```

## High-definition 4K image

```bash
python3 scripts/process_image.py create \
  --category "banana" \
  --prompt "a stunning landscape photograph" \
  --processing-mode "text_to_image" \
  --image-size "4K" \
  --aspect-ratio "16:9"
```

## Associate with project

```bash
python3 scripts/manage_project.py create-with-project \
  --category "banana" \
  --prompt "a beautiful landscape" \
  --processing-mode "text_to_image" \
  --project-id "auto"
```

## Agent complete workflow examples

Typical processing flow after agent receives a user message:

### User says: "Generate an image of a cat"
```
1. Agent analyzes: text-to-image request, select category=banana
2. Translate prompt: "a cute cat, detailed fur, soft lighting"
3. Execute create(processing-mode=text_to_image) → poll → deliver
```

### User sends an image, then says: "Remove the background"
```
1. Agent finds image_key from context
2. Execute transfer → create(category=remove-bg) → poll → deliver
```

### User sends an image, then says: "Convert this to oil painting style"
```
1. Agent finds image_key from context
2. Execute transfer → create(category=banana, processing-mode=image_to_image) → poll → deliver
```
