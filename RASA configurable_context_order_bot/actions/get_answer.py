from typing import Any, Text, Dict, List

from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json


class ValidateGetAnswerForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_get_answer_form"

    def validate_answer(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:

        answer = tracker.latest_message["text"]
        qn_id = tracker.get_slot("qn_id")
        with open('resources/answers.json', 'r+') as file:
            data = json.load(file)
            data[qn_id] = answer  # <--- add `id` value.
            file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, file, indent=4)
            file.truncate()  # remove remaining part

        with open('resources/history.json', 'r+') as file:
            data = json.load(file)
            data["completed_questions"].append(int(qn_id))  # <--- add `id` value.
            file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, file, indent=4)
            file.truncate()  # remove remaining part

        return {"answer": answer}
