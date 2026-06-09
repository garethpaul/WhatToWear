# Camera Capture Guards Plan

Date: 2026-06-08

Status: Completed

## Goal

Make the legacy camera capture callback tolerate failed captures and invalid
image conversion without crashing or triggering navigation from a background
callback.

## Scope

- Ignore capture callbacks that include an error or nil sample buffer.
- Guard JPEG data creation before saving a photo.
- Guard `UIImage` decoding and JPEG encoding before writing to local storage.
- Dispatch the display-image segue back to the main queue.
- Add dependency-free static checks for the capture and save guards.

## TDD Notes

- Red: `python3 scripts/check_whattowear_contracts.py` failed with
  `AssertionError: capture callback must ignore errors and nil sample buffers`.
- Green: `python3 scripts/check_whattowear_contracts.py` passed after adding
  capture callback, image conversion, and main-queue segue guards.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `git diff --check`
