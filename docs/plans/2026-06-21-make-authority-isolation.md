# Make Authority Isolation

## Status: Completed

## Context

The repository rooted its file arguments, but GNU Make still accepted caller-
controlled Python/Xcode expressions, shell state, startup files, unsafe modes,
and later public recipe replacement. A forged root could also redirect cleanup
or make the native build appear unavailable.

## Implementation

- Froze literal Python and Xcode executable values, `/bin/sh`, and the canonical
  repository root for every public verification target.
- Rejected startup files, replaced Makefile lists, executable Make syntax,
  non-executing or error-ignoring modes, and later single-colon recipes.
- Added an adversarial authority harness and bound hosted verification to
  `/usr/bin/make check`.

## Verification

- Repository-root and external-directory `/usr/bin/make check` run the static contracts,
  12 camera mutations, authority harness, cleanup, and truthful Xcode boundary.
- The authority harness covers 35 target/root/shell combinations, hostile tool
  paths, parenthesized and braced Make syntax, startup and Makefile-list
  boundaries, later recipes and variables, cleanup containment, and unsafe
  execution modes.

## Trust Boundary

GNU Make parses earlier startup files before this Makefile can reject them, and
an explicit later `override` directive remains caller authority. A caller who
chooses the default `python3` still controls `PATH`; hosted verification installs
the reviewed Python runtime before invoking the fixed system Make executable.

## Scope Boundary

This change does not alter Swift source, camera behavior, assets, Xcode project
settings, signing, dependencies, or credential state. Native compilation and
physical-device camera validation still require a compatible macOS/Xcode host.
