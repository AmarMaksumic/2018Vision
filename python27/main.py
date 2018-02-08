import cv2
import yellow_profile
import tracker_frame

VIDEO_SOURCE_NUMBER = 0


def video(debug=False):

    cap = cv2.VideoCapture(VIDEO_SOURCE_NUMBER)

    while(True):

        _, frame = cap.read()

        img = tracker_frame.process(frame, yellow_profile, debug)

        cv2.imshow('frame', img )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def single_frame(debug=False):

    img = cv2.imread("frc_cube.jpg")
    img = tracker_frame.process(img, yellow_profile, debug)

    cv2.imshow('Objects Detected',img)
    cv2.waitKey()


if __name__ == '__main__':
    single_frame()
