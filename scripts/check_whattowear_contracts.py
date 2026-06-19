#!/usr/bin/env python3
"""Static privacy contracts for the legacy WhatToWear camera sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PLIST = ROOT / "What To Wear" / "Info.plist"
APP_DELEGATE = ROOT / "What To Wear" / "AppDelegate.swift"
VIEW_CONTROLLER = ROOT / "What To Wear" / "ViewController.swift"
DISPLAY_IMAGE = ROOT / "What To Wear" / "DisplayImage.swift"
README_PATH = ROOT / "README.md"
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
CAPTURE_GENERATION_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-13-camera-capture-generation-guard.md"
MAKE_ROOT_PROTECTION_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-14-make-root-override-protection.md"
FINAL_CAPTURE_REVEAL_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-14-final-capture-reveal-generation-guard.md"
DEVICE_VERIFICATION_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-16-device-verification-guide.md"
CAMERA_CONFIGURATION_LOCK_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-17-camera-configuration-lock-guard.md"
)
CAMERA_OWNERSHIP_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-19-camera-ownership-deep-review.md"
)
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "check.yml"
MAKEFILE_PATH = ROOT / "Makefile"
MUTATION_SCRIPT_PATH = ROOT / "scripts" / "test_whattowear_mutations.py"

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
        "dispatch_async(dispatch_get_main_queue())" in source,
        "capture state and segue work must be dispatched back to the main queue",
    )


def test_photo_save_requires_successful_write_before_segue():
    source = VIEW_CONTROLLER.read_text()
    method = source.split("func persistCapture", 1)[1].split(
        "func dispatchCaptureFailure", 1
    )[0]

    assert_true(
        "if imageData.writeToFile(destinationPath, atomically: true)" in method,
        "photo save must check that the local JPEG write succeeded",
    )
    assert_true(
        method.index("if imageData.writeToFile(destinationPath, atomically: true)")
        < method.index("dispatch_async(dispatch_get_main_queue())")
        < method.index("self.completeCapture"),
        "capture completion must only run after the successful local write guard",
    )


def test_photo_handoff_is_protected_and_ephemeral():
    capture_source = VIEW_CONTROLLER.read_text()
    save_method = capture_source.split("func persistCapture", 1)[1].split(
        "func dispatchCaptureFailure", 1
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
        save_method.index("imageData.writeToFile(destinationPath, atomically: true)")
        < save_method.index(protection_call)
        < save_method.index("self.completeCapture"),
        "photo completion must follow a successful protected write",
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
    capture_flow = source.split("func requestCapture", 1)[1].split(
        "func persistCapture", 1
    )[0]
    callback_guard = (
        "queuedCaptureGeneration != self.captureGeneration || "
        "!self.captureViewVisible || !self.cameraReady || self.activeCaptureID != captureID"
    )

    assert_true(
        "!self.sessionConfigured || !self.captureSession.running" in capture_flow,
        "camera queue must reject capture work when its configured session is inactive",
    )
    assert_true(
        callback_guard in capture_flow,
        "capture completion must recheck main-queue lifecycle state before persistence",
    )


def test_stale_capture_work_is_rejected_after_camera_resumes():
    source = VIEW_CONTROLLER.read_text()
    capture_flow = source.split("func requestCapture", 1)[1].split(
        "func persistCapture", 1
    )[0]
    pause_method = source.split("func pauseCaptureSession()", 1)[1].split(
        "func resumeCaptureSession()", 1
    )[0]

    assert_true(
        "var captureGeneration = 0" in source,
        "camera lifecycle must retain a capture generation",
    )
    assert_true(
        "queuedCaptureGeneration != self.captureGeneration" in capture_flow,
        "capture completion must reject an obsolete lifecycle generation",
    )
    assert_true(
        "captureGeneration += 1" in pause_method,
        "pausing the camera must invalidate capture work from the prior generation",
    )
    assert_true(
        pause_method.index("captureGeneration += 1")
        < pause_method.index("captureSession.stopRunning()"),
        "capture generation must advance before an active session is stopped",
    )


def test_saved_photo_reveal_rechecks_capture_generation():
    source = VIEW_CONTROLLER.read_text()
    save_method = source.split("func completeCapture", 1)[1].split(
        "func capturePath", 1
    )[0]

    assert_true(
        "queuedCaptureGeneration != captureGeneration" in save_method
        and "!captureViewVisible" in save_method
        and "!cameraReady" in save_method,
        "saved photo reveal must recheck lifecycle state after persistence",
    )
    assert_true(
        save_method.index("failCapture(captureID, destinationPath: destinationPath)")
        < save_method.index('performSegueWithIdentifier("displayImage", sender: self)'),
        "stale persisted photos must be cleaned before the only reveal site",
    )


def test_capture_identity_and_ui_delivery_are_exactly_once():
    source = VIEW_CONTROLLER.read_text()
    start_method = source.split("func startSnap()", 1)[1].split("func updateTime()", 1)[0]
    assert_true(
        "func completeCapture" in source and "func capturePath" in source,
        "camera flow must centralize successful capture completion and owned path creation",
    )
    completion_method = source.split("func completeCapture", 1)[1].split(
        "func capturePath", 1
    )[0]

    assert_true(
        "var activeCaptureID: Int?" in source and "var nextCaptureID = 0" in source,
        "camera flow must assign a unique identity to each in-flight capture",
    )
    assert_true(
        "var revealInProgress = false" in source,
        "camera flow must reserve the result reveal while its transition is active",
    )
    assert_true(
        "activeCaptureID != nil || revealInProgress" in start_method,
        "countdown must reject overlapping capture or reveal work",
    )
    assert_true(
        "if activeCaptureID != captureID" in completion_method,
        "capture completion must only release the matching active capture",
    )
    assert_true(
        completion_method.count('performSegueWithIdentifier("displayImage", sender: self)') == 1,
        "a capture must have one result reveal site",
    )
    assert_true(
        "revealInProgress = true" in completion_method,
        "result reveal must be reserved before performing the segue",
    )


def test_camera_state_and_session_mutations_use_owned_queues():
    source = VIEW_CONTROLLER.read_text()
    persist_method = source.split("func persistCapture", 1)[1].split(
        "func dispatchCaptureFailure", 1
    )[0]

    assert_true(
        'dispatch_queue_create("com.garethpaul.WhatToWear.camera", DISPATCH_QUEUE_SERIAL)'
        in source,
        "camera session work must use one serial ownership queue",
    )
    assert_true(
        "dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)" not in source,
        "capture work must not use an unowned global queue",
    )
    assert_true(
        "dispatch_async(captureQueue)" in source,
        "camera session mutations must be dispatched to the camera queue",
    )
    assert_true(
        'dispatch_queue_create("com.garethpaul.WhatToWear.photo", DISPATCH_QUEUE_SERIAL)'
        in source,
        "protected JPEG persistence must use a separate serial ownership queue",
    )
    assert_true(
        "dispatch_async(photoQueue)" in persist_method,
        "photo writes must not delay camera session stop and configuration work",
    )
    assert_true(
        "dispatch_async(dispatch_get_main_queue())" in source,
        "capture callbacks must return to the main queue before reading UI lifecycle state",
    )
    assert_true(
        "authorizationStatusForMediaType(AVMediaTypeVideo)" in source
        and "requestAccessForMediaType(AVMediaTypeVideo)" in source,
        "camera setup must handle authorization before configuring a device",
    )
    assert_true(
        "captureSession.beginConfiguration()" in source
        and "captureSession.commitConfiguration()" in source,
        "camera input and output changes must be committed as one session configuration",
    )


def test_capture_handoffs_are_unique_and_preserve_encoded_images():
    capture_source = VIEW_CONTROLLER.read_text()
    display_source = DISPLAY_IMAGE.read_text()

    assert_true(
        '"what_to_wear_\\(captureID).jpg"' in capture_source,
        "each capture must own a unique handoff path",
    )
    assert_true(
        "imageData.writeToFile(destinationPath, atomically: true)" in capture_source,
        "captured JPEG data must be persisted without a decode/re-encode memory spike",
    )
    assert_true(
        "UIImageJPEGRepresentation" not in capture_source,
        "camera flow must not discard capture orientation metadata by re-encoding",
    )
    assert_true(
        "connection.supportsVideoOrientation" in capture_source
        and "connection.videoOrientation = .Portrait" in capture_source,
        "capture connection must record portrait orientation before producing the JPEG",
    )
    assert_true(
        "connection.supportsVideoMirroring" in capture_source
        and "connection.videoMirrored = true" in capture_source,
        "front-camera capture must mirror at the capture connection instead of rebuilding pixels",
    )
    assert_true(
        "var capturePath: String?" in display_source,
        "result controller must receive the exact capture-owned handoff path",
    )
    assert_true(
        "UIImage(CGImage:" not in display_source,
        "result display must preserve the captured image orientation metadata",
    )
    assert_true(
        "if let destinationPath = capturePath" in display_source,
        "result display must fail closed when no owned handoff path was supplied",
    )


def test_capture_failures_release_only_owned_work_and_files():
    source = VIEW_CONTROLLER.read_text()
    assert_true(
        "func failCapture" in source and "func completeCapture" in source,
        "camera flow must centralize capture failure and completion",
    )
    failure_method = source.split("func failCapture", 1)[1].split(
        "func completeCapture", 1
    )[0]
    assert_true(
        "override func prepareForSegue" in source,
        "camera flow must explicitly transfer capture ownership during the result segue",
    )
    prepare_method = source.split("override func prepareForSegue", 1)[1].split(
        "@IBOutlet var snapBtn", 1
    )[0]

    assert_true(
        "if activeCaptureID == captureID" in failure_method,
        "capture failure must not clear a newer in-flight capture",
    )
    assert_true(
        "removeItemAtPath(path" in failure_method,
        "capture failure must remove only its owned handoff file",
    )
    assert_true(
        "displayController.capturePath = pendingCapturePath" in prepare_method,
        "segue preparation must transfer the exact owned handoff path",
    )
    assert_true(
        "pendingCapturePath = nil" in prepare_method,
        "segue preparation must consume the pending handoff exactly once",
    )


def test_abandoned_capture_files_are_cleaned_on_launch():
    source = VIEW_CONTROLLER.read_text()
    assert_true(
        "func cleanupAbandonedCaptures()" in source,
        "camera flow must centralize abandoned handoff cleanup",
    )
    cleanup_method = source.split("func cleanupAbandonedCaptures()", 1)[1].split(
        "func configureCameraAccess()", 1
    )[0]
    view_did_load = source.split("override func viewDidLoad()", 1)[1].split(
        "func cleanupAbandonedCaptures()", 1
    )[0]
    assert_true(
        "cleanupAbandonedCaptures()" in view_did_load,
        "launch must remove abandoned captures before requesting camera access",
    )
    assert_true(
        'fileName.hasPrefix("what_to_wear_")' in cleanup_method
        and 'fileName.hasSuffix(".jpg")' in cleanup_method,
        "abandoned cleanup must be limited to capture-owned JPEG names",
    )
    assert_true(
        "removeItemAtPath(filePath" in cleanup_method,
        "abandoned capture cleanup must remove each matched handoff",
    )


def test_result_close_is_exactly_once():
    source = DISPLAY_IMAGE.read_text()
    close_method = source.split("@IBAction func close", 1)[1]
    assert_true(
        "var closeInProgress = false" in source,
        "result UI must track whether dismissal has already started",
    )
    assert_true(
        "if closeInProgress {\n            return\n        }" in close_method,
        "repeated close taps must not start overlapping dismissals",
    )
    assert_true(
        close_method.index("closeInProgress = true")
        < close_method.index("POPSpringAnimation"),
        "dismissal ownership must be reserved before starting its animation",
    )


def test_camera_session_guards_input_and_output_setup():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "stillImageOutput!" not in source,
        "camera session setup must not force-unwrap the still image output",
    )
    assert_true(
        "let output = AVCaptureStillImageOutput()" in source,
        "camera session setup must create a local output before publishing it",
    )
    assert_true(
        "captureSession.canAddOutput(output)" in source,
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
        "let input = AVCaptureDeviceInput(device: cameraDevice, error: &error)" in source,
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
        "touch.locationInView(view).x / screenWidth" in source,
        "focus touch handlers must keep using the guarded touch location",
    )


def test_countdown_ignores_duplicate_timers():
    source = VIEW_CONTROLLER.read_text()

    assert_true(
        "if timer.valid" in source,
        "countdown start must guard an already-running timer",
    )
    assert_true(
        "if timer.valid || activeCaptureID != nil || revealInProgress" in source,
        "countdown start must return before scheduling a duplicate timer",
    )
    assert_true(
        source.count("NSTimer.scheduledTimerWithTimeInterval") == 1,
        "countdown flow must keep a single timer scheduling path",
    )


def test_camera_configuration_unlock_requires_successful_lock():
    source = VIEW_CONTROLLER.read_text()
    configure_device = source.split("func focusTo", 1)[1].split(
        "let screenWidth", 1
    )[0]
    successful_lock = "if device.lockForConfiguration(nil) {"

    assert_true(
        configure_device.count("device.lockForConfiguration(nil)") == 1,
        "focus configuration must attempt exactly one camera configuration lock",
    )
    assert_true(
        configure_device.count("device.unlockForConfiguration()") == 1,
        "focus configuration must release exactly one acquired camera configuration lock",
    )
    assert_true(
        successful_lock in configure_device,
        "focus configuration must check successful camera lock acquisition",
    )
    lock_branch = configure_device.split(successful_lock, 1)[1].split(
        "\n            }", 1
    )[0]
    assert_true(
        "device.unlockForConfiguration()" in lock_branch,
        "focus configuration must unlock only inside the successful lock branch",
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
        and "captureViewVisible = true" in view_source
        and "resumeCaptureSession()" in view_source,
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
        "if self.captureSession.running" in pause_method
        and "self.captureSession.stopRunning()" in pause_method,
        "pausing the camera must stop an active capture session",
    )
    resume_method = view_source.split("func resumeCaptureSession()", 1)[1].split(
        "override func viewDidLoad()", 1
    )[0]
    assert_true(
        "if self.sessionConfigured && !self.captureSession.running" in resume_method,
        "camera restart must require a configured and stopped session",
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
    assert_true(
        "var captureLifecycleEnabled = true" in view_source,
        "camera lifecycle must separately track whether app/view events allow capture",
    )
    assert_true(
        "captureLifecycleEnabled = false" in pause_method,
        "a pause event must disable capture before queued session work runs",
    )
    assert_true(
        "captureLifecycleEnabled = true" in resume_method
        and "startCaptureSessionIfEligible()" in resume_method,
        "only an explicit resume event may re-enable and start capture",
    )
    begin_session = view_source.split("func beginSession()", 1)[1].split(
        "func installPreviewLayer()", 1
    )[0]
    assert_true(
        "self.startCaptureSessionIfEligible()" in begin_session
        and "self.resumeCaptureSession()" not in begin_session,
        "late camera configuration must respect the latest lifecycle pause",
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
    assert_true("UIImage(CGImage:" not in source, "display flow must preserve image orientation metadata")
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


def test_device_verification_guide_is_actionable():
    readme = README_PATH.read_text()
    normalized_readme = " ".join(readme.split()).lower()

    required_guidance = [
        "## Native Device Verification",
        "Swift 2-era source",
        "physical iOS device with a front camera",
        "Camera unavailable",
        "does not link directly to Settings",
        "Run `make check` before opening Xcode",
        "Tap the snap button repeatedly",
        "Background the app or cover the camera screen",
        "portrait, mirrored result preview appears",
        "Tap close repeatedly",
        "late setup completion does not restart capture",
        "The temporary JPEG uses complete file protection",
        "what_to_wear_*.jpg",
        "The app has no upload or sharing path",
    ]
    for guidance in required_guidance:
        assert_true(
            " ".join(guidance.split()).lower() in normalized_readme,
            "README device verification guide must include: {0}".format(guidance),
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
    makefile_lines = set(makefile.splitlines())

    assert_true(
        "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile_lines,
        "Makefile must protect the repository root",
    )
    assert_true("PYTHON ?= python3" in makefile_lines, "Makefile must preserve the Python command override")
    assert_true("XCODEBUILD ?= xcodebuild" in makefile_lines, "Makefile must preserve the Xcode command override")
    assert_true(
        '\tfind "$(ROOT)" -type f \\( -name \'*.pyc\' -o -name \'*.pyo\' \\) -delete' in makefile_lines,
        "Makefile cleanup must remove Python bytecode from the repository root",
    )
    assert_true(
        '\tfind "$(ROOT)" -type d -name \'__pycache__\' -prune -exec rm -rf {} +' in makefile_lines,
        "Makefile cleanup must remove Python cache directories from the repository root",
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


def test_mutation_suite_guards_camera_ownership_contracts():
    assert_true(MUTATION_SCRIPT_PATH.is_file(), "camera mutation test script must exist")
    mutation_source = MUTATION_SCRIPT_PATH.read_text()
    required_mutations = [
        "serial camera queue",
        "unique capture path",
        "active capture identity",
        "camera authorization",
        "session configuration transaction",
        "capture orientation",
        "owned file cleanup",
        "one-shot segue handoff",
        "abandoned file cleanup",
        "exactly-once close",
        "late configuration resume",
        "photo persistence queue",
    ]
    for mutation in required_mutations:
        assert_true(
            mutation in mutation_source,
            "camera mutation suite must cover: {0}".format(mutation),
        )
    assert_true(
        '$(PYTHON) "$(MUTATION_SCRIPT)"' in MAKEFILE_PATH.read_text(),
        "Make test gate must execute the camera mutation suite",
    )


def assert_completed_plan(path, label):
    assert_true(path.is_file(), "{0} plan must live under docs/plans".format(label))
    plan_text = path.read_text()
    assert_true("status: completed" in plan_text.lower(), "{0} plan must be completed".format(label))
    assert_true("make check" in plan_text, "{0} plan must document make check verification".format(label))


def test_completed_plans_are_in_docs_plans():
    checker_source = Path(__file__).read_text()
    registered_tests = checker_source.rsplit("\ndef main():", 1)[1].split(
        "for test in tests:", 1
    )[0]
    assert_true(
        "test_camera_configuration_unlock_requires_successful_lock," in registered_tests,
        "camera configuration lock contract must remain registered",
    )
    assert_true(
        "docs/plans/2026-06-17-camera-configuration-lock-guard.md"
        in README_PATH.read_text(),
        "README must index the camera configuration lock plan",
    )
    assert_true(
        "docs/plans/2026-06-19-camera-ownership-deep-review.md"
        in README_PATH.read_text(),
        "README must index the camera ownership deep-review plan",
    )
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
    assert_completed_plan(CAPTURE_GENERATION_PLAN_PATH, "camera capture generation guard")
    assert_completed_plan(MAKE_ROOT_PROTECTION_PLAN_PATH, "Make root override protection")
    assert_completed_plan(FINAL_CAPTURE_REVEAL_PLAN_PATH, "final capture reveal generation guard")
    assert_completed_plan(DEVICE_VERIFICATION_PLAN_PATH, "device verification guide")
    assert_completed_plan(CAMERA_CONFIGURATION_LOCK_PLAN_PATH, "camera configuration lock guard")
    assert_completed_plan(CAMERA_OWNERSHIP_PLAN_PATH, "camera ownership deep review")


def main():
    tests = [
        test_camera_usage_description_is_declared,
        test_captures_remain_local_to_documents_directory,
        test_camera_capture_guards_nil_buffers_and_jpegs,
        test_photo_save_requires_successful_write_before_segue,
        test_photo_handoff_is_protected_and_ephemeral,
        test_camera_capture_guards_connection_input_ports,
        test_stale_capture_work_is_rejected_when_camera_is_inactive,
        test_stale_capture_work_is_rejected_after_camera_resumes,
        test_saved_photo_reveal_rechecks_capture_generation,
        test_capture_identity_and_ui_delivery_are_exactly_once,
        test_camera_state_and_session_mutations_use_owned_queues,
        test_capture_handoffs_are_unique_and_preserve_encoded_images,
        test_capture_failures_release_only_owned_work_and_files,
        test_abandoned_capture_files_are_cleaned_on_launch,
        test_result_close_is_exactly_once,
        test_camera_session_guards_input_and_output_setup,
        test_focus_touch_handlers_guard_optional_touches,
        test_camera_configuration_unlock_requires_successful_lock,
        test_countdown_ignores_duplicate_timers,
        test_camera_session_stops_when_inactive_or_covered,
        test_camera_flow_avoids_console_logging,
        test_display_image_loads_capture_safely,
        test_device_verification_guide_is_actionable,
        test_launch_mask_guards_optional_window_and_assets,
        test_hosted_verification_is_least_privilege_and_pinned,
        test_makefile_is_root_independent,
        test_mutation_suite_guards_camera_ownership_contracts,
        test_completed_plans_are_in_docs_plans,
    ]
    for test in tests:
        test()
    print("WhatToWear contracts passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
