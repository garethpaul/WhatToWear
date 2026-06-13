# Camera Capture Generation Guard

Status: Planned

## Problem

The existing lifecycle checks reject queued and completed still-image work while
the camera is paused. After the app or view resumes, however, visibility and
session-running state become true again, so a callback created before the pause
can pass those checks and persist an obsolete photo.

## Requirements

1. Associate each queued capture with the current camera lifecycle generation.
2. Advance the generation whenever the capture session is paused so pre-pause
   queued work and completion callbacks remain invalid after a later resume.
3. Require both the generation and existing visibility/session conditions
   before connection discovery and before JPEG conversion or persistence.
4. Preserve countdown cancellation, protected atomic storage, ephemeral photo
   handoff, main-thread navigation, and all existing routes and assets.
5. Add portable ordering contracts and hostile mutations for missing,
   misplaced, or weakened generation checks.

## Verification

- Run the focused generation contract and hostile mutations.
- Run local and external-working-directory `make check` with explicit timeouts.
- Compile the Python checker, inspect the exact diff, and scan changed lines for
  credentials, artifacts, conflict markers, and whitespace errors.
- Record that `xcodebuild` and physical-device camera timing remain unavailable
  on this Linux host rather than claiming Apple platform validation.

## Scope Boundaries

- Do not modernize Swift syntax, replace deprecated AVFoundation APIs, alter
  signing/project settings, or redesign the capture flow.
- Do not merge or close any pull request without explicit owner authorization.
