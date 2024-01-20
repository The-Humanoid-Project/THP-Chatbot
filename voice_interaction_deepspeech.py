from __future__ import absolute_import, division, print_function
import numpy as np
import wave
from deepspeech import Model, version
from pipes import quote
import requests
import pyaudio
from gtts import gTTS
import playsound
import os
import tkinter as tk
import time
 
# Reference : https://deepspeech.readthedocs.io/en/r0.9/Python-Examples.html

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "captures/latestrecording.wav"
device_index = 0

#Rasa API endpoint
url = "http://localhost:5002/webhooks/rest/webhook"

#humanoid bot
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
            return "I had a problem interpreting what you told"
    
    def speak(self, message):
        voice = gTTS(text=message, lang='en', slow=False)
        filename = "response.mp3"
        voice.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

def wait_for_trigger(ds, bot, root):
    root.update()
    try:
        #triggerword detection
        message = ""
        while message != "activate":
            #recording using pyaudio
            #start recording here
            curr_l = tk.Label(root, text = "Say Activate")
            curr_l.config(font =("Courier", 12))
            curr_l.pack()
            root.update()
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
            #recording terminates here
            audio_outp = np.frombuffer(binary, np.int16)
            #using deepspeech speech to text
            message = str(ds.stt(audio_outp)).lower()
            curr_l.destroy()
            curr_l = tk.Label(root, text = '"' + message + '" was heard')
            curr_l.config(font =("Courier", 12))
            curr_l.pack()
            root.update() 
            time.sleep(0.5)
            curr_l.destroy()
            root.update()
        
        curr_l.destroy()
        curr_l = tk.Label(root, text = "Hello, Speak Now")
        curr_l.config(font =("Courier", 12))
        curr_l.pack()
        root.update() 
        Recordframes = []
        audio_class = pyaudio.PyAudio()
        stream = audio_class.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = 0,
                    frames_per_buffer=CHUNK)
        for i in range(0, int(RATE / CHUNK * (RECORD_SECONDS+2))):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        
        binary = b''.join(Recordframes) 
        stream.stop_stream()
        stream.close()
        audio_class.terminate()
        #recording terminates here
        audio_outp = np.frombuffer(binary, np.int16)
        #using deepspeech speech to text
        message = str(ds.stt(audio_outp)).lower()

        curr_l.destroy()
        curr_l = tk.Label(root, text = '"' + message + '" was heard')
        curr_l.config(font =("Courier", 12))
        curr_l.pack()
        root.update() 
        bot.speak(bot.send_message(message))
        curr_l.destroy()
        root.update()
        wait_for_trigger(ds, bot, root)
    except KeyboardInterrupt:
        root.quit()
        print("\nShutting Down Humanoid")

def main():
    model = "deepspeech/deepspeech-0.9.3-models.pbmm"
    scorer = "deepspeech/deepspeech-0.9.3-models.scorer"
    audio = "captures/latestrecording.wav"
    beam_width = 500
    ds = Model(model)
    if beam_width:
        ds.setBeamWidth(beam_width)

    if scorer:
        ds.enableExternalScorer(scorer)
    name = "user"
    bot = humanoid(name)

    # GUI for Humanoid
    root = tk.Tk()
    root.title("The Humanoid Project GUI")
    root.geometry("300x250")

    l = tk.Label(root, text = "The Humanoid Project")
    l.config(font =("Courier", 14))
    l.pack()
    wait_for_trigger(ds, bot, root)

if __name__ == '__main__':
    main()