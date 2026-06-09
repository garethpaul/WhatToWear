# Display Image Load Guard

## Status: Completed

## Context

The display flow loaded `what_to_wear.jpg` from the app documents directory and
force-unwrapped the image before mirroring it. If the saved capture was missing
or corrupt, the app could crash while showing the result screen.

## Objectives

- Preserve local-only image loading from the app documents directory.
- Avoid force-unwrapping the saved image.
- Show a visible fallback when no local capture is available.
- Keep the behavior covered by `make check`.

## Work Completed

- Guarded `UIImage(contentsOfFile:)` in `DisplayImage.swift`.
- Preserved mirrored display for valid saved captures.
- Added fallback copy and hid suggested colors when the capture is unavailable.
- Extended `scripts/check_whattowear_contracts.py` and docs.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add a retake flow when no saved image exists.
- Add explicit deletion controls for the local capture.
