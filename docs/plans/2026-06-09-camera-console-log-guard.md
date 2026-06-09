# Camera Console Log Guard

## Status: Completed

## Context

The camera flow wrote device discovery and setup error state to stdout with
`println`. Camera availability and capture setup are local privacy-sensitive
state, and this sample does not need console logging for the happy path or setup
failure path.

## Objectives

- Preserve camera discovery, session setup, and guarded input behavior.
- Remove camera setup console logging from `ViewController.swift`.
- Keep setup errors local without formatting them for stdout.
- Cover the guard with `make check`.

## Work Completed

- Removed the camera discovery `println` before `beginSession()`.
- Removed the setup error `println` and kept input addition behind the existing
  `err == nil`, non-nil input, and `canAddInput` checks.
- Extended `scripts/check_whattowear_contracts.py`.
- Updated README, VISION, SECURITY, and CHANGES.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Surface setup failure through explicit UI state if the sample gains a retake
  or troubleshooting screen.
