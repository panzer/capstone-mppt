#include "data_transfer.h"

// Start of frame delimiter
#define SOF 0x81
#define ESC 0x7e
#define MAXDATA 10

typedef struct Message {
  byte sof;
  size_t len;  // How many more bytes to read after this
  msg_type_t type;
  byte data[MAXDATA];   // Data goes here (variable length)
} msg_t;

void send_msg(msg_type_t type, byte *data, size_t len) {
  msg_t m;
  m.sof = SOF;
  m.type = type;

  byte out_buf[sizeof(msg_t) + MAXDATA];
  size_t j = sizeof(msg_t) - MAXDATA;  // Output buffer index

  if (len > MAXDATA) {
    len = MAXDATA;
  }

  for (size_t i = 0; i < len; i++) {
    if (data[i] == ESC || data[i] == SOF) {
      out_buf[j++] = ESC;
    }
    out_buf[j++] = data[i];
  }
  m.len = j - 3;  // Remove SOF and len
  memcpy(out_buf, &m, sizeof(msg_t));
  
  Serial.write(out_buf, j);
}

