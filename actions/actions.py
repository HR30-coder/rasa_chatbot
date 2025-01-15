# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

# class ActionProvidePhone(Action):
#     def name(self):
#         return "action_provide_phone"

#     def run(self, dispatcher, tracker, domain):
#         # Extract the phone number from the tracker
#         user_phone = next(tracker.get_latest_entity_values("number"), None)

#         # Respond with the phone number
#         if user_phone:
#             dispatcher.utter_message(f"Got it! Your phone number is {user_phone}.")
#         else:
#             dispatcher.utter_message("Sorry, I couldn't find your phone number.")
        
#         return []
    

# class ActionSayUser(Action):
#     def name(self):
#         return "action_say_user"

#     def run(self, dispatcher, tracker, domain):
#         # Extract the phone number from the tracker


#         print("Slots:", tracker.slots)
  
#         edpoint = tracker.get_slot("endpoint")
#         src = tracker.get_slot("source")
        
#         print(edpoint," :: ",src)

        
#         dispatcher.utter_message(f"Got your data ! Your source is {src} your endpoint is {edpoint}")

        
#         return [
#             SlotSet("endpoint", None),
#             SlotSet("source", None),
#         ]
    

    