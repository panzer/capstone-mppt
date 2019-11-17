// Lux sensor

#include "veml7700.h"
#include "Adafruit_VEML7700.h"

Adafruit_VEML7700 veml = Adafruit_VEML7700();

veml7700_status_t veml7700_init() {
    if (!veml.begin()) {
        return VEML7700_NOT_FOUND;
    }

    veml.setGain(VEML7700_GAIN_1_8);
    veml.setIntegrationTime(VEML7700_IT_25MS);

    veml.setLowThreshold(10000);
    veml.setHighThreshold(20000);
    veml.interruptEnable(true);
    
    return VEML7700_OK;
}

float veml7700_get_lux() {
    return veml.readLux();
}