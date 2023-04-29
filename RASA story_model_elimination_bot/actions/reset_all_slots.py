from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk.events import AllSlotsReset


class ActionResetAllSlots(Action):

    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
    