from dataclasses import dataclass, field
from typing import Optional
import enum
import queue
from typing import Iterable
from loguru import logger


SOF = 0x81
ESC = 0x7e


class MessageType(enum.Enum):
    NOTYPE = -1
    TEMP = 0
    LUX = 1


@dataclass()
class Message:
    msg_type: MessageType = MessageType.NOTYPE
    length: int = 0
    data: list = field(default_factory=list)


class Parser:
    def __init__(self):
        self.buffer = queue.Queue(maxsize=256)
        self.data_len = 0
        self.remaining = None
        self.escaped = False
        self.header_bytes_remaining = None
        self.message = Message()

    def add_bytes(self, byte_data: Iterable) -> None:
        # Queue all provided bytes
        for byte in byte_data:
            self.buffer.put(byte)

    def next_message(self) -> Optional[Message]:
        # Clear the buffer of awaiting bytes, returning before all bytes are cleared
        # if and only if a Message is returned
        while not self.buffer.empty():
            byte = self.buffer.get()
            if byte == ESC and not self.escaped:
                self.escaped = True
                self.remaining -= 1  # escape bytes count in the message length
            elif byte == SOF and not self.escaped:
                self.message = Message()  # unescaped SOF byte indicates start of new message
                self.header_bytes_remaining = 3  # all messages contain 3 bytes after SOF
            elif self.header_bytes_remaining is None:
                # Used to short circuit parsing logic in the case no SOF has been read
                # since the last message.
                pass
            else:
                # Normal operation is non escaped
                self.escaped = False

                # Count down through the header bytes, filling in global state
                if self.header_bytes_remaining == 3:
                    self.remaining = byte
                elif self.header_bytes_remaining == 2:
                    self.remaining += byte << 8
                elif self.header_bytes_remaining == 1:
                    self.message.msg_type = byte
                    self.remaining -= 1
                    self.data_len = self.remaining
                else:
                    # self.header_bytes == 0 indicates non header info
                    self.message.data.append(byte)
                    self.remaining -= 1

                    # 0 remaining means end of message
                    if self.remaining <= 0:
                        self.header_bytes_remaining = None
                        self.message.length = self.data_len
                        return self.message

                if self.header_bytes_remaining > 0:
                    self.header_bytes_remaining -= 1

        return None





