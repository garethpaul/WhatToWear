#!/usr/bin/env python3
"""Prove that camera ownership regressions break the static contract suite."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEW_CONTROLLER = Path("What To Wear") / "ViewController.swift"
DISPLAY_IMAGE = Path("What To Wear") / "DisplayImage.swift"

MUTATIONS = [
    (
        "serial camera queue",
        VIEW_CONTROLLER,
        'dispatch_queue_create("com.garethpaul.WhatToWear.camera", DISPATCH_QUEUE_SERIAL)',
        "dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)",
    ),
    (
        "unique capture path",
        VIEW_CONTROLLER,
        '"what_to_wear_\\(captureID).jpg"',
        '"what_to_wear.jpg"',
    ),
    (
        "active capture identity",
        VIEW_CONTROLLER,
        "if activeCaptureID != captureID || queuedCaptureGeneration != captureGeneration",
        "if queuedCaptureGeneration != captureGeneration",
    ),
    (
        "camera authorization",
        VIEW_CONTROLLER,
        "AVCaptureDevice.requestAccessForMediaType(AVMediaTypeVideo)",
        "AVCaptureDevice.requestAccessForMediaType(AVMediaTypeAudio)",
    ),
    (
        "session configuration transaction",
        VIEW_CONTROLLER,
        "self.captureSession.beginConfiguration()",
        "// configuration transaction removed",
    ),
    (
        "capture orientation",
        VIEW_CONTROLLER,
        "connection.videoOrientation = .Portrait",
        "// portrait orientation removed",
    ),
    (
        "owned file cleanup",
        VIEW_CONTROLLER,
        "removeItemAtPath(path, error: nil)",
        "removeItemAtPath(\"what_to_wear.jpg\", error: nil)",
    ),
    (
        "one-shot segue handoff",
        VIEW_CONTROLLER,
        "pendingCapturePath = nil",
        "// pending handoff retained",
    ),
    (
        "abandoned file cleanup",
        VIEW_CONTROLLER,
        'fileName.hasPrefix("what_to_wear_")',
        'fileName.hasPrefix("unrelated_")',
    ),
    (
        "exactly-once close",
        DISPLAY_IMAGE,
        "if closeInProgress {\n            return\n        }",
        "// duplicate close guard removed",
    ),
    (
        "late configuration resume",
        VIEW_CONTROLLER,
        "self.installPreviewLayer()\n                        self.startCaptureSessionIfEligible()",
        "self.installPreviewLayer()\n                        self.resumeCaptureSession()",
    ),
    (
        "photo persistence queue",
        VIEW_CONTROLLER,
        "dispatch_async(photoQueue) {",
        "dispatch_async(captureQueue) {",
    ),
]


def run_checker(repo):
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "check_whattowear_contracts.py")],
        cwd=str(repo),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )


def main():
    with tempfile.TemporaryDirectory(prefix="whattowear-mutations-") as temp_directory:
        copy_root = Path(temp_directory) / "repo"
        shutil.copytree(ROOT, copy_root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

        baseline = run_checker(copy_root)
        if baseline.returncode != 0:
            raise AssertionError("baseline contract suite failed:\n{0}".format(baseline.stdout))

        for label, relative_path, original, replacement in MUTATIONS:
            path = copy_root / relative_path
            source = path.read_text()
            if original not in source:
                raise AssertionError("mutation target missing for {0}".format(label))
            path.write_text(source.replace(original, replacement, 1))
            result = run_checker(copy_root)
            path.write_text(source)
            if result.returncode == 0:
                raise AssertionError("mutation survived: {0}".format(label))

    print("WhatToWear mutation contracts passed ({0} mutations)".format(len(MUTATIONS)))


if __name__ == "__main__":
    main()
