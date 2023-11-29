from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from typing import Any, Text, Dict, List


from rasa_sdk.events import UserUtteranceReverted



import httpx

from azure.cosmos import CosmosClient



import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Access environment variables
endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")

client = CosmosClient(endpoint, key)


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # # Replace 'http://localhost:8000' with the URL of your FastAPI server
        # url = 'http://localhost:8000'

        # # Define the data to be sent in the request (if any)
        # data = {"key": "value"}

        # # Make a GET request
        # response = httpx.get(url + '/test', params=data)

        # # Make a POST request
        # # response = httpx.post(url + '/endpoint', json=data)

        # # Check if the request was successful (status code 200)
        # if response.status_code == 200:
        #     print("Request was successful")
        #     print("Response content:", response.text)
        # else:
        #     print(f"Request failed with status code {response.status_code}")
        #     print("Error message:", response.text)

        # dispatcher.utter_message(text=f"{response.text}")

        dispatcher.utter_message(text="hello word")


        return []
    

class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:



        dispatcher.utter_message(text="Good bye")
                    

        return []
    

class ActionTesting(Action):

    def name(self) -> Text:
        return "action_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        database_name = "test"
        container_name = "sample"

        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        category = 'personal'
        name = 'home'



        query = f"SELECT * FROM c WHERE c.category = '{category}' and c.name = '{name}'"
        items = list(container.query_items(query, enable_cross_partition_query=True))

        data = []


        for item in items:
            data.append(item)
            print(item)

        dispatcher.utter_message(text=f"{data}")
                    

        return []
    

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "custom_fallback_action"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        print("im inside call back function")

        dispatcher.utter_message(template="utter_default")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]

        return []

    


