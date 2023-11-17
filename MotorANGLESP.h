
#ifndef MOTOR_ANGLE_SP_H
#define MOTOR_ANGLE_SP_H

#include <stdint.h>
#include <iostream>

class MotorANGLESP : public ProcessMessageInterface {
public:
    MotorANGLESP();

    bool processMessage();

private:
    float m_Anglesp;

};

#endif // MOTOR_ANGLE_SP_H
