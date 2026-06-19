import UIKit
import AVFoundation

class ViewController: UIViewController {

    let captureSession = AVCaptureSession()
    let captureQueue = dispatch_queue_create("com.garethpaul.WhatToWear.camera", DISPATCH_QUEUE_SERIAL)
    let photoQueue = dispatch_queue_create("com.garethpaul.WhatToWear.photo", DISPATCH_QUEUE_SERIAL)
    var previewLayer: AVCaptureVideoPreviewLayer?
    var stillImageOutput: AVCaptureStillImageOutput?
    var captureDevice: AVCaptureDevice?
    var sessionConfigured = false

    var startTime = NSTimeInterval()
    var timer = NSTimer()
    var snapTime: Double = 5
    var captureViewVisible = false
    var captureLifecycleEnabled = true
    var cameraReady = false
    var captureGeneration = 0
    var nextCaptureID = 0
    var activeCaptureID: Int?
    var pendingCapturePath: String?
    var revealInProgress = false

    @IBOutlet var countdown: UILabel!
    @IBOutlet var captureBtn: UIButton!
    @IBOutlet var snapBtn: UIButton!

    @IBAction func snapClick(sender: AnyObject) {
        startSnap()
    }

    func startSnap() {
        if timer.valid || activeCaptureID != nil || revealInProgress || !captureViewVisible || !cameraReady {
            return
        }

        let aSelector: Selector = "updateTime"
        timer = NSTimer.scheduledTimerWithTimeInterval(1, target: self, selector: aSelector, userInfo: nil, repeats: true)
        startTime = NSDate.timeIntervalSinceReferenceDate()
    }

    func updateTime() {
        let currentTime = NSDate.timeIntervalSinceReferenceDate()
        var elapsedTime = currentTime - startTime
        let seconds = snapTime - elapsedTime
        if seconds > 0 {
            elapsedTime -= NSTimeInterval(seconds)
            countdown.hidden = false
            countdown.text = "\(Int(seconds + 1))"
            return
        }

        countdown.hidden = true
        timer.invalidate()
        if !captureViewVisible || !cameraReady || activeCaptureID != nil || revealInProgress {
            return
        }

        nextCaptureID += 1
        let captureID = nextCaptureID
        let queuedCaptureGeneration = captureGeneration
        activeCaptureID = captureID
        requestCapture(captureID, forCaptureGeneration: queuedCaptureGeneration)
    }

