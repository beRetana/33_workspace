# test_device.py
import unittest

from communication import Message, MessageType
from device import Device


class TestDevice(unittest.TestCase):

    def setUp(self):
        Device.clear_network()
        Device.set_life_time(4000)
        self._device_one = Device(1)
        self._device_two = Device(2)
        self._device_zero = Device(0)
        self._network = Device.get_network()

    def test_network_is_empty(self):
        self.assertEqual(dict(), self._network)

    def test_network_has_one_device_of_the_right_id(self):
        self._device_one.add_to_network()
        self.assertEqual(self._network[self._device_one.get_id()], self._device_one)

    def test_alerts_received_is_empty_at_start(self):
        self.assertEqual(list(), self._device_one.get_formated_alerts())

    def test_alerts_received_contains_one(self):
        Device.set_life_time(351)
        self._device_zero.add_to_network()
        self._device_one.add_to_network()
        self._device_zero.add_propagation_contact(self._device_one, 0)
        alert = Message(MessageType.ALERT, "Test_Alert_1", 0)
        self._device_one.receive_message(0, alert)
        alert_format = f"@0: #1 RECEIVED ALERT FROM #0: Test_Alert_1"
        self.assertEqual(alert_format, self._device_one.get_formated_alerts()[0])

    def test_alerts_received_contains_ten(self):
        alerts_list = list()
        self._device_zero.add_to_network()
        self._device_one.add_to_network()
        self._device_zero.add_propagation_contact(self._device_one, 100)

        for number in range(1, 11):
            alerts_list.append(Message(MessageType.ALERT,f"Test_Alert_{number}", number*100))

        expected = list()
        for alert in alerts_list:
            self._device_one.receive_message(0, alert)
            expected.append(f"@{alert.get_time_sent()+100}: #1 RECEIVED ALERT FROM #0: {alert.get_description()}")

        self.assertEqual(expected, self._device_one.get_formated_alerts())

    def test_cancellations_received_is_empty_at_start(self):
        self._device_zero.add_to_network()
        self._device_zero.add_propagation_contact(self._device_one, 0)
        cancellation = Message(MessageType.CANCEL, "Test_Alert", 340)
        self._device_one.receive_message(0, cancellation)
        cancellation_format = "@340: #1 RECEIVED CANCELLATION FROM #0: Test_Alert"
        self.assertEqual([cancellation_format], self._device_one.get_formated_cancelled())

    def test_check_for_anomalies_no_cancellations(self):
        self._device_one.add_to_network()

    def test_return_sorted_registry_no_cancellations(self):
        device_three = Device(3)
        self._device_zero.add_to_network()
        self._device_one.add_to_network()
        self._device_two.add_to_network()
        device_three.add_to_network()

        self._device_zero.add_propagation_contact(self._device_one, 0)
        self._device_two.add_propagation_contact(self._device_one, 0)
        device_three.add_propagation_contact(self._device_one, 0)

        alert_1 = Message(MessageType.ALERT, "Test_Alert_1", 340)
        alert_2 = Message(MessageType.ALERT,"Test_Alert_2", 0)
        alert_3 = Message(MessageType.ALERT,"Test_Alert_3", 3000)

        self._device_one.receive_message(0,alert_1)
        self._device_one.receive_message(2, alert_3)
        self._device_one.receive_message(3,alert_2)

        cancel_list = {3:alert_2, 0:alert_1, 2:alert_3}
        expected = list()

        for cancel in cancel_list.keys():
            expected.append(
                f"@{cancel_list[cancel].get_time_sent()}: #1 RECEIVED ALERT FROM #{cancel}: {cancel_list[cancel].get_description()}")
        interactions_list = Device.get_formated_registry()
        self.assertEqual(expected, interactions_list)

    def test_return_sorted_registry_with_cancellations(self):
        self._device_one.add_to_network()

        alert_1 = Message(MessageType.ALERT, "Test_Alert_1", 340)
        alert_2 = Message(MessageType.ALERT, "Test_Alert_2", 0)
        alert_3 = Message(MessageType.ALERT, "Test_Alert_3", 5000)

        cancellation_1 = Message(MessageType.CANCEL,"Test_Alert_1", 400)
        cancellation_2 = Message(MessageType.CANCEL,"Test_Alert_2", 5)
        cancellation_3 = Message(MessageType.CANCEL,"Test_Alert_3", 3500)

        list_devices = [self._device_two, self._device_zero]

        for index in range(3, 7):
            list_devices.append(Device(index))

        for device in list_devices:
            device.add_to_network()
            device.add_propagation_contact(self._device_one, 0)

        self._device_one.receive_message(2,alert_1)
        self._device_one.receive_message(2, alert_2)
        self._device_one.receive_message(3, alert_3)

        self._device_one.receive_message(4,cancellation_1)
        self._device_one.receive_message(5,cancellation_2)
        self._device_one.receive_message(6,cancellation_3)

        expected = list()
        expected.append(
            f"@{alert_2.get_time_sent()}: #1 RECEIVED ALERT FROM #{2}: {alert_2.get_description()}")
        expected.append(
            f"@{cancellation_2.get_time_sent()}: #1 RECEIVED CANCELLATION FROM #{5}: {cancellation_2.get_description()}")
        expected.append(
            f"@{alert_1.get_time_sent()}: #1 RECEIVED ALERT FROM #{2}: {alert_1.get_description()}")
        expected.append(
            f"@{cancellation_1.get_time_sent()}: #1 RECEIVED CANCELLATION FROM #{4}: {cancellation_1.get_description()}")
        expected.append(
            f"@{cancellation_3.get_time_sent()}: #1 RECEIVED CANCELLATION FROM #{6}: {cancellation_3.get_description()}")

        interactions_list = Device.get_formated_registry()

        self.assertEqual(expected, interactions_list)

    def test_add_propagation_contact_empty_at_start(self):
        self.assertEqual(self._device_one.get_propagation_settings(), dict())

    def test_add_propagation_contact_not_empty(self):
        self._device_one.add_to_network()
        self._device_two.add_to_network()

        device_two_id = 2

        latency = 750

        self._device_one.add_propagation_contact(self._network[device_two_id], latency)

        setting = self._device_one.get_propagation_settings()

        expected = {device_two_id: latency}

        self.assertEqual(expected, setting)

    def test_network_life_time(self):
        Device.clear_network()
        self.assertEqual(0,Device.get_life_time())
        Device.set_life_time(2000)
        self.assertEqual(2000,Device.get_life_time())

    def test_propagation_with_one_other_device_and_one_alert(self):
        self._device_two.add_to_network()
        self._device_one.add_to_network()

        Device.set_life_time(3500)

        self._device_one.add_propagation_contact(self._network[self._device_two.get_id()], 500)
        self._device_two.add_propagation_contact(self._network[self._device_one.get_id()], 750)
        cancellation_1 = Message(MessageType.CANCEL, "Test_Alert_1", 2000)
        self._device_one.propagate(cancellation_1)
        self._device_one.propagate(Message(MessageType.ALERT, "Test_Alert_1", 450))

        interactions_list = Device.get_formated_registry()

        expected = list()
        expected.append("@450: #1 SENT ALERT TO #2: Test_Alert_1")
        expected.append("@950: #2 RECEIVED ALERT FROM #1: Test_Alert_1")
        expected.append("@950: #2 SENT ALERT TO #1: Test_Alert_1")
        expected.append("@1700: #1 RECEIVED ALERT FROM #2: Test_Alert_1")
        expected.append("@1700: #1 SENT ALERT TO #2: Test_Alert_1")
        expected.append("@2000: #1 SENT CANCELLATION TO #2: Test_Alert_1")
        expected.append("@2200: #2 RECEIVED ALERT FROM #1: Test_Alert_1")
        expected.append("@2200: #2 SENT ALERT TO #1: Test_Alert_1")
        expected.append("@2500: #2 RECEIVED CANCELLATION FROM #1: Test_Alert_1")
        expected.append("@2500: #2 SENT CANCELLATION TO #1: Test_Alert_1")
        expected.append("@2950: #1 RECEIVED ALERT FROM #2: Test_Alert_1")
        expected.append("@3250: #1 RECEIVED CANCELLATION FROM #2: Test_Alert_1")

        self.assertEqual(expected, interactions_list)

    def test_propagation_with_four_devices__one_alerts_and_one_cancellation(self):
        Device.set_life_time(9999)

        device_three = Device(3)
        device_four = Device(4)

        self._device_two.add_to_network()
        self._device_one.add_to_network()
        device_three.add_to_network()
        device_four.add_to_network()

        self._device_one.add_propagation_contact(self._device_two, 750)
        self._device_two.add_propagation_contact(device_three, 1250)
        device_three.add_propagation_contact(device_four, 500)
        device_four.add_propagation_contact(self._device_one, 1000)

        cancellation_1 = Message(MessageType.CANCEL, "Trouble", 2200)
        alert_1 = Message(MessageType.ALERT, "Trouble", 0)

        self._device_one.propagate(cancellation_1)
        self._device_one.propagate(alert_1)

        formated_registry = Device.get_formated_registry()

        expected = list()
        expected.append("@0: #1 SENT ALERT TO #2: Trouble")
        expected.append("@750: #2 RECEIVED ALERT FROM #1: Trouble")
        expected.append("@750: #2 SENT ALERT TO #3: Trouble")
        expected.append("@2000: #3 RECEIVED ALERT FROM #2: Trouble")
        expected.append("@2000: #3 SENT ALERT TO #4: Trouble")
        expected.append("@2200: #1 SENT CANCELLATION TO #2: Trouble")
        expected.append("@2500: #4 RECEIVED ALERT FROM #3: Trouble")
        expected.append("@2500: #4 SENT ALERT TO #1: Trouble")
        expected.append("@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble")
        expected.append("@2950: #2 SENT CANCELLATION TO #3: Trouble")
        expected.append("@3500: #1 RECEIVED ALERT FROM #4: Trouble")
        expected.append("@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble")
        expected.append("@4200: #3 SENT CANCELLATION TO #4: Trouble")
        expected.append("@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble")
        expected.append("@4700: #4 SENT CANCELLATION TO #1: Trouble")
        expected.append("@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble")

        self.assertEqual(expected, formated_registry)

    def test_check_for_messages_sent_after_the_life_time_of_the_simulation(self):
        message = Message(MessageType.ALERT, "Trouble", 2200)

        Device.set_life_time(500)

        self.assertEqual(self._device_one.propagate(message), None)

    def test_propagate_message_that_is_there_cancel_for_it(self):
        alert = Message(MessageType.ALERT, "Trouble", 200)
        cancellation_1 = Message(MessageType.CANCEL, "Trouble", 100)

        self._device_one.propagate(cancellation_1)

        self.assertEqual(self._device_one.propagate(alert), None)

if __name__ == '__main__':
    unittest.main()