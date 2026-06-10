# Hosted Static Verification

Status: completed

## Goal

Run the repository's portable privacy and camera-safety contracts on every push
and pull request without pretending that a Linux runner can validate the
legacy iOS binary.

## Changes

- Add a read-only GitHub Actions workflow for Python 3.10, 3.12, and 3.14.
- Support manual dispatch for maintenance verification.
- Pin all third-party actions to immutable revisions.
- Run the existing `make check` gate, which executes static contracts and
  explicitly reports that Xcode compilation is unavailable on Linux.
- Extend the static checker to protect workflow permissions, matrix coverage,
  immutable action pins, and the verification command.

## Verification

- `python3 -m py_compile scripts/check_whattowear_contracts.py`
- `make check`

## Follow-up Boundary

The application source predates modern Swift and AVFoundation APIs. A macOS
build job should follow a dedicated Swift migration with a shared scheme and
simulator tests; the portable workflow intentionally does not claim that the
legacy Xcode project compiles on a current toolchain.
