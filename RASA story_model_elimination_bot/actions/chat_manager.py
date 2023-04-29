from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
import json


class ActionChatManager(Action):

    def name(self) -> Text:
        return "action_chat_manager"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('resources/history.json', 'r') as r:
            data = json.load(r)

        completed_questions = data["completed_questions"]

        with open('resources/order.json', 'r') as r:
            data = json.load(r)

        order = data["order"]

        if len(completed_questions) == len(order):
            dispatcher.utter_message(text="You have now answered all the questions. Thank You!")
            return [FollowupAction("action_listen")]

        pending_questions = [i for i in order if i not in completed_questions]
        qn_id = str(pending_questions[0])

        return [SlotSet("qn_id", qn_id), FollowupAction("get_answer_form")]
