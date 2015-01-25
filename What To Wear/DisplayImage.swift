//
//  DisplayImage.swift
//  What To Wear
//
//  Created by Gareth Jones  on 1/24/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

class DisplayImage: UIViewController {

    @IBOutlet var imageView: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()

        let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as String
        let destinationPath = documentsPath.stringByAppendingPathComponent("what_to_wear.jpg")

        let image = UIImage(contentsOfFile: destinationPath )
        // display the image

        let flippedImage

        UIImage* sourceImage = [UIImage imageNamed:@"whatever.png"];

        UIImage* flippedImage = [UIImage imageWithCGImage:sourceImage.CGImage
        scale:sourceImage.scale
        orientation:UIImageOrientationUpMirrored];

        self.imageView.image = image


    }


}
