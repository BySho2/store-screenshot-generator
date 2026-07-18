---
name: store-listing-screenshots
description: Inspect a mobile app, capture suitable screens from an iOS Simulator or Android device/emulator when possible, write Japanese and English store copy, generate App Store and Google Play listing images, and visually validate the results. Use for app store screenshots, store listing images, promotional screenshots, App Store assets, or Google Play graphics. Do not upload or publish anything to a store.
---

# Store Listing Screenshots

Create store listing images from a runnable mobile app or from screenshots supplied by the user. Run this workflow from the target app repository. The skill directory contains the generator, themes, dependencies, capture helpers, and validation tools required by the workflow.

## Resolve paths

1. Resolve this `SKILL.md` to an absolute path.
2. Set `SKILL_DIR` to its containing directory. Do not infer tool paths from the current working directory.
3. Resolve the current target app repository and confirm its platform before acting.
4. Create a dedicated `store-listing-assets` working directory in the target app repository unless the user specifies another output location.
5. Keep source captures, the run configuration, generated images, and QA artifacts inside that working directory.

The generator entry point is `SKILL_DIR/scripts/generate.py`. Supporting scripts, dependencies, configuration templates, and themes are all relative to `SKILL_DIR`.

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

Read `SKILL_DIR/references/screen-selection.md` before choosing screens.

### 2. Propose a capture plan

- Select three to six screens that tell one coherent story.
- Prefer screens that show distinct user value rather than multiple near-identical states.
- State how each screen will be reached and what safe sample data it needs.
- If reaching a screen requires login, payment, personal information, destructive actions, or an external service, stop and request the missing access or use a safe fixture.
- Ask for user confirmation only when the screen choice or data setup would materially change the result. Otherwise proceed with the strongest evidence-backed selection.

### 3. Build and capture

Read the relevant platform reference:

- iOS: `SKILL_DIR/references/ios-capture.md`
- Android: `SKILL_DIR/references/android-capture.md`

For iOS Simulator captures, use:

```bash
python "$SKILL_DIR/scripts/capture_ios.py" <output.png> [device-udid-or-booted]
```

For Android captures, use:

```bash
python "$SKILL_DIR/scripts/capture_android.py" <output.png> [device-serial]
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

Read `SKILL_DIR/references/copy-guidelines.md`.

- Write one benefit-led headline and one short supporting sentence for each screen.
- Prepare Japanese and English as natural, independent copy. Do not translate word-for-word when that sounds unnatural.
- Make only claims supported by the visible screen or verified app behavior.
- Keep terminology consistent across all slides.
- Localize the displayed app name when appropriate.

### 6. Configure the design

- Copy `SKILL_DIR/assets/config.template.yaml` to `<run-directory>/config.yaml`.
- Copy the selected theme from `SKILL_DIR/assets/themes` to `<run-directory>/theme.yaml`, then customize that run-specific copy when needed.
- Use absolute screenshot paths or paths relative to the run configuration.
- Keep the configuration's theme path set to `./theme.yaml`.
- Keep App Store and Google Play outputs enabled unless the user requests only one store.
- Prefer `modern-gradient.yaml` as the starting point unless the app's existing brand clearly calls for another theme.
- Do not add a large background panel by default. Use `panel.enabled: false` unless the panel materially improves contrast.
- Use `device.frame: rounded` as the safe general default. A neutral `generic` frame may be used when it improves the presentation without implying a specific manufacturer.
- Configure App Store and Google Play device presentation separately in each output when appropriate. Prefer a plain rounded screenshot for Google Play listing output.
- Use `device.frame: asset` only with a frame image the user is authorized to use. Do not download or redistribute Apple, Google, or manufacturer artwork without confirming its terms.
- Never overwrite the user's existing configuration without explicit intent. Use a new run directory by default.

### 7. Generate

Create an isolated Python environment when one is not already available, install `SKILL_DIR/requirements.txt`, then run:

```bash
python "$SKILL_DIR/scripts/generate.py" --config <run-directory>/config.yaml
```

Use `--overwrite` only after confirming that replacing the current run outputs is intended.

### 8. Validate deterministically

Run:

```bash
python "$SKILL_DIR/scripts/validate_outputs.py" --config <run-directory>/config.yaml
```

Validation must confirm expected file count, filename expansion, dimensions, PNG format, and RGB color mode.

### 9. Perform visual QA

Read `SKILL_DIR/references/qa-checklist.md`. Inspect all generated images, preferably as contact sheets grouped by store and locale. Check:

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
