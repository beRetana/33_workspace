# device.py

from communication import Message, MessageType, InteractionType, Interaction

class Device:

    _network = dict()
    _life_time = 0

    def __init__(self, device_id: int):
        self._id = device_id
        self._alerts = list()
        self._cancellations = list()
        self._propagation_contacts = dict()

    def add_to_network(self) -> None:
        """Adds the class object to the network class attribute."""
        self._network[self.get_id()] = self

    def get_id(self) -> int:
        """Returns the id of the device."""
        return self._id

    def get_formated_alerts(self) -> list[str]:
        """Returns the list of alerts received in a formatted way."""
        formated_alerts = list()
        for alert in self._alerts:
            formated_alerts.append(alert.get_formated_interaction())
        return formated_alerts

    def get_alerts(self) -> list[Interaction]:
        """Returns the list of alerts received."""
        return self._alerts

    def get_formated_cancelled(self) -> list[str]:
        """Returns the list of cancellations in a formatted way."""
        formated_cancels = list()
        for cancel in self._cancellations:
            formated_cancels.append(cancel.get_formated_interaction())
        return formated_cancels

    def get_cancellations(self) -> list[Interaction]:
        """Returns the list of cancellations."""
        return self._cancellations

    def add_propagation_contact(self, device: 'Device', latency: float) -> None:
        """Adds a device and propagation time into a dictionary as a contact list."""
        self._propagation_contacts[device.get_id()] = latency

    def get_propagation_settings(self) -> dict[int:float]:
        """Returns the propagation contact."""
        return self._propagation_contacts

    def get_contacts_latency(self, device_id: int) -> float:
        """Returns the latency of the propagation contact."""
        return self._propagation_contacts[device_id]

    def is_there_cancelled(self, message: Message) -> bool:
        """Returns true if the alert has been cancelled."""
        for cancelled_alert in self._cancellations:
            if message.get_description() == cancelled_alert.get_message().get_description():
                if message.get_time_sent() > cancelled_alert.get_time_sent():
                    return True

        return False

    def receive_message(self, sender: int, message: Message) -> None:
        """Takes in an alert from sender and adds it to list of alerts."""

        # NEED TO TEST WHEN CANCELLED
        sender_latency = self.get_network()[sender].get_contacts_latency(self.get_id())
        if message.get_time_sent() + sender_latency < Device.get_life_time():
            new_message = Message(message.get_message_type(), message.get_description(),
                              message.get_time_sent() + sender_latency)

            interaction = Interaction(new_message, InteractionType.RECEIVED, sender, self._id)

            if new_message.get_message_type() == MessageType.CANCEL:
                self._cancellations.append(interaction)
            else:
                self._alerts.append(interaction)

            if not self.is_there_cancelled(new_message):
                self.propagate(new_message)

    def propagate(self, message: Message) -> None:
        # iterate through list of devices and add time
        if message.get_time_sent() >= Device.get_life_time():
            return

        # ask tmr during lab
        if not self.is_there_cancelled(message):
            for device_id in self.get_propagation_settings():

                interaction = Interaction(message, InteractionType.SENT, self._id, device_id)

                if message.get_message_type() == MessageType.CANCEL:
                    self._cancellations.append(interaction)
                else:
                    self._alerts.append(interaction)

                Device._network[device_id].receive_message(self._id, message)

    @classmethod
    def get_network(cls) -> dict[int: 'Device']:
        """Returns the network dictionary class."""

        return cls._network

    @classmethod
    def set_life_time(cls, life_time: int) -> None:
        """Sets the lifetime of the network."""
        if life_time >= 0:
            cls._life_time = life_time

    @classmethod
    def get_life_time(cls) -> int:
        """Returns the lifetime of the network."""
        return cls._life_time

    @classmethod
    def clear_network(cls) -> None:
        """Clears the network dictionary and registries."""

        cls._network = dict()
        cls._life_time = 0

    @classmethod
    def check_for_anomalies(cls, device: 'Device') -> list[Interaction]:
        """Checks if there is an alert registered after a cancellation."""

        check_list = list()
        list_cancellations = device.get_cancellations()
        list_alerts = device.get_alerts()
        if len(list_cancellations) == 0:
            return list_alerts

        for cancellation in list_cancellations:
            check_list.append(cancellation)
            for alert in list_alerts:
                if alert.get_message().get_description() == cancellation.get_message().get_description():
                    if cancellation.get_time_sent() >= alert.get_time_sent():
                        check_list.append(alert)

        return list(check_list)

    @staticmethod
    def sorter(log_list: list[Interaction]) -> list[Interaction]:
        """Returns a sorted list of interactions."""

        for index in range(len(log_list)-1):
            interaction = log_list[index]
            next_interaction = log_list[index + 1]
            if interaction.get_time_sent() == next_interaction.get_time_sent():
                if interaction.get_message().get_description() == next_interaction.get_message().get_description():
                    if (interaction.get_interaction_type() == InteractionType.SENT) and (
                            next_interaction.get_interaction_type() == InteractionType.RECEIVED):
                        log_list[index + 1] = interaction
                        log_list[index] = next_interaction

        return log_list

    @classmethod
    def return_sorted_registry(cls) -> list[Interaction]:
        """Returns a list of all the interactions in chronological order."""
        communication_registry = list()
        for device_id in cls._network.keys():
            communication_registry += cls.check_for_anomalies(cls._network[device_id])

        communication_registry = sorted(set(communication_registry), key=lambda action: action.get_time_sent())
        return cls.sorter(communication_registry)

    @classmethod
    def get_formated_registry(cls) -> list[str]:
        """Returns a list of all alerts and cancellations in chronological order
        in a format."""

        sorted_list = cls.return_sorted_registry()

        return Interaction.get_formated_interactions(sorted_list)

