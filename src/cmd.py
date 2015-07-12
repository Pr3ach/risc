# # -*- coding: utf-8 -*-

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

from irc import COLOR
import time

cmds = {"quit": [["quit", "leave", "disconnect", "q"], ""],
        "help": [["h", "help"], ""],
        "status": [["status", "st"], ""],
        "players": [["players", "p"], ""],
        "base64": [["b64", "base64"], ""],
        "search": [['search', "s"], ""],
        "google": [["google", "g"], ""],
        "uptime": [["uptime"], ""],
        "version": [["version", "v"], ""],
        "roulette": [["roulette", "r"], ""],
        "kill": [["kill", "k"], ""],
        "raw": [["raw"], ""]}

CMD_ALIASES = 0
CMD_LEVEL = 1

class Cmd():
    def __init__(self, risc):
        self.risc = risc
        self.privmsg = self.risc.irc.privmsg

    def clean_list(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != "" and e != ' ':
                ret.append(e)
        return ret

    def get_cmd(self, cmd):
        """
        Return the original command name if it exists, return "" otherwise
        """
        if cmd in cmds:
            return cmd

        for c in cmds:
            if cmd in cmds[c][CMD_ALIASES]:
                return c
        return ""

    def init_cmd(self, _from, to, msg):
        """
        Return a list ["level_required", "output_type"] for a given command
        """
        ret = []
        cmd = self.get_cmd(self.clean_list(msg.split(' '))[0])

        ret[0] = cmds[cmd][CMD_LEVEL]

        if msg[0] == self.risc.cmd_prefix:
            ret[1] = _from
        else:
            ret[1] = self.risc.channel
        return ret

    def process(self, _from, to, msg):
        """
        Parse IRC messages for valid commands to call the appropriate functions
        """
        cmd = self.get_cmd(self.clean_list(msg.split(' '))[0])

        if cmd != "":
            getattr(self, "cmd_"+cmd)(_from, to, msg)
        return None

    def cmd_help(self, _from, to, msg):
        """
        Display the main help message
        """
        init = self.init_cmd(_from, to, msg)
        argv = self.clean_list(msg.split(' '))

        self.privmsg(init[1], "TEST")
        self.privmsg(init[1], "l: "+init[0])
        return None
