#!/usr/bin/env python3
import sys
from subprocess import Popen

new_window_command = "x-terminal-emulator -e".split()
proc = Popen(new_window_command + [sys.executable, "-c", "input('Press Enter..')"])
proc.wait()                                               # tail -f info.log
