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
    

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


class ActionDocumentSearch(Action):
    def name(self) -> str:
        return "action_document_search"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> list:
        # Extract user query from the conversation
        query = tracker.latest_message.get("text")

        # API endpoint to fetch data
        api_url = "http://localhost:3000/askWoStream"
        # headers = {"Content-Type": "application/json"}

        # Prepare request body
        payload = {"query": query}
        try:
            # Make a POST request to the API
            response = requests.post(api_url, json=payload)

            # Check if the response was successful
            if response.status_code == 200:
                data = response.json()  # Assuming the response contains JSON data
                important_data = data.get("message", "Sorry i dont have anything in my knowledge to answer this")

                # Send the response back to the user
                dispatcher.utter_message(text=f"{important_data}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the data at the moment. Please try again later.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        # try:
        #     # Make the POST request to the API with streaming enabled
        #     with requests.post(api_url, json=payload, headers=headers, stream=True) as response:
        #         # Check if the response is successful
        #         if response.status_code == 200:
        #             # Streaming the response in chunks
        #             for chunk in response.iter_lines():
        #                 # Decode and filter out empty chunks
        #                 if chunk:
        #                     chunk_data = chunk.decode('utf-8')
        #                     dispatcher.utter_message(text=chunk_data)  # Send each chunk to the user
        #         else:
        #             dispatcher.utter_message(text="Sorry, I could not fetch the information at the moment.")
        # except requests.exceptions.RequestException as e:
        #     dispatcher.utter_message(text=f"An error occurred: {e}")
        return []

class ActionFetchImportantData(Action):
    def name(self) -> str:
        return "action_fetch_important_data"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Extract the entity values from the tracker
        data_type_user = next(tracker.get_latest_entity_values("user"), None)
        data_type_subprocess = next(tracker.get_latest_entity_values("subprocess"), None)
        data_type_downtime = next(tracker.get_latest_entity_values("downtime"), None)
        
        interval = next(tracker.get_latest_entity_values("DATE"), None)

        data_type = ""

        if data_type_user:
            print("date_type : "+data_type_user)
            data_type = "USER"
        if data_type_subprocess:
            print("date_type : "+data_type_subprocess)
            data_type = "KPI"
        if data_type_downtime:
            data_type = "DOWNTIME"
            print("date_type : "+data_type_downtime)
        if interval:
            print("interval is : "+interval)

        # If we don't have both required entities, ask the user for more details
        if data_type == "" or not interval:
            dispatcher.utter_message(text="I need both the data type (user, subprocess, downtime) and the interval (day, week, month). Could you please provide them?")
            return []


        # dispatcher.utter_message(text="I recieved data type (user, subprocess, downtime) and the interval (day, week, month). thanks !!")

        # return []
    
        # Prepare the payload for the API request
        payload = {
            "type": data_type,
            "interval": interval
        }

        # # Define the API URL
        api_url = "http://localhost:3000/metrics"  # Update with the correct API URL if needed
        
        try:
            # Make a POST request to the API
            response = requests.post(api_url, json=payload)

            # Check if the response was successful
            if response.status_code == 200:
                data = response.json()  # Assuming the response contains JSON data
                important_data = data.get("data", "No data available")

                # Send the response back to the user
                dispatcher.utter_message(text=f"The requested data: {important_data}")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the data at the moment. Please try again later.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")
        
        return []

class ActionHandleFAQQuery(Action):
    def name(self) -> str:
        return "action_handle_faq_query"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Create a list to collect all responses
        final_response = []

        # Extract the relevant entities from the tracker
        downtime = next(tracker.get_latest_entity_values("downtime"), None)
        subprocess = next(tracker.get_latest_entity_values("subprocess"), None)
        support = next(tracker.get_latest_entity_values("support"), None)

        # Append response for downtime entity
        if downtime:
            final_response.append("To track downtime in the KPI portal, go to the 'Downtime Tracking' section.")
        
        # Append response for subprocess entity
        if subprocess:
            final_response.append("You can track them under the 'Processes Overview' section.")

        # Append response for support entity
        if support:
            final_response.append("For support with the KPI portal, you can contact our support team at support@kpiportal.com or visit the 'Help' section in the portal.")
        
        # If no relevant entities are found, append a fallback response
        if not (downtime or subprocess or support):
            final_response.append("I'm sorry, I couldn't find the information you were looking for. Could you please clarify your question?")
        
        # Join all the appended responses into a single message and send it
        dispatcher.utter_message(text=" ".join(final_response))

        return []

    