    func requestCapture(captureID: Int, forCaptureGeneration queuedCaptureGeneration: Int) {
        dispatch_async(captureQueue) {
            if !self.sessionConfigured || !self.captureSession.running {
                self.dispatchCaptureFailure(captureID, destinationPath: nil)
                return
            }
            if let stillOutput = self.stillImageOutput {
                var videoConnection: AVCaptureConnection?
                for connection in stillOutput.connections {
                    if let inputPorts = connection.inputPorts {
                        for port in inputPorts {
                            if port.mediaType == AVMediaTypeVideo {
                                videoConnection = connection as? AVCaptureConnection
                                break
                            }
                        }
                    }
                    if videoConnection != nil {
                        break
                    }
                }

                if let connection = videoConnection {
                    if connection.supportsVideoOrientation {
                        connection.videoOrientation = .Portrait
                    }
                    if connection.supportsVideoMirroring {
                        connection.videoMirrored = true
                    }
                    stillOutput.captureStillImageAsynchronouslyFromConnection(connection) {
                        (imageSampleBuffer: CMSampleBuffer!, error: NSError!) in
                        if error != nil || imageSampleBuffer == nil {
                            self.dispatchCaptureFailure(captureID, destinationPath: nil)
                            return
                        }
                        if let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageSampleBuffer) {
                            dispatch_async(dispatch_get_main_queue()) {
                                if queuedCaptureGeneration != self.captureGeneration || !self.captureViewVisible || !self.cameraReady || self.activeCaptureID != captureID {
                                    self.failCapture(captureID, destinationPath: nil)
                                    return
                                }
                                self.persistCapture(imageData, captureID: captureID, forCaptureGeneration: queuedCaptureGeneration)
                            }
                        } else {
                            self.dispatchCaptureFailure(captureID, destinationPath: nil)
                        }
                    }
                } else {
                    self.dispatchCaptureFailure(captureID, destinationPath: nil)
                }
            } else {
                self.dispatchCaptureFailure(captureID, destinationPath: nil)
            }
        }
    }

    func persistCapture(imageData: NSData, captureID: Int, forCaptureGeneration queuedCaptureGeneration: Int) {
        let destinationPath = capturePath(captureID)
        dispatch_async(photoQueue) {
            if imageData.writeToFile(destinationPath, atomically: true) {
                let protectionAttributes = [NSFileProtectionKey: NSFileProtectionComplete]
                if NSFileManager.defaultManager().setAttributes(protectionAttributes, ofItemAtPath: destinationPath, error: nil) {
                    dispatch_async(dispatch_get_main_queue()) {
                        self.completeCapture(captureID, forCaptureGeneration: queuedCaptureGeneration, destinationPath: destinationPath)
                    }
                    return
                }
            }
            self.dispatchCaptureFailure(captureID, destinationPath: destinationPath)
        }
    }

    func dispatchCaptureFailure(captureID: Int, destinationPath: String?) {
        dispatch_async(dispatch_get_main_queue()) {
            self.failCapture(captureID, destinationPath: destinationPath)
        }
    }

    func failCapture(captureID: Int, destinationPath: String?) {
        if let path = destinationPath {
            NSFileManager.defaultManager().removeItemAtPath(path, error: nil)
        }
        if activeCaptureID == captureID {
            activeCaptureID = nil
        }
    }

    func completeCapture(captureID: Int, forCaptureGeneration queuedCaptureGeneration: Int, destinationPath: String) {
        if activeCaptureID != captureID || queuedCaptureGeneration != captureGeneration || !captureViewVisible || !cameraReady || revealInProgress {
            failCapture(captureID, destinationPath: destinationPath)
            return
        }

        activeCaptureID = nil
        pendingCapturePath = destinationPath
        revealInProgress = true
        performSegueWithIdentifier("displayImage", sender: self)
    }

    func capturePath(captureID: Int) -> String {
        let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as String
        return documentsPath.stringByAppendingPathComponent("what_to_wear_\(captureID).jpg")
    }

    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "displayImage" {
            if let displayController = segue.destinationViewController as? DisplayImage {
                displayController.capturePath = pendingCapturePath
                pendingCapturePath = nil
            }
        }
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        captureGeneration += 1
        captureViewVisible = true
        revealInProgress = false
        resumeCaptureSession()
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        captureViewVisible = false
        pauseCaptureSession()
    }

    func pauseCaptureSession() {
        captureGeneration += 1
        captureLifecycleEnabled = false
        activeCaptureID = nil
        cameraReady = false
        timer.invalidate()
        countdown.hidden = true
        dispatch_async(captureQueue) {
            if self.captureSession.running {
                self.captureSession.stopRunning()
            }
        }
    }

    func resumeCaptureSession() {
        captureLifecycleEnabled = true
        startCaptureSessionIfEligible()
    }

    func startCaptureSessionIfEligible() {
        let resumeGeneration = captureGeneration
        if !captureViewVisible || !captureLifecycleEnabled {
            return
        }
        dispatch_async(captureQueue) {
            if self.sessionConfigured && !self.captureSession.running {
                self.captureSession.startRunning()
            }
            let running = self.sessionConfigured && self.captureSession.running
            dispatch_async(dispatch_get_main_queue()) {
                if resumeGeneration == self.captureGeneration && self.captureViewVisible && self.captureLifecycleEnabled {
                    self.cameraReady = running
                    self.snapBtn.enabled = running
                }
            }
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        countdown.font = UIFont(name: "BadaBoom BB", size: 92)
        snapBtn.enabled = false
        cleanupAbandonedCaptures()
        configureCameraAccess()
    }

    func cleanupAbandonedCaptures() {
        let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as String
        let fileManager = NSFileManager.defaultManager()
        if let fileNames = fileManager.contentsOfDirectoryAtPath(documentsPath, error: nil) as? [String] {
            for fileName in fileNames {
                if fileName.hasPrefix("what_to_wear_") && fileName.hasSuffix(".jpg") {
                    let filePath = documentsPath.stringByAppendingPathComponent(fileName)
                    fileManager.removeItemAtPath(filePath, error: nil)
                }
            }
        }
    }

    func configureCameraAccess() {
        let status = AVCaptureDevice.authorizationStatusForMediaType(AVMediaTypeVideo)
        if status == .Authorized {
            discoverCaptureDevice()
        } else if status == .NotDetermined {
            AVCaptureDevice.requestAccessForMediaType(AVMediaTypeVideo) { granted in
                dispatch_async(dispatch_get_main_queue()) {
                    if granted {
                        self.discoverCaptureDevice()
                    } else {
                        self.setCameraUnavailable()
                    }
                }
            }
        } else {
            setCameraUnavailable()
        }
    }

    func discoverCaptureDevice() {
        for device in AVCaptureDevice.devices() {
            if device.hasMediaType(AVMediaTypeVideo) && device.position == AVCaptureDevicePosition.Front {
                captureDevice = device as? AVCaptureDevice
                break
            }
        }
        if captureDevice != nil {
            beginSession()
        } else {
            setCameraUnavailable()
        }
    }

    func setCameraUnavailable() {
        cameraReady = false
        snapBtn.enabled = false
        countdown.hidden = false
        countdown.text = "Camera unavailable"
    }

    func focusTo(value: Float) {
        if let device = captureDevice {
            dispatch_async(captureQueue) {
                if device.lockForConfiguration(nil) {
                    device.unlockForConfiguration()
                }
            }
        }
    }

    let screenWidth = UIScreen.mainScreen().bounds.size.width

    override func touchesBegan(touches: NSSet, withEvent event: UIEvent) {
        if let touch = touches.anyObject() as? UITouch {
            let touchPercent = touch.locationInView(view).x / screenWidth
            focusTo(Float(touchPercent))
        }
    }

    override func touchesMoved(touches: NSSet, withEvent event: UIEvent) {
        if let touch = touches.anyObject() as? UITouch {
            let touchPercent = touch.locationInView(view).x / screenWidth
            focusTo(Float(touchPercent))
        }
    }

    func beginSession() {
        if let cameraDevice = captureDevice {
            dispatch_async(captureQueue) {
                self.captureSession.beginConfiguration()
                self.captureSession.sessionPreset = AVCaptureSessionPresetHigh

                var error: NSError? = nil
                let input = AVCaptureDeviceInput(device: cameraDevice, error: &error)
                let output = AVCaptureStillImageOutput()
                output.outputSettings = [AVVideoCodecKey: AVVideoCodecJPEG]

                var configured = false
                if error == nil && input != nil && self.captureSession.canAddInput(input) {
                    self.captureSession.addInput(input)
                    if self.captureSession.canAddOutput(output) {
                        self.captureSession.addOutput(output)
                        self.stillImageOutput = output
                        configured = true
                    } else {
                        self.captureSession.removeInput(input)
                    }
                }

                self.captureSession.commitConfiguration()
                self.sessionConfigured = configured
                dispatch_async(dispatch_get_main_queue()) {
                    if configured {
                        self.installPreviewLayer()
                        self.startCaptureSessionIfEligible()
                    } else {
                        self.setCameraUnavailable()
                    }
                }
            }
        } else {
            setCameraUnavailable()
        }
    }

    func installPreviewLayer() {
        if previewLayer == nil {
            previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
            if let layer = previewLayer {
                view.layer.insertSublayer(layer, atIndex: 0)
            }
        }
        previewLayer?.frame = view.bounds
        view.bringSubviewToFront(snapBtn)
        view.bringSubviewToFront(countdown)
        snapBtn.opaque = true
        snapBtn.alpha = 0.4
    }
}
