# Changelog

All notable changes to the Git Cycle plugin are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 1.0.0 - 2026-06-17

### Added

- Initial packaging of six in-production git-lifecycle skills (`git-hygiene`, `closeout-check`,
  `merge-branch`, `exiting-worktrees`, `gh-address-comments`, `gh-pr-review-loop`) as one coherent
  dual-runtime plugin. Version 1.0.0 reflects established skills, not new ones; the only behavior
  changes shipped separately ahead of packaging were the git-hygiene protected-resolution convergence
  and revert marker (issues #9/#10) and the `exiting-worktrees` native-git dual-runtime port. No shared
  reference file: safety conventions stay inline in each skill, drift-guarded by
  `scripts/check-protected-set.sh`.
