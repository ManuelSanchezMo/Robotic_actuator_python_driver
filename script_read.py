#!/usr/bin/env python

"""
Shows how to receive messages via polling.
"""

import can
from can.bus import BusState


def receive_all():
    """Receives all messages and prints them to the console until Ctrl+C is pressed."""

    # this uses the default configuration (for example from environment variables, or a
    # config file) see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus: 
        # set to read-only, only supported on some interfaces
        try:
            bus.state = BusState.PASSIVE
        except NotImplementedError:
            pass

        try:
            while True:
                msg = bus.recv(1)
                if msg is not None:
                    x = int((msg.data[0] << 8) + msg.data[1]);
                    print(msg)
                    print(x)
                    print(float(80/65535*x  - 80/2))

        except KeyboardInterrupt:
            pass  # exit normally


if __name__ == "__main__":
    receive_all()
