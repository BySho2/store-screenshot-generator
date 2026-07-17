---
name: store-listing-screenshots
description: Inspect a mobile app, capture suitable screens from an iOS Simulator or Android device/emulator when possible, write Japanese and English store copy, generate App Store and Google Play listing images, and visually validate the results. Use for app store screenshots, store listing images, promotional screenshots, App Store assets, or Google Play graphics. Do not upload or publish anything to a store.
---

# Store Listing Screenshots

Create store listing images from a runnable mobile app or from screenshots supplied by the user. Treat the repository containing this skill as the generator repository and the user's app repository as the target app.

## Resolve paths

1. Resolve this `SKILL.md` to an absolute path.
2. Set `SKILL_DIR` to its containing directory.
3. Set `GENERATOR_ROOT` to `SKILL_DIR/../../..`.
4. Resolve and confirm the target app repository separately. Never write generated artifacts into the target app unless the user requests it.
5. Create a dedicated working directory for the run outside tracked source folders when possible.

The generator entry point is `GENERATOR_ROOT/generate.py`. Supporting scripts are in `SKILL_DIR/scripts`.

## Required outcome

Produce both of these output sets unless the user narrows the request:

- App Store portrait images in Japanese and English.
- Google Play portrait images in Japanese and English.

Do not claim completion until the source screenshots, configuration, generated images, dimension checks, and visual review all exist.

## Workflow

### 1. Inspect the target app

- Determine whether the app is iOS, Android, Flutter, React Native, or another supported mobile stack.
- Read the app's navigation and feature structure before selecting screens.
- Identify the app name, primary value proposition, brand colors, and supported languages from repository evidence.
- Identify build commands, bundle/package identifiers, launch targets, test fixtures, demo accounts, and existing UI tests.
- Do not invent credentials or use production customer data.

Read `references/screen-selection.md` before choosing screens.

### 2. Propose a capture plan

- Select three to six screens that tell one coherent story.
- Prefer screens that show distinct user value rather than multiple near-identical states.
- State how each screen will be reached and what safe sample data it needs.
- If reaching a screen requires login, payment, personal information, destructive actions, or an external service, stop and request the missing access or use a safe fixture.
- Ask for user confirmation only when the screen choice or data setup would materially change the result. Otherwise proceed with the strongest evidence-backed selection.

### 3. Build and capture

Read the relevant platform reference:

- iOS: `references/ios-capture.md`
- Android: `references/android-capture.md`

For iOS Simulator captures, use:

```bash
scripts/capture_ios.sh <output.png> [device-udid-or-booted]
```

For Android captures, use:

```bash
scripts/capture_android.sh <output.png> [device-serial]
```

The helper scripts capture only the current device display. The agent remains responsible for building the app, launching it, creating safe sample state, navigating to the intended screen, and verifying that the captured state is correct.

If automated capture is unavailable, switch to supplied-screenshot mode. Clearly report why capture was unavailable and ask the user for the required screenshots. Continue from those images without lowering later QA requirements.

### 4. Review source screenshots

Inspect every captured image before generation. Reject or recapture images containing:

- personal information, real customer data, tokens, email addresses, or account identifiers
- debug banners, layout guides, pointer indicators, developer menus, or error overlays
- unexpected permission dialogs, keyboards, notifications, or loading states
- inconsistent time, locale, theme, orientation, or sample data
- content the user has not authorized for public store use

### 5. Write store copy

Read `references/copy-guidelines.md`.

- Write one benefit-led headline and one short supporting sentence for each screen.
- Prepare Japanese and English as natural, independent copy. Do not translate word-for-word when that sounds unnatural.
- Make only claims supported by the visible screen or verified app behavior.
- Keep terminology consistent across all slides.
- Localize the displayed app name when appropriate.

### 6. Configure the design

- Copy `GENERATOR_ROOT/config.example.yaml` into the run working directory.
- Use absolute screenshot paths or paths relative to the run configuration.
- Point the theme to one of the files under `GENERATOR_ROOT/themes`, or create a run-specific theme based on the app's verified brand colors.
- Keep App Store and Google Play outputs enabled unless the user requests only one store.
- Never overwrite the user's existing configuration without explicit intent. Use a new run directory by default.

### 7. Generate

Create an isolated Python environment when one is not already available, install `GENERATOR_ROOT/requirements.txt`, then run:

```bash
python GENERATOR_ROOT/generate.py --config <run-directory>/config.yaml
```

Use `--overwrite` only after confirming that replacing the current run outputs is intended.

### 8. Validate deterministically

Run:

```bash
python scripts/validate_outputs.py --config <run-directory>/config.yaml
```

Validation must confirm expected file count, filename expansion, dimensions, PNG format, and RGB color mode.

### 9. Perform visual QA

Read `references/qa-checklist.md`. Inspect all generated images, preferably as contact sheets grouped by store and locale. Check:

- headline and body text are fully visible
- app screenshots are not distorted or unintentionally cropped
- visual hierarchy is consistent across the set
- Japanese and English both read naturally
- screenshots and copy match each other
- no private, unreleased, or misleading content is present

Repair and regenerate any failed image. Deterministic validation alone is not visual approval.

### 10. Deliver

Report:

- target app and platforms actually captured
- whether screenshots were captured automatically or supplied
- selected screens and their order
- output directories for each store and locale
- deterministic validation result
- visual QA result and any remaining caveats

Do not upload images to App Store Connect or Google Play Console unless the user separately and explicitly requests that action.

## Boundaries

- This skill creates store listing images; it does not submit, publish, or release an app.
- Do not use production credentials, customer records, or undisclosed app features to stage screenshots.
- Do not promise that capture is fully automatic for every app. Build failures, authentication, hardware-only features, and unavailable simulators require a fallback or user input.
- Store requirements can change. Confirm current Apple and Google requirements before an actual upload.
