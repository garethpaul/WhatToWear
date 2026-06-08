# Camera Privacy Contract Plan

Date: 2026-06-08

status: completed

## Goal

Make the camera permission and local photo-storage behavior explicit for the legacy WhatToWear app.

## Scope

- Add `NSCameraUsageDescription` to the app `Info.plist`.
- Add a dependency-free contract that checks the camera purpose string.
- Keep the capture flow local to the app documents directory and guard against hidden upload behavior.
- Add local verification targets that work even when Xcode is unavailable.

## TDD Notes

- Red: `python3 scripts/check_whattowear_contracts.py` failed with `AssertionError: app Info.plist must declare NSCameraUsageDescription`.
- Green: `python3 scripts/check_whattowear_contracts.py` passed after adding the camera usage description.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
- Xcode build is skipped in this environment because `xcodebuild` is not installed.
