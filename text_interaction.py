import requests
import tkinter as tk
from PIL import ImageTk, Image
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
        try:
            return request.json()[0]["text"]
        except:
            return "I'm sorry, I'm facing some technical issues currently"


def main():
    name = "user"
    bot = humanoid(name)

    # GUI for Humanoid
    root = tk.Tk()
    root.title("Text Interface")
    root.geometry("900x150")

    l = tk.Label(root, text = "The Humanoid Project")
    l.config(font =("Courier", 22))
    l.pack()
    
    flag = True
    bot = humanoid(name)
    while flag:
        try:
            curr_l = tk.Label(root, text = "Enter your message and press continue")
            curr_l.config(font =("Courier", 12))
            curr_l.pack()
            inputtxt = tk.Text(root, height = 1.5, width = 60, bg = "light yellow")
            inputtxt.pack()
            user_input = ""
            received = False
            move_ahead = False

            def move():
                nonlocal move_ahead
                move_ahead = True

            def got_message():
                nonlocal inputtxt, received
                nonlocal user_input
                user_input = inputtxt.get("1.0", "end-1c")
                if(len(user_input) > 0):
                    received = True
            
            B = tk.Button(root, text ="Continue", command = got_message)
            B.pack()
            root.update()

            while (not received):
                root.update()

            message = user_input.lower()
            response = bot.send_message(message)

            if(response == "Bye"):
                flag = False 

            elif(response[0] == '&'):
                curr_l.destroy()
                inputtxt.destroy()
                B.destroy()

                curr_l = tk.Label(root, text = response[1:])
                curr_l.config(font =("Courier", 12))
                curr_l.pack()



                B = tk.Button(root, text ="Ask me something else", command = move)
                B.pack()

                window = tk.Tk()#creating window
                window.resizable()#geometry of window
                window.title('The Humanoid Project')#title to window
                tk.Label(window,text="What I saw through my eyes",font=('bold',20)).pack()#label
                
                #creating frame
                frame = tk.Frame(window, width=230, height=200, bg='white')
                frame.pack()

                image3 = ImageTk.PhotoImage(Image.open(image_url), master = window)

                image_label = tk.Label(frame, image=image3) #packing image into the window
                image_label.pack()

                while (not move_ahead):
                    root.update()
                
                curr_l.destroy()
                B.destroy()
                window.destroy()
                
            else:
                curr_l.destroy()
                inputtxt.destroy()
                B.destroy()

                curr_l = tk.Label(root, text = response)
                curr_l.config(font =("Courier", 15))
                curr_l.pack()

                B = tk.Button(root, text ="Ask me something else", command = move)
                B.pack()

                while (not move_ahead):
                    root.update()
                
                curr_l.destroy()
                B.destroy()

        except KeyboardInterrupt:
            print("\nHope you had a nice time! Goodbye\n")
            flag = False


if __name__ == '__main__':
    main()
