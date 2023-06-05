//
// Created by n7 on 5/6/23.
//

#include "timer_mod.h"

TimerMod::TimerMod(unsigned short timer_id) : DueTimer(timer_id) {
    handled[timer_id] = true;
    switch(timer_id) {
        case 0:
            attachInterrupt(isr0);
            break;
        case 1:
            attachInterrupt(isr1);
            break;
        case 2:
            attachInterrupt(isr2);
            break;
        case 3:
            attachInterrupt(isr3);
            break;
        case 4:
            attachInterrupt(isr4);
            break;
        case 5:
            attachInterrupt(isr5);
            break;
#if NUM_TIMERS > 6
        case 6:
            attachInterrupt(isr6);
            break;
        case 7:
            attachInterrupt(isr7);
            break;
        case 8:
            attachInterrupt(isr8);
            break;
#endif
        default:
            attachInterrupt(isr0);
            break;
    }

}

void TimerMod::handle(void *arg) {
    if (handled) {
        return;
    }
    handler(arg);
    handled[timer] = true;
}

void TimerMod::start(double ms) {
    DueTimer::start(ms);
}

void TimerMod::stop() {
    DueTimer::stop();
}

void TimerMod::setPeriod(double ms) {
    DueTimer::setPeriod(ms);
}

double TimerMod::getPeriod() const {
    return DueTimer::getPeriod();
}