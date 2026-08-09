# Diagnosis Workflow

Inspect the supplied output first. Compare it with the intended image and exact source prompt, then identify the earliest supported divergence in this order:

1. identity or visual thesis
2. reference use or identity
3. camera, geometry, crop, or occlusion
4. frozen time, interaction, pose, or biomechanics
5. lighting or material physics
6. rendering, typography, or UI leakage
7. salience
8. compiler mismatch
9. generation variance

Name downstream symptoms separately from the earliest plausible cause. Partition the explanation among prompt invitation, target behavior, reference failure, and generation variance; do not claim more than the supplied evidence supports. A single stochastic sample can support a hypothesis and one controlled next change, but cannot establish prompt causality.

Preserve user locks and unaffected controls. Recommend one controlled next change that isolates the earliest supported domain. Apply the authorization mapping in `SKILL.md`; otherwise stop at evidence, diagnosis, and the next experiment. Keep the evidence record separate from Intent and Prompt.
