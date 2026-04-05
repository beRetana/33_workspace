# communication.py
from enum import Enum

class MessageType(Enum):
    ALERT = 0
    CANCEL = 1

class InteractionType(Enum):
    RECEIVED = 0
    SENT = 1

class Message:

    def __init__(self, message_type: MessageType, description: str, time_sent: float):
        self._message_type = message_type
        self._description = description
        self._time_sent = time_sent

    def get_message_type(self) -> MessageType:
        """Returns the type of message"""
        return self._message_type

    def get_description(self) -> str:
        """Returns the description of the alert."""
        return self._description

    def get_time_sent(self) -> float:
        """Returns the time sent of the alert."""
        return self._time_sent

class Interaction:

    def __init__(self, message: Message, interaction_type: InteractionType, sender_id: int, receiver_id: int):
        self._message = message
        self._interaction_type = interaction_type
        self._sender_id = sender_id
        self._receiver_id = receiver_id
        self._time_sent = message.get_time_sent()

    def get_message(self) -> Message:
        """Returns the message"""
        return self._message

    def get_interaction_type(self) -> InteractionType:
        """Returns the type of interaction"""
        return self._interaction_type

    def get_sender_id(self) -> int:
        """Returns the sender id"""
        return self._sender_id

    def get_receiver_id(self) -> int:
        """Returns the receiver id"""
        return self._receiver_id

    def get_time_sent(self) -> float:
        """Returns the time sent of the alert."""
        return self._time_sent

    def get_formated_interaction(self) -> str:
        """Returns the formated interaction"""
        message_type = self._message.get_message_type()
        match message_type:
            case MessageType.ALERT:
                message_type = "ALERT"
            case MessageType.CANCEL:
                message_type = "CANCELLATION"
        message = ""
        match self._interaction_type:
            case InteractionType.RECEIVED:
                message =  f"@{self._time_sent}: #{self.get_receiver_id()} RECEIVED {message_type} FROM #{self.get_sender_id()}: "
            case InteractionType.SENT:
                message = f"@{self._time_sent}: #{self.get_sender_id()} SENT {message_type} TO #{self.get_receiver_id()}: "
        return message + self._message.get_description()

    @staticmethod
    def get_formated_interactions(interactions_list: reversed | list['Interaction']) -> list[str]:
        """Returns the list of interactions in their formated way"""
        formated_interactions = list()
        for interaction in interactions_list:
            formated_interactions.append(interaction.get_formated_interaction())

        return formated_interactions




