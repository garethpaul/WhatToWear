# Final Capture Reveal Generation Guard

## Status: Planned

## Context

The still-image callback verifies camera visibility, session state, and capture
generation before starting JPEG persistence. The successful save path then
queues its result segue on the main thread without repeating that lifecycle
check. If the camera view disappears or its generation changes during image
conversion, file protection, or main-queue scheduling, stale work can still
present the result screen and leave a capture file behind.

## Requirements

- Carry the queued capture generation through the photo persistence path.
- Recheck generation, visibility, and session-running state immediately before
  presenting the saved photo.
- Delete the saved photo instead of presenting it when that final check fails.
- Preserve protected atomic storage, successful main-thread presentation,
  countdown behavior, and existing camera callback guards.
- Add mutation-sensitive portable contracts for the generation handoff, final
  reveal ordering, stale-file cleanup, and completed plan evidence.

## Verification Plan

- Run the focused final-reveal contract and isolated hostile mutations.
- Run bounded local, external-directory, and hostile-root `make check` gates.
- Compile the checker and audit the exact diff, generated artifacts, structured
  project files, whitespace, and changed lines for credential material.
- Record the unavailable Xcode/device validation boundary truthfully.

## Scope Boundaries

- Do not modernize Swift syntax, AVFoundation APIs, project settings, or the
  existing protected-photo format.
- Do not merge or close stacked pull requests without explicit authorization.
