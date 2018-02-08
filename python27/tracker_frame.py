"""

Object Tracker based on a color profile

uses contour lines and rough area calculations

"""

import cv2
import filters
import random

FRAME_WIDTH = 768
FRAME_HEIGHT = 1024

MIN_SQUARE_AREA = 400

def process(img, profile, debug):

    img = filters.resize(img, FRAME_WIDTH, FRAME_HEIGHT )

    original_img = img

    mask = filters.rgb_threshold(img, profile, strong=True)

    img = filters.mask(img, mask)
    if debug:
        cv2.imshow("yellow threshold", img)

    img = filters.hsv_threshold(img, profile)
    if debug:
        cv2.imshow("hsv", img)

    img = filters.median_filter(img)
    if debug:
        cv2.imshow('median filter', img)


    _, contours, hierarchy = cv2.findContours(img,
                                              cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for (index,contour) in enumerate(contours):

        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        #
        # limit the number of contours to process
        #
        if area > MIN_SQUARE_AREA:
            contour_list.append(contour)
            blue = random.randint(0,255)
            red = random.randint(0,255)
            green = random.randint(0,255)


            color = (blue, red, green)

            x,y,w,h = cv2.boundingRect(contour)

            print index, area, len(approx), blue, red, green

            #
            # if it is a cube, then outbound rectangle should be close to a square
            #
            if is_square(w,h):
                print 'not a square'
                continue

            print 'square: %s,%s' % (w,h)
            print w/h, h/w

            center_mass_x = x+w/2
            center_mass_y = y+h/2

            cv2.drawContours(original_img, contours,  index, color, 2)
            cv2.rectangle(original_img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(original_img, (center_mass_x, center_mass_y),5,color, -1);
            cv2.line(original_img,(FRAME_WIDTH/2,FRAME_HEIGHT),(center_mass_x,center_mass_y),color,2)

    return original_img


def is_square(w,h):
    if w > h:
       return float(w)/h > 1.5
    else:
        return float(h)/w > 1.5