from pathlib import Path
from typing import Any, Text, Dict, List
import time
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from labelDetector import LabelDetector
from imagecapturer import imagecapture
from opac_interface import OPACInterface
import requests
import glob, os

class ActionPick(Action):
    def name(self) -> Text:
        return "action_pick"
    
    def processAccessionNo(self, accessionNumber):
        if str(accessionNumber).isnumeric():
            return "240866"
        else:
            return accessionNumber

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = -1
        
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity'] == 'object':
                name = blob['value']    
        
        outputs = [
            f"&Okay I'll pick up the {name}",
            f"&On my way to pick up the {name}",
            f"&One {name}? coming right up!"
        ]
        
        json_response = {"message": ""}
        if(name == -1):
            json_response["message"] =  json_response["message"] + "Sorry, I didn't understand, you didn't mention what to pick up properly or this object is not supported. "
            json_response["status"] = 404
        else:
            labelDetector = LabelDetector()
            imageCapture = imagecapture()
            opacInterface = OPACInterface()

            MAX_LATENCY = 10
            isCached = True
            start_time = time.perf_counter()
            
            files_books = glob.glob("./crops/Book/*")
            files_labels = glob.glob("./crops/Label/*")
            for f in files_books:
                os.remove(f)
            for f in files_labels:
                os.remove(f)

            # while(time.perf_counter() - start_time <= MAX_LATENCY):
            if(imageCapture.click()):
                flag, labels = labelDetector.run(f'./captures/latestimg.png') 
                json_response["message"] = json_response["message"] + "This is what I saw. "
                json_response["isImage"] = True
                if(flag == 0):
                    print("No labels here")
                    json_response["message"] = json_response["message"] + "No object were detected! "
                    json_response["status"] = 205
                    # continue
                else:
                    print(labels)     
                    json_response["message"] = json_response["message"] + "I found a book! "
                    foundLabel = False
                    for label in labels:
                        res = requests.post("http://localhost:5000/tests/endpoint", json={"path": label})
                        print(res)
                        if(res.status_code == 200):
                            json_response["accessionNo"] = self.processAccessionNo(res.text)
                            print("Accession No. :", res.text)
                            book_details = opacInterface.get_book_details(res.text, cached=isCached)
                            print(book_details)
                            json_response["book_details"] = book_details
                            json_response["status"] = 200
                            foundLabel = True
                        else:
                            print("Accession no. not found for this book!")
                            # json_response["message"] = json_response["message"] + "I could not get its details. "
                            json_response["status"] = 204
                    if(foundLabel):
                        json_response["message"] = json_response["message"] + "Here are its details: "
                    else:
                        json_response["message"] = json_response["message"] + "There are no labels in the image or the label is blurred"
                    # break                  
            else:
                json_response["message"] = json_response["message"] + "My eyes are not working! "
                json_response["status"] = 404

            dispatcher.utter_message(json_message=json_response) 
        
        return []

class ActionKeep(Action):
    def name(self) -> Text:
        return "action_keep"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = -1
        destination = -1
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity'] == 'object':
                name = blob['value'] 
            if blob['entity'] == 'destination':
                destination = blob['value']
        if(name ==-1 or destination == -1):
            dispatcher.utter_message(text=f"Sorry, I didn't understand. It could be either because the instruction is not supported by me, or you didn't mention what to keep or where to keep.")
        else:
            dispatcher.utter_message(text=f"Okay I'll keep the {name} on the {destination}")
        return []