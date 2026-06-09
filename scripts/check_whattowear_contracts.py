#!/usr/bin/env python3
"""Static privacy contracts for the legacy WhatToWear camera sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PLIST = ROOT / "What To Wear" / "Info.plist"
APP_DELEGATE = ROOT / "What To Wear" / "AppDelegate.swift"
VIEW_CONTROLLER = ROOT / "What To Wear" / "ViewController.swift"
DISPLAY_IMAGE = ROOT / "What To Wear" / "DisplayImage.swift"
CAMERA_PRIVACY_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-camera-privacy-contract.md"
CAPTURE_GUARDS_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-camera-capture-guards.md"
DISPLAY_IMAGE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-display-image-load-guard.md"
LAUNCH_MASK_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-launch-mask-guards.md"
INPUT_PORTS_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-camera-input-port-guards.md"

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


def test_camera_capture_guards_connection_input_ports():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "connection.inputPorts!" not in source,
        "capture connection scanning must not force-unwrap input ports",
    )
    assert_true(
        "if let inputPorts = connection.inputPorts" in source,
        "capture connection scanning must guard optional input ports",
    )
    assert_true(
        "for port in inputPorts" in source,
        "capture connection scanning must iterate the guarded input ports",
    )


def test_display_image_loads_capture_safely():
    source = DISPLAY_IMAGE.read_text()
    source_without_spaces = source.replace(" ", "")

    assert_true(
        "UIImage(contentsOfFile:destinationPath)" in source_without_spaces,
        "display flow must load the saved local capture path",
    )
    assert_true(
        "if let image = UIImage(contentsOfFile: destinationPath)" in source,
        "display flow must guard saved image loading",
    )
    assert_true(
        "image!.CGImage" not in source,
        "display flow must not force-unwrap the saved image",
    )
    assert_true(
        '"No photo available"' in source and "suggestedColors.hidden = true" in source,
        "display flow must show a fallback when the local capture is missing",
    )


def test_launch_mask_guards_optional_window_and_assets():
    source = APP_DELEGATE.read_text()

    assert_true(
        "self.window!" not in source,
        "app launch must not force-unwrap the window",
    )
    assert_true(
        "mask!" not in source,
        "launch mask animation must not force-unwrap the mask layer",
    )
    assert_true(
        'UIImage(named: "whatToWearWhite")!' not in source,
        "launch mask must not force-unwrap the mask image asset",
    )
    assert_true(
        "if let window = self.window" in source,
        "app launch must guard the optional window",
    )
    assert_true(
        "if let maskLayer = self.mask" in source,
        "launch mask setup and animation must guard the optional mask layer",
    )
    assert_true(
        'if let maskImage = UIImage(named: "whatToWearWhite")' in source,
        "launch mask setup must guard the image asset",
    )


def assert_completed_plan(path, label):
    assert_true(path.is_file(), "{0} plan must live under docs/plans".format(label))
    plan_text = path.read_text()
    assert_true("status: completed" in plan_text.lower(), "{0} plan must be completed".format(label))
    assert_true("make check" in plan_text, "{0} plan must document make check verification".format(label))


def test_completed_plans_are_in_docs_plans():
    assert_completed_plan(CAMERA_PRIVACY_PLAN_PATH, "camera privacy")
    assert_completed_plan(CAPTURE_GUARDS_PLAN_PATH, "camera capture guards")
    assert_completed_plan(DISPLAY_IMAGE_PLAN_PATH, "display image load guard")
    assert_completed_plan(LAUNCH_MASK_PLAN_PATH, "launch mask guards")
    assert_completed_plan(INPUT_PORTS_PLAN_PATH, "camera input port guards")


def main():
    tests = [
        test_camera_usage_description_is_declared,
        test_captures_remain_local_to_documents_directory,
        test_camera_capture_guards_nil_buffers_and_jpegs,
        test_camera_capture_guards_connection_input_ports,
        test_display_image_loads_capture_safely,
        test_launch_mask_guards_optional_window_and_assets,
        test_completed_plans_are_in_docs_plans,
    ]
    for test in tests:
        test()
    print("WhatToWear contracts passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
