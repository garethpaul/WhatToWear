# Device Verification Guide

## Status: Completed

## Context

The README names Xcode and a compatible Apple toolchain, but it does not give a
maintainer a repeatable device checklist for this Swift 2-era front-camera
sample. The hosted Linux gate can prove portable source contracts only, so the
remaining native boundary must state exactly what to inspect on a compatible
macOS/Xcode host and physical device without implying that simulator camera
behavior has been validated.

## Requirements

- Document the legacy toolchain and signing assumptions before opening the
  project.
- Distinguish portable `make check` verification from native Xcode and device
  validation.
- Add a physical-device checklist for camera permission, repeated snap taps,
  background or covered-view cancellation, result display, retake, and local
  photo deletion.
- Document the denied-permission and unavailable-front-camera boundaries
  without claiming UI behavior the legacy sample does not implement.
- Add mutation-sensitive portable contracts that keep the guide, its privacy
  lifecycle, and completed plan evidence present.

## Verification Plan

- Run the focused documentation contracts and isolated hostile mutations.
- Run bounded local and external-directory `make check` gates.
- Audit the exact diff, generated artifacts, whitespace, file modes, and
  changed lines for credential material.
- Record the unavailable Xcode/device validation boundary truthfully.

## Scope Boundaries

- Do not modernize Swift syntax, AVFoundation APIs, project settings, signing,
  or the capture UI.
- Do not claim simulator or physical-device results from the Linux host.
- Do not merge or close stacked pull requests without explicit authorization.

## Work Completed

- Added legacy Swift and Xcode compatibility guidance without changing project
  settings or claiming a supported modern toolchain.
- Added a physical-device checklist for permission, repeated taps,
  interruptions, successful preview, retake, and denied-permission behavior.
- Documented the protected temporary JPEG lifecycle and absence of upload or
  sharing behavior.
- Added a portable, whitespace-tolerant documentation contract and completed
  plan assertion.

## Verification Results

- The focused device-guide contract passed after the README update.
- Eight isolated hostile mutations were rejected: missing native-device
  heading, toolchain boundary, denied-permission caveat, interruption check,
  protected JPEG lifecycle, no-upload guarantee, completed status, and
  `make check` evidence.
- Repository and external-directory `make check` gates each passed all 20
  portable contracts with paths rooted to this worktree.
- `xcodebuild` is unavailable on this Linux host; no simulator, physical-device,
  signing, or native compilation result is claimed.
