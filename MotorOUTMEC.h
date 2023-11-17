
#ifndef MOTOR_OUT_MEC_H
#define MOTOR_OUT_MEC_H

#include <stdint.h>
#include <iostream>

class MotorOUTMEC : public ProcessMessageInterface {
public:
    MotorOUTMEC();

    bool processMessage();

private:
    float m_Shaftangle;
    float m_Shaftanglesp;
    float m_Shaftvelocity;

};

#endif // MOTOR_OUT_MEC_H
