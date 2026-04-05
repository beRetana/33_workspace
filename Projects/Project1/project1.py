from pathlib import Path
from collections import namedtuple

from device import Device
from communication import Message, MessageType

Commands = namedtuple("Commands", ["length", "devices", "propagate", "alerts", "cancellations"])

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def read_from_file(file_path: Path | None) -> list[str] | None:
    """Reads the input file from the standard input"""

    if file_path is None:
        file_path = _read_input_file_path()

    content = list()

    try:
        with open(file_path) as input_file:
            for line in input_file:
                if check_valid_line(line):
                    line = line.strip()
                    content.append(line)
    except FileNotFoundError:
        print("FILE NOT FOUND")
        return

    return content

def check_valid_line(line: str) -> bool:
    """Checks if the line is valid"""

    if line == "\n" or line == "\t":
        return False

    new_line = ""
    for char in line:
        if char == "#":
            break
        else:
            new_line += char

    if not new_line:
        return False

    return True

def get_commands(lines: list[str]) -> Commands:
    """Iterates through the lines of input and returns a named tuple with
    the commands to run the simulation"""

    initial_word_index = 0
    second_word_index = 1

    length = 0
    devices = []
    propagate = []
    alerts = []
    cancellations = []

    for line in lines:
        words = line.split()
        initial_word = words[initial_word_index]

        match initial_word:
            case "LENGTH":
                length = words[second_word_index]
            case "DEVICE":
                devices.append(int(words[second_word_index]))
            case "PROPAGATE":
                propagate.append(words[second_word_index:])
            case "ALERT":
                alerts.append(words[second_word_index:])
            case "CANCEL":
                cancellations.append(words[second_word_index:])

    return Commands(length, devices, propagate, alerts, cancellations)

def run_simulation(commands: Commands) -> list[str]:
    """Runs the simulation and returns the logs of it as a list of strings"""

    length = commands.length

    Device.clear_network()
    Device.set_life_time(int(length))

    list_of_alerts = list()
    list_of_cancellations = list()

    for device in commands.devices:
        new_device = Device(device)
        new_device.add_to_network()

    for propagate in commands.propagate:
        device = Device.get_network()[int(propagate[0])]
        contact = Device.get_network()[int(propagate[1])]
        latency = int(propagate[2])
        device.add_propagation_contact(contact, latency)

    for alert in commands.alerts:
        list_of_alerts.append((int(alert[0]), Message(MessageType.ALERT, alert[1], int(alert[2]))))

    for cancellation in commands.cancellations:
        list_of_cancellations.append((int(cancellation[0]),Message(MessageType.CANCEL, cancellation[1], int(cancellation[2]))))

    for cancellation in list_of_cancellations:
        device =  Device.get_network()[cancellation[0]]
        device.propagate(cancellation[1])

    for alert in list_of_alerts:
        device = Device.get_network()[alert[0]]
        device.propagate(alert[1])

    registry_log = Device.get_formated_registry()

    return registry_log

def print_log(registry_log: list[str]) -> None:
    """Prints out the registry log"""

    for log in registry_log:
        print(log)
    print(f"@{Device.get_life_time()}: END")

def main() -> None:
    """Runs the simulation program in its entirety"""

    content = read_from_file(None)
    commands = get_commands(content)
    registry_log = run_simulation(commands)
    print_log(registry_log)

if __name__ == '__main__':
    main()
