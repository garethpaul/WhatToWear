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
PHOTO_WRITE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-photo-write-success-guard.md"
DISPLAY_IMAGE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-display-image-load-guard.md"
LAUNCH_MASK_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-launch-mask-guards.md"
INPUT_PORTS_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-camera-input-port-guards.md"
SESSION_INPUT_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-camera-session-input-guards.md"
FOCUS_TOUCH_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-focus-touch-guards.md"
COUNTDOWN_TIMER_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-countdown-timer-guard.md"
CAMERA_LOGGING_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-camera-console-log-guard.md"
DISPLAY_CGIMAGE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-display-cgimage-guard.md"
HOSTED_VERIFICATION_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-10-hosted-static-verification.md"
PHOTO_LIFECYCLE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-10-protected-photo-lifecycle.md"
CAMERA_SESSION_LIFECYCLE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-10-camera-session-lifecycle.md"
CHECKOUT_CREDENTIAL_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-12-checkout-credential-boundary.md"
STALE_CAPTURE_CALLBACK_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-13-stale-camera-capture-callback.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "check.yml"
MAKEFILE_PATH = ROOT / "Makefile"

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


def test_photo_save_requires_successful_write_before_segue():
    source = VIEW_CONTROLLER.read_text()
    method = source.split("func didTakePhoto", 1)[1].split("@IBOutlet var snapBtn", 1)[0]

    assert_true(
        "if jpegData.writeToFile(destinationPath, atomically: true)" in method,
        "photo save must check that the local JPEG write succeeded",
    )
    assert_true(
        method.index("if jpegData.writeToFile(destinationPath, atomically: true)")
        < method.index("dispatch_async(dispatch_get_main_queue())")
        < method.index('self.performSegueWithIdentifier("displayImage", sender: self)'),
        "display segue must only run after the successful local write guard",
    )


def test_photo_handoff_is_protected_and_ephemeral():
    capture_source = VIEW_CONTROLLER.read_text()
    save_method = capture_source.split("func didTakePhoto", 1)[1].split(
        "@IBOutlet var snapBtn", 1
    )[0]
    display_source = DISPLAY_IMAGE.read_text()

    protection_call = (
        "setAttributes(protectionAttributes, ofItemAtPath: destinationPath, error: nil)"
    )
    assert_true(
        "[NSFileProtectionKey: NSFileProtectionComplete]" in save_method,
        "saved photos must use complete iOS file protection",
    )
    assert_true(
        protection_call in save_method,
        "photo saving must verify file protection before display",
    )
    assert_true(
        save_method.index("writeToFile(destinationPath, atomically: true)")
        < save_method.index(protection_call)
        < save_method.index('performSegueWithIdentifier("displayImage", sender: self)'),
        "photo display must follow a successful protected write",
    )
    assert_true(
        "else {\n                        NSFileManager.defaultManager().removeItemAtPath(destinationPath, error: nil)"
        in save_method,
        "a photo must be removed if file protection cannot be applied",
    )
    assert_true(
        "NSFileManager.defaultManager().removeItemAtPath(destinationPath, error: nil)"
        in display_source,
        "display flow must remove the local handoff file after decoding it",
    )
    assert_true(
        display_source.index("UIImage(contentsOfFile: destinationPath)")
        < display_source.index(
            "NSFileManager.defaultManager().removeItemAtPath(destinationPath, error: nil)"
        ),
        "display flow must decode the photo before removing its handoff file",
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


def test_stale_capture_work_is_rejected_when_camera_is_inactive():
    source = VIEW_CONTROLLER.read_text()
    lifecycle_guard = "if !self.captureViewVisible || !self.captureSession.running"
    capture_flow = source.split(
        "dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0))",
        1,
    )[1].split("func didTakePhoto", 1)[0]

    assert_true(
        capture_flow.count(lifecycle_guard) == 2,
        "queued capture work and its completion must both recheck camera lifecycle state",
    )
    first_guard = capture_flow.index(lifecycle_guard)
    connection_scan = capture_flow.index("for connection in stillOutput.connections")
    completion = capture_flow.index("captureStillImageAsynchronouslyFromConnection")
    second_guard = capture_flow.index(lifecycle_guard, first_guard + 1)
    jpeg_conversion = capture_flow.index(
        "AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageSampleBuffer)"
    )
    assert_true(
        first_guard < connection_scan < completion < second_guard < jpeg_conversion,
        "camera lifecycle guards must run before connection scanning and JPEG conversion",
    )


def test_camera_session_guards_input_and_output_setup():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "stillImageOutput!" not in source,
        "camera session setup must not force-unwrap the still image output",
    )
    assert_true(
        "if let stillOutput = stillImageOutput" in source,
        "camera session setup must guard the still image output",
    )
    assert_true(
        "captureSession.canAddOutput(stillOutput)" in source,
        "camera session setup must check whether the output can be added",
    )
    assert_true(
        "captureSession.addInput(AVCaptureDeviceInput(device: captureDevice" not in source,
        "camera session setup must not add an unguarded camera device input",
    )
    assert_true(
        "if let cameraDevice = captureDevice" in source,
        "camera session setup must guard the optional capture device",
    )
    assert_true(
        "let input = AVCaptureDeviceInput(device: cameraDevice, error: &err)" in source,
        "camera session setup must create input from the guarded capture device",
    )
    assert_true(
        "captureSession.canAddInput(input)" in source and "captureSession.addInput(input)" in source,
        "camera session setup must check canAddInput before adding the input",
    )


