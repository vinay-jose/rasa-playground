import logging

logger = logging.getLogger(__name__)


class UIMessage:
    def __init__(self):
        self.ui_message = {}

    def get_ui_message(self):
        return self.ui_message

    def set_ui_message(self, message):
        self.ui_message = message
