import cv2
import os
from datetime import datetime

class take_pic():

    @staticmethod
    def save_pic(img):
        cwd_ = os.getcwd
        cwd = cwd_() + "\\taken_images"
        curr_time =  "\\" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') 
        cv2.imwrite(cwd + curr_time + ".jpeg", img )

    @staticmethod
    def get_pic(cam_nr):

        dec = 'y'

        while(dec == 'y'):

            # Start capturing video from cam 0 aka 
            # laptop integraded webcam, or cam 1 aka 
            # external webcam
            cap = cv2.VideoCapture(cam_nr)

            # Check if capture is opened
            if cap.isOpened():

                # read the capture and get 
                # result and frame captured 
                res,frame = cap.read()

                # releasing camera immediately after capturing picture
                cap.release() 

                # if result was succsesful
                if res is True:
                    
                    # self explaining here
                    if frame is not None:

                        cv2.imshow("takenImage",frame)
                        cv2.waitKey(0)
                        print(frame.shape)

                        take_pic.save_pic(frame)
                        
                        break
                else:
                    dec = input("Taking a picture wasn't succsesful!/n do you want to try again? y,n")
                    print(dec )

        return frame