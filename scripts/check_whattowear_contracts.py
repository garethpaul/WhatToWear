#!/usr/bin/env python3
"""Static privacy contracts for the legacy WhatToWear camera sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PLIST = ROOT / "What To Wear" / "Info.plist"
VIEW_CONTROLLER = ROOT / "What To Wear" / "ViewController.swift"
PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-camera-privacy-contract.md"

EXPECTED_CAMERA_DESCRIPTION = (
    "WhatToWear uses the camera to capture a local outfit photo for preview."
)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_camera_usage_description_is_declared():
    with APP_PLIST.open("rb") as plist_file:
        info = plistlib.load(plist_file)

    assert_true(
        info.get("NSCameraUsageDescription") == EXPECTED_CAMERA_DESCRIPTION,
        "app Info.plist must declare the camera usage purpose",
    )


def test_captures_remain_local_to_documents_directory():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        ".DocumentDirectory" in source,
        "captured photos must be written to the app documents directory",
    )
    assert_true(
        "writeToFile(destinationPath" in source,
        "captured photos must be written through the local destination path",
    )
    forbidden_terms = ["http://", "https://", "upload", "URLRequest"]
    for term in forbidden_terms:
        assert_true(
            term not in source,
            "camera flow must not contain hidden network or upload behavior: {0}".format(term),
        )


def test_completed_plan_is_in_docs_plans():
    assert_true(PLAN_PATH.is_file(), "camera privacy plan must live under docs/plans")
    assert_true("status: completed" in PLAN_PATH.read_text(), "camera privacy plan must be completed")


def main():
    tests = [
        test_camera_usage_description_is_declared,
        test_captures_remain_local_to_documents_directory,
        test_completed_plan_is_in_docs_plans,
    ]
    for test in tests:
        test()
    print("WhatToWear contracts passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
