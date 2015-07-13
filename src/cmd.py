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

cmds = {"quit": [["quit", "leave", "disconnect", "q"], 0],
        "help": [["h", "help"], 0],
        "status": [["status", "st"], 0],
        "players": [["players", "p"], 0],
        "base64": [["b64", "base64"], 0],
        "search": [['search', "s"], 0],
        "google": [["google", "g"], 0],
        "uptime": [["uptime"], 0],
        "version": [["version", "v"], 0],
        "roulette": [["roulette", "r"], 0],
        "kill": [["kill", "k"], 0],
        "raw": [["raw"], 0]}

CMD_ALIASES = 0
CMD_LEVEL = 1

class Cmd():
    def __init__(self, risc):
        self.risc = risc
        self.irc = risc.irc
        self.privmsg = self.irc.privmsg

    def clean_list(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != "" and e != ' ':
                ret.append(e)
        return ret

    def get_cmd(self, msg):
        """
        Return the original command name if it exists, return "" otherwise
        """
        cmd = self.clean_list(msg.split(' '))[0][1:]

        if cmd in cmds:
            return cmd

        for c in cmds:
            if cmd in cmds[c][CMD_ALIASES]:
                return c
        return ""

    def init_cmd(self, _from, to, msg):
        """
        Return a list [cmd_level, "output"] for a given command
        """
        ret = []
        cmd = self.get_cmd(msg)

        ret.append(cmds[cmd][CMD_LEVEL])

        if msg[0] == self.risc.cmd_prefix:
            ret.append(_from)
        else:
            ret.append(self.risc.channel)
        return ret

    def process(self, _from, to, msg):
        """
        Parse IRC messages for valid commands to call the appropriate functions
        """
        cmd = self.get_cmd(msg)
        if cmd != "":
            getattr(self, "cmd_"+cmd)(_from, to, msg)
        return None

    def cmd_help(self, _from, to, msg):
        """
        Display the main help message
        help
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        self.privmsg(cinfo[1], "Commands: %s." %(', '.join(cmds.keys())))
        return None
