# Protect the Make Repository Root from Overrides

## Status: Completed

## Context

The Makefile-derived root anchors camera/privacy contracts, cleanup, and
optional Xcode builds, but an ordinary assignment can be replaced from the
command line.

## Requirements

- Protect the Makefile-derived root with GNU Make's `override` directive.
- Preserve configurable Python and Xcode commands.
- Require exact protected root and tool override lines in the checker.
- Pass local, external-directory, and hostile-root full gates.
- Reject root, checker, tool override, cleanup, and plan regressions.
- Preserve camera lifecycle, storage, privacy, workflow, and project behavior.

## Verification Plan

- focused Makefile contract and Python compilation
- bounded local, external-directory, and hostile-root `make check`
- focused mutations and structured-file audits
- artifact, whitespace, and changed-line credential scans

## Scope Boundaries

- Do not alter Swift behavior, project files, workflows, or privacy policy.
- Do not merge or close stacked pull requests without owner authorization.

## Work Completed

- Protected the Makefile-derived root while preserving Python and Xcode tool
  overrides.
- Added exact-line checker contracts and registered this completed plan.

## Verification

- Python compilation and all 18 static contracts passed.
- Local, external-directory, and hostile `ROOT` full `make check` gates each
  passed; the optional Xcode build was truthfully skipped because `xcodebuild`
  is not installed on the Linux validation host.
- Eight focused mutations covering protected-root derivation, tool overrides,
  rooted cleanup, and completed-plan status were rejected.
- Structured-file, whitespace, explicit-artifact, and changed-line credential
  audits passed before shipment.
