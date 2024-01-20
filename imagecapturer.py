import cv2
import os

class imagecapture:
    def initialize(self):
        self.cam = cv2.VideoCapture(0)
    
    def click(self):
        self.initialize()
        result, image = self.cam.read()
        if not os.path.exists('captures'):
            os.makedirs('captures')
        cv2.imwrite('captures/latestimg.png', image)
        cv2.imwrite('frontend/src/assets/latestimg.png', image)
        self.closecam()
        return result
        
    def closecam(self):
        self.cam.release()