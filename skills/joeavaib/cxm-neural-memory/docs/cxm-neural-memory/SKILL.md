---
name: cxm-neural-memory
description: Use this skill when you need to understand the architecture of a codebase, perform semantic searches across files, map dependencies before refactoring, or ingest non-code documentation into your context memory. It leverages the CXM (ContextMachine) tool to prevent context collapse.
---

# CXM Neural Memory Skill

This skill equips you with the ability to use the local CXM (ContextMachine) tool. CXM acts as an external "Neural Memory" and architectural mapping tool for your context window.

## 🛠️ Setup & Self-Healing

If you are triggered but notice that the directory `src/` or the file `src/cli.py` is missing in the current workspace, you **MUST** perform the following setup steps before using any CXM tools:

1. **Clone the Engine:**
   ```bash
   git clone https://github.com/Joeavaib/partner .
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**Crucial Instruction:** Always use the `--agent-mode` flag when calling `python src/cli.py` so that the output is strict, parseable JSON.

## Core Capabilities & Usage

### 1. Semantic Search (Vibe Searching)

When you know *what* a piece of code does but not what it is called or where it is located, use the semantic vector search.

**Command:**
```bash
python src/cli.py --agent-mode harvest --semantic "your natural language query"
```

**Example:**
If you need to find where user permissions are checked, do not run `grep "permission"`. Instead, ask CXM:
```bash
python src/cli.py --agent-mode harvest --semantic "Where is the user authorization and permission logic?"
```

**Interpretation:** 
The output will be a JSON object containing a `results` array with file paths and the relevant code chunks.

### 2. Dependency Graphing (Blast Radius Check)

Before refactoring a core module, you must verify what other parts of the system depend on it.

**Command:**
```bash
python src/cli.py --agent-mode map path/to/target/file.py
```

**Example:**
If you are asked to change `src/auth.py`, first check its dependencies:
```bash
python src/cli.py --agent-mode map src/auth.py
```

**Interpretation:**
The output is a JSON dependency graph (AST-based) showing which files import the target and what functions/classes are connected. Use this to formulate a safe refactoring plan.

### 3. Architecture & Documentation Ingestion

By default, standard searches might focus mostly on code. If you need high-level understanding (e.g., from `README.md`, `docker-compose.yml`, or `package.json`), force CXM to ingest these non-code files.

**Command:**
```bash
python src/cli.py --agent-mode ingest docs_or_root_directory
```

**Example:**
```bash
python src/cli.py --agent-mode ingest .
```

### 4. Background Memory Sync (Watcher)

If the user mentions that they are actively editing files while you work, you can suggest they start the background watcher in a separate terminal tab so your searches always return the freshest state. 

*(Note: As an agent, do not run the `watch` command yourself as it is a blocking daemon process. Advise the user to run it).*
User Command: `python src/cli.py watch`

## Workflow Checklist for Complex Refactoring

1. **Understand:** Run `python src/cli.py --agent-mode ingest .` to ensure docs are indexed.
2. **Locate:** Use `python src/cli.py --agent-mode harvest --semantic "<intent>"` to find the relevant code sections.
3. **Map:** Once you identify the file to change, run `python src/cli.py --agent-mode map <file_path>` to see what else might break.
4. **Execute:** Perform your file edits using your standard tools.
