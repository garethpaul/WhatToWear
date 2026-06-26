# Changes

## 2026-06-26 14:21 PDT - P1 - Gate camera resume on application activity

### Summary

Closed a launch-time lifecycle gap where camera view appearance could mark
capture eligible before `UIApplication` reached the active state.

### Work completed

- Defaulted camera lifecycle eligibility to disabled.
- Derived every resume attempt from the current application state before the
  existing visibility-aware session start path runs.
- Added one static lifecycle contract, one hostile mutation, and a completed
  implementation plan for the inactive-launch boundary.

### Threads

- None; the focused Swift, contract, mutation, and documentation work was
  completed directly.

### Files changed

- `What To Wear/ViewController.swift` — fail closed and gate resume on active
  application state.
- `scripts/check_whattowear_contracts.py` — enforce activity-derived resume.
- `scripts/test_whattowear_mutations.py` — reject unconditional resume.
- `README.md`, `VISION.md`, `AGENTS.md`,
  `docs/plans/2026-06-26-active-application-camera-resume.md` — document the
  privacy boundary and verification.

### Validation

- `python3 scripts/check_whattowear_contracts.py` — 30 contracts passed.
- `python3 scripts/test_whattowear_mutations.py` — 18 mutations rejected.
- `/usr/bin/make check` and external-directory Make verification — passed.
- Hosted verification — pending.
- Physical front-camera verification — not available in this Linux environment.

### Bugs / findings

- P1 fixed: `viewWillAppear` called an unconditional resume path, so initial
  view appearance could enable capture while the app was still inactive and
  before `applicationDidBecomeActive` established permission to run.

### Blockers

- Native launch/interruption timing still requires the existing physical-device
  checklist and a compatible Swift 2/Xcode environment.

### Next action

- Run the protected portable gate, hosted CI, and then verify cold-launch camera
  startup on a physical front-camera device.

## 2026-06-26 03:58 PDT - P1 - Apply the selected camera focus point

### Summary

Fixed the touch-focus flow so guarded touch locations now change the front
camera's autofocus point instead of being calculated and discarded.

### Work completed

- Converted full view touch coordinates through the preview layer into camera
  device coordinates.
- Applied the converted point and `.AutoFocus` only when both capabilities are
  supported, under the existing single successful configuration lock.
- Added five hostile focus mutations and a completed implementation plan.

### Threads

- None; the focused Swift and portable-contract work was completed directly.

### Files changed

- `What To Wear/ViewController.swift` — apply preview-mapped touch autofocus.
- `scripts/check_whattowear_contracts.py` — enforce conversion, support guards,
  assignment ordering, and completed-plan registration.
- `scripts/test_whattowear_mutations.py` — reject five focus regressions.
- `README.md`, `VISION.md`, `AGENTS.md`, `docs/plans/2026-06-26-touch-focus-point.md`
  — document behavior and verification.

### Validation

- `python3 scripts/check_whattowear_contracts.py` — 29 contracts passed.
- `python3 scripts/test_whattowear_mutations.py` — 17 mutations rejected.
- `/usr/bin/make check` and external-directory Make verification — passed.
- Physical front-camera verification — not available in this Linux environment.

### Bugs / findings

- P1 fixed: `focusTo` previously locked and unlocked the device without using
  the selected touch value or changing focus configuration.

### Blockers

- Native focus behavior still requires the existing physical-device checklist.

### Next action

- Verify tap and drag focus behavior on a physical front-camera device before
  attempting the larger camera API modernization roadmap item.

## 2026-06-21

- Isolated repository verification from caller-controlled Make startup files,
  shell state, execution modes, root overrides, and Python/Xcode expressions.
- Added adversarial Make authority coverage and pinned hosted verification to
  `/usr/bin/make` without changing camera behavior or native project settings.

## 2026-06-19

- Serialized camera session configuration, start, stop, focus, and still-image
  requests on one owned queue while keeping lifecycle and UI identity on the
  main queue and protected JPEG writes on a separate persistence queue.
