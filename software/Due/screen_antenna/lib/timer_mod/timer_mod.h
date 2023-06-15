//
// Created by n7 on 5/6/23.
//

#ifndef SCREEN_ANTENNA_TIMER_MOD_H
#define SCREEN_ANTENNA_TIMER_MOD_H

#include "DueTimer.h"

class TimerMod: protected DueTimer {
    static bool handled[NUM_TIMERS];
    static void isr0() {handled[0]=false;};
    static void isr1() {handled[1]=false;};
    static void isr2() {handled[2]=false;};
    static void isr3() {handled[3]=false;};
    static void isr4() {handled[4]=false;};
    static void isr5() {handled[5]=false;};
#if NUM_TIMERS > 6
    static void isr6() {handled[6]=false;};
    static void isr7() {handled[7]=false;};
    static void isr8() {handled[8]=false;};
#endif
    void (*handler)(void *);
    bool started=false;

public:
    TimerMod(unsigned short timer_id);
    void setHandler(void (*handler_func)(void *));
    void handle(void *arg);

    void start(double ms = -1);
    void stop(void);
    void setPeriod(double us);
    double getPeriod() const;
    bool has_started() const;

};

#endif //SCREEN_ANTENNA_TIMER_MOD_H
