# Android Capture

## Preconditions

- Android SDK Platform Tools with `adb`
- a connected emulator or authorized device
- a buildable and installable app variant
- safe demo data or a deterministic fixture

## Procedure

1. Inspect the Gradle project and identify the application ID and runnable variant.
2. Build, install, and launch the app on the selected emulator or device.
3. Set a consistent appearance, locale, status bar state, and orientation.
4. Navigate to the planned screen and wait for the UI to settle.
5. Capture with `python "$SKILL_DIR/scripts/capture_android.py" <output.png> [device-serial]`.
6. Inspect the PNG immediately and recapture if the state is wrong.

The helper uses `adb exec-out screencap -p`. It does not build, install, seed, launch, or navigate the app.

## Stop conditions

Stop and request input when device authorization, credentials, external hardware, production data, or an irreversible action is required. If multiple devices are connected, pass an explicit serial.