def test_focus_touch_handlers_guard_optional_touches():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "touches.anyObject() as UITouch" not in source,
        "focus touch handlers must not force-cast optional touch objects",
    )
    assert_true(
        source.count("if let touch = touches.anyObject() as? UITouch") >= 2,
        "focus touch handlers must guard optional touch objects",
    )
    assert_true(
        "touch.locationInView(self.view).x / screenWidth" in source,
        "focus touch handlers must keep using the guarded touch location",
    )


def test_countdown_ignores_duplicate_timers():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "if timer.valid" in source,
        "countdown start must guard an already-running timer",
    )
    assert_true(
        "if timer.valid {\n            return\n        }" in source,
        "countdown start must return before scheduling a duplicate timer",
    )
    assert_true(
        source.count("NSTimer.scheduledTimerWithTimeInterval") == 1,
        "countdown flow must keep a single timer scheduling path",
    )


def test_camera_session_stops_when_inactive_or_covered():
    view_source = VIEW_CONTROLLER.read_text()
    app_source = APP_DELEGATE.read_text()

    assert_true(
        "var captureViewVisible = false" in view_source,
        "camera lifecycle must track whether the capture screen is visible",
    )
    assert_true(
        "override func viewWillAppear(animated: Bool)" in view_source
        and "captureViewVisible = true\n        resumeCaptureSession()" in view_source,
        "the visible camera screen must resume its capture session",
    )
    assert_true(
        "override func viewWillDisappear(animated: Bool)" in view_source
        and "captureViewVisible = false\n        pauseCaptureSession()" in view_source,
        "a covered camera screen must stop its capture session",
    )
    pause_method = view_source.split("func pauseCaptureSession()", 1)[1].split(
        "func resumeCaptureSession()", 1
    )[0]
    assert_true(
        "timer.invalidate()" in pause_method and "countdown.hidden = true" in pause_method,
        "pausing the camera must cancel and hide an in-progress countdown",
    )
    assert_true(
        "if captureSession.running" in pause_method
        and "captureSession.stopRunning()" in pause_method,
        "pausing the camera must stop an active capture session",
    )
    resume_method = view_source.split("func resumeCaptureSession()", 1)[1].split(
        "override func viewDidLoad()", 1
    )[0]
    assert_true(
        "if captureViewVisible && captureDevice != nil && !captureSession.running" in resume_method,
        "camera restart must require a visible view, configured device, and stopped session",
    )
    assert_true(
        "captureSession.startRunning()" in resume_method,
        "camera lifecycle must restart an eligible capture session",
    )
    assert_true(
        view_source.count("captureSession.startRunning()") == 1,
        "all capture-session starts must use the visibility-aware resume path",
    )
    assert_true(
        app_source.count("cameraController.pauseCaptureSession()") == 1,
        "app inactivity must pause the camera session exactly once",
    )
    assert_true(
        app_source.count("cameraController.resumeCaptureSession()") == 1,
        "app activation must resume the visible camera session exactly once",
    )


