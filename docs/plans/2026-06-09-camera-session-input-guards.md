# Camera Session Input Guards

## Status: Completed

## Context

The camera session setup force-unwrapped the still image output and directly
constructed and added an `AVCaptureDeviceInput` from the optional capture
device. If the output, device, or input is unavailable, the setup path can fail
before the capture flow reaches the existing callback guards.

## Objectives

- Preserve the legacy front-camera preview and countdown capture flow.
- Guard the still image output before configuring and adding it.
- Guard the optional capture device before creating a session input.
- Check `canAddInput` before adding the camera input to the capture session.

## Work Completed

- Replaced the `stillImageOutput!` setup with an `if let stillOutput` guard.
- Created the camera input from a guarded `cameraDevice`.
- Checked `captureSession.canAddInput(input)` before adding the input.
- Added static checker coverage and completed-plan coverage.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `python3 -m py_compile scripts/check_whattowear_contracts.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `make verify`
- `git diff --check`

On this workspace, the `make build`, `make check`, and `make verify` build
steps reported `Skipping xcodebuild: xcodebuild is not installed.`

## Follow-Up Candidates

- Add a user-visible error when no camera input can be created.
- Add simulator/device verification notes for camera-denied and no-camera
  paths.
