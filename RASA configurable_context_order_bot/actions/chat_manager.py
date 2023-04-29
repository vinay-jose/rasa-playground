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

        with open('resources/questions.json', 'r') as r:
            data = json.load(r)

        question = data[qn_id]
        next_action = "utter_ask_" + question

        return [SlotSet("qn_id", qn_id), FollowupAction(next_action)]


class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
