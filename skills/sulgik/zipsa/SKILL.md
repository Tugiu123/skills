---
name: zipsa
description: Local-first privacy gateway for LLM applications. Use when the user needs to process sensitive, private, or proprietary information (PII, health records, internal business strategy, SSNs, credentials) while still utilizing cloud models (Claude, Gemini, GPT). Zipsa reformulates queries locally to remove identity and secrets before routing to the cloud, then synthesizes the answer back to the local context.
---

# Zipsa

Zipsa is a local-first privacy gateway that sits between OpenClaw and cloud LLMs. It ensures that raw private context never leaves the local environment while still allowing the use of powerful frontier models for reasoning.

## When to Use

Trigger this skill whenever the user provides or asks to process:
- **PII**: Names, SSNs, DOBs, contact info.
- **Healthcare Data**: Patient records, clinical notes, symptoms.
- **Internal Business Context**: Pricing floors, negotiation terms, churn warnings, project codenames.
- **Secrets**: API keys, credentials, internal system details.

## Core Workflow

Zipsa operates as an OpenAI-compatible gateway (default: `http://localhost:8000/v1`). 

### 1. Identify Sensitive Context
When the user's request contains sensitive data, explain that Zipsa will be used to protect their privacy.

### 2. Route Through Zipsa
Instead of calling the standard cloud providers directly, use the Zipsa endpoint. Zipsa will:
- **Scan locally** for high-risk markers.
- **Classify** the query (Private, Hybrid, or Knowledge).
- **Reformulate** (rewrite) the query to abstract identity and proprietary details.
- **Route** the safe version to the cloud.
- **Synthesize** the final answer back with the local details.

## Integration Examples

### Using with OpenClaw
OpenClaw can be configured to use Zipsa as its backend:
- `OPENAI_BASE_URL=http://localhost:8000/v1`
- `OPENAI_API_KEY=zipsa-key`
- `OPENAI_MODEL=zipsa`

### Multi-turn Sessions
For conversation continuity, always pass a `session_id`.
```json
{
  "model": "zipsa",
  "messages": [...],
  "extra_body": { "session_id": "unique-session-id" }
}
```

## Reference
For detailed configuration and advanced examples, see [references/README.md](references/README.md).
