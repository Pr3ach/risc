# -*- coding: utf-8 -*-

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

import irc
import ioq3
import risc
from irc import COLOR
import time
import datetime
import json
import requests
import re
import MySQLdb as mysql
import hashlib
import base64
import random

cmds = {"help": [["h"], 0],
        "quit": [["leave", "disconnect", "q"], 0],
        "google": [["g"], 0],
        "server": [["status", "sv", "st"], 0],
        "hash": [[], 0],
        "base64": [["b64"], 0],
        "uptime": [[], 0],
        "version": [["v"], 0],
        "search": [["s"], 0],
        "roulette": [["r"], 0],
        "kill": [["k"], 0],
        "raw": [[], 0],
        "lower": [[], 0],
        "upper": [[], 0],
        "quote": [["kek", "topkek"], 0]}

CMD_ALIASES = 0
CMD_LEVEL = 1

# Russian roulette game variables
r_bullet = random.randint(1, 0xffff) % 7
r_chamber = random.randint(1, 0xffff) % 7

class Cmd():
    def __init__(self, risc):
        self.risc = risc
        self.irc = risc.irc
        self.privmsg = self.irc.privmsg
        self.debug = self.risc.debug

    def clean_list(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != "" and e != ' ':
                ret.append(e)
        return ret

    def is_valid_re(self, regex):
        try:
            re.compile(regex)
        except re.error:
            return False
        return True

    def get_cmd(self, msg):
        """
        Return the original command name from the message if it exists, return "" otherwise
        """
        cmd = self.clean_list(msg.split(' '))[0][1:]

        if cmd.lower() in cmds:
            return cmd.lower()

        for c in cmds:
            if cmd.lower() in cmds[c][CMD_ALIASES]:
                return c
        return ""

    def get_cmd_from_alias(self, cmd_alias):
        """
        Retrieve the original cmd name from an alias, if it exists, return "" otherwise
        """
        if cmd_alias.lower() in cmds:
            return cmd_alias.lower()

        for cmd in cmds:
            if cmd_alias.lower() in cmds[cmd][CMD_ALIASES]:
                return cmd
        return ""

    def init_cmd(self, ident, _from, to, msg):
        """
        Return a list [cmd_level, "privmsg_output", user_level] for a given command
        """
        ret = []
        cmd = self.get_cmd(msg)

        ret.append(cmds[cmd][CMD_LEVEL])

        if msg[0] == self.risc.cmd_prefix:
            ret.append(_from)
        else:
            ret.append(self.risc.channel)

        if self.risc.is_root(ident):
            ret.append(4)
        else:
            ret.append(self.irc.get_user_level(_from))
        return ret

    def process(self, ident, _from, to, msg):
        """
        Parse IRC messages for valid commands to call the appropriate functions
        """
        cmd = self.get_cmd(msg)
        if cmd != "":
            if hasattr(self, "cmd_"+cmd):
                getattr(self, "cmd_"+cmd)(ident, _from, to, msg)
        return None

    def cmd_help(self, ident, _from, to, msg):
        """
        Display the main help message
        help
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc == 1:
            self.privmsg(cinfo[1], "Commands: %s." %(', '.join(cmds.keys())))
        else:
            cmd = self.get_cmd_from_alias(argv[1])
            if cmd == "":
                self.privmsg(cinfo[1], "Command not found: %s." %(argv[1]))
                return None
            if hasattr(self, "_cmd_help_"+cmd):
                getattr(self, "_cmd_help_"+cmd)(ident, _from, to, msg, cmd)
        return None

    def _cmd_help_help(self, ident, _from, to, msg, cmd):
        """
        Help for help command ...
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        self.privmsg(cinfo[1], "-_-'")
        return None

    def _cmd_help_quit(self, ident, _from, to, msg, cmd):
        """
        Help for quit command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": quit."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Close the connection to the IRC server and exit."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_google(self, ident, _from, to, msg, cmd):
        """
        Help for google command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": google <query>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Search for <query> using google and display the results."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_server(self, ident, _from, to, msg, cmd):
        """
        Help for server command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": server [<ip:opt_port> | <name> | "\
                "add <ip:opt_port> <name> | drop <name> | rename <old_name> <new_name> | list]."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Manage IoQ3 based game servers."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_hash(self, ident, _from, to, msg, cmd):
        """
        Help for hash command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": hash [md5 | sha1 | sha256 | sha512] <data>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Hash <data> using the specified algorithm."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_base64(self, ident, _from, to, msg, cmd):
        """
        Help for base64 command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": base64 [d | e] <data>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Base64 decode/encode <data>."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_uptime(self, ident, _from, to, msg, cmd):
        """
        Help for uptime command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": uptime."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Display risc's uptime."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_version(self, ident, _from, to, msg, cmd):
        """
        Help for version command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": version."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Display risc version and author information."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_search(self, ident, _from, to, msg, cmd):
        """
        Help for search command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": search <player>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Search for <player> in the server list."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_roulette(self, ident, _from, to, msg, cmd):
        """
        Help for roulette command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": roulette."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Russian roulette game."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_kill(self, ident, _from, to, msg, cmd):
        """
        Help for kill command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": kill <opt_user> <opt_weapon>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": UrT-like kill messages. The <opt_user> "\
                "parameter can be any user on the channel or -all, <opt_weapon> can be any UrT weapon."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_raw(self, ident, _from, to, msg, cmd):
        """
        Help for raw command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": raw <data>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Send raw commands to the IRC server."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_lower(self, ident, _from, to, msg, cmd):
        """
        Help for lower command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": lower <string>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Return a lowercased string."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_upper(self, ident, _from, to, msg, cmd):
        """
        Help for upper command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": upper <string>."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Return a uppercased string."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def _cmd_help_quote(self, ident, _from, to, msg, cmd):
        """
        Help for quote command
        """
        cinfo = self.init_cmd(ident, _from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        usage = COLOR["boldwhite"] + "Usage" + COLOR["rewind"] + ": quote [add <quote> | drop <quote_id> | find <regex> | last]."
        desc = COLOR["boldwhite"] + "Description" + COLOR["rewind"] + ": Manage quotes."
        aliases = COLOR["boldwhite"] + "Aliases" + COLOR["rewind"] + ': ' +  ", ".join(cmds[cmd][CMD_ALIASES]) + '.'
        access = COLOR["boldwhite"] + "Access" + COLOR["rewind"] + ": %s." %access

        self.privmsg(cinfo[1], usage + ' ' + desc + ' ' + aliases + ' ' + access)
        return None

    def cmd_quit(self, ident, _from, to, msg):
        """
        Simply leave
        quit
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        self.risc.stop()
        return None

    def cmd_google(self, ident, _from, to, msg):
        """
        Query google
        google <query>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help google.")
            return None

        i = 0
        search_str = ' '.join(msg.split(' ')[1:])
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % search_str
        res = requests.get(url)

        if not len(json.loads(res.text)['responseData']['results']):
            self.privmsg(cinfo[1], "No results.")
            return None

        self.privmsg(cinfo[1], "Top hits:")
        for hit in json.loads(res.text)["responseData"]["results"]:
            self.privmsg(cinfo[1], hit["unescapedUrl"])
            i+=1
            if i > 4:
                break
        return None

    def cmd_server(self, ident, _from, to, msg):
        """
        Display game information about the specified server
        server [<ip:opt_port> | <name> | add <ip:opt_port> <name> | drop <name> | rename <old_name> <new_name> | list]
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help server.")
            return None

        if argv[1].lower() == "add":
            if argc < 4:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help server.")
                return None
            self._cmd_server_add(argv[2], argv[3], cinfo, _from)
            return None
        elif argv[1].lower() in ("drop", "rm"):
            if argc < 3:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help server.")
                return None
            self._cmd_server_drop(argv[2], cinfo)
            return None
        elif argv[1].lower() in ("rename", "mv"):
            if argc < 4:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help server.")
                return None
            self._cmd_server_rename(argv[2], argv[3], cinfo)
            return None
        elif argv[1].lower() in ("list", "ls"):
            self._cmd_server_list(cinfo)
            return None

        re_full_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{5}$')
        re_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}$')

        if re.match(re_full_ip, argv[1]):
            ip = argv[1].split(':')[0]
            port = int(argv[1].split(':')[1])
        elif re.match(re_ip, argv[1]):
            ip = argv[1]
            port = 27960
        else:
            tmp = self._cmd_server_retrieve(argv[1])
            if tmp[0] == "":
                self.privmsg(cinfo[1], "No such server.")
                return None
            ip = tmp[0]
            port = tmp[1]

        try:
            sv = ioq3.Ioq3(ip, port)
        except Exception, e:
            self.debug.error("cmd_server: Exception: '%s'" %(e))
            self.privmsg(cinfo[1], COLOR["boldred"] + "Server seems unreachable." + COLOR["rewind"])
            return None

        self._cmd_server_display(sv, cinfo)
        return None

    def _cmd_server_add(self, ip, name, cinfo, _from):
        """
        Add a server to the database
        """
        re_full_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{5}$')
        re_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}$')

        if re.match(re_full_ip, name) or re.match(re_ip, name) or name.lower() in ("add", "drop", "rm", "list", "ls", "rename", "mv") or len(mysql.escape_string(name)) >= 16:
            self.privmsg(cinfo[1], "Invalid server name.")
            return None

        if re.match(re_ip, ip):
            port = 27960
        elif re.match(re_full_ip, ip):
            port = int(ip.split(':')[1])
            ip = ip.split(':')[0]
        else:
            self.privmsg(cinfo[1], "Invalid IP address.")
            return None

        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM ioq3_blacklist WHERE ip = '%s' AND port = %d""" %(ip, port))

        if cur.rowcount:
            con.close()
            self.privmsg(cinfo[1], "Invalid IP address.")
            return None

        cur.execute("""SELECT * FROM ioq3_servers WHERE (ip = '%s' AND port = %d) OR name = '%s'""" %(ip, port, mysql.escape_string(name)))

        if cur.rowcount:
            con.close()
            self.privmsg(cinfo[1], "Server already exists.")
            return None

        cur.execute("""SELECT * FROM ioq3_servers""")

        if cur.rowcount > 32:
            con.close()
            self.privmsg(cinfo[1], "Server limit reached.")
            return None

        try:
            sv = ioq3.Ioq3(ip, port, name)
        except:
            cur.execute("""INSERT INTO ioq3_blacklist(ip, port, name, added_by)
                    VALUES ('%s', %d, '%s', '%s')""" %(ip, port, mysql.escape_string(name), mysql.escape_string(_from)))
            con.commit()
            con.close()
            self.privmsg(cinfo[1], "Invalid IP address.")
            return None

        cur.execute("""INSERT INTO ioq3_servers(ip, port, name, added_by)
                VALUES ('%s', %d, '%s', '%s')""" %(ip, port, mysql.escape_string(name), _from))
        con.commit()
        con.close()
        self.privmsg(cinfo[1], "Operation successful.")
        return None

    def _cmd_server_drop(self, name, cinfo):
        """
        Remove a server from the database
        """
        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM ioq3_servers WHERE name = '%s'""" %(mysql.escape_string(name)))

        if cur.rowcount == 0:
            self.privmsg(cinfo[1], "No such server.")
        elif cur.rowcount == 1:
            cur.execute("""DELETE FROM ioq3_servers WHERE name = '%s'""" %(mysql.escape_string(name)))
            con.commit()
            if cur.rowcount == 1:
                self.privmsg(cinfo[1], "Operation successful.")
            else:
                con.rollback()
                self.privmsg(cinfo[1], "Operation failed.")
        else:
            self.privmsg(cinfo[1], "Operation failed.")

        con.close()
        return None

    def _cmd_server_rename(self, old_name, new_name, cinfo):
        """
        Rename a server in the database
        """
        re_full_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{5}$')
        re_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}$')

        if len(mysql.escape_string(old_name)) >= 16 or len(mysql.escape_string(new_name)) >= 16:
            self.privmsg(cinfo[1], "Invalid server name(s).")
            return None

        if re.match(re_full_ip, mysql.escape_string(new_name)) or re.match(re_ip, mysql.escape_string(new_name)):
            self.privmsg(cinfo[1], "Invalid new server name.")
            return None

        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM ioq3_servers WHERE name = '%s'""" %(mysql.escape_string(old_name)))

        if cur.rowcount == 0:
            self.privmsg(cinfo[1], "No such server.")
        elif cur.rowcount == 1:
            cur.execute("""SELECT * FROM ioq3_servers WHERE name = '%s'""" %(mysql.escape_string(new_name)))
            if cur.rowcount != 0:
                self.privmsg(cinfo[1], "Server name in use.")
                con.close()
                return None
            cur.execute("""UPDATE ioq3_servers SET name = '%s' WHERE name = '%s'"""
                    %(mysql.escape_string(new_name), mysql.escape_string(old_name)))
            con.commit()
            if cur.rowcount == 1:
                con.commit()
                self.privmsg(cinfo[1], "Operation successful.")
            else:
                con.rollback()
                self.privmsg(cinfo[1], "Operation failed.")
        else:
            self.privmsg(cinfo[1], "Operation failed.")

        con.close()
        return None

    def _cmd_server_list(self, cinfo):
        """
        List the servers in the db
        """
        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT name FROM ioq3_servers""")

        if cur.rowcount > 32:
            con.close()
            self.privmsg(cinfo[1], "Server limit reached.")
            return None

        l = []
        for t in cur.fetchall():
            l.append(t[0])

        con.close()

        if len(l) == 0:
            self.privmsg(cinfo[1], "Server list is empty.")
        else:
            self.privmsg(cinfo[1], COLOR["boldgreen"]+"Current servers"+COLOR["rewind"]+':')
            self.privmsg(cinfo[1], ", ".join(l))
        return None

    def _cmd_server_retrieve(self, name):
        """
        Retrieve a server ip/port from the database given its name
        """
        ret = ["", 0]
        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT ip, port FROM ioq3_servers WHERE name = '%s'""" %(mysql.escape_string(name)))

        if cur.rowcount == 1:
            res = cur.fetchall()
            con.close()
            ret = [res[0][0], int(res[0][1])]
        else:
            cur.execute("""SELECT ip, port FROM ioq3_servers WHERE name LIKE '%s'""" %('%'+mysql.escape_string(name)+'%'))
            if cur.rowcount == 1:
                res = cur.fetchall()
                ret = [res[0][0], int(res[0][1])]
            con.close()

        return ret

    def _cmd_server_display(self, sv, cinfo):
        """
        Display game info from an ioq3.Ioq3 instance
        """
        players = []
        nb_bot = 0

        nb_cl = len(sv.cl_list)

        if sv.cl_list == []:
            use_pings = False
        elif len(sv.cl_pings) == len(sv.cl_list):
            use_pings = True

        for i in range(len(sv.cl_list)):
            if use_pings and sv.cl_pings[i] == 0:
                players.append(COLOR["boldgreen"] + ' ' + sv.cl_list[i] + COLOR["rewind"] +\
                        ' (' + COLOR["boldblue"] + "BOT" + COLOR["rewind"] + ')')
                nb_bot += 1
            else:
                players.append(COLOR["boldgreen"] + ' ' + sv.cl_list[i] + COLOR["rewind"])

        status = COLOR["boldwhite"] + sv.hostname + COLOR["rewind"] +\
                ': Playing:' + COLOR["boldgreen"] + ' ' + str(nb_cl - nb_bot) + (('+' +\
                str(nb_bot)) if nb_bot != 0 else '') + COLOR['rewind'] + '/' + str(sv.max_clients) +\
                ', map:' + COLOR["boldgreen"] + ' ' + sv.map + COLOR["rewind"] +\
                ', nextmap:' + COLOR["boldgreen"] + ' ' + sv.nextmap + COLOR["rewind"] +\
                ', gametype:' + COLOR["boldgreen"] + ' ' + sv.gametype2str(sv.gametype) + COLOR["rewind"] +\
                ', version:' + COLOR["boldgreen"] + ' ' + sv.version + COLOR["rewind"] +\
                ", IP:" + COLOR["boldgreen"] + ' ' + sv.ip + ':' + str(sv.port) + COLOR["rewind"]

        self.privmsg(cinfo[1], status)

        if nb_cl == 0:
            self.privmsg(cinfo[1], "Server is currently empty.")
        else:
            self.privmsg(cinfo[1], "Playing (" + str(nb_cl - nb_bot) +\
                    ('+' + str(nb_bot) if nb_bot != 0 else '') + '/' +\
                    str(sv.max_clients) + "):" + ','.join(players))
        return None

    def cmd_hash(self, ident, _from, to, msg):
        """
        Hash data using the specified hash algotithm
        hash [md5 | sha1 | sha256 | sha512] <data>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 3:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help hash.")
            return None

        if argv[1].lower() not in hashlib.algorithms:
            self.privmsg(cinfo[1], "Hash algorithm not available. Check "+self.risc.cmd_prefix+"help hash.")
            return None

        data = ' '.join(msg.split(' ')[2:])
        self.privmsg(cinfo[1], getattr(hashlib, argv[1].lower())(data).hexdigest())
        return None

    def cmd_base64(self, ident, _from, to, msg):
        """
        Base64 encode/decode data
        base64 [d|e] <data>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 3:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help base64.")
            return None

        data = ' '.join(msg.split(' ')[2:])

        if argv[1].lower() in ("d", "decode"):
            self.privmsg(cinfo[1], "'" + base64.b64decode(data) + "'")
        elif argv[1].lower() in ("e", "encode"):
            self.privmsg(cinfo[1], base64.b64encode(data))
        else:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help base64.")
            return None
        return None

    def cmd_uptime(self, ident, _from, to, msg):
        """
        Display risc's uptime
        uptime
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        self.privmsg(cinfo[1], COLOR["boldwhite"] + "Uptime" + COLOR["rewind"] +\
                ': ' + str(datetime.timedelta(seconds=int(time.time()) - risc.init_time)))
        return None

    def cmd_version(self, ident, _from, to, msg):
        """
        Display version and author(s) info
        version
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        self.privmsg(cinfo[1], "Version" + COLOR["boldwhite"] + ' ' + risc.__version__ +\
                ' ' + COLOR["rewind"] + "by" + COLOR["boldwhite"] + ' ' + risc.__author__ +\
                COLOR["rewind"])
        return None

    def cmd_search(self, ident, _from, to, msg):
        """
        Search for a player in the server list
        search <player>
        """
        ret = []
        fails = []
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help search.")
            return None

        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT ip, port, name FROM ioq3_servers""")

        if cur.rowcount == 0:
            con.close()
            self.privmsg(cinfo[1], "Server list is empty.")
            return None

        for info in cur.fetchall():
            sv = None
            use_pings = False
            try:
                sv = ioq3.Ioq3(info[0], int(info[1]), name=info[2], timeout=0.3)
            except Exception, e:
                fails.append(info[2] + ' (' + COLOR["boldred"] + str(e) + COLOR["rewind"] + ')')
                continue

            if len(sv.cl_list) == len(sv.cl_pings):
                use_pings = True

            for cl in sv.cl_list:
                if len(ret) >= 11:
                    self.privmsg(cinfo[1], "Too many matches. Try to be more specific.")
                    return None
                if re.search(argv[1].lower(), cl.lower()):
                    if use_pings and sv.cl_pings[sv.cl_list.index(cl)] == 0:
                        ret.append(COLOR["boldgreen"] + cl + ' ' + COLOR["rewind"] + '(' + COLOR["boldblue"] +\
                                "BOT" + COLOR["rewind"] + ', ' + COLOR["boldblue"] + sv.name + COLOR["rewind"] + ')')
                    else:
                        ret.append(COLOR["boldgreen"] + cl + ' ' + COLOR["rewind"] + '(' + COLOR["boldblue"] +\
                                sv.name + COLOR["rewind"] + ')')

        if len(fails) > 0 and len(fails) < 6:
            self.privmsg(cinfo[1], "Failed to query the following servers: %s." %(", ".join(fails)))
        elif len(fails) > 5:
            self.privmsg(cinfo[1], "%s servers failed to respond." %(COLOR["boldred"] + str(len(fails)) + COLOR["rewind"]))

        if len(ret) > 0:
            self.privmsg(cinfo[1], COLOR["boldwhite"] + "Players matching the request" + COLOR["rewind"] + ':')
            self.privmsg(cinfo[1], ", ".join(ret))
        else:
            self.privmsg(cinfo[1], "No players matching the request.")
        return None

    def cmd_roulette(self, ident, _from, to, msg):
        """
        Russian roulette game
        roulette
        """
        global r_bullet
        global r_chamber

        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        if r_bullet == r_chamber:
            self.privmsg(cinfo[1], COLOR["boldred"] + "* BANG *" + COLOR["rewind"]+" -" + COLOR["boldred"] +\
                    ' ' + _from + ' ' + COLOR["rewind"] + "is no more.")
            self.irc.kick(_from, "rekt")
            r_bullet = random.randint(1, 0xffff) % 7
            r_chamber = random.randint(1, 0xffff) % 7
        else:
            self.privmsg(cinfo[1], COLOR["boldgreen"] + "+ click +" + COLOR["rewind"]+" -" + COLOR["boldgreen"] +\
                    ' ' + _from + ' ' + COLOR["rewind"] + "is safe.")
            r_chamber = (r_chamber + 1) % 7
        return None

    def cmd_kill(self, ident, _from, to, msg):
        """
        UrT-like kill messages
        kill <opt_user> <opt_weapon>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        weapons = {"colt": [" was given a new breathing hole by ", "'s Colt 1911."],
                "spas": [" was turned into peppered steak by ", "'s SPAS blast."],
                "ump45": [" danced the ump tango to ", "'s sweet sweet music."],
                "mp5": [" was MP5K spammed without mercy by ", "'s MP5K."],
                "mac11": [" was minced to death by ", "'s Mac 11."],
                "lr300": [" played 'catch the shiny bullet with ", "'s LR-300 rounds."],
                "g36": [" was on the wrong end of ", "'s G36."],
                "ak103": [" was torn asunder by ", "'s crass AK103."],
                "m4": [" got a lead enema from ", "'s retro M4."],
                "psg1": [" was taken out by ", "'s PSG1. Plink!"],
                "hk69": [" HEARD ", "'s HK69 gren... didn't AVOID it. Sucka."],
                "boot": [" git himself some lovin' from ", "'s boot o' passion."],
                "sr8": [" managed to slow down ", "'s SR-8 round just a little."],
                "bleed": [" bled to death from ", "'s attacks."],
                "negev": [" got shredded to pieces by ", "'s Negev."],
                "knife": [" was sliced a new orifice by ", "."],
                "knife_throw": [" managed to sheath ", "'s flying knife in their flesh."],
                "beretta": [" was pistol whipped by ", "."],
                "g18": [" got a whole plastic surery with ", "'s Glock"],
                "de": [" got a whole lot of hole from ", "'s DE round."],
                "nuke": [" has been nuked by ", "."],
                "bfg": [" has been blasted by ", "'s BFG."],
                "rpg": [" ate ", "'s rockets."],
                "lightning": [" has been deep fried by ", "."],
                "slap": [" has been slapped to death by ", "."]}

        if argc == 1:
            self.privmsg(cinfo[1], COLOR["boldgreen"] + _from + ' ' + COLOR["rewind"] + "has an urge to kill ...")

        elif argc == 2:
            if argv[1].lower() in ("-all", "-channel", "-everyone"):
                self.privmsg(cinfo[1], COLOR["boldred"] + random.choice(["The whole channel", "Everyone", "Everybody"]) +\
                        ' ' + COLOR["rewind"] + "has been murdered by" + ' ' + COLOR["boldgreen"] + _from + COLOR['rewind']+".")
            elif _from.lower() == argv[1].lower():
                self.privmsg(cinfo[1], COLOR["boldred"] + _from + ' ' + COLOR["rewind"] + "went an hero.")
            elif self.irc.nick.lower() == argv[1].lower():
                self.privmsg(cinfo[1], "You cannot kill me," + ' ' + COLOR['boldred'] + "I KILL YOU!" + COLOR["rewind"])
                self.irc.kick(_from, "I KILL YOU!")
            elif argv[1] in self.irc.users:
                self.privmsg(cinfo[1], COLOR["boldgreen"] + _from + ' ' + COLOR["rewind"] + "killed " + argv[1] + ".")
            else:
                self.privmsg(cinfo[1], "This person doesn't exist.")

        elif argc >= 3:
            if not argv[1] in self.irc.users:
                self.privmsg(cinfo[1], "This person doesn't exist.")
            elif argv[2].lower() in weapons:
                self.privmsg(cinfo[1], COLOR["boldred"] + argv[1] + COLOR['rewind'] + weapons[argv[2].lower()][0] +\
                        COLOR["boldgreen"] + _from + COLOR["rewind"] + weapons[argv[2].lower()][1])
            else:
                self.privmsg(cinfo[1], COLOR["boldred"] + argv[1] + ' ' + COLOR["rewind"] + "has been creatively killed by" +\
                        ' ' + COLOR["boldgreen"] + _from + ' ' + COLOR["rewind"] + "using a " + argv[2] + ".")

        else:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help kill.")
        return None

    def cmd_raw(self, ident, _from, to, msg):
        """
        Send raw commands to the IRC server
        raw <command>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        cmd = ' '.join(argv[1:])
        self.irc._send(self.risc.ident + ' ' + cmd)
        return None

    def cmd_lower(self, ident, _from, to, msg):
        """
        Return a lowercased string
        lower <string>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help lower.")
            return None

        self.privmsg(cinfo[1], ' '.join(argv[1:]).lower())
        return None

    def cmd_upper(self, ident, _from, to, msg):
        """
        Return a uppercased string
        upper <string>
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help upper.")
            return None

        self.privmsg(cinfo[1], ' '.join(argv[1:]).upper())
        return None

    def cmd_quote(self, ident, _from, to, msg):
        """
        Add a quote to the database
        quote [add <quote> | drop <quote_id> | find <regex> | last]
        """
        cinfo = self.init_cmd(ident, _from, to, msg)

        if cinfo[2] < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        argv = self.clean_list(msg.split(' '))
        argc = len(argv)

        if argc < 2:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
            return None

        if argv[1].lower() == "add":
            if argc < 3:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
                return None
            self._cmd_quote_add(' '.join(msg.split(' ')[2:]), _from, cinfo)
        elif argv[1].lower() in ("drop", "rm"):
            if argc < 3:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
                return None
            elif not argv[2].isdigit():
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
                return None
            self._cmd_quote_drop(int(argv[2]), cinfo)
        elif argv[1].lower() in ("find", "ls", "match"):
            if argc < 3:
                self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
                return None
            self._cmd_quote_find(' '.join(msg.split(' ')[2:]), cinfo)
        elif argv[1].lower() == "last":
            self._cmd_quote_last(cinfo)
        else:
            self.privmsg(cinfo[1], "Check "+self.risc.cmd_prefix+"help quote.")
        return None

    def _cmd_quote_add(self, quote, _from, cinfo):
        """
        Add a quote to the database
        """
        _quote = mysql.escape_string(quote)
        author = mysql.escape_string(_from)

        if len(_quote) > 256:
            self.privmsg(cinfo[1], "Quote length overflow.")
            return None

        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM quote WHERE quote.quote = '%s'""" %(_quote))

        if cur.rowcount:
            con.close()
            self.privmsg(cinfo[1], "Quote already exists.")
            return None

        cur.execute("""INSERT INTO quote(quote, added_by) VALUES('%s', '%s')""" %(_quote, author))
        con.commit()
        con.close()

        self.privmsg(cinfo[1], "Operation successful.")
        return None

    def _cmd_quote_drop(self, quote_id, cinfo):
        """
        Remove a quote from the database
        """
        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM quote WHERE id = %d""" %(quote_id))

        if cur.rowcount == 0:
            self.privmsg(cinfo[1], "No such quote.")
        elif cur.rowcount == 1:
            cur.execute("""DELETE FROM quote WHERE id = %d""" %(quote_id))
            con.commit()
            if cur.rowcount == 1:
                self.privmsg(cinfo[1], "Operation successful.")
            else:
                con.rollback()
                self.privmsg(cinfo[1], "Operation failed.")
        else:
            self.privmsg(cinfo[1], "Operation failed.")

        con.close()
        return None

    def _cmd_quote_find(self, regex, cinfo):
        """
        Search for a quote in the database
        """
        matches = []

        if not self.is_valid_re(regex):
            self.privmsg(cinfo[1], "Invalid regex.")
            return None

        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM quote""")

        if cur.rowcount:
            for quote in cur.fetchall():
                if re.search(regex, quote[1], re.IGNORECASE):
                    matches.append(quote)
                    if len(matches) > 3:
                        break
        con.close()

        if not matches:
            self.privmsg(cinfo[1], "No such quote.")
            return None

        for quote in matches:
            self._cmd_quote_display(quote, cinfo)
        return None

    def _cmd_quote_last(self, cinfo):
        """
        Display last quote
        """
        con = mysql.connect(self.risc.db_host, self.risc.db_user, self.risc.db_passwd, self.risc.db_name)
        cur = con.cursor()

        cur.execute("""SELECT * FROM quote ORDER BY id DESC LIMIT 1""")

        if cur.rowcount:
            self._cmd_quote_display(cur.fetchall()[0], cinfo)
        else:
            self.privmsg(cinfo[1], "Quote list is empty.")

        con.close()
        return None

    def _cmd_quote_display(self, quote, cinfo):
        """
        Display a quote, from quote tuple retrieved in the database
        quote[0] = id
        quote[1] = quote
        quote[2] = added_by
        quote[3] = added_on
        """
        if not quote:
            return None

        _id = quote[0]
        _quote = quote[1].decode("string_escape")
        author = quote[2].decode("string_escape")
        timestamp = str(quote[3])

        fmt = "\x02#" + str(_id) + "\x0f " + _quote + " - \x02" + author + "\x0f - \x02" + timestamp + "\x0f"
        self.privmsg(cinfo[1], fmt)
        return None
