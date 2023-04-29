# This files contains your custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import FollowupAction

from response_retriever import Response
import logging

logger = logging.getLogger(__name__)


class ActionUtter(Action):

    def name(self) -> Text:
        return "action_utter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        intent = tracker.latest_message["intent"].get("name")
        status_id = 0
        utter_msg = Response.response_retriever(intent, status_id)
        user_id = '1234'  # to be read from ui_data.json

        key = 1111  # randomly generated identifier
        feedback = {"response": None, "key": key}
        dispatcher.utter_message(text=utter_msg, attachment=user_id, custom=feedback)

        return None


class ActionSaveChat(Action):

    def name(self) -> Text:
        return "action_save_chat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        history = tracker.events_after_latest_restart()
        logger.info(history)
        logger.info(type(history))

        return None


class ActionDefaultFallback(Action):

    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):

        dispatcher.utter_message(text="Could you please rephrase that?", attachment=intent)

        return [FollowupAction('action_listen')]


