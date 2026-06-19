import UIKit

class DisplayImage: UIViewController {

    var capturePath: String?
    var closeInProgress = false

    override func viewDidLoad() {
        super.viewDidLoad()

        message.font = UIFont(name: "BadaBoom BB", size: 43)
        logoText.font = UIFont(name: "BadaBoom BB", size: 22)
        overlayView.backgroundColor = UIColor.blackColor().colorWithAlphaComponent(0.5)
        suggestion1.tintColor = toColor("#41A378")
        suggestion2.tintColor = toColor("#2342FF")
        suggestedColors.backgroundColor = UIColor.clearColor()

        if let destinationPath = capturePath {
            if let image = UIImage(contentsOfFile: destinationPath) {
                imageView.image = image
            } else {
                showMissingPhoto()
            }
            NSFileManager.defaultManager().removeItemAtPath(destinationPath, error: nil)
            capturePath = nil
        } else {
            showMissingPhoto()
        }
    }

    func showMissingPhoto() {
        message.text = "No photo available"
        suggestedColors.hidden = true
    }

    @IBOutlet var logoText: UILabel!
    @IBOutlet var imageView: UIImageView!
    @IBOutlet var message: UILabel!
    @IBOutlet var closeBtn: UIButton!
    @IBOutlet var suggestion1: UIButton!
    @IBOutlet var suggestion2: UIButton!
    @IBOutlet var overlayView: UIView!
    @IBOutlet var suggestedColors: UIView!

    @IBAction func close(sender: AnyObject) {
        if closeInProgress {
            return
        }
        closeInProgress = true

        let animClose = POPSpringAnimation(propertyNamed: kPOPLayerScaleXY)
        animClose.toValue = NSValue(CGSize: CGSizeMake(0.8, 0.8))
        closeBtn.layer.pop_addAnimation(animClose, forKey: "popClose")
        animClose.completionBlock = { (animation, finished) in
            self.closeBtn.layer.pop_removeAllAnimations()
            self.presentingViewController?.dismissViewControllerAnimated(true, completion: nil)
        }
    }
}