def test_camera_flow_avoids_console_logging():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "println(" not in source,
        "camera flow must not write camera discovery or setup state to stdout",
    )
    assert_true(
        "localizedDescription" not in source,
        "camera setup errors must not be formatted for console logging",
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
        "UIImage(CGImage: image.CGImage" not in source,
        "display flow must not assume saved images have CGImage backing",
    )
    assert_true(
        "if let imageRef = image.CGImage" in source,
        "display flow must guard the saved image CGImage backing before mirroring",
    )
    assert_true(
        "func showMissingPhoto()" in source,
        "display flow must centralize missing-photo fallback UI",
    )
    assert_true(
        "showMissingPhoto()" in source and source.count("showMissingPhoto()") >= 3,
        "display flow must use the missing-photo fallback for load and CGImage failures",
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


def test_hosted_verification_is_least_privilege_and_pinned():
    assert_true(WORKFLOW_PATH.is_file(), "hosted verification workflow must exist")
    workflow = WORKFLOW_PATH.read_text()
    workflow_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in WORKFLOW_PATH.parent.iterdir()
        if path.is_file()
    )
    checkout_step = (
        "      - name: Check out repository\n"
        "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3\n"
        "        with:\n"
        "          persist-credentials: false"
    )

    assert_true(
        workflow_files == [".github/workflows/check.yml"],
        "workflow inventory must contain only .github/workflows/check.yml",
    )
    assert_true(
        workflow.count("actions/checkout@") == 1 and checkout_step in workflow,
        "hosted verification must use one pinned credential-free checkout",
    )
    assert_true(
        workflow.count("persist-credentials:") == 1
        and "persist-credentials: true" not in workflow,
        "hosted verification must not persist checkout credentials",
    )

    assert_true(
        "permissions:\n  contents: read" in workflow,
        "hosted verification permissions must be read-only",
    )
    assert_true(
        "python-version: ['3.10', '3.12', '3.14']" in workflow,
        "hosted verification must cover Python 3.10, 3.12, and 3.14",
    )
    assert_true(
        "workflow_dispatch:" in workflow,
        "hosted verification must support manual dispatch",
    )
    assert_true(
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10" in workflow,
        "checkout must use an immutable revision",
    )
    assert_true(
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in workflow,
        "setup-python must use an immutable revision",
    )
    assert_true("run: make check" in workflow, "hosted verification must run make check")
    assert_true("timeout-minutes: 5" in workflow, "hosted verification must have a timeout")
    assert_true("concurrency:" in workflow, "hosted verification must define concurrency")
    assert_true(
        "cancel-in-progress: true" in workflow,
        "hosted verification must cancel superseded runs",
    )
    assert_true(
        "runs-on: ubuntu-24.04" in workflow,
        "hosted verification must use a fixed Ubuntu runner",
    )
    assert_true(
        "ubuntu-latest" not in workflow,
        "hosted verification must not use a floating Ubuntu runner",
    )
    checkout_plan = CHECKOUT_CREDENTIAL_PLAN_PATH.read_text()
    assert_true(
        "status: completed" in checkout_plan.lower()
        and "persist-credentials: false" in checkout_plan
        and "hostile mutations rejected" in checkout_plan,
        "checkout credential plan must record completed verification",
    )
    guidance = " ".join(
        "\n".join(
            (ROOT / path).read_text()
            for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]
        ).split()
    ).lower()
    assert_true(
        "checkout credentials are not persisted" in guidance
        and "credential-free checkout" in guidance,
        "repository guidance must document the credential-free checkout boundary",
    )


