from pathlib import Path
import random
from typing import Any, Text, Dict, List
import time
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from yolov5.detect import objectdetector

class ActionPick(Action):
    def name(self) -> Text:
        return "action_pick"

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
        if(name == -1):
            dispatcher.utter_message(text=f"Sorry, I didn't understand, you didn't mention what to pick up properly or this object is not supported")
        else:
            yolo = objectdetector()
            timeout = time.time() + 20
            while True:
                if(time.time() > timeout):
                    break
                else:
                    outp = yolo.main(obj=name)
                    print(outp)
                    if(outp[0] == 0):
                        dispatcher.utter_message(text=outp[1])
                        break
                    elif(outp[0] == 2):
                        dispatcher.utter_message(text=random.choice(outputs))
                        break
                    elif(outp[0]==4):
                        dispatcher.utter_message(text=outp[1])
                        break
            if(outp[0] == 1):
                dispatcher.utter_message(text=outp[1])
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
