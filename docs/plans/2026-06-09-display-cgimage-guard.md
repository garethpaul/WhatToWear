# Display CGImage Guard

Status: Completed

## Context

The display flow already guarded loading the saved local capture file before
showing it. It still passed `image.CGImage` directly into the mirrored preview
constructor. If UIKit produced an image without a `CGImage` backing, the display
path could fail instead of showing the existing missing-photo fallback.

## Plan

- Guard `image.CGImage` before constructing the mirrored preview image.
- Reuse one missing-photo fallback for both load failures and missing `CGImage`
  backing.
- Extend `scripts/check_whattowear_contracts.py` so future edits keep the
  display fallback for both failure modes.

## Verification

- `python3 scripts/check_whattowear_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

On this non-macOS host, `make verify` runs the static checks and skips Xcode
because `xcodebuild` is unavailable.
