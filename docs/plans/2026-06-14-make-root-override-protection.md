# Protect the Make Repository Root from Overrides

## Status: Planned

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
