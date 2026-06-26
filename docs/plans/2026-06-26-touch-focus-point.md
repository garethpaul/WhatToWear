# Touch Focus Point Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make camera touch gestures apply the selected preview point to the front camera's autofocus configuration.

**Architecture:** Keep touch handling and preview-coordinate conversion on the main thread, where the view and preview layer are owned. Pass the converted device point to the serial camera queue, acquire the existing configuration lock once, and update focus only when both point-of-interest and autofocus modes are supported.

**Tech Stack:** Swift 2, UIKit, AVFoundation, Python static contracts and hostile mutations.

---

### Task 1: Add the failing focus contract

**Files:**
- Modify: `scripts/check_whattowear_contracts.py`
- Modify: `scripts/test_whattowear_mutations.py`

**Step 1: Write the failing contract**

Require the source to convert the touch through `previewLayer.captureDevicePointOfInterestForPoint`, pass the resulting point into `focusTo`, guard both `focusPointOfInterestSupported` and `.AutoFocus`, and assign `focusPointOfInterest` before `focusMode` under the existing successful lock.

**Step 2: Verify RED**

Run: `python3 scripts/check_whattowear_contracts.py`
Expected: FAIL because `focusTo` currently ignores its value and never sets a camera focus point.

### Task 2: Apply guarded touch focus

**Files:**
- Modify: `What To Wear/ViewController.swift`

**Step 1: Convert touch coordinates**

Add a helper that guards `previewLayer`, converts `touch.locationInView(view)` with `captureDevicePointOfInterestForPoint`, and passes the device point to `focusTo` from both touch handlers.

**Step 2: Configure autofocus minimally**

Change `focusTo` to accept `CGPoint`. On `captureQueue`, retain the single successful configuration-lock guard, require point-of-interest and autofocus support, assign the point, set `.AutoFocus`, and then unlock.

**Step 3: Verify GREEN**

Run: `python3 scripts/check_whattowear_contracts.py`
Expected: PASS.

### Task 3: Protect against regression

**Files:**
- Modify: `scripts/test_whattowear_mutations.py`

**Step 1: Add hostile mutations**

Reject removal of preview conversion, point assignment, point support, autofocus support, and autofocus mode assignment.

**Step 2: Run mutation tests**

Run: `python3 scripts/test_whattowear_mutations.py`
Expected: PASS with all focus mutations rejected.

### Task 4: Reconcile public documentation

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `AGENTS.md`

Document that touch focus now maps preview coordinates and applies autofocus only on supported camera devices. Record the P1 bug, validation evidence, lack of physical-device execution in this environment, and the next device verification action.

### Task 5: Run complete verification

Run:
- `python3 scripts/check_whattowear_contracts.py`
- `python3 scripts/test_whattowear_mutations.py`
- `/usr/bin/make check`
- `/usr/bin/make -f /tmp/code/WhatToWear/Makefile check` from an external directory
- `git diff --check`

Expected: all portable checks pass; Xcode/device execution is reported honestly if unavailable.

## Verification Completed

- The RED contract failed because both touch handlers bypassed preview
  conversion and `focusTo` never assigned a camera focus point or mode.
- `python3 scripts/check_whattowear_contracts.py` passed 29 contracts.
- `python3 scripts/test_whattowear_mutations.py` rejected 17 mutations,
  including five touch-focus regressions.
- `/usr/bin/make check` and the external-directory Make gate passed; Xcode and
  physical front-camera behavior remain covered by the documented native
  device checklist rather than this Linux environment.
