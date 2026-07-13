# Sink-Correct Defenses

The named defense per sink class. Apply the entry for each sink the census names; the binding rule stays with the skill body — validation supplements, defenses replace.

- **SQL/NoSQL query**: parameterized queries / prepared statements — never string-building, never escaping-as-primary; escaping is a legacy fallback at best, parameterization removes the class.
- **Shell or process invocation**: argument arrays with `shell=false` — never string interpolation into a command line.
- **Filesystem path**: canonicalize FIRST, then enforce an allowlisted base-directory prefix — the order is the content: decode and normalize before the check, or `%2e%2e%2f` and symlinks walk past it.
- **HTML/JS render context**: context-aware output encoding at render time — the sink side, never the entry; encoding at input time corrupts the data for every non-HTML sink and still misses render contexts — with framework auto-escaping left ON.
- **Template engine**: user input as data only, never concatenated into template source (server-side template injection).
- **LDAP/directory query**: the engine's escaping API.
