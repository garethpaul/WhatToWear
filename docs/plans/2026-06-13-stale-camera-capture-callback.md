# Stale Camera Capture Callback Guard

Status: In Progress

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

- Run the focused stale-capture lifecycle contract.
- Run the complete portable `make check` gate locally and from an external
  working directory.
- Reject hostile mutations for either guard, inverted state, late ordering,
  missing session checks, and stale plan status.
- Run Python compilation and `git diff --check`.
- Record Xcode availability without claiming device behavior on Linux.
