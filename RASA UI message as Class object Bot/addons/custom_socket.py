import logging
import warnings
import uuid
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from socketio import AsyncServer
from typing import Optional, Text, Any, List, Dict, Iterable, Callable, Awaitable
import time
import json
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa_sdk import Action
import asyncio

logger = logging.getLogger(__name__)

global que1


class SocketBlueprint(Blueprint):
    def __init__(self, sio: AsyncServer(async_mode="sanic"), socketio_path, *args, **kwargs):
        self.sio = sio
        self.socketio_path = socketio_path
        super().__init__(*args, **kwargs)

    def register(self, app, options) -> None:
        self.sio.attach(app, self.socketio_path)
        super().register(app, options)


class SocketIOOutput(OutputChannel):

    @classmethod
    def name(cls) -> Text:
        return "socketio"

    def __init__(self, sio, sid, bot_message_evt) -> None:
        self.sio = sio
        self.sid = sid
        self.bot_message_evt = bot_message_evt

    async def _send_message(self, socket_id: Text, response: Any) -> None:
        """Sends a message to the recipient using the bot event."""

        await self.sio.emit(self.bot_message_evt, response, room=socket_id)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a message through this channel."""
        time.sleep(2)
        message = {"message": text, "userName": recipient_id, "identifier": "9051"}
        await self._send_message(self.sid, message)
        # chat_history2(message['message'], recipient_id)

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image to the output"""

        message = {"attachment": {"type": "image", "payload": {"src": image}}}
        await self._send_message(self.sid, message)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Sends buttons to the output."""

        message = {"message": text, "buttons": [], "userName": recipient_id, "identifier": "9050"}

        for button in buttons:
            message["buttons"].append(
                {
                    "content_type": "text",
                    "title": button["title"],
                    "payload": button["payload"],
                }
            )

        await self._send_message(self.sid, message)

    async def send_elements(
        self, recipient_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        """Sends elements to the output."""

        for element in elements:
            message = {
                "attachment": {
                    "type": "template",
                    "payload": {"template_type": "generic", "elements": element},
                }
            }

            await self._send_message(self.sid, message)

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends custom json to the output"""
        json_message['userName'] = recipient_id
        time.sleep(2)
        await self._send_message(self.sid, json_message)

    async def send_attachment(
        self, recipient_id: Text, attachment: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends an attachment to the user."""
        await self._send_message(self.sid, {"attachment": attachment})


class SocketIOInput(InputChannel, Action):
    """A socket.io input channel."""

    @classmethod
    def name(cls) -> Text:
        return "socketio"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        credentials = credentials or {}
        return cls(
            credentials.get("user_message_evt", "user_uttered"),
            credentials.get("bot_message_evt", "bot_uttered"),
            credentials.get("namespace"),
            credentials.get("session_persistence", False),
            credentials.get("socketio_path", "/socket.io"),
        )

    def __init__(
        self,
        user_message_evt: Text = "user_uttered",
        bot_message_evt: Text = "bot_uttered",
        namespace: Optional[Text] = None,
        session_persistence: bool = False,
        socketio_path: Optional[Text] = "/socket.io"
    ):
        self.bot_message_evt = bot_message_evt
        self.session_persistence = session_persistence
        self.user_message_evt = user_message_evt
        self.namespace = namespace
        self.socketio_path = socketio_path

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        # Workaround so that socketio works with requests from other origins.
        # https://github.com/miguelgrinberg/python-socketio/issues/205#issuecomment-493769183
        sio = AsyncServer(async_mode="sanic", cors_allowed_origins=[])

        socketio_webhook = SocketBlueprint(
            sio, self.socketio_path, "socketio_webhook", __name__
        )

        @socketio_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @sio.on("connect", namespace=self.namespace)
        async def connect(sid: Text, _) -> None:
            logger.debug(f"User {sid} connected to socketIO endpoint.")
        # ------------------------------------------------------------------------


        @sio.on("disconnect", namespace=self.namespace)
        async def disconnect(sid: Text) -> None:
            print("DISCONNECTED---------------------------99999999999999999999999")
            initial_chat = {

                "company": "",
                "id": "",
                "chatDate": "",
                "eventId": "",
                "candidateId": "",
                "chat": []

            }
            chat={}
            json_object = json.dumps(initial_chat, indent=4)
            with open('chat_log.json', 'w') as outfile:
                outfile.write(json_object)

            logger.debug(f"User {sid} disconnected from socketIO endpoint.")

        @sio.on("session_request", namespace=self.namespace)
        async def session_request(sid: Text, data: Optional[Dict]):

            if data is None:
                data = {}
            if "session_id" not in data or data["session_id"] is None:
                data["session_id"] = uuid.uuid4().hex
            await sio.emit("session_confirm", data["session_id"], room=sid)
            logger.debug(f"User {sid} connected to socketIO endpoint.")

        @sio.on(self.user_message_evt, namespace=self.namespace)
        async def handle_message(sid: Text, data: Dict) -> Any:
            output_channel = SocketIOOutput(sio, sid, self.bot_message_evt)

            if self.session_persistence:
                if not data.get("session_id"):
                    warnings.warn(
                        "A message without a valid sender_id "
                        "was received. This message will be "
                        "ignored. Make sure to set a proper "
                        "session id using the "
                        "`session_request` socketIO event."
                    )
                    return
                sender_id = data["session_id"]
            else:
                sender_id = data["session_id"]

            # metadata = {
            #     "existingUsername": data.get("existingUsername", None),
            #     "userZone": data.get("userZone", None),
            #     "userTime": data.get("userTime", None)
            # }

            # message = UserMessage(
            #     data["message"], output_channel, sender_id, input_channel=self.name(), metadata=metadata
            # )

            message = UserMessage(
                data["message"], output_channel, sender_id, input_channel=self.name(), metadata=data
            )
            # json_object = json.dumps(data, indent=4)
            # # Writing to sample.json
            # with open("ui_message.json", "w") as outfile:
            #     outfile.write(json_object)

            await on_new_message(message)

            await asyncio.sleep(5)

        return socketio_webhook
