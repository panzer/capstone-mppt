import pytest
from utils.message_parse import Parser, Message


byte_data = [
    0x81, 0x05, 0x00, 0x05,
    0x01, 0x02, 0x03, 0x04
]


def test_parser_whole():
    # Arrange
    parser = Parser()

    # Act
    parser.add_bytes(byte_data)
    msg = parser.next_message()

    # Assert
    assert msg.data == [0x01, 0x02, 0x03, 0x04]


def test_parser_one_at_a_time():
    # Arrange
    parser = Parser()

    # Act
    msg: Message = None
    for byte in byte_data:
        parser.add_bytes([byte])
        msg = parser.next_message()

    # Assert
    assert msg.data == [0x01, 0x02, 0x03, 0x04]