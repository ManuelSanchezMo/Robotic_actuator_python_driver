
#ifndef MOTOR_OUT_ELEC_H
#define MOTOR_OUT_ELEC_H

#include <stdint.h>
#include <iostream>

class MotorOUTELEC : public ProcessMessageInterface {
public:
    MotorOUTELEC();

    bool processMessage();

private:
    float m_Ua;
    float m_Ub;
    float m_Current;
    float m_Electricalangle;

};

#endif // MOTOR_OUT_ELEC_H
