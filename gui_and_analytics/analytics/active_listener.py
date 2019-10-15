import argparse
import serial
import serial.tools.list_ports
from utils.message_parse import Parser, Message
from loguru import logger
from utils import string_formatter as fmt


def main():
    parser = argparse.ArgumentParser("Collects data from the Arduino via serial port connection")

    port = serial.Serial(port="/dev/cu.usbserial-DN01JH39",
                         baudrate=9600,
                         timeout=0.2)
    parser = Parser()

    while True:
        byte_data = port.read()

        parser.add_bytes(byte_data)
        msg = parser.next_message()

        if msg is not None:
            logger.info(msg)


if __name__ == "__main__":
    main()
