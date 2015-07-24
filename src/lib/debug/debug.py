#-*- coding: utf-8 -*-

#
#  Copyright (C) 2015 - Preacher
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Preacher"
__version__ = "1.3"

import time
import sys

class Debug():
    """
    Set of functions providing simple logging/debugging capabilities
    """
    def __init__(self, log_prefix=""):
        t = time.time()
        self.log_file = ""

        if log_prefix != "":
            self.log_file = log_prefix + "_"+ str(int(t)) + ".log"
            sys.stdout = open(self.log_file, "w+")

    def info(self, info_msg):
        t = time.localtime()
        print ("%02d/%02d/%04d %02d:%02d:%02d INFO     %s" %(t[0], t[1], t[2], t[3], t[4], t[5], info_msg))
        return None

    def debug(self, debug_msg):
        t = time.localtime()
        print ("%02d/%02d/%04d %02d:%02d:%02d DEBUG    %s" %(t[0], t[1], t[2], t[3], t[4], t[5], debug_msg))
        return None

    def warning(self, warning_msg):
        t = time.localtime()
        print ("%02d/%02d/%04d %02d:%02d:%02d WARNING  %s" %(t[0], t[1], t[2], t[3], t[4], t[5], warning_msg))
        return None

    def error(self, error_msg):
        t = time.localtime()
        print ("%02d/%02d/%04d %02d:%02d:%02d ERROR    %s" %(t[0], t[1], t[2], t[3], t[4], t[5], error_msg))
        return None

    def critical(self, critical_msg):
        t = time.localtime()
        print ("%02d/%02d/%04d %02d:%02d:%02d CRITICAL %s" %(t[0], t[1], t[2], t[3], t[4], t[5], critical_msg))
        return None

    def close(self):
        """
        Close the log file, if stdout is not used
        """
        if self.log_file != "":
            sys.stdout.close()
        return None
