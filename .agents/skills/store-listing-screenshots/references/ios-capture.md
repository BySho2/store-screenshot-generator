# iOS Capture

## Preconditions

- macOS with Xcode and command-line tools
- a bootable iOS Simulator matching the intended store screenshot family
- a buildable app target and known bundle identifier
- safe demo data or a deterministic fixture

## Procedure

1. Inspect the Xcode project or workspace and determine the scheme.
2. Build and install the app into the selected Simulator.
3. Set a consistent appearance, locale, status bar state, and orientation.
4. Launch the app and navigate to the planned screen.
5. Wait for animations, network activity, and transient messages to finish.
6. Capture with `scripts/capture_ios.sh`.
7. Inspect the PNG immediately and recapture if the state is wrong.

The helper uses `xcrun simctl io <device> screenshot`. It does not build, install, seed, launch, or navigate the app.

## Stop conditions

Stop and request input when the app requires unavailable signing, credentials, hardware-only features, production data, or an irreversible action. Do not substitute fabricated UI.
