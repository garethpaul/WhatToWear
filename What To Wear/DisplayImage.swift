//
//  DisplayImage.swift
//  What To Wear
//

class DisplayImage: UIViewController {


    
    override func viewDidLoad() {
        super.viewDidLoad()

        self.message.font = UIFont (name: "BadaBoom BB", size: 43 )
        self.logoText.font = UIFont (name: "BadaBoom BB", size: 22 )

        // Opacity Overlay
        self.overlayView.backgroundColor = UIColor.blackColor().colorWithAlphaComponent(0.5)

        // Get Suggested Colors
        self.suggestion1.tintColor = toColor("#41A378")
        self.suggestion2.tintColor = toColor("#2342FF")
        // Transparent suggestedColors
        self.suggestedColors.backgroundColor = UIColor.clearColor()

        // load image from "camera" into the UIImage
        let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as String
        let destinationPath = documentsPath.stringByAppendingPathComponent("what_to_wear.jpg")
        let image = UIImage(contentsOfFile: destinationPath )

        // image needs to be flipped to get the view intended form the selfie
        let flippedImage = UIImage(CGImage: image!.CGImage, scale: 1.0, orientation: .LeftMirrored)

        // display image
        self.imageView.image = flippedImage

    }

    // IBOutlets
    @IBOutlet var logoText: UILabel!
    @IBOutlet var imageView: UIImageView!
    @IBOutlet var message: UILabel!
    @IBOutlet var closeBtn: UIButton!
    @IBOutlet var suggestion1: UIButton!
    @IBOutlet var suggestion2: UIButton!
    @IBOutlet var overlayView: UIView!
    @IBOutlet var suggestedColors: UIView!

    // IBActions
    @IBAction func close(sender: AnyObject) {
        // close the window
        let animClose = POPSpringAnimation(propertyNamed: kPOPLayerScaleXY)
        animClose.toValue = NSValue(CGSize: CGSizeMake(0.8, 0.8))
        self.closeBtn.layer.pop_addAnimation(animClose, forKey: "popClose")

        // Once the animation has completed move back
        animClose.completionBlock = {(animation, finished) in
            //Code goes here
            self.closeBtn.layer.pop_removeAllAnimations()
            self.presentingViewController?.dismissViewControllerAnimated(true, completion: nil)
        }


    }




}
