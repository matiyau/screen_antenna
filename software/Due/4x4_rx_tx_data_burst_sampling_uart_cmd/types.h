#ifndef _TYPES_H_
#define _TYPES_H_

typedef enum {
  RX_STANDBY,
  RX_PREAMBLE,
  RX_LENGTH,
  RX_DATA,
  TX_PREAMBLE,
  TX_LENGTH,
  TX_DATA
}state_t;

#endif
