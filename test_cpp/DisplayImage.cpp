#include <iostream>
 
//Include OpenCV
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

inline int getRed(cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[0];
}

inline int getGreen (cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[1];
}

inline int getBlue (cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[2];
}



inline int getHue (cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[0];
}

inline int getSat (cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[1];
}

inline int getVal (cv::Mat &img, int r, int c) {
    return img.at<cv::Vec3b>(r, c)[2];
}

int main(void )
{
   //Capture stream from webcam.
   cv::VideoCapture capture(1);
 
   //Check if we can get the webcam stream.
   if(!capture.isOpened())
   {
      std::cout << "Could not open camera" << std::endl;
      return -1;
   }
 
   while (true)
   {

        //initialize raw & processed image matrices
        cv::Mat img;

        //Read an image from the camera.
        capture.read(img);

        // RESIZE 
        cv::Mat resizedMat;

        cv::Size s( 1024/2, 768/2 );
        cv::resize( img, resizedMat, s, 0, 0, CV_INTER_AREA );


        // RGB THRESHOLD   
        cv::Mat rgbMat , rgbThreshed;

        int MIN_RED = 150, MAX_RED = 255;
        int MIN_GREEN = 93, MAX_GREEN = 255;
        int MIN_BLUE = 0, MAX_BLUE = 111;

        cv::cvtColor(resizedMat, rgbMat, cv::COLOR_BGR2RGB );
        cv::inRange(rgbMat,
                    cv::Scalar(MIN_RED, MIN_GREEN, MIN_BLUE),
                    cv::Scalar(MAX_RED, MAX_GREEN, MAX_BLUE),
                    rgbThreshed);


        // END RGB


        // START MASK

        cv::Mat rgbThresholdOutput;

        cv::bitwise_and(resizedMat, resizedMat, rgbThresholdOutput, rgbThreshed );




        // HSV THRESHOLD   
        cv::Mat hsvMat, hsvThreshold, output_img;

        int MIN_HUE = 21, MAX_HUE = 64;
        int MIN_SAT = 122, MAX_SAT= 255;
        int MIN_VAL = 96, MAX_VAL= 255;

        cv::cvtColor(rgbThresholdOutput, hsvMat, cv::COLOR_BGR2HSV );
        cv::inRange(hsvMat,
                    cv::Scalar(MIN_HUE, MIN_SAT, MIN_VAL),
                    cv::Scalar(MAX_HUE, MAX_SAT, MAX_VAL),
                    hsvThreshold);

        cv::bitwise_and(rgbThresholdOutput, rgbThresholdOutput, output_img, hsvThreshold );

        // END HSV
 
        //Here we show the drawn image in a named window called "output".
        cv::imshow("output", output_img);






   // //store HSV values at a given test point to send back
   //  int hue = getHue(hsvMat, TEST_POINT.x, TEST_POINT.y);
   //  int sat = getSat(hsvMat, TEST_POINT.x, TEST_POINT.y);
   //  int val = getVal(hsvMat, TEST_POINT.x, TEST_POINT.y);

   //  //threshold on green (light ring color)
   //  cv::Mat greenThreshed;
   //  cv::inRange(hsvMat,
   //              cv::Scalar(MIN_HUE, MIN_SAT, MIN_VAL),
   //              cv::Scalar(MAX_HUE, MAX_SAT, MAX_VAL),
   //              greenThreshed);


   //  out = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
   //  return cv2.inRange(out, (red[0], green[0], blue[0]),  (red[1], green[1], blue[1]))


        //Waits 50 miliseconds for key press, returns -1 if no key is pressed during that time
        if (cv::waitKey(50) >= 0)
            break;
   }
 
   return 0;
}