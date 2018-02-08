import cv2
import filters
import random

FRAME_WIDTH = 768
FRAME_HEIGHT = 1024

MIN_SQUARE_AREA = 400


def process(img, profile, debug):

    img = filters.resize(img, FRAME_WIDTH, FRAME_HEIGHT )

    original_img = img

    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hue ,saturation ,value = cv2.split(hsv)
    # # cv2.imshow('Saturation Image',saturation)
    #
    yellow_mask = filters.rgb_threshold(img, profile, strong=True)

    img = filters.mask(img, yellow_mask)
    if debug:
        cv2.imshow("yellow threshold", img)

    img = filters.hsv_threshold(img, profile)
    if debug:
        cv2.imshow("hsv", img)

    img = filters.median_filter(img)
    #cv2.imshow('median filter', img)

    # # Display Image
    # # Thresholding the image
    # ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)
    # # cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
    # # Creating a Named window to display image
    # cv2.imshow("3. Image after Thresholding",thresh_image)
    # # Display Image


    # dilation to strengthen the edges
    # kernel = np.ones((3,3), np.uint8)
    # # Creating the kernel for dilation
    # dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
    # cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
    # # Creating a Named window to display image
    # cv2.imshow("5. Dilation", dilated_image)

    # Displaying Image

    # print cv2.findContours(dilated_image, 1, 2)

    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for (index,contour) in enumerate(contours):

        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)


        if area > MIN_SQUARE_AREA:
            contour_list.append(contour)
            blue = random.randint(0,255)
            red = random.randint(0,255)
            green = random.randint(0,255)

            # hull = cv2.convexHull(contour)
            # contour = hull
            # print hull

            color = (blue, red, green)


            x,y,w,h = cv2.boundingRect(contour)

            print index, area, len(approx), blue, red, green

            #
            # if is_square(w,h):
            #     print 'not a square'
            #     continue

            print 'square: %s,%s' % (w,h)
            print w/h, h/w

            center_mass_x = x+w/2
            center_mass_y = y+h/2

            cv2.drawContours(original_img, contours,  index, color, 2)

            # print '---'
            # print 'dot', original_img[center_mass_x][center_mass_y]  # B,G,R
            # print '----'
            cv2.rectangle(original_img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(original_img, (center_mass_x, center_mass_y),5,color, -1);
            cv2.line(original_img,(FRAME_WIDTH/2,FRAME_HEIGHT),(center_mass_x,center_mass_y),color,2)


    return original_img
            #
            # rows,cols = img.shape[:2]
            # [vx,vy,x,y] = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
            # lefty = int((-x*vy/vx) + y)
            # righty = int(((cols-x)*vy/vx)+y)
            # cv2.line(original_img,(cols-1,righty),(0,lefty),(0,255,0),2)


def is_square(w,h):

    if w > h:
       return float(w)/h > 1.5

    else:
        return float(h)/w > 1.5

# contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
# pt = (180, 3 * img.shape[0] // 4)
# for cnt in contours:
#     approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
#     # print len(cnt)
#     print len(approx)
#     if len(approx) ==6 :
#         print "Cube"
#         cv2.drawContours(img,[cnt],-1,(255,0,0),3)
#         cv2.putText(img,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0,255, 255], 2)
#     elif len(approx) == 7:
#         print "Cube"
#         cv2.drawContours(img,[cnt],-1,(255,0,0),3)
#         cv2.putText(img,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
#     elif len(approx) == 8:
#         print "Cylinder"
#         cv2.drawContours(img,[cnt],-1,(255,0,0),3)
#         cv2.putText(img,'Cylinder', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
#     elif len(approx) > 10:
#         print "Sphere"
#         cv2.drawContours(img,[cnt],-1,(255,0,0),3)
#         cv2.putText(img,'Sphere', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [255, 0, 0], 2)


#
# cv2.namedWindow("Shape", cv2.WINDOW_NORMAL)
# cv2.imshow('Shape',img)
#
# corners    = cv2.goodFeaturesToTrack(thresh_image,6,0.06,25)
# corners    = np.float32(corners)
# for    item in    corners:
#     x,y    = item[0]
#     cv2.circle(img,(x,y),10,255,-1)
# cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
# cv2.imshow("Corners",img)

if __name__ == '__main__':
    video(debug=False)