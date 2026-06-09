# Countdown Timer Guard

## Status: Completed

## Context

The camera view starts a one-second repeating `NSTimer` each time the snap
button calls `startSnap()`. Repeated taps during an active countdown can create
overlapping timers, causing duplicate countdown updates and multiple capture
attempts from a single user action.

## Objectives

- Preserve the legacy countdown-to-photo flow.
- Ignore duplicate snap starts while the countdown timer is already valid.
- Keep one timer scheduling path for the capture countdown.
- Cover the behavior with `make check`.

## Work Completed

- Added an early return in `startSnap()` when the countdown timer is already
  valid.
- Preserved the existing timer interval, start-time recording, and capture
  callback flow.
- Extended `scripts/check_whattowear_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- Pre-change inspection found no guard before
  `NSTimer.scheduledTimerWithTimeInterval`.
- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Disable or visually mark the snap button while countdown is active.
- Add device verification notes for repeated tap behavior.
