#!/usr/bin/env python3
"""Static privacy contracts for the legacy WhatToWear camera sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PLIST = ROOT / "What To Wear" / "Info.plist"
VIEW_CONTROLLER = ROOT / "What To Wear" / "ViewController.swift"
CAMERA_PRIVACY_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-camera-privacy-contract.md"
CAPTURE_GUARDS_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-camera-capture-guards.md"

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


def test_camera_capture_guards_nil_buffers_and_jpegs():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "error != nil || imageSampleBuffer == nil" in source,
        "capture callback must ignore errors and nil sample buffers",
    )
    assert_true(
        "if let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageSampleBuffer)" in source,
        "capture callback must guard JPEG data creation",
    )
    assert_true(
        "if let image = UIImage(data: imageData)" in source,
        "photo saving must guard UIImage decoding",
    )
    assert_true(
        "if let jpegData = UIImageJPEGRepresentation(image,1.0)" in source,
        "photo saving must guard JPEG encoding",
    )
    assert_true(
        "dispatch_async(dispatch_get_main_queue())" in source,
        "segue must be dispatched back to the main queue",
    )


def assert_completed_plan(path, label):
    assert_true(path.is_file(), "{0} plan must live under docs/plans".format(label))
    plan_text = path.read_text()
    assert_true("status: completed" in plan_text.lower(), "{0} plan must be completed".format(label))
    assert_true("make check" in plan_text, "{0} plan must document make check verification".format(label))


def test_completed_plans_are_in_docs_plans():
    assert_completed_plan(CAMERA_PRIVACY_PLAN_PATH, "camera privacy")
    assert_completed_plan(CAPTURE_GUARDS_PLAN_PATH, "camera capture guards")


def main():
    tests = [
        test_camera_usage_description_is_declared,
        test_captures_remain_local_to_documents_directory,
        test_camera_capture_guards_nil_buffers_and_jpegs,
        test_completed_plans_are_in_docs_plans,
    ]
    for test in tests:
        test()
    print("WhatToWear contracts passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
