# Hosted Static Verification

Status: completed

## Goal

Run the repository's portable privacy and camera-safety contracts on every push
and pull request without pretending that a Linux runner can validate the
legacy iOS binary.

## Changes

- Add a read-only GitHub Actions workflow for Python 3.10 and 3.12.
- Pin all third-party actions to immutable revisions.
- Run the existing `make check` gate, which executes static contracts and
  explicitly reports that Xcode compilation is unavailable on Linux.
- Extend the static checker to protect workflow permissions, matrix coverage,
  immutable action pins, and the verification command.

## Verification

- `python3 -m py_compile scripts/check_whattowear_contracts.py`
- `make check`
