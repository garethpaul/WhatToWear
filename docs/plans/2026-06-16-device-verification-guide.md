# Device Verification Guide

## Status: Planned

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
