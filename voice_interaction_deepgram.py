from __future__ import absolute_import, division, print_function
import numpy as np
from deepgram import Deepgram
import numpy as np
import asyncio
import requests
import pyaudio
from gtts import gTTS
import playsound
import os
import tkinter as tk
import time
from scipy.io.wavfile import write

# The Audio formats
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "captures/latestrecording.wav"
device_index = 0

#Deepgram stuff
AUDIO_URL = WAVE_OUTPUT_FILENAME
DEEPGRAM_API_KEY = 'bf2e79ea687e52bfb78f976ee939e6cff78ab008'
dg_client = Deepgram(DEEPGRAM_API_KEY)
source = {'url': AUDIO_URL}
options = { "punctuate": False, "model": "general", "language": "en-IN", "tier": "base"}

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
    
    def speak(self, message):
        voice = gTTS(text=message, lang='en', slow=False)
        filename = "response.mp3"
        voice.save(filename)
        playsound.playsound(filename)
        os.remove(filename)


def record_voice():
    Recordframes = []
    audio_class = pyaudio.PyAudio()
    stream = audio_class.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,input_device_index = device_index,
                frames_per_buffer=CHUNK)

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)

    binary = b''.join(Recordframes) 
    stream.stop_stream()
    stream.close()
    audio_class.terminate()
    audio_outp = np.frombuffer(binary, np.int16)
    write(WAVE_OUTPUT_FILENAME, RATE, audio_outp)

async def main():
    name = "user"
    bot = humanoid(name)

    # GUI for Humanoid
    root = tk.Tk()
    root.title("Voice Interface")
    root.geometry("900x150")

    l = tk.Label(root, text = "The Humanoid Project")
    l.config(font =("Courier", 22))
    l.pack()
    
    flag = True
    bot = humanoid(name)
    while flag:
        try:
            curr_l = tk.Label(root, text = "Press Continue to Talk")
            curr_l.config(font =("Courier", 12))
            curr_l.pack()
            received = False
            move_ahead = False

            def move():
                nonlocal move_ahead
                move_ahead = True

            def got_message():
                nonlocal curr_l
                nonlocal received
                curr_l.destroy()
                curr_l = tk.Label(root, text = "Speak Now")
                curr_l.config(font =("Courier", 12))
                curr_l.pack()
                root.update()
                record_voice()
                received = True
                curr_l.destroy()
                
            
            B = tk.Button(root, text ="Continue", command = got_message)
            B.pack()
            root.update()

            while (not received):
                root.update()

            with open(WAVE_OUTPUT_FILENAME, 'rb') as audio:
                # ...or replace mimetype as appropriate
                curr_l.destroy()
                curr_l = tk.Label(root, text = "Analyzing what you said")
                curr_l.config(font =("Courier", 12))
                curr_l.pack()
                root.update()
                source = {'buffer': audio, 'mimetype': 'audio/wav'}
                response = await dg_client.transcription.prerecorded(source, options)
                message = response["results"]["channels"][0]["alternatives"][0]["transcript"]
                curr_l.destroy()
            
            curr_l = tk.Label(root, text = '"' + message + '" was heard')
            curr_l.config(font =("Courier", 12))
            curr_l.pack()
            root.update()

            response = bot.send_message(message)
            
            time.sleep(1)

            if(response == "Bye"):
                flag = False 

            elif(response[0] == '&'):
                curr_l.destroy()
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
    asyncio.run(main())