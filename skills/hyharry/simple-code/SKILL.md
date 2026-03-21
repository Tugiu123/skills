---
name: simple-code
description: "Plan and build small, readable coding projects with a strict workflow: think first, make a short plan, implement with an ACP Codex agent using GPT-5.3-Codex, then personally verify, add focused tests, add minimal documentation, and organize the result cleanly. Use when the user asks for simple code, a small project, a self-contained utility, or a straightforward implementation that should stay easy to read and easy to manage."
---

# Simple Code

## Overview

Follow a lightweight project workflow for small coding tasks where readability matters more than cleverness.

## Workflow

1. If the task is project-like, create a properly named project folder under `agent_code/<project-name>` first.
2. Do all further work inside that project folder.
3. Think through the request before coding.
4. Make a short plan and state the chosen approach briefly.
5. Spawn an ACP Codex run with model `openai/gpt-5.3-codex` to implement the core code inside the project folder.
6. Wait for the ACP Codex run to finish writing, and check status with acpx status or /acp status until it is clearly done before touching the files yourself.
7. Keep the implementation simple, readable, and standard-library-first unless the user asks otherwise.
8. After ACP implementation is complete, personally inspect the result.
9. Add tests for the most important functionality inside the same project folder.
10. Add minimal documentation if ACP did not already provide enough.
11. Verify the project by running the relevant build/test commands from the project folder.
12. Use git inside the project folder, not at the whole-workspace level, unless the user explicitly wants workspace-level git.

## Coding Rules

- Prefer clear names over compact tricks.
- Prefer fewer files and a smaller API when possible.
- Prefer standard tools for the language ecosystem.
- Avoid unnecessary dependencies.
- Handle invalid input and obvious failure cases clearly.
- Do not leave the code unverified if a local build/test command is available.

## Project Layout Rules

For project-like requests, create this structure first and work only inside it by default:

- `agent_code/<project-name>/`
- source files in that folder root unless there is a good reason to add subdirectories
- tests in the same folder if the project is very small
- add a simple build file when appropriate, such as `CMakeLists.txt` for C++

## Git Rules

- Initialize git in the project folder if needed.
- Commit meaningful milestones after verification.
- If the workspace root has temporary bootstrap git history and the user asks to remove it, remove only that root-level history.
- Do not rewrite git history unless the user explicitly asks.

## Response Style

When reporting back to the user, include:

- what was built
- where it lives
- how it was verified
- the latest relevant commit hash if git was used
