# Stale Camera Capture Callback Guard

Status: Completed

## Problem

The countdown queues still-image work on a background queue. If the camera view
is covered or the app resigns active after that work is queued, the current
closure can continue into capture and persist an image after the session has
been paused.

## Plan

1. Require the camera view to remain visible and the capture session to remain
   running before queued capture work scans connections.
2. Recheck the same lifecycle state in the asynchronous still-image completion
   before JPEG conversion and local persistence.
3. Preserve timer cancellation, file protection, ephemeral handoff cleanup,
   and main-thread segue behavior.
4. Add portable ordering contracts and hostile mutation coverage.
5. Document that physical-device timing still requires Apple hardware.

## Verification

- The focused stale-capture lifecycle contract passed.
- Local and external-directory `make check` passed all 17 portable contracts.
- Six hostile mutations were rejected: either lifecycle guard removed,
  inverted visibility, missing session state, JPEG conversion ordered before
  the completion guard, and stale plan status.
- Python compilation and `git diff --check` passed.
- `xcodebuild` is unavailable on this Linux host, so no simulator or physical
  device behavior is claimed.
