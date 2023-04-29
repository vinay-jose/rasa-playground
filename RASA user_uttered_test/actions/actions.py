# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUttered, ActionExecuted


class ActionUtter(Action):

    def name(self) -> Text:
        return "action_utter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Inside action_utter.")
        data = {
            "intent": {
                "name": "user_utterance",
                "confidence": 1.0,
            }
        }

        # evt = UserUttered(text="/user_utterance")

        return [
            ActionExecuted("action_listen"),
            UserUttered(text="/user_utterance", parse_data=data),
        ]
