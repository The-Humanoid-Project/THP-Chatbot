import requests
import os

curr_loc = os.getcwd()
url = "http://localhost:5002/webhooks/rest/webhook"
image_url = curr_loc+"/yolov5/detections/latest/latestimg.png"


class humanoid:
    def __init__(self, user):
        username = user
        self.obj = {"sender":username}
    
    def send_message(self, message):
        self.obj["message"] = message
        request = requests.post(url, json = self.obj)
        print(request.json())

if __name__ == '__main__':
    bot = humanoid('user')
    bot.send_message('get the book')

