# Cross-Domain Examples

These examples calibrate scene architecture, compiler handoff, and selective omission across different image classes. They are not prompt templates. The target-model owner may change wording and structure as its current guidance changes.

## Contents

- [Photorealistic candid action](#photorealistic-candid-action)
- [Stylized editorial illustration](#stylized-editorial-illustration)
- [Product-marketing hero](#product-marketing-hero)
- [Reference-conditioned image edit](#reference-conditioned-image-edit)
- [Premise-diversity exploration](#premise-diversity-exploration)
- [Controlled variation](#controlled-variation)
- [Surgical edit](#surgical-edit)
- [Finalization](#finalization)
- [Authorized repair brief](#authorized-repair-brief)
- [Cross-domain lesson](#cross-domain-lesson)

## Photorealistic candid action

### Seed

> Make a real-looking phone photo from an employee behind the register of a local restaurant. A customer five or six feet away is screaming and flailing because a bee briefly landed on her face and flew away. Use my restaurant references for the environment.

### Scene architecture

**Creative latitude:** Tasteful completion.

**Visual thesis:** An ordinary, slightly chaotic phone snapshot whose obstructed employee viewpoint, off-center framing, and asymmetric recoil make a harmless startle feel accidental rather than performed.

**Salience budget:**

- employee viewpoint remains physically behind the counter;
- bee is already out of frame while the customer's asymmetric recoil is still escalating;
- the subject looks away from the camera and reads as involuntary rather than posed;
- consumer-phone realism and the reference-controlled storefront structure survive.

**Supporting internal reasoning:** The counter edge can establish camera origin; unequal hand depths and weight moving over one flexed leg maintain believable balance; the immediately-before and after states prevent mixed motion phases.

### Compiler handoff

Target the active OpenAI image tool only through its current `imagegen` skill or current guidance. Pass the visual thesis, four salience priorities, restaurant reference roles, portrait framing, and only the biomechanics needed to prevent the symmetric `hands beside face` substitute. If that authority is unavailable, provide a portable unverified handoff rather than claiming target-specific readiness.

### Illustrative target-compiler output

> Create a photorealistic, candid iPhone snapshot from an employee's viewpoint behind a restaurant register. A narrow counter edge and cropped POS corner cross the bottom of the portrait frame, while a customer stands slightly off-center several feet away. Freeze the instant just after a bee has left the frame: she recoils asymmetrically, weight shifting back over one flexed leg, one hand rising toward her cheek and the other thrown outward at a different depth. Her widened eyes follow the bee's former path rather than the camera. Keep the moment ordinary, harmless, and genuinely unposed, with broad phone-camera depth, natural mixed storefront light, restrained HDR, and slight motion softness only in the fastest fingertips. Use the supplied references for storefront proportions, counter materials, and functional layout—not their people or camera angle.

### Keep internal or omit

- the full immediately-before and immediately-after sequence;
- exact frame percentages and secondary table distances;
- provenance labels, decision history, and validation rationale;
- repeated negatives naming every unwanted genre.
- storefront visual controls if the restaurant references are inaccessible; retain only the user-declared environment role and request reattachment if those controls are material.

## Stylized editorial illustration

### Seed

> Design a magazine illustration about urban loneliness: one commuter waiting in rain beneath an enormous elevated train line. Make it beautiful, not bleak.

### Scene architecture

**Creative latitude:** Exploratory authorship.

**Visual thesis:** A rain-muted editorial illustration that makes the lone commuter feel small inside broad architectural rhythm, while warm reflected color keeps solitude contemplative rather than hopeless.

**Salience budget:**

- one small commuter remains the emotional focal point beneath monumental repeating beams;
- cool rain and concrete are interrupted by warm reflected shop light;
- the composition uses broad negative space and rhythmic vertical structure;
- the finish reads as sophisticated editorial illustration, not literal photography or dystopian concept art.

### Compiler handoff

Target the active image tool. Give it the visual thesis, wide horizontal use, subject scale, shape rhythm, palette contrast, and the prohibited dystopian read. Do not give it photographic exposure mechanics or a biomechanical inventory.

### Illustrative target-compiler output

> Create a wide editorial illustration about urban loneliness: a single small commuter waits under the monumental repeating beams of an elevated train line in steady rain. Use large fields of cool blue-gray concrete and soft rain haze, interrupted by warm amber shop-light reflections crossing the wet pavement around the figure. The architecture should form a calm vertical rhythm with generous negative space, making the commuter feel solitary but not abandoned. Sophisticated magazine-art finish, simplified shapes, restrained texture, and selective detail; contemplative and beautiful rather than bleak, cinematic, or dystopian.

### Keep internal or omit

- exact beam spacing or measured subject distance;
- camera-holder motivation and phone-lens behavior;
- detailed anatomy unless the pose becomes a failure;
- a catalog of rain artifacts, surface defects, and background props.

## Product-marketing hero

### Seed

> I need a landing-page hero for a matte ceramic travel mug. Quiet premium feel, plenty of room for copy, no logo or text in the image.

### Scene architecture

**Creative latitude:** Tasteful completion.

**Visual thesis:** Quiet premium product photography built around one tactile matte form, soft directional light, and disciplined empty space rather than decorative luxury signals.

**Salience budget:**

- the mug's silhouette, lid construction, and matte ceramic texture remain crisp and believable;
- the product occupies the right side with clean negative space on the left for page copy;
- soft directional studio light creates controlled highlights and a grounded shadow;
- no logo, text, decorative props, or glossy-plastic substitution.

### Compiler handoff

Target the active image tool with the asset use, landscape composition, product material, copy-safe negative space, and exclusions. Omit narrative, frozen-time machinery, and most environment fields.

### Illustrative target-compiler output

> Create a landscape landing-page hero in quiet premium product-photography style. Place one matte ceramic travel mug on the right side of a warm neutral studio surface, leaving broad uncluttered negative space on the left for web copy. Preserve a clean, distinctive silhouette, believable fitted lid, fine ceramic grain, and subtle manufacturing variation. Use soft directional light with controlled highlights, a natural contact shadow, and restrained warm-gray color. No logo, no text, no decorative props, no steam, no watermark, and no glossy-plastic finish.

### Keep internal or omit

- interpersonal interaction, narrative read, and adjacent moments;
- depth-plane detail beyond product, surface, and backdrop;
- arbitrary lifestyle props added merely to signal premium quality;
- exact lighting diagrams unless a generated result requires diagnosis.

## Reference-conditioned image edit

### Seed

> Use Image 1 as the edit target. Replace only the person's jacket with the jacket from Image 2. Everything else must remain the same.

### Scene architecture

**Creative latitude:** Strict preservation.

**Visual thesis:** A seamless wardrobe substitution that preserves the original photograph's identity and moment so completely that only the jacket design changes.

**Salience budget:**

- preserve the person's face, body, pose, hands, hair, expression, and identity from Image 1;
- preserve Image 1's framing, background, lighting, shadows, and all non-jacket pixels as closely as the target permits;
- use Image 2 only for jacket cut, material, color, closures, and construction details;
- fit the replacement naturally to the existing pose, occlusion, folds, and light.

### Compiler handoff

Use the target image-edit skill, not a general scene-generation compiler. Pass the exact edit, reference roles, strict invariants, locality, and continuity requirements. Do not redescribe unrelated scene content.

### Illustrative target-compiler output

> Edit Image 1 by replacing only the person's jacket with the jacket shown in Image 2. Use Image 2 only for the jacket's cut, material, color, closures, and construction details. Preserve the person's identity, face, body, pose, hands, hair, expression, framing, background, lighting, shadows, and every non-jacket element from Image 1. Fit the replacement jacket naturally to the existing posture and occlusions, with folds, highlights, and shadows consistent with the original photograph. Make no other changes.

### Keep internal or omit

- a new description of the person's appearance or background;
- global art direction that invites regeneration;
- invented garment accessories or styling changes;
- camera and scene geometry already fixed by the edit target.

## Premise-diversity exploration

For the commuter illustration, three candidates may all preserve the theme of urban loneliness while materially changing the image: the commuter under a station canopy watching rain on the tracks; the commuter framed in a warm shop doorway as an elevated train passes; and the commuter seen as a small reflection in a bus shelter. These differ in premise, relationship to the city, composition, and emotional read, so they are `premise_diversity` candidates. None replaces the active prompt until selected.

## Controlled variation

For the mug hero, keep the matte ceramic mug, right-side placement, left copy space, soft studio light, and no-logo rule locked. Vary only the neutral surface from warm gray to pale stone and the shadow direction from lower right to lower left. This is `controlled_variation`: it cannot introduce lifestyle props, a new finish, or a different product composition.

## Surgical edit

For the jacket edit, “make only the jacket dark olive and otherwise identical” is `surgical`. The active prompt and Image 1 remain the source. The new version changes the jacket color and allows only dependent fabric highlights, folds, and local shadow response; it does not re-art-direct the photograph, the person, the background, or the mood.

## Finalization

When the user accepts the edited jacket prompt and says “prompt only,” `FINALIZE` removes its explanatory lead-in and emits the accepted prompt once, character-for-character in visual and semantic meaning. It does not improve, compress, or re-target it.

## Authorized repair brief

An authorized reviewer brief might say: “Implement only: preserve the original restaurant prompt and protected employee viewpoint, but clarify that the customer’s outward hand is farther from camera than the cheekward hand; keep strict preservation.” The architect treats this as `EDIT`, retains the source prompt, adds that single geometric clarification and any required continuity wording, then returns a new prompt version. It does not inspect the output or claim why the output failed.

## Cross-domain lesson

The scene architecture stays available in every domain, but the target handoff changes shape:

- photorealistic action keeps frozen time and decisive biomechanics;
- editorial illustration keeps visual thesis, shape rhythm, palette, and emotional read;
- product imagery keeps intended use, material, placement, light, and negative space;
- image edits keep locality, reference roles, and preservation invariants.

Do not reward a prompt for carrying every module. Reward it for preserving the few instructions that make this image this image.
