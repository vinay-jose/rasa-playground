# This files contains your custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import logging

logger = logging.getLogger(__name__)


class ActionAskAnswer(Action):

    def name(self) -> Text:
        return "action_ask_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Call API to get NPS data from DB

        if len("returned list from object"):
            dispatcher.utter_message(text="Pass on the questions as UI message")

        else:

            dispatcher.utter_message(text="Thank You message as text for the user")

            # set the slot using SlotSet method to stop form from running
            return [SlotSet("answer", "blue")]


class ValidateQuestionForm(FormValidationAction):
    """Reference for forms in 2.0: https://www.youtube.com/watch?v=pzvBJtwCW4I"""

    def name(self) -> Text:
        return "validate_question_form"

    def validate_answer(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:

        ans = tracker.latest_message["text"]
        logger.info(ans)

        # Call the other API to save the feedback given by user

        return {"answer": None}


