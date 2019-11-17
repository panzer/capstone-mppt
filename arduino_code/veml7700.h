// Lux sensor

#ifndef VEML_7700_H
#define VEML_7700_H

// Status codes
enum veml7700_status_t: int {
  VEML7700_OK,
  VEML7700_NOT_FOUND,

};

veml7700_status_t veml7700_init();

float veml7700_get_lux();

#endif // VEML_7700_H