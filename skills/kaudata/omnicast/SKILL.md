# OmniCast Studio API Reference

## Overview
The OmniCast Studio local API (`http://127.0.0.1:7860`) provides a multi-modal pipeline to ingest media, draft scripts, synthesize audio, generate cover art, and compile social media video assets. 

All endpoints accept JSON (except `/api/ingest` which accepts multipart/form-data). A consistent `<UNIQUE_SESSION_ID>` must be passed to link the pipeline steps together.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - node
        - npm
        - ffmpeg
      env:
        - GEMINI_API_KEY
        - OPENAI_API_KEY
    always: false

---

### 1. Media Ingestion (`/api/ingest`)
Extracts raw text from a target URL (Web article, MP4 video, or YouTube link).

    curl -X POST http://127.0.0.1:7860/api/ingest \
      -H "Content-Type: multipart/form-data" \
      -F "id=<UNIQUE_SESSION_ID>" \
      -F "sourceType=url" \
      -F "url=<TARGET_URL>"

---

### 2. Script Drafting (`/api/draft-script`)
Drafts a multi-host podcast script from the ingested text (max 2100 words).

    curl -X POST http://127.0.0.1:7860/api/draft-script \
      -H "Content-Type: application/json" \
      -d '{
        "id": "<UNIQUE_SESSION_ID>",
        "host1": "Alex",
        "host2": "Sam",
        "targetLanguage": "English"
      }'

---

### 3. Audio Synthesis (`/api/synthesize`)
Converts the drafted script into a compiled `.m4a` podcast file. Default engine is `openai`.

    curl -X POST http://127.0.0.1:7860/api/synthesize \
      -H "Content-Type: application/json" \
      -d '{
        "id": "<UNIQUE_SESSION_ID>", 
        "script": "<ESCAPED_SCRIPT_STRING>", 
        "host1": "Alex", 
        "host2": "Sam",
        "ttsEngine": "openai"
      }'

---

### 4. Draft Cover Art Prompt (`/api/draft-image-prompt`)
Analyzes the script to generate a 1-sentence prompt for the image generator.

    curl -X POST http://127.0.0.1:7860/api/draft-image-prompt \
      -H "Content-Type: application/json" \
      -d '{"id": "<UNIQUE_SESSION_ID>"}'

---

### 5. Render Widescreen Cover Art (`/api/generate-thumbnail`)
Generates a 16:9 podcast thumbnail based on the prompt.

    curl -X POST http://127.0.0.1:7860/api/generate-thumbnail \
      -H "Content-Type: application/json" \
      -d '{
        "id": "<UNIQUE_SESSION_ID>",
        "prompt": "<PROMPT_STRING_FROM_STEP_4>"
      }'

---

### 6. LinkedIn Package Generation (`/api/generate-linkedin`)
Compiles the audio and cover art into a formatted MP4 video and returns a social media post.

    curl -X POST http://127.0.0.1:7860/api/generate-linkedin \
      -H "Content-Type: application/json" \
      -d '{
        "id": "<UNIQUE_SESSION_ID>",
        "targetCaptionLanguages": ["English"]
      }'

---

### 7. File Download & Deletion
* **Download:** `GET http://127.0.0.1:7860/api/download-zip?id=<UNIQUE_SESSION_ID>`
* **Delete:** `DELETE http://127.0.0.1:7860/api/delete-folder` (Pass `id` in JSON body).