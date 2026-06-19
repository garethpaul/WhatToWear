# WhatToWear

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Device Preview

<!-- DEVICE-PREVIEW-IMAGE -->
![Device preview](docs/device-preview.svg)

## Overview

`garethpaul/WhatToWear` is an Apple platform application or Objective-C/Swift sample. Sample App What To Wear

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (6), C/C++ headers (1).

## Repository Contents

- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails
- `What To Wear` - source or example code
- `What To Wear.xcodeproj` - Xcode project file
- `What To WearTests` - source or example code

Additional scan context:

- Source directories: What To Wear, What To WearTests
- Dependency and build manifests: none detected
- Entry points or build surfaces: What To Wear.xcodeproj
- Test-looking files: What To WearTests/Info.plist, What To WearTests/What_To_WearTests.swift

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects

### Setup

```bash
git clone https://github.com/garethpaul/WhatToWear.git
cd WhatToWear
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `What To Wear.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.

## Testing and Verification

- `make verify` runs static camera privacy, local-storage, capture identity,
  authorization, serial session ownership, orientation, display, photo
  write-success, capture input-port, camera configuration locking, lifecycle,
  cleanup, app-launch mask, focus touch, countdown timer, and camera console
  logging checks. It also runs 12 hostile mutations, verifies complete file
  protection and post-preview deletion for each capture-owned JPEG handoff,
  then attempts an Xcode build when `xcodebuild` is available.
- `make check` runs `make verify` with bytecode cleanup before and after.
- `python3 scripts/check_whattowear_contracts.py` runs the static
  WhatToWear contracts without the optional Xcode build.
- `python3 scripts/test_whattowear_mutations.py` proves that queue, lifecycle,
  authorization, orientation, capture identity, cleanup, and one-shot UI
  regressions fail the portable contract suite.
- GitHub Actions runs the portable `make check` gate on Python 3.10, 3.12, and
  3.14 using fixed Ubuntu 24.04 runners, read-only permissions, per-branch
  concurrency cancellation, and manual dispatch. Linux jobs intentionally skip
  Xcode compilation until the Swift 2-era project is migrated. Checkout
  credentials are not persisted after source retrieval.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- Camera lifecycle contracts require pending countdowns and active capture
  sessions to stop when the app becomes inactive or the camera view is covered.
  One serial queue owns session configuration and blocking start/stop work;
  protected JPEG persistence uses another serial queue so disk I/O cannot delay
  camera interruption. Main-queue capture IDs and generations reject stale
  completions. Late camera setup cannot re-enable a paused lifecycle, and every
  failure removes only its capture-owned handoff.
- Camera permission and front-camera availability are checked before session
  setup. The snap control stays disabled and the app reports `Camera
  unavailable` when capture cannot be configured.
- Captured JPEG bytes are written directly to a unique protected path. Portrait
  orientation and front-camera mirroring are requested on the capture
  connection, avoiding a decode/re-encode memory spike and preserving image
  metadata for display.
- Camera configuration is released only after the legacy
  `lockForConfiguration(nil)` call reports success; failed lock acquisition
  leaves the device untouched.
- Xcode's test action or `xcodebuild test` can be used with the appropriate scheme and destination on a macOS/Xcode workstation.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Native Device Verification

This project contains Swift 2-era source and legacy AVFoundation APIs. Use a
macOS/Xcode combination that can open the project without silently migrating
its Swift syntax or project settings. Select a development team locally when
signing is required; do not commit signing identities or provisioning data.

Run `make check` before opening Xcode. That portable gate verifies the camera,
privacy, lifecycle, workflow, and documentation contracts but does not compile
the app on Linux. Native camera behavior requires a physical iOS device with a
front camera. The iOS Simulator does not provide equivalent capture evidence.

The app uses the countdown label for its legacy `Camera unavailable` fallback;
it does not link directly to Settings or distinguish denial, restriction,
missing hardware, and configuration failure. Record the exact cause during
device verification rather than treating the fallback as complete diagnosis.

On a compatible physical device:

1. Install and launch the app, grant camera permission, and confirm the live
   front-camera preview appears.
