# Markdown Reformat Examples

Use this reference when a concrete example would prevent guessing.

## Labels And Lists

**Input:**

```text
Review Notes

1. Risks

- first issue
- second issue

Correctness

The current parser is too eager.
```

**Output:**

```markdown
# Review Notes

## 1. Risks

- first issue
- second issue

### Correctness

The current parser is too eager.
```

## Code-Like Blocks

**Input:**

```text
Deploy checklist

Run:
npm test
npm run build

Regex
^feature/.+$
```

**Output:**

````markdown
# Deploy checklist

Run:

```bash
npm test
npm run build
```

## Regex

```regex
^feature/.+$
```
````
