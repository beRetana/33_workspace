# project2.py
#
# ICS 33 Winter 2025
# Project 2: Learning to Fly
#
# This is the main module that runs the entire program.
#
# YOU WILL NOT NEED TO MODIFY THIS FILE AT ALL

from p2app import EventBus
from p2app import Engine
from p2app import MainView


def main():

    # event_bus is somewhat of an event manager, and it gets used heavily by MainView
    event_bus = EventBus()

    # the engine should take no parameters to be initialized
    engine = Engine()

    # The visuals use event manager to send messages
    main_view = MainView(event_bus)

    # Makes the event manager to be aware of the engine and main_view
    event_bus.register_engine(engine)
    event_bus.register_view(main_view)

    # run the application
    main_view.run()


if __name__ == '__main__':
    main()