2. Tap the snap button repeatedly and confirm only one countdown and capture
   sequence starts.
3. Background the app or cover the camera screen before the countdown or
   capture completes, then return and confirm no stale result is shown.
4. Complete a capture and confirm the portrait, mirrored result preview appears
   only after the countdown and successful local write.
5. Tap close repeatedly and confirm one dismissal returns to the camera for a
   retake without redisplaying the prior capture.
6. Interrupt the app while its first camera setup is still pending and confirm
   the late setup completion does not restart capture until the app resumes.
7. Repeat with camera permission denied and, if available, without a front
   camera; confirm the snap control stays disabled and `Camera unavailable`
   appears.

The temporary JPEG uses complete file protection, remains in the app documents
directory only long enough to hand the capture to the result controller, and
is removed after decode or rejected stale work. Launch also removes abandoned
`what_to_wear_*.jpg` handoffs from a prior crash. The app has no upload or
sharing path. Device inspection should confirm no capture handoff remains after
the result screen loads or the app relaunches.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- Camera access uses `NSCameraUsageDescription` to explain that the app captures a local outfit photo for preview.
- The captured JPEG must receive complete iOS file protection before preview
  and is removed from disk after the display controller decodes it.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include What To Wear/ViewController.swift.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include What To Wear/Info.plist, What To WearTests/Info.plist.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include What To Wear/DisplayImage.swift, What To Wear/ViewController.swift.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include What To Wear/DisplayImage.swift, What To Wear/Info.plist, What To Wear/ViewController.swift, What To WearTests/Info.plist.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-camera-privacy-contract.md` for the current
  camera privacy baseline.
- See `docs/plans/2026-06-08-camera-capture-guards.md` for the camera capture
  failure and image-conversion guard contract.
- See `docs/plans/2026-06-09-photo-write-success-guard.md` for only showing
  the display flow after the local JPEG write succeeds.
- See `docs/plans/2026-06-08-display-image-load-guard.md` for saved capture
  display fallback behavior.
- See `docs/plans/2026-06-09-display-cgimage-guard.md` for guarding mirrored
  preview construction when a saved image has no `CGImage` backing.
- See `docs/plans/2026-06-09-launch-mask-guards.md` for app-launch mask asset
  and optional-state guards.
- See `docs/plans/2026-06-09-camera-input-port-guards.md` for optional
  AVCapture connection input-port guard coverage.
- See `docs/plans/2026-06-09-camera-session-input-guards.md` for guarded
  capture session input and output setup.
- See `docs/plans/2026-06-09-focus-touch-guards.md` for guarded touch handling
  in the camera focus controls.
- See `docs/plans/2026-06-09-countdown-timer-guard.md` for duplicate countdown
  timer prevention.
- See `docs/plans/2026-06-09-camera-console-log-guard.md` for camera setup
  console logging prevention.
- See `docs/plans/2026-06-10-hosted-static-verification.md` for the pinned,
  least-privilege hosted contract baseline.
- See `docs/plans/2026-06-10-protected-photo-lifecycle.md` for complete file
  protection, ephemeral preview handoff, and root-independent verification.
- See `docs/plans/2026-06-10-camera-session-lifecycle.md` for interruption,
  countdown cancellation, and camera visibility controls.
- See `docs/plans/2026-06-13-stale-camera-capture-callback.md` for rejecting
  queued capture work after camera lifecycle changes.
- See `docs/plans/2026-06-13-camera-capture-generation-guard.md` for keeping
  pre-pause callbacks invalid after the camera resumes.
- See `docs/plans/2026-06-14-final-capture-reveal-generation-guard.md` for the
  final main-thread lifecycle check before displaying a saved photo.
- See `docs/plans/2026-06-16-device-verification-guide.md` for the native
  front-camera, interruption, retake, and privacy verification checklist.
- See `docs/plans/2026-06-17-camera-configuration-lock-guard.md` for checked
  legacy camera configuration lock ownership.
- See `docs/plans/2026-06-19-camera-ownership-deep-review.md` for the serial
  session queue, capture identity, unique handoff, orientation, cleanup, and
  exactly-once UI review.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
