# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# from dotenv import load_dotenv
# from pathlib import Path

import os
import logging

logger = logging.getLogger(__name__)


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")
        # env_path = Path('.') / '.env'
        # load_dotenv(dotenv_path=env_path)
        # '''os.getenv() used to read varibles from .env file'''
        # ticket_url = os.getenv("all_tikcket_url")
        # print(ticket_url)
        env_var = os.environ
        for i in dict(env_var):
            print(i)
            # print(j)
        # logger.info(dict(env_var))

        return []