def test_makefile_is_root_independent():
    makefile = MAKEFILE_PATH.read_text()

    assert_true(
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile,
        "Makefile must resolve the repository root",
    )
    assert_true(
        "CONTRACT_SCRIPT := $(ROOT)/scripts/check_whattowear_contracts.py" in makefile,
        "Makefile must use the rooted contract script path",
    )
    assert_true(
        "SCHEME := What To Wear" in makefile and "SCHEME := What\\ To\\ Wear" not in makefile,
        "Makefile must pass the Xcode scheme without literal backslashes",
    )
    assert_true(
        makefile.count('"$(CONTRACT_SCRIPT)"') >= 2,
        "Makefile must quote the rooted contract script path",
    )
    assert_true(
        '$(MAKE) -f "$(ROOT)/Makefile" clean' in makefile,
        "recursive cleanup must use the rooted Makefile",
    )


def assert_completed_plan(path, label):
    assert_true(path.is_file(), "{0} plan must live under docs/plans".format(label))
    plan_text = path.read_text()
    assert_true("status: completed" in plan_text.lower(), "{0} plan must be completed".format(label))
    assert_true("make check" in plan_text, "{0} plan must document make check verification".format(label))


def test_completed_plans_are_in_docs_plans():
    assert_completed_plan(CAMERA_PRIVACY_PLAN_PATH, "camera privacy")
    assert_completed_plan(CAPTURE_GUARDS_PLAN_PATH, "camera capture guards")
    assert_completed_plan(PHOTO_WRITE_PLAN_PATH, "photo write success guard")
    assert_completed_plan(DISPLAY_IMAGE_PLAN_PATH, "display image load guard")
    assert_completed_plan(LAUNCH_MASK_PLAN_PATH, "launch mask guards")
    assert_completed_plan(INPUT_PORTS_PLAN_PATH, "camera input port guards")
    assert_completed_plan(SESSION_INPUT_PLAN_PATH, "camera session input guards")
    assert_completed_plan(FOCUS_TOUCH_PLAN_PATH, "focus touch guards")
    assert_completed_plan(COUNTDOWN_TIMER_PLAN_PATH, "countdown timer guard")
    assert_completed_plan(CAMERA_LOGGING_PLAN_PATH, "camera console log guard")
    assert_completed_plan(DISPLAY_CGIMAGE_PLAN_PATH, "display CGImage guard")
    assert_completed_plan(HOSTED_VERIFICATION_PLAN_PATH, "hosted static verification")
    assert_completed_plan(PHOTO_LIFECYCLE_PLAN_PATH, "protected photo lifecycle")
    assert_completed_plan(CAMERA_SESSION_LIFECYCLE_PLAN_PATH, "camera session lifecycle")
    assert_completed_plan(CHECKOUT_CREDENTIAL_PLAN_PATH, "checkout credential boundary")
    assert_completed_plan(STALE_CAPTURE_CALLBACK_PLAN_PATH, "stale camera capture callback")


def main():
    tests = [
        test_camera_usage_description_is_declared,
        test_captures_remain_local_to_documents_directory,
        test_camera_capture_guards_nil_buffers_and_jpegs,
        test_photo_save_requires_successful_write_before_segue,
        test_photo_handoff_is_protected_and_ephemeral,
        test_camera_capture_guards_connection_input_ports,
        test_stale_capture_work_is_rejected_when_camera_is_inactive,
        test_camera_session_guards_input_and_output_setup,
        test_focus_touch_handlers_guard_optional_touches,
        test_countdown_ignores_duplicate_timers,
        test_camera_session_stops_when_inactive_or_covered,
        test_camera_flow_avoids_console_logging,
        test_display_image_loads_capture_safely,
        test_launch_mask_guards_optional_window_and_assets,
        test_hosted_verification_is_least_privilege_and_pinned,
        test_makefile_is_root_independent,
        test_completed_plans_are_in_docs_plans,
    ]
    for test in tests:
        test()
    print("WhatToWear contracts passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
