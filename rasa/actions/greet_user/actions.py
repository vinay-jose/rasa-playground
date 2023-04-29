# This file contains custom actions which is used to run
# custom Python code.

import requests
import json
import logging
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

# def chat_history(tracker: Tracker) -> None:
#     """Save Chat History To DB"""
#
#     history = tracker.events_after_latest_restart()
#     logger.info(history)
#     logger.info(type(history))
#
#     chat = dict()  # Empty dictionary for saving chat
#     for obj in history:
#         if obj['event'] == 'bot':
#             if obj['text'] is None:
#                 chat.update({obj['event']: obj['data']['custom']['message']})
#             else:
#                 chat.update({obj['event']: obj['text']})
#
#             if obj['data']['buttons'] is not None:
#                 # for item in obj['data']['buttons']:
#                 #     buttons_list.append(item['title'])
#                 buttons_list = list(obj['data']['buttons'][:]['title'])
#                 chat.update({'buttons': buttons_list})
#
#         elif obj['event'] == 'user':
#             chat.update({obj['event']: obj['text']})
#
#         else:
#             pass
#
#         logger.info(chat)
#
#         return None


class ActionMaster(Action):

    def name(self) -> Text:
        return "action_master"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # read this data from ui_message
        company_title = "Abc Ltd"
        SlotSet("company_title", company_title)

        # define bot's name
        bot_name = "Hyreo"
        SlotSet("bot_name", bot_name)

        dispatcher.utter_message(template="utter_welcome", company_title=company_title, bot_name=bot_name)
        dispatcher.utter_message(template="utter_email_request")
        # dispatcher.utter_message(template="utter_warning_1", company_title=company_title, bot_name=bot_name)
        # dispatcher.utter_message(template="utter_warning_2", company_title=company_title, bot_name=bot_name)
        # # return [FollowupAction('communication_preference_form')]
        # buttons = [{'title': 'Send OTP and nudges via email and SMS', 'payload': '/send_info_via_email_and_sms'},
        #            {'title': 'Send OTP and nudges only via email', 'payload': '/send_info_via_email'},
        #            {'title': 'Do not contact me', 'payload': '/do_not_send_info'}]
        # dispatcher.utter_message(template="utter_info_preference_request", payload=buttons)

        return [FollowupAction('action_listen')]


class ActionEmailVerification(Action):

    def name(self) -> Text:
        return "action_email_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")
        """Validate email using regex"""
        email = str(tracker.latest_message["text"])
        logger.info(email)

        # Make a regular expression for validating an Email
        regex1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.match(regex1, email):
            # call API for getting candidate details
            host = 'https://stg-sggsc.hyreo.com/'
            base_url = host + 'ChatBot/'
            url = base_url + 'candidateStatus'
            logger.info(url)
            payload = {
                'userName': 'chatbot',
                'userPassword': '1234',
                'candidateEmail': email
            }

            response = requests.get(url, params=payload, verify=False)
            logger.info(response.status_code)
            r = response.text
            data = json.loads(r)
            logger.info(data.keys())

            eu_citizenship = data['candidates'][0]['isEuropeanNationalist']
            SlotSet("EU_Citizenship", eu_citizenship)

            if

        else:
        return [FollowupAction('conversation_context_form')]
