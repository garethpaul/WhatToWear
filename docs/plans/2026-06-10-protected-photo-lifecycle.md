# Protected Photo Lifecycle

Status: Completed

## Context

The camera flow used a fixed JPEG in the app documents directory to hand a
capture to the display controller. The file was local, but it did not require
iOS complete file protection and remained on disk after the preview loaded.

## Changes

- Require `NSFileProtectionComplete` before navigating to the display flow.
- Remove the JPEG if file protection cannot be applied.
- Remove the local handoff file after the display controller decodes it.
- Pin hosted verification to Ubuntu 24.04 with superseded-run cancellation.
- Make repository verification independent of the caller's working directory.
- Pass the legacy Xcode scheme to `xcodebuild` without literal backslashes.

## Verification

- `make check`
- Root-independent `make test`
- Mutation checks for file protection, cleanup ordering, CI, and Make paths
- `git diff --check`
