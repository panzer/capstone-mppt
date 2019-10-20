// Lux sensor

#include "veml7700.h"
#include "Adafruit_VEML7700.h"

Adafruit_VEML7700 veml = Adafruit_VEML7700();

int veml7700_init() {
    if (!veml.begin()) {
        return -1;
    }

    veml.setGain(VEML7700_GAIN_1_8);
    veml.setIntegrationTime(VEML7700_IT_25MS);

    veml.setLowThreshold(10000);
    veml.setHighThreshold(20000);
    veml.interruptEnable(true);
    
    return 0;
}

float veml7700_get_lux() {
    return veml.readLux();
}