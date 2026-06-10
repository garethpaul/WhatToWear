## WhatToWear Vision

WhatToWear is a legacy iOS camera app that starts a countdown, captures a front
camera photo, saves it locally, and moves to a display flow.

The repository is useful as a small AVCapture and countdown prototype for a
camera-driven outfit or style app.

The goal is to preserve the camera prototype while making privacy, storage, and
Swift/iOS legacy assumptions explicit.

The current focus is:

Priority:

- Preserve the countdown-to-photo capture flow
- Keep captured images local to the app documents directory
- Only display captured photos after a successful local write
- Make camera permission and storage behavior explicit
- Guard optional camera connection data before capture
- Guard camera session inputs and outputs before adding them
- Guard optional focus touch data before moving camera focus
- Prevent repeated snap taps from starting overlapping countdown timers
- Avoid console logging camera discovery or setup state
- Show a fallback if the saved local capture cannot be displayed
- Show the same fallback if the saved image cannot be mirrored for preview
- Avoid force-unwrapping app-launch mask assets and optional startup state
- Treat Swift and AVFoundation APIs as legacy until documented
- Keep portable privacy and camera-safety contracts running in hosted CI

Next priorities:

- Add README setup and privacy notes
- Add controls for retake, delete, and image lifecycle
- Modernize camera APIs in a dedicated compatibility pass
- Add simulator/device verification notes

Contribution rules:

- One PR = one focused camera, timer, storage, UI, or documentation change.
- Do not commit user photos.
- Keep uploads and sharing out unless explicitly designed.
- Include device notes for camera behavior changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Photos can be highly sensitive. The app should keep captures local by default,
avoid hidden uploads, avoid console logging camera setup state, and make
deletion or retention behavior clear.

## What We Will Not Merge (For Now)

- Silent image upload or sharing
- Real user photos in fixtures
- Hidden analytics
- Storage changes without privacy notes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
