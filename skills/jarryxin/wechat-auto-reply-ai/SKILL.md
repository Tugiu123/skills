# 🦇 wechat-auto-reply (Generic WeChat UI Automation Skill)

**Author:** OpenClaw / Selia's Assistant
**Version:** 1.0 (Based on V26 Core)
**Description:** A generic, secure UI-automation agent that silently monitors a detached WeChat window via OCR (`peekaboo` + `summarize`) and automatically replies using a customizable LLM persona. It employs robust "Safety Lock" mechanisms to prevent cross-app typing interference.

---

## 🛠 Prerequisites (Important)

This skill relies on macOS UI automation and OCR. You MUST meet these requirements:
1. **Operating System:** macOS
2. **WeChat Client:** Official WeChat Desktop Client for Mac.
3. **OpenClaw Dependencies:**
   * `peekaboo` CLI installed and authorized (Screen Recording & Accessibility permissions granted in System Settings).
   * `summarize` CLI installed (for OCR vision).
   * `gemini` CLI installed (for generating replies).
4. **Window Setup (CRITICAL):** The target chat **MUST** be double-clicked to open as a **Detached/Independent Window**. The script relies on the exact Window Title (e.g., "微信名" or "工作群").

---

## 🚀 Features

* **Visual Monitoring (OCR):** Uses AI vision to read the last message bubble instead of brittle UI element scraping.
* **Detached Window Targeting:** Only interacts with the specific detached chat window by its exact title, minimizing interference with the main WeChat interface.
* **Dual Safety Locks (Focus Protection):** Before pasting text and before hitting return, the script queries macOS to ensure WeChat is the *frontmost* application. If the user clicks away (e.g., to a code editor), it instantly aborts the action.
* **IME-Safe Injection:** Uses clipboard pasting (`Cmd+V`) instead of simulated typing to bypass Chinese Input Method (IME) interference and swallowed characters.
* **Customizable Persona:** Accepts generic prompt arguments to dictate the reply style. You can also instruct the persona to use native WeChat bracket codes for emojis (e.g., `[旺柴]`, `[吃瓜]`, `[捂脸]`).

---

## 🕹 Usage Instructions for OpenClaw Agent

When a user asks you to start an auto-reply or monitor a WeChat conversation, follow these steps:

### 1. Confirm Detached Window
Ask the user to double-click the target chat in WeChat to make it an independent window. Obtain the exact window title from the user.

### 2. Start the Monitor
Use the `exec` tool to run the `monitor.py` script in the background. You must provide the `--target` (window title) and `--persona` (reply instructions).

**Example Command:**
```bash
python3 ~/.openclaw/workspace/skills/wechat-auto-reply/monitor.py --target "微信名" --persona "回复要简短、干脆，不带句号，用词口语化，像好朋友聊天一样。"
```

*Note: Use `background: true` when running this via the `exec` tool so it doesn't block your current session.*

### 3. Check Status / View Logs
To check what the monitor is doing, view its process logs or the generic output.
```bash
# View active background sessions via OpenClaw process tool
process(action="list")

# Check process logs if it was started in the background
process(action="log", sessionId="<session_id>")
```

### 4. Stop the Monitor
To stop the monitoring, use the `process` tool to kill the specific session, or forcefully kill the script via terminal if necessary.
```bash
pkill -f "wechat-auto-reply/monitor.py"
```

---

## ⚙️ Script Arguments (`monitor.py`)

* `--target`: (Required) The exact title of the detached WeChat window (e.g., `"John Doe"`).
* `--persona`: (Required) The system prompt telling the LLM how to reply (e.g., `"Be very formal and concise"`).
* `--interval`: (Optional) How often to take a screenshot and check for new messages in seconds. Default is `15`. Do not set lower than 10 to avoid API rate limits on the vision model.