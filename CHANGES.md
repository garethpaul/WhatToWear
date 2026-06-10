# Changes

## 2026-06-10

- Added immutable, read-only GitHub Actions verification on Python 3.10 and
  3.12 for the portable privacy and camera-safety contracts.
- Added static coverage for workflow permissions, action pins, matrix versions,
  timeout, and the `make check` command.
- Documented that hosted Linux checks intentionally skip legacy Xcode builds.

## 2026-06-09

- Guarded mirrored preview construction when the saved capture has no
  `CGImage` backing and reused the missing-photo fallback.
- Added static checker coverage for display `CGImage` fallback behavior.
- Required successful local JPEG writes before navigating to the captured-photo
  display flow.
- Added static checker coverage for the photo write-success guard.
- Guarded countdown start so repeated snap taps cannot schedule overlapping
  capture timers.
- Added static checker coverage for duplicate countdown timer prevention.
- Guarded camera session output and input setup before adding them to the
  capture session.
- Added static checker coverage for capture session input and output guards.
- Guarded focus touch handlers before reading touch locations.
- Added static checker coverage for optional focus touch handling.
- Guarded optional AVCapture connection input ports before scanning for the
  video capture connection.
- Added static checker coverage for camera input-port guards.
- Guarded app launch window, mask layer, and launch mask image setup instead of
  force-unwrapping optional startup state.
- Added static checker coverage for launch mask optional guards.
- Removed camera setup console logging and added static checker coverage.

## 2026-06-08

- Guarded saved image loading in the display flow and added a missing-photo
  fallback.
- Guarded camera capture failures, image conversion, and display navigation.
- Tightened docs-plan verification to require recorded `make check` evidence.
- Added a camera usage description to the app plist.
- Added dependency-free camera privacy and local-storage contract checks.
- Added local `make verify` and `make check` targets with an Xcode build fallback when `xcodebuild` is unavailable.
