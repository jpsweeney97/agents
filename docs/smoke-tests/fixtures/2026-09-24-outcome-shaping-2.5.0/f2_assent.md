User: /decide:outcome-shaping — I want to work out what I want the CLI's config file format to be before I commit to one.

Assistant: My read so far: you want a config format that stays readable by hand and never surprises a user who edits it. First question: should comments be allowed in the file? I'd suggest yes; hand-edited config without comments tends to rot. The trade: comments rule out plain JSON.

User: Yes, allow comments; comments rule out plain JSON, fine.

Assistant: Noted. Second: should the format allow nesting deeper than two levels? I'd suggest no; deep nesting is where hand editing goes wrong. The trade: some settings become long dotted keys.

User: No deep nesting; long dotted keys are fine.

Assistant: Third: should unknown keys be an error or a warning? I'd suggest error; silent typos are the worst failure. The trade: renaming a key becomes a breaking change.

User: Error on unknown keys; renaming is a breaking change, accepted.

Assistant: Fourth: should the file support including other files? I'd suggest no for v1. The trade: large configs stay in one file.

User: No includes for v1; one file is fine.

Assistant: Fifth: should environment variables be expandable inside values? I'd suggest yes, with a strict `${VAR}` syntax only. The trade: a literal `${` needs escaping.

User: Yes, strict ${VAR} only; escaping a literal ${ is fine.
