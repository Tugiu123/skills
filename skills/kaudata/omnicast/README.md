# OmniCast Studio 🎙️

A secure, multi-modal AI podcast studio that transforms raw inputs (YouTube, Web URLs, PDFs, MP4s, and Text) into fully drafted, multi-host audio podcasts and ready-to-upload LinkedIn video assets. 

Built with a modular Node.js backend, this studio handles heavy media processing locally while leveraging advanced AI models for script generation, audio synthesis, and visual design.

## 🚀 Key Features
* **Multi-Modal Ingestion:** Natively extracts YouTube closed captions, scrapes web articles via Cheerio, parses PDFs, or transcribes raw MP4 audio using OpenAI's Whisper.
* **AI Script Drafting:** Powered by Gemini 2.5 Flash to automatically generate conversational, multi-host podcast scripts translated into your language of choice. Includes a live word-counter to ensure scripts comply with social media duration limits.
* **Dynamic Audio Synthesis & VTT:** Compiles audio using OpenAI's TTS or ElevenLabs, automatically generating WebVTT files to drive a real-time, interactive "teleprompter" UI.
* **Two-Step Cover Art (Nano Banana 2):** Drafts highly descriptive image prompts before rendering stunning 16:9 widescreen thumbnails using the state-of-the-art **Gemini 3.1 Flash Image Preview** model.
* **Autonomous LinkedIn Packaging:** Uses `ffprobe` to enforce 3-to-14 minute duration constraints, pads the cover art, stitches it to the audio via FFmpeg, and writes a professional social media post.
* **Real-Time Telemetry:** Streams backend Node.js logs directly to the frontend UI via Server-Sent Events (SSE) for instant user feedback.

## 🛠️ Prerequisites
* **Node.js** (v20.0.0 or higher)
* **FFmpeg**: Required for audio chunking, padding, and stitching.
  * macOS: `brew install ffmpeg`
  * Windows: Download via gyan.dev and add to System PATH.

## 📦 Installation
1. Clone or download the repository.
2. Install the required dependencies:
   npm install

3. Verify your system's FFmpeg bridge:
   node test-ffmpeg.js

## 🔑 Configuration
Create a `.env` file in the root directory and add your required API keys:
GEMINI_API_KEY="your_gemini_key_here"
OPENAI_API_KEY="your_openai_key_here"
ELEVENLABS_API_KEY="your_elevenlabs_key_here" # Optional (For premium voice clones)
PORT=7860

## 💻 Usage
Start the local Express server:
npm start

Access the interactive web UI at: **http://127.0.0.1:7860**

## 🤖 OpenClaw Agent Integration
OmniCast Studio includes a strict `SKILL.md` API manual. Point your OpenClaw framework to this file to grant it the ability to autonomously drive the entire content pipeline using standard cURL commands.