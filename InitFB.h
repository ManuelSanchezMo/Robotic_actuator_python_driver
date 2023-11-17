
#ifndef INIT_FB_H
#define INIT_FB_H

#include <stdint.h>
#include <iostream>

class InitFB : public ProcessMessageInterface {
public:
    InitFB();

    bool processMessage();

private:
    float m_Pcontrol;
    float m_Icontrol;
    float m_Dcontrol;
    float m_Voltlimit;

};

#endif // INIT_FB_H
