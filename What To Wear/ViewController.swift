import UIKit
import AVFoundation

class ViewController: UIViewController {

    let captureSession = AVCaptureSession()
    var previewLayer : AVCaptureVideoPreviewLayer?
    var stillImageOutput : AVCaptureStillImageOutput?

    var startTime = NSTimeInterval()
    var timer = NSTimer()
    var snapTime:Double = 5


    @IBOutlet var countdown: UILabel!

    @IBOutlet var captureBtn: UIButton!

    // Take Picture with Button    /
    @IBAction func snapClick(sender: AnyObject) {

        //
        self.startSnap()

    }

    func startSnap() {

        let aSelector : Selector = "updateTime"
        timer = NSTimer.scheduledTimerWithTimeInterval(1, target: self, selector: aSelector, userInfo: nil, repeats: true)
        startTime = NSDate.timeIntervalSinceReferenceDate()
        
    }

    func updateTime() {
        var currentTime = NSDate.timeIntervalSinceReferenceDate()
        var elapsedTime = currentTime - startTime
        var seconds = snapTime-elapsedTime
        if seconds > 0 {
            elapsedTime -= NSTimeInterval(seconds)
            self.countdown.hidden = false
            self.countdown.text = "\(Int(seconds+1))"

        } else {
            self.countdown.hidden = true
            timer.invalidate()

            // wow we are ready to save some photos
            // setup still OutPut to save
            if let stillOutput = self.stillImageOutput {

                // we do this on another thread so we don't hang the UI
                dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)) {

                    // find video connection
                    var videoConnection : AVCaptureConnection?
                    for connection in stillOutput.connections {
                        // find a matching input port
                        for port in connection.inputPorts! {
                            // and matching type
                            if port.mediaType == AVMediaTypeVideo {
                                videoConnection = connection as? AVCaptureConnection
                                break
                            }
                        }
                        if videoConnection != nil {
                            break // for connection
                        }
                    }

                    if videoConnection != nil {
                        // found the video connection, let's get the image
                        stillOutput.captureStillImageAsynchronouslyFromConnection(videoConnection) {
                            (imageSampleBuffer:CMSampleBuffer!, _) in

                            let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageSampleBuffer)
                            self.didTakePhoto(imageData)




                            
                        }
                    }
                }
            }
        }
    }



    func didTakePhoto(imageData: NSData) {
        // parse not dropbox
        let image = UIImage(data: imageData)


        let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as String
        let destinationPath = documentsPath.stringByAppendingPathComponent("what_to_wear.jpg")
        UIImageJPEGRepresentation(image,1.0).writeToFile(destinationPath, atomically: true)

        self.performSegueWithIdentifier("displayImage", sender: self);



    }

    @IBOutlet var snapBtn: UIButton!
    // If we find a device we'll store it here for later use
    var captureDevice : AVCaptureDevice?

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view, typically from a nib.
        captureSession.sessionPreset = AVCaptureSessionPresetHigh

        let devices = AVCaptureDevice.devices()

        // Loop through all the capture devices on this phone
        for device in devices {
            // Make sure this particular device supports video
            if (device.hasMediaType(AVMediaTypeVideo)) {
                // Finally check the position and confirm we've got the back camera
                if(device.position == AVCaptureDevicePosition.Front) {
                    captureDevice = device as? AVCaptureDevice
                    if captureDevice != nil {
                        println("Capture device found")
                        beginSession()
                    }
                }
            }
        }

    }

    func focusTo(value : Float) {
        if let device = captureDevice {
            if(device.lockForConfiguration(nil)) {
                device.unlockForConfiguration()
            }
        }
    }

    let screenWidth = UIScreen.mainScreen().bounds.size.width
    override func touchesBegan(touches: NSSet, withEvent event: UIEvent) {
        var anyTouch = touches.anyObject() as UITouch
        var touchPercent = anyTouch.locationInView(self.view).x / screenWidth
        focusTo(Float(touchPercent))
        
    }

    override func touchesMoved(touches: NSSet, withEvent event: UIEvent) {
        var anyTouch = touches.anyObject() as UITouch
        var touchPercent = anyTouch.locationInView(self.view).x / screenWidth
        focusTo(Float(touchPercent))
    }

    func configureDevice() {
        if let device = captureDevice {
            device.lockForConfiguration(nil)
            //device.focusMode = .Locked
            device.unlockForConfiguration()
        }

    }

    func beginSession() {

        configureDevice()
        stillImageOutput = AVCaptureStillImageOutput()
        let outputSettings = [ AVVideoCodecKey : AVVideoCodecJPEG ]
        stillImageOutput!.outputSettings = outputSettings

        // add output to session
        if captureSession.canAddOutput(stillImageOutput) {
            captureSession.addOutput(stillImageOutput)
        }
        

        var err : NSError? = nil
        captureSession.addInput(AVCaptureDeviceInput(device: captureDevice, error: &err))

        if err != nil {
            println("error: \(err?.localizedDescription)")
        }

        previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)

        self.view.layer.addSublayer(previewLayer)

        // bringSubview to the front
        self.view.bringSubviewToFront(snapBtn)
        self.view.bringSubviewToFront(countdown)

        // Make the snapBtn opaque
        self.snapBtn.opaque = true
        self.snapBtn.alpha = 0.4

        // Start the magic
        previewLayer?.frame = self.view.layer.frame
        captureSession.startRunning()
    }
    
}