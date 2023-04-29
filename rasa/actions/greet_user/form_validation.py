from typing import Any, Text, Dict, List

from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import re
import requests
import logging
import json

logger = logging.getLogger(__name__)


class ValidateEmailOtpForm(FormValidationAction):
    """Reference for forms in 2.0: https://www.youtube.com/watch?v=pzvBJtwCW4I"""

    def name(self) -> Text:
        return "validate_email_otp_form"

    def validate_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:

        """Validate email using regex"""
        email = str(tracker.latest_message["text"])
        logger.info(email)

        # Make a regular expression for validating an Email
        regex1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.match(regex1, email):
            # call API for sending otp
            # host = 'https://crm-dev-2.centralindia.cloudapp.azure.com/'
            # base_url = host + 'ChatBot/'
            # host1 = 'http://127.0.0.1:5000'
            # url = host1 + '/sendEmailOTP'
            #
            # # Generate 5-digit OTP using random module
            # generated_otp = ''.join(random.sample('0123456789', 5))
            # logger.info(generated_otp)
            #
            # applicant_id = '16374'
            # logger.info(url)
            # messages = {'email': email, 'otp': generated_otp, 'applicantId': applicant_id}
            # payload = {
            #     'userName': 'chatbot',
            #     'userPassword': '1234',
            #     'messages': messages
            # }
            #
            # response = requests.post(url, json=payload, verify=False)
            # logger.info(response)
            # # logger.info(response.request.body)

            # call API for getting candidate details
            host = 'https://crm-dev-2.centralindia.cloudapp.azure.com/'
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
            # print(r)
            data = json.loads(r)
            logger.info(data)

            return {"email": email}

        else:
            dispatcher.utter_message(text="This is not a valid email id")
            return {"email": None}

    def validate_otp(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:

        """Validate otp using regex"""
        entered_otp = tracker.latest_message["text"]
        logger.info(entered_otp)

        # Make a regular expression for validating 5-digit OTP
        regex2 = r'\b[0-9]{5}\b'

        if re.match(regex2, entered_otp):
            # call API for verifying otp
            base_url = 'https://crm-dev-2.centralindia.cloudapp.azure.com/ChatBot/'
            url = base_url + 'verifyEmailOTP'
            generated_otp = '11555'
            logger.info(url)

            verify = True if entered_otp == generated_otp else False

            if verify:
                dispatcher.utter_message(text="Welcome to Hyreo")
                dispatcher.utter_message(text="How can I help you today?")
                return {"otp": slot_value}

            else:
                dispatcher.utter_message(text="This OTP is incorrect.")
                return {"otp": None}

        else:
            dispatcher.utter_message(text="This OTP is invalid.")
            return {"otp": None}
