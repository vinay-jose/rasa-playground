from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

logger = logging.getLogger(__name__)


class ActionCreateSlot(Action):

    def name(self) -> Text:
        return "action_create_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Inside Create Slot")
        obj = {
            "status": 1,
            "candidates": [
                {
                    "companyId": 2,
                    "companyName": "Societie Generale",
                    "jdId": 7724,
                    "jdTitle": "Senior Analyst - Reference Management",
                    "jobRequistionnumber": "22000DUR",
                    "applicantId": 186582,
                    "candidateId": 4517466,
                    "candidateName": "Harika",
                    "phone": "919666272834",
                    "email": "harikateegala28@gmail.com",
                    "recruiterName": "Surajbhan Ranawat",
                    "noticePeriod": 0,
                    "conversationContexts": [],
                    "postOfferEngagements": [
                        {
                            "postOfferEngagementId": 1537,
                            "noticePeriod": 15,
                            "day": 0,
                            "engagementContextId": 23,
                            "engagementContext": {
                                "engagementContextId": 23,
                                "engagementContext": "E34",
                                "engagementContextDescription": "Rejected",
                                "mandatory": 'true'
                            },
                            "value": 4
                        }
                    ],
                    "applicantIntervention": [],
                    "jobStatus": 'true',
                    "consentGiven": "false",
                    "isEuropeanNationalist": "false",
                    "isSubscribeNudges": "false",
                    "isSubscribeSMS": "false",
                    "applicantAddressConfirmation": 'false',
                    "applicantAddress": ""
                }
            ]
        }

        return [SlotSet("test", obj)]


class ActionDisplaySlot(Action):

    def name(self) -> Text:
        return "action_display_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        data = tracker.get_slot("test")
        logger.info(data)

        dispatcher.utter_message(text="Inside Display Slot")
        return []
