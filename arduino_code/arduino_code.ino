#include "data_transfer.h"
#include "veml7700.h"
#include "ntc3950.h"

/*
 * Capstone MPPT controller
 * 
 */

void setup(void) {
  Serial.begin(9600);
  analogReference(EXTERNAL);  // Needed for temperature (ntc3950)

  veml7700_init();

}

void loop(void) {
  float temp = ntc3950_get_temperature();
  send_msg(MSG_TEMPERATURE, (byte *) &temp, sizeof(float));

  float lux = veml7700_get_lux();
  send_msg(MSG_LUX, (byte *) &lux, sizeof(float));
  
  delay(1000);
}
