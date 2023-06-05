//
// Created by n7 on 1/6/23.
//

#ifndef SCREEN_ANTENNA_CFG_H
#define SCREEN_ANTENNA_CFG_H

#define CFG_4x4

#include "grid.h"

#ifdef CFG_4x4
#include "conn_4x4.h"
#endif

Grid create_grid();

#endif //SCREEN_ANTENNA_CFG_H
