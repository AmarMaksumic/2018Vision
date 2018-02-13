import cv2

import yellow_profile
from cameras import logitech_c270, generic
from pipelines import cube_tracker

from Tkinter import Tk
from gui import Controls

VIDEO_SOURCE_NUMBER = 0


def video(debug=False):

    cap = cv2.VideoCapture(VIDEO_SOURCE_NUMBER)
    root = Tk()
    controller = Controls(root, yellow_profile)
    root.mainloop()

    while(True):

        _, frame = cap.read()

        img = cube_tracker.process(frame,
                                   controller,
                                   logitech_c270,
                                   debug)

        print 'here'
        cv2.imshow('frame', img )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def single_frame(debug=False):

    img = cv2.imread("frc_cube.jpg")
    img = cube_tracker.process(img,
                               yellow_profile,
                               generic,
                               debug)

    cv2.imshow('Objects Detected',img)
    cv2.waitKey()


#TODO enable options to be passed from command line
if __name__ == '__main__':
    video(debug=False)
