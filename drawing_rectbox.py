import cv2
import numpy as np
import imutils

windowName = 'Drawing Demo'
#cv2.namedWindow(windowName)

#img= np.zeros((512, 512, 3), np.uint8)
# true if mouse is pressed
drawing = False

# if True, draw rectangle. Press 'm' to toggle to curve
mode = True 

# mouse callback function
def draw_shape(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, fx, fy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                #img=np.zeros((512, 512, 3), np.uint8)
                fx, fy= x, y
                #cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            fx, fy= x, y
            cap.release()
            #cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)

    #return x, y
# cv2.setMouseCallback(windowName, draw_shape)

def main():
    global mode, img, fx, fy, ix, iy
    cap = cv2.VideoCapture(0)
    ix, iy = -1, -1
    fx, fy = 0, 0
    while(True):
        ret, img=cap.read()
        img=imutils.resize(img, width=640)
        cv2.rectangle(img, (ix, iy), (fx, fy), (0, 255, 0), 1)
        cv2.imshow(windowName, img)
        
        k = cv2.waitKey(25)
        if k == ord('m') or k == ord('M'):
            mode = not mode
        elif k == 27:
                break
        #print (ix, iy, fx, fy)
        cv2.setMouseCallback(windowName, draw_shape)
    cv2.destroyAllWindows()
    return (ix, iy, fx, fy)

def draw_box1(cap):
    global mode, img, fx, fy, ix, iy
    #cap=cv2.VideoCapture(rtsp)
    ret, frame=cap.read()
    frame=imutils.resize(frame, width=640)
    ix, iy = -1, -1
    fx, fy = 0, 0
    cv2.rectangle(frame, (ix, iy), (fx, fy), (0, 255, 0), 1)
    cv2.setMouseCallback(windowName, draw_shape)
    return frame#, (ix, iy, fx, fy)

#if __name__ == "__main__":
    #main()
    #draw_box