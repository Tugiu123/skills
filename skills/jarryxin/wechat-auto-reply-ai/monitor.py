import time
import subprocess
import os
import argparse
import json
import logging

# Set up simple logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_cmd(cmd, timeout=45):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s: {cmd}")
        # Return a dummy completed process to avoid crashing the caller
        class DummyProcess:
            stdout = ""
            stderr = "TimeoutExpired"
            returncode = 124
        return DummyProcess()

def check_focus():
    res = run_cmd("osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'")
    return res.stdout.strip() in ["WeChat", "微信"]

def safe_send_detached(target_title, text):
    logger.info(f"Attempting to focus detached window: {target_title}")
    
    # 1. Focus the exact window by Title
    focus_res = run_cmd(f"peekaboo window focus --app 微信 --window-title '{target_title}'")
    if "Error" in focus_res.stdout or "not found" in focus_res.stdout:
        logger.error(f"Target window '{target_title}' not found.")
        return False
        
    time.sleep(0.5)

    # 2. Check if WeChat is indeed in front to prevent cross-app paste
    if not check_focus():
        logger.warning("Safety Abort: WeChat is not the frontmost app.")
        return False

    # 3. Paste the message securely
    safe_text = text.replace('"', '\\"').replace('`', '')
    run_cmd(f"peekaboo paste \"{safe_text}\"")
    time.sleep(0.5)
    
    # 4. Final check before sending (hitting return)
    if check_focus():
        run_cmd("peekaboo hotkey 'return'")
        return True
    else:
        logger.warning("Safety Abort: WeChat lost focus right before hitting return.")
        return False

def clean_output(output):
    lines = output.split('\n')
    fail_markers = ["cannot", "unable", "don't have", "can't see", "Hook registry", "via model", "I am an AI"]
    filtered = [l for l in lines if not any(m in l for m in fail_markers) and l.strip() and not l.startswith('#')]
    return "\n".join(filtered).strip()

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Generic WeChat Auto-Reply Monitor (UI-based)")
    parser.add_argument("--target", required=True, help="The exact title of the detached WeChat chat window.")
    parser.add_argument("--persona", required=True, help="The prompt guiding the LLM's reply style.")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval in seconds (default: 15).")
    args = parser.parse_args()

    TARGET = args.target
    PERSONA = args.persona
    INTERVAL = args.interval
    
    # Workspace setup for state and images
    WORKSPACE = os.path.expanduser("~/.openclaw/workspace/memory/wechat_skill")
    os.makedirs(WORKSPACE, exist_ok=True)
    RAW_IMG = os.path.join(WORKSPACE, f"wechat_raw_{TARGET.replace(' ', '_')}.png")
    STATE_FILE = os.path.join(WORKSPACE, f"last_seen_{TARGET.replace(' ', '_')}.txt")

    logger.info(f"Monitor started for target: '{TARGET}' with interval {INTERVAL}s.")
    logger.info(f"Persona: {PERSONA}")

    # Remove old state
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

    # Establish Baseline
    run_cmd(f"peekaboo see --app 微信 --window-title '{TARGET}' --path '{RAW_IMG}'")
    baseline_prompt = (
        "Look ONLY at the VERY LAST message bubble at the bottom. "
        "If it is WHITE (received), output the text. If it is GREEN (sent), output [SELF]. "
        "If it contains an image, output a short description. No other words."
    )
    res = run_cmd(f"summarize \"{RAW_IMG}\" --prompt \"{baseline_prompt}\" --plain --no-color --metrics off")
    baseline = clean_output(res.stdout)
    if baseline:
        with open(STATE_FILE, "w") as f:
            f.write(baseline)
        logger.info(f"Baseline set: {baseline}")

    # Monitor Loop
    while True:
        try:
            run_cmd(f"peekaboo see --app 微信 --window-title '{TARGET}' --path '{RAW_IMG}'")
            
            analysis_prompt = (
                "You are a WeChat chat analyst. Look at the VERY LAST message bubble at the bottom of this chat. "
                "1. If it's a WHITE bubble (received), output the text content. "
                "2. If it's a GREEN bubble (sent by user), output ONLY [SELF]. "
                "3. If the message contains an image or emoji, briefly describe it. If it is completely unreadable, output [UNKNOWN_CONTENT]. "
                "Output ONLY the result, no explanation or formatting."
            )
            res = run_cmd(f"summarize \"{RAW_IMG}\" --prompt \"{analysis_prompt}\" --plain --no-color --metrics off")
            analysis_res = clean_output(res.stdout)
            
            if not analysis_res or "cannot" in analysis_res.lower() or len(analysis_res) > 500 or analysis_res == "[UNKNOWN_CONTENT]":
                time.sleep(INTERVAL)
                continue

            if analysis_res != "[SELF]":
                last_seen = ""
                if os.path.exists(STATE_FILE):
                    with open(STATE_FILE, "r") as f:
                        last_seen = f.read().strip()
                
                if analysis_res != last_seen:
                    logger.info(f"New incoming message: {analysis_res}")
                    
                    # Generate reply via gemini CLI
                    reply_prompt = f"Reply to '{analysis_res}' following this persona/style: {PERSONA}"
                    reply_res = run_cmd(f"gemini \"{reply_prompt}\"")
                    reply = clean_output(reply_res.stdout)
                    
                    if not reply or "cannot" in reply.lower():
                        logger.warning("LLM failed to generate a reply, skipping.")
                        time.sleep(INTERVAL)
                        continue
                        
                    logger.info(f"Action: Replying '{reply}' to '{analysis_res}'")
                    
                    # Safe Send via specific window title
                    if safe_send_detached(TARGET, reply):
                        with open(STATE_FILE, "w") as f:
                            f.write(analysis_res)
                        logger.info("Action: Reply sent and state updated.")
                    else:
                        logger.error("Action: Failed to safely send reply (Safety Abort triggered).")
                        
        except Exception as e:
            logger.error(f"Error in Monitor Loop: {str(e)}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()