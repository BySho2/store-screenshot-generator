# Planning and resumable workflow

Use files in the run directory as the source of truth. Do not depend on an agent-specific memory feature.

## Initialize or resume

For a new run, copy these templates:

- `assets/project.template.yaml` to `<run-directory>/project.yaml`
- `assets/capture-plan.template.md` to `<run-directory>/capture-plan.md`

If `project.yaml` already exists, read it and the capture plan before changing the app or generating images. Continue from `status.phase`, verify that referenced files still exist, and preserve confirmed decisions.

Recommended phases are `planning`, `capture`, `copy`, `design`, `generation`, `qa`, and `complete`. Update `status.phase` and `status.updated_at` after every completed phase.

## Discover benefits before choosing screens

Identify three to six user benefits from repository evidence, supplied product material, or verified app behavior. Rank them and record the evidence in the Benefits table. The first slide must communicate the strongest benefit, not merely the first feature in the navigation.

Ask the user to confirm benefit priorities only when evidence is ambiguous or the choice would materially change the story.

## Evaluate and pair screenshots

Pair one distinct benefit with one screen. Rate each candidate:

- `Great`: clear state, strong proof of the benefit, store-ready without changes.
- `Usable`: understandable and safe, but visually weaker or less direct.
- `Retake`: private data, transient UI, weak proof, poor composition, inconsistent locale/theme, or another correctable issue.

For `Retake`, write a concrete instruction: destination screen, state to create, safe sample data, overlays to close, and what must be visible. Do not silently lower the quality bar because automated capture is difficult.

## Compare themes before full generation

Choose three themes that suit the app and render only the first slide with each. Save them under `<run-directory>/design-options/<theme-name>/`, then create `<run-directory>/qa/theme-options.png` with the contact-sheet script.

Select the option with the best readability, brand fit, and screenshot prominence. Ask the user to choose only when the alternatives are genuinely subjective or materially different. Record the selected theme and reason in both planning files, then generate the complete set.

## Finish with evidence

Save deterministic validation results and contact sheets under `<run-directory>/qa/`. Mark the run `complete` only after source review, generation, validation, and visual QA have all passed.
