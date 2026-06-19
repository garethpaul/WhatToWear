# Camera Configuration Lock Guard

## Status: Completed

## Context

`ViewController.configureDevice()` calls `unlockForConfiguration()` even when
the preceding legacy `lockForConfiguration(nil)` call fails. The same Swift
2-era controller already checks the Boolean lock result in `focusTo`, so the
unconditional unlock is both inconsistent and unsafe on unavailable or
interrupted camera devices.

## Priority

P1 camera lifecycle correctness. Never unlock an `AVCaptureDevice` unless this
call site successfully acquired its configuration lock.

## Requirements

- Guard configuration work with the existing Swift 2-compatible Boolean
  `lockForConfiguration(nil)` pattern.
- Call `unlockForConfiguration()` only inside the successful lock branch.
- Preserve current camera selection, session startup, focus behavior, capture
  generation, photo lifecycle, and UI behavior.
- Add a registered static contract that proves lock-before-unlock ordering and
  rejects unconditional or inverted locking.
- Keep documentation and completed verification evidence aligned without
  claiming native compilation or camera execution on Linux.

## Implementation Units

### U1. Guard device configuration ownership

**Files:** `What To Wear/ViewController.swift`

Wrap the existing `configureDevice()` configuration block in the checked lock
pattern already used by `focusTo`. Keep the commented focus assignment and all
session setup behavior otherwise unchanged.

**Verification:** The focused contract rejects missing, unconditional,
inverted, or post-unlock lock checks.

### U2. Enforce and document the boundary

**Files:** `scripts/check_whattowear_contracts.py`, `README.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-17-camera-configuration-lock-guard.md`

Register a portable contract for successful lock ownership and update
maintenance guidance to record the fail-closed behavior and native validation
limit.

**Verification:** Repository-root and external-directory gates pass, hostile
mutations are rejected, and exact diff/artifact/credential audits remain clean.

## Scope Boundaries

- Do not modernize Swift syntax, AVFoundation APIs, project settings, signing,
  capture UI, or focus behavior.
- Do not add a speculative error UI for a failed configuration lock.
- Do not claim Xcode compilation, simulator behavior, or physical-camera
  execution from this Linux host.
- Do not merge or close stacked pull requests without explicit authorization.

## Verification Plan

- Run the focused static contract and isolated hostile mutations.
- Run `make check` from the repository and through the absolute Makefile path
  from an external directory.
- Audit generated artifacts, untracked files, whitespace, file modes, changed
  lines for credentials, and exact staged paths.
- Push without force, open a stacked pull request against
  `lfg/whattowear-device-verification-guide-20260616`, and capture one bounded
  exact-head hosted/security snapshot.

## Verification Results

- The focused camera-configuration contract passed with the existing Swift
  2-compatible checked-lock pattern.
- Five isolated hostile mutations were rejected: unconditional unlock,
  inverted lock success, unlock moved outside the success branch, contract
  deregistration, and README plan unindexing.
- Repository-root and external-directory `make check` passed all 21 portable
  contracts; `xcodebuild` remained unavailable and was truthfully skipped.
- Exact diff, generated-artifact, untracked-file, whitespace, file-mode,
  credential-pattern, staged-path, and upstream audits are completed before
  shipping.
