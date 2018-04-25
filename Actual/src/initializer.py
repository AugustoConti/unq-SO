#!/usr/bin/env python

from src.hardware import *
from src.interruptionHandlers import *

def registerHandlers(scheduler, pcbTable, loader, dispatcher, ioDeviceController):
    HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE,
                                      NewInterruptionHandler(scheduler, pcbTable, loader))
    HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE,
                                      KillInterruptionHandler(scheduler, pcbTable, dispatcher))
    HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE,
                                      IoInInterruptionHandler(scheduler, pcbTable, ioDeviceController, dispatcher))
    HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE,
                                      IoOutInterruptionHandler(scheduler, ioDeviceController))
    HARDWARE.interruptVector.register(TIME_OUT_INTERRUPTION_TYPE,
                                      TimeOutInterruptionHandler(scheduler, dispatcher))
