# Camera Input Port Guards

## Status: Completed

## Context

The countdown capture path scanned `AVCaptureConnection` input ports with a
force unwrap. If a connection does not expose input ports, the capture flow can
crash before it reaches the existing sample-buffer and JPEG guards.

## Objectives

- Preserve the countdown-to-photo capture flow.
- Continue selecting the video capture connection when available.
- Skip connections that do not expose input ports.
- Keep the saved-photo and display navigation guards unchanged.

## Work Completed

- Replaced the `connection.inputPorts!` force unwrap with an `if let` guard.
- Iterated only the guarded input-port collection when searching for video.
- Added static checker coverage for camera input-port guards.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Guard camera input creation with `canAddInput`.
- Add a user-visible error when no camera video connection is available.
