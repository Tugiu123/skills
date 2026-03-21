#!/bin/bash
# OpenClaw Callback - Send callback via OpenClaw system event

set -euo pipefail

# Default values
STATUS="done"
MODE="single"
TASK=""
MESSAGE=""
OUTPUT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build the summary instruction and task content
SUMMARY_INSTRUCTION="请总结以下 Claude Code 任务的执行结果，并回复用户："

# Build message with clear structure
MSG="$SUMMARY_INSTRUCTION

=== 任务信息 ===
模式: $MODE
状态: $STATUS
任务标识: $TASK"

# Append original task/command
MSG="$MSG

=== 用户请求 ===
$MESSAGE"

# Append output if provided
if [[ -n "$OUTPUT" ]]; then
    MSG="$MSG

=== 执行结果 ===
$OUTPUT"
else
    MSG="$MSG

=== 执行结果 ===
(无输出内容)"
fi

# Check if openclaw is available
if command -v openclaw &> /dev/null; then
    openclaw system event --text "$MSG" --mode now
else
    echo "Warning: openclaw not found, using echo instead"
    echo "$MSG"
fi
