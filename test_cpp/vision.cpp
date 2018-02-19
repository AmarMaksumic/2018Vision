#include "vision.hpp"
using namespace std;


bool isValidArea(int camera_height, int camera_width, contour_type &contour){

    cv::Rect rect = cv::boundingRect(contour);

    double width = rect.width, height = rect.height;
    double totalArea = ( camera_height * camera_width );
    
    double contour_side_ratio = width/height;
    if (height > width) {
        contour_side_ratio = height/width;
    }

    if (contour_side_ratio > SIDE_RATIO) {
        return false;
    }

    //calculate relevant ratios & values
    double area_ratio = width * height/totalArea * 100;

//    std::cout << area_ratio << std::endl;
//
    if( area_ratio < 1 ){
        return false;
    }
    return true;
}

bool isCubeShape (contour_type &contour) {

    vector<cv::Point> approx;
    cv::approxPolyDP(contour, approx, cv::arcLength(contour, true) * 0.01, true);
    if( approx.size() < 4 ){
        return false;
    }
    if( approx.size() > 10 ){
        return false;
    }

    return true;
}

float get_angle( cv::Mat image, cv::Point point)
{
    float a = float(abs(image.cols/2 - point.x));
    float b = float(image.rows - point.y);

    float radians = atan(a/b);
    float angle = radians * 180 / CV_PI;
    return angle;
}


float get_distance( int width_pixel ){
    return float(CAMERA_FOCAL_LENGTH * CUBE_LENGTH) / width_pixel;
}


void calculate(const cv::Mat &img, cv::Mat &processedImage) {

    // RGB THRESHOLD
    cv::Mat rgbMat, rgbThreshold;

    cv::cvtColor(img, rgbMat, cv::COLOR_BGR2RGB);
    cv::inRange(rgbMat,
                cv::Scalar(RGB_RED[0], RGB_GREEN[0], RGB_BLUE[0]),
                cv::Scalar(RGB_RED[1], RGB_GREEN[1], RGB_BLUE[1]),
                rgbThreshold);

    // END RGB


    // START MASK

    cv::Mat rgbThresholdOutput;

    cv::bitwise_and(img, img, rgbThresholdOutput, rgbThreshold);
//
    cv::imshow("RGB", rgbThresholdOutput);

    // HSV THRESHOLD
    cv::Mat hsvMat, hsvThreshold;

    cv::cvtColor(rgbThresholdOutput, hsvMat, cv::COLOR_BGR2HSV);
    cv::inRange(hsvMat,
                cv::Scalar(HSV_HUE[0], HSV_SAT[0], HSV_VAL[0]),
                cv::Scalar(HSV_HUE[1], HSV_SAT[1], HSV_VAL[1]),
                hsvThreshold);

    // END HSV

    cv::imshow("HSV", hsvThreshold);

    cv::Mat medianBlurMat;

    cv::medianBlur(hsvThreshold, medianBlurMat, MEDIAN_BLUR_LEVEL);

    cv::imshow("BLUR", medianBlurMat);
    //contour detection
    vector<contour_type> contours;
    vector<cv::Vec4i> hierarchy; //throwaway, needed for function
    cv::findContours(medianBlurMat, contours, hierarchy,
                     cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
//

    //store the convex hulls of any valid contours
    vector<contour_type> contour_hulls;
    for (int i = 0; i < (int) contours.size(); i++) {
        contour_type contour = contours[i];
        if (isValidArea( processedImage.rows,
                         processedImage.cols,
                         contour)) {
            contour_type hull;
            cv::convexHull(contour, hull);
            contour_hulls.push_back(hull);
        }
    }

    vector<contour_type> contour_to_loop;

    // we can choose to use the contours or its convex hull
    contour_to_loop = contour_hulls;
    //contour_to_loop = contours;

    cv::Point robot_center( processedImage.cols / 2, processedImage.rows);
    cv::Point top_center( processedImage.cols / 2, 0 );

    for (size_t i = 0; i < contour_to_loop.size(); i++)
    {
        contour_type contour = contour_to_loop[i];
        if (isCubeShape(contour)) {
            cv::drawContours(processedImage, contour_to_loop, i, MY_GREEN, 1);

            cv::Rect rect = cv::boundingRect(contour);

            // find center of mass
            cv::Moments centerMass = cv::moments(contour, true);
            double centerX = (centerMass.m10) / (centerMass.m00);
            double centerY = (centerMass.m01) / (centerMass.m00);
            cv::Point center(centerX, centerY);
            cv::drawMarker(processedImage, center, MY_PURPLE, 1);

            // draw line from robot to center mass
            cv::line(processedImage, robot_center, center, MY_PURPLE, 1);

            cv::rectangle(processedImage, rect, MY_PURPLE, 1);

            // calculate angle
            float angle;

            angle = get_angle(processedImage, center );

            // calculate distance
            float distance;


//            void putText(Mat& img, const string& text, Point org,
//                         int fontFace, double fontScale,
//                         Scalar color,
//                         int thickness=1, int lineType=8, bool bottomLeftOrigin=false )¶

            //cv::putText(processedImage, to_string(angle), center, cv::FONT_HERSHEY_DUPLEX, 1.0, MY_GREEN );
            cv::putText(processedImage, to_string(distance), center, cv::FONT_HERSHEY_DUPLEX, 1.0, MY_GREEN );
            distance = get_distance(rect.width);


        }
    }

    cv::line(processedImage, robot_center, top_center, MY_WHITE, 2);


}