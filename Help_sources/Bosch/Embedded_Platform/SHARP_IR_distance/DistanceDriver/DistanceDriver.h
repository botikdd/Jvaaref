#ifndef DRIVER_H
#define DRIVER_H

#include <mbed.h>

class DistanceDriver
{
public:
    DistanceDriver(PinName pin);
    ~DistanceDriver();
    float ReadDistance(void);

private:
    AnalogIn pin;

};

#endif