# Active Application Camera Resume Plan

Status: Completed

**Goal:** Prevent the camera session from becoming eligible before the iOS
application reaches the active state.

**Architecture:** Keep the existing view visibility and serial camera queue
ownership. Make lifecycle eligibility fail closed, derive it synchronously from
`UIApplication.applicationState` on every resume event, and let the existing
visibility-aware start helper enforce the combined state.

**Tech Stack:** Swift 2, UIKit, AVFoundation, Python static contracts and hostile
mutations.

## Implementation

1. Added a failing contract proving that lifecycle eligibility defaulted open
   and `viewWillAppear` could unconditionally enable capture.
2. Defaulted `captureLifecycleEnabled` to `false`.
3. Changed `resumeCaptureSession()` to record whether `UIApplication` is
   currently active before calling `startCaptureSessionIfEligible()`.
4. Added a hostile mutation that replaces the application-state comparison with
   `true` and must be rejected by the contract suite.
5. Updated public lifecycle and verification documentation.

## Verification Completed

- The RED contract failed on the prior open default before Swift changed.
- `python3 scripts/check_whattowear_contracts.py` passed 30 contracts.
- `python3 scripts/test_whattowear_mutations.py` rejected 18 mutations.
- `/usr/bin/make check` passed the protected repository verification authority.
- Native cold-launch and interruption timing remains assigned to the physical
  device checklist because this Linux environment cannot run the Swift 2 app.
