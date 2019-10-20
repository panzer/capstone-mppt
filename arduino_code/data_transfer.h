#ifndef DATA_TRANSFER_H
#define DATA_TRANSFER_H

#include "Arduino.h"

/*
 * Mechanisms for sending data from the Arduino to the computer
 */

// Message types
enum msg_type_t: byte {
  MSG_TEMPERATURE,
  MSG_LUX
};

void send_msg(msg_type_t type, byte *data, size_t len);

#endif  // DATA_TRANSFER_H
