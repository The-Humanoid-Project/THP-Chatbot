import cv2

class imagecapture:
    def initialize(self):
        self.cam = cv2.VideoCapture(0)
    
    def click(self):
        self.initialize()
        result, image = self.cam.read()
        cv2.imwrite('captures/latestimg.png', image)
        self.closecam()
        return result
        
    def closecam(self):
        self.cam.release()