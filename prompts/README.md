# Prompts — Contract & Style Guide

## How to consume a prompt file

Every prompt in `/prompts/*.md` follows this contract:

1. **Read the full file** before doing anything else.
2. **Extract:** goal, tech stack, deliverables, and any output format requirements.
3. **Execute** the task end-to-end (code, file tree, commands).
4. **Report** using the same format the prompt specifies.

## Standard prompt structure

Every master prompt in this repo MUST contain these sections:

```
# <Name>

## Goal / UX
## Tech Stack
## Data Model   (TS interfaces where relevant)
## Service Layer (abstraction boundaries)
## Project Structure (file tree)
## Deliverables
  1. File/folder tree
  2. Full code for all files
  3. package.json + tsconfig.json
  4. CLI run commands
  5. Brief explanation of key mechanism
```

## Style rules for AI consumption

- No hidden assumptions — state every constraint explicitly
- Tech stack specified as exact package names + versions where possible
- TS interfaces for all data models; no `any`
- Service layer always abstracted (swappable impl, not hard‑coded)
- Deliverables listed as a numbered checklist — easy to verify
- Always include: file tree, full code, package.json, run commands

## What this enables

- **Zo Computer:** `etpk-systems/prompts/<name>.md` → paste into chat → get full output
- **Perplexity Computer:** same — paste → get code + tree + commands
- **Orchestrator (zo-space):** picks the right prompt by task + repo name, runs it, logs output
- **JSON index:** future proof — allows programmatic prompt discovery

## Adding a new prompt

1. Save to `etpk-systems/prompts/<descriptive-name>.md`
2. Follow the structure above exactly
3. Add entry to `prompts/index.json`
4. Commit and push
