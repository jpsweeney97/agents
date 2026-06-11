---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

# Writing Skills

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: "Use when <user intent/situation> for <target/scope>."
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

The `description` is loader-facing routing text. It helps the next agent decide
whether to read this skill now.

Start with `Use when...`.

Include:

- the user intent or situation that should trigger the skill
- the target scope when it matters
- concrete user-facing phrases, symptoms, tools, or file types when they improve
  discovery
- nearest non-trigger boundaries when overlap is likely
- selection-critical constraints such as read-only, repo-wide, PR-scoped,
  technology-specific, or external-service-specific behavior

Do not include:

- workflow steps
- validation ladders
- output formats
- internal phases
- implementation details
- rationale for why the skill exists

Use this skeleton:

```yaml
description: "Use when <user intent/situation> for <target/scope>. Trigger on <short natural phrases/symptoms> when helpful. Do not use for <nearest collision>; use <neighbor skill> for <neighbor intent>."
```

Default to 25-60 words. Use more only when the extra words prevent a specific
likely misroute; descriptions over about 90 words should be rare.

Good:

```yaml
description: "Use when tests have race conditions, timing dependencies, hangs, or inconsistent pass/fail behavior. Use for test behavior diagnosis across frameworks; do not use for ordinary test writing or broad CI triage."
```

Bad:

```yaml
description: "Use when tests are flaky; first reproduce the failure, inspect async timing, replace sleeps with deterministic waits, add regression tests, and then refactor the helper."
```

The bad example summarizes workflow. That can tempt the next agent to execute
from the description instead of reading the full skill.

## When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Review Checklist

After drafting, verify:

- [ ] Description is routing text that starts with `Use when...`
- [ ] Description omits workflow steps and output formats
- [ ] SKILL.md under 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep
