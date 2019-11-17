import argparse
import serial
import serial.tools.list_ports
from utils.message_parse import Parser, Message, MessageType
from loguru import logger
from utils import string_formatter as fmt
import struct
import os
import datetime
import jsonlines


def main():
    parser = argparse.ArgumentParser("Collects data from the Arduino via serial port connection")
    parser.add_argument("-o", "--output", default="output")

    args = parser.parse_args()

    port = serial.Serial(port="/dev/cu.usbserial-DN01JH39",
                         baudrate=9600,
                         timeout=0.2)
    parser = Parser()

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, "arduino_feed_{}.jsonl".format(datetime.datetime.now()))

    with jsonlines.open(output_file, "w", flush=True) as f:
        while True:
            byte_data = port.read()

            parser.add_bytes(byte_data)
            msg = parser.next_message()

            if msg is not None:
                measurement = struct.unpack("f", fmt.bytes_from_list(msg.data))[0]
                msg_type = MessageType.to_string(msg.msg_type)
                logger.info("Type: {}, Data: {}".format(msg_type,
                                                        measurement))
                f.write({
                    msg_type: measurement
                })


if __name__ == "__main__":
    main()
