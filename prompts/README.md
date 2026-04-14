# ETPK Systems — Prompts & Skills

## Structure

```
prompts/       → master prompts (human-readable .md specs)
skills/        → machine-readable tool manifests (JSON)
policy/        → policy-guardrails.md
docs/          → etpk-stack-manifest.yaml, run-log.md
```

## How to consume a prompt file

Every prompt in `/prompts/*.md` follows this contract:

- **Inputs**: described at top (file paths, parameters, constraints)
- **Outputs**: described at top (generated code, file tree, commands)
- **Style rules**: listed in the prompt itself (e.g. "use TypedDict", "no TODO comments")
- **Risk level**: low / medium / high (from `index.json`)

## How to consume a skill manifest

Every skill in `/skills/<skill-id>/manifest.json` follows this contract:

- **Entry**: how to invoke (e.g. `python zo_skill.py`)
- **Modes**: discrete operations (e.g. `run-skill` vs `run-chat`)
- **Inputs/Outputs**: typed per mode
- **orchestrator_instructions**: when to prefer this skill over alternatives

## Orchestrator rules

1. Read `prompts/index.json` to find the right prompt or skill by `id`
2. Load the referenced file (prompt .md or skill manifest JSON)
3. Execute the task — write files, run commands, call APIs
4. Commit and push changes to the appropriate repo
5. Append a timestamped entry to `docs/run-log.md`

## Style rules for generated code

- Prefer `TypedDict` over raw dicts for typed contracts
- No TODO or placeholder comments in final output
- Include exact CLI commands for running the output
- Add `// ... existing code ...` markers when editing existing files