- Added explicit camera authorization and front-camera availability handling,
  atomic session configuration, and a late-configuration guard that cannot
  undo an app or view pause.
- Added unique per-capture protected handoffs, exact capture identity, one-shot
  result presentation and dismissal, launch cleanup for abandoned handoffs,
  and direct JPEG persistence that preserves orientation metadata.
- Added 28 portable contracts and 12 hostile mutations covering camera queue,
  lifecycle, authorization, orientation, ownership, cleanup, and UI delivery.

## 2026-06-17

- Guarded camera configuration unlock behind successful legacy device-lock
  acquisition and added a portable ordering contract.

## 2026-06-16

- Added a native device verification guide for the legacy Swift toolchain,
  front-camera permission, repeated capture, interruption, retake, and local
  photo lifecycle boundaries.
- Added portable contracts that keep the device checklist and its explicit
  Linux/Xcode limitation documented.

## 2026-06-14

- Carried the originating capture generation through protected photo storage
  and revalidated it immediately before main-thread result presentation.
- Removed a saved photo instead of revealing stale capture work when camera
  visibility, session state, or generation changed during persistence.

## 2026-06-13

- Invalidated queued camera captures across pause-and-resume cycles with a
  lifecycle generation guard at both asynchronous capture boundaries.
- Rechecked camera visibility and session state before queued connection scans
  and again before asynchronous JPEG conversion and local persistence.
- Added a portable ordering contract for both stale capture lifecycle guards.

## 2026-06-12

- Disabled persisted checkout credentials and enforced the sole pinned
  credential-free workflow boundary.

## 2026-06-10

- Stopped active camera sessions and cancelled pending countdowns when the app
  becomes inactive or the capture view is covered, with visibility-aware
  restart guards and portable regression coverage.
- Added immutable, read-only GitHub Actions verification on Python 3.10, 3.12,
  and 3.14 for the portable privacy and camera-safety contracts, with manual
  dispatch for maintenance runs.
- Added static coverage for workflow permissions, action pins, matrix versions,
  timeout, and the `make check` command.
- Documented that hosted Linux checks intentionally skip legacy Xcode builds.
- Required complete iOS file protection before displaying a captured JPEG,
  removed the file on protection failure, and deleted the handoff after preview
  decoding.
- Pinned hosted verification to Ubuntu 24.04 with superseded-run cancellation
  and made Make targets independent of the caller's working directory. The
  Xcode scheme is now passed without literal path-escape backslashes.

## 2026-06-09

- Guarded mirrored preview construction when the saved capture has no
  `CGImage` backing and reused the missing-photo fallback.
- Added static checker coverage for display `CGImage` fallback behavior.
- Required successful local JPEG writes before navigating to the captured-photo
  display flow.
- Added static checker coverage for the photo write-success guard.
- Guarded countdown start so repeated snap taps cannot schedule overlapping
  capture timers.
- Added static checker coverage for duplicate countdown timer prevention.
- Guarded camera session output and input setup before adding them to the
  capture session.
- Added static checker coverage for capture session input and output guards.
- Guarded focus touch handlers before reading touch locations.
- Added static checker coverage for optional focus touch handling.
- Guarded optional AVCapture connection input ports before scanning for the
  video capture connection.
- Added static checker coverage for camera input-port guards.
- Guarded app launch window, mask layer, and launch mask image setup instead of
  force-unwrapping optional startup state.
- Added static checker coverage for launch mask optional guards.
- Removed camera setup console logging and added static checker coverage.

## 2026-06-08

- Guarded saved image loading in the display flow and added a missing-photo
  fallback.
- Guarded camera capture failures, image conversion, and display navigation.
- Tightened docs-plan verification to require recorded `make check` evidence.
- Added a camera usage description to the app plist.
- Added dependency-free camera privacy and local-storage contract checks.
- Added local `make verify` and `make check` targets with an Xcode build fallback when `xcodebuild` is unavailable.
