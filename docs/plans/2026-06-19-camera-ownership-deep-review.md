---
status: completed
date: 2026-06-19
---

# Camera ownership deep review

## Scope

Review the stacked maintenance changes in PRs #2 through #9 and reconcile the
parallel PR #1 baseline. Follow camera work from authorization and device
selection through session configuration, countdown, still capture, protected
file handoff, result presentation, dismissal, interruption, and resume.

## Findings

- Capture generation and visibility were read from arbitrary callback queues.
- Session configuration and blocking start/stop calls had no single queue owner.
- Generation-only stale guards shared one filename, so an old failure cleanup
  could remove or overwrite a newer capture.
- Repeated input could begin new work while capture or reveal callbacks were
  still active.
- Camera permission and missing front-camera states were not handled explicitly.
- Decode/re-encode and forced `CGImage` reconstruction increased peak memory and
  discarded the still image output's orientation metadata.
- Camera setup completing after a lifecycle pause could restart the session.
- A crash could leave an otherwise ephemeral capture handoff on disk.

## Design

- Main-queue state owns visibility, lifecycle generation, active capture ID,
  pending handoff, and one-shot result UI reservations.
- A dedicated serial queue owns session configuration, start/stop, focus locks,
  and still-image requests. A separate serial persistence queue prevents JPEG
  writes from delaying camera interruption.
- Every capture writes a unique protected JPEG path and only that capture may
  reveal or remove it.
- Capture connection orientation and mirroring preserve encoded metadata without
  rebuilding image pixels.
- Launch removes only `what_to_wear_*.jpg` abandoned handoffs.

## Verification

- RED-first portable contracts reproduce each ownership and lifecycle defect.
- `python3 scripts/check_whattowear_contracts.py`
- `python3 scripts/test_whattowear_mutations.py`
- `make XCODEBUILD=whattowear-no-xcode check`
- Hosted Linux validation runs the repository's exact `make check` gate.
- External-directory Make invocation with the absolute Makefile path.
- `plutil`, Python compilation, workflow parsing, diff hygiene, and hosted gates.
- Modern Xcode project/build probing is recorded separately because the project
  requires missing CocoaPods support files, targets iOS 8.1, and has no supported
  `SWIFT_VERSION` for Xcode 26.

## Native risk

Physical front-camera capture, permission prompts, interruption timing, image
orientation, memory pressure, protected-file behavior, and repeated UI input
still require a compatible historical Swift/Xcode toolchain and an iOS device.
