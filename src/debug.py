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
__version__ = "1.0"

import time

class Debug():
    """
    Set of functions providing simple logging/debugging capabilities
    """
    def __init__(self, use__stdout__, log_prefix=""):
        t = time.time()
        self.log_file = ""

        if not use__stdout__:
            self.log_file = log_prefix + str(int(t)) + ".log"
            sys.stdout = open(self.log_file, "w+", 0)

    def info(self, info_msg):
        t = time.localtime()
        print ("%d/%d/%d %d:%d:%d INFO     %s" %(t[1], t[2], t[0], t[3], t[4], t[5], info_msg))
        return None

    def debug(self, debug_msg):
        t = time.localtime()
        print ("%d/%d/%d %d:%d:%d DEBUG    %s" %(t[1], t[2], t[0], t[3], t[4], t[5], debug_msg))
        return None

    def warning(self, warning_msg):
        t = time.localtime()
        print ("%d/%d/%d %d:%d:%d WARNING  %s" %(t[1], t[2], t[0], t[3], t[4], t[5], warning_msg))
        return None

    def error(self, error_msg):
        t = time.localtime()
        print ("%d/%d/%d %d:%d:%d ERROR    %s" %(t[1], t[2], t[0], t[3], t[4], t[5], error_msg))
        return None

    def critical(self, critical_msg):
        t = time.localtime()
        print ("%d/%d/%d %d:%d:%d CRITICAL %s" %(t[1], t[2], t[0], t[3], t[4], t[5], critical_msg))
        return None
