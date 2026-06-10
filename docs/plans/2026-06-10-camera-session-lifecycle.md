# Camera Session Lifecycle

Status: Completed

## Goal

Prevent the legacy camera session or countdown from continuing when the user
cannot see the capture screen.

## Scope

- Track whether the camera controller is visible.
- Cancel and hide an in-progress countdown when the view is covered or the app
  becomes inactive.
- Stop a running AVFoundation capture session during those transitions.
- Resume only when the camera view is visible, a capture device exists, and the
  session is currently stopped.
- Enforce the view and application lifecycle wiring in portable contracts.

## Verification

- `make check`
- Mutation check: removing the capture-session stop call causes the contract
  checker to fail.
- Xcode build skipped locally because `xcodebuild` is unavailable; hosted
  Linux verification intentionally exercises the portable contracts.

## Outcome

Phone interruptions, backgrounding, and the full-screen photo preview no longer
leave the camera or a pending countdown active. Returning to the visible camera
screen restarts an eligible session without duplicating it.
