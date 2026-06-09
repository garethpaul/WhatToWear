# Launch Mask Guards

## Status: Completed

## Context

The camera and display paths were guarded, but app launch still force-unwrapped
the `window`, splash mask layer, and `whatToWearWhite` image asset. A missing
asset or unexpected nil optional should not crash the sample before the camera
flow is visible.

## Objectives

- Preserve the animated launch mask when the expected asset exists.
- Guard the optional `window` before configuring root view and launch UI.
- Guard the optional mask layer before assigning properties or animating.
- Guard the launch mask image asset before reading its `CGImage`.
- Keep static checks covering app-launch optional guards.

## Work Completed

- Wrapped launch setup in `if let window = self.window`.
- Guarded the mask layer and `whatToWearWhite` image before assigning mask
  contents.
- Updated `animateMask` to return safely when no mask layer is available.
- Added static checker coverage for window, mask layer, and mask image guards.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Guard camera input creation before adding it to the capture session.
- Stop the capture session when the camera view disappears.
