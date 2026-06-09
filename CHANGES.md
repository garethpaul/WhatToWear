# Changes

## 2026-06-08

- Guarded saved image loading in the display flow and added a missing-photo
  fallback.
- Guarded camera capture failures, image conversion, and display navigation.
- Tightened docs-plan verification to require recorded `make check` evidence.
- Added a camera usage description to the app plist.
- Added dependency-free camera privacy and local-storage contract checks.
- Added local `make verify` and `make check` targets with an Xcode build fallback when `xcodebuild` is unavailable.
