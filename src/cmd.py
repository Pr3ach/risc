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

cmds = {"help": [["h"], 0],
        "quit": [["leave", "disconnect", "q"], 0],
        "google": [["g"], 0],
        "server": [["status", "sv", "st"], 0],
        "hash": [[], 0],
        "uptime": [[], 0],
        "base64": [["b64"], 0],
        "search": [["s"], 0],
        "version": [["v"], 0],
        "roulette": [["r"], 0],
        "kill": [["k"], 0],
        "raw": [["raw"], 0]}

CMD_ALIASES = 0
CMD_LEVEL = 1

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

    def get_cmd(self, msg):
        """
        Return the original command name from the message if it exists, return "" otherwise
        """
        cmd = self.clean_list(msg.split(' '))[0][1:]

        if cmd in cmds:
            return cmd

        for c in cmds:
            if cmd in cmds[c][CMD_ALIASES]:
                return c
        return ""

    def get_cmd_from_alias(self, cmd_alias):
        """
        Retrieve the original cmd name from an alias, if it exists, return "" otherwise
        """
        if cmd_alias in cmds:
            return cmd_alias

        for cmd in cmds:
            if cmd_alias in cmds[cmd][CMD_ALIASES]:
                return cmd
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
            if hasattr(self, "cmd_"+cmd):
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

        if argc == 1:
            self.privmsg(cinfo[1], "Commands: %s." %(', '.join(cmds.keys())))
        else:
            cmd = self.get_cmd_from_alias(argv[1])
            if cmd == "":
                self.privmsg(cinfo[1], "Command not found: %s." %(argv[1]))
                return None
            if hasattr(self, "_cmd_help_"+cmd):
                getattr(self, "_cmd_help_"+cmd)(_from, to, msg, cmd)
        return None

    def _cmd_help_help(self, _from, to, msg, cmd):
        """
        Help for help command ...
        """
        cinfo = self.init_cmd(_from, to, msg)
        self.privmsg(cinfo[1], "-_-'")
        return None

    def _cmd_help_quit(self, _from, to, msg, cmd):
        """
        Help for quit command
        """
        cinfo = self.init_cmd(_from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        self.privmsg(cinfo[1], "Usage: quit. Description: Close the connection to "\
                "the IRC server and exit. Aliases: " +\
                ", ".join(cmds[cmd][CMD_ALIASES])+'.'+" Access: "+access+'.')
        return None

    def _cmd_help_google(self, _from, to, msg, cmd):
        """
        Help for google command
        """
        cinfo = self.init_cmd(_from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        self.privmsg(cinfo[1], "Usage: google <query>. Description: Search for <query> in google "\
                "and display the results. Aliases: " +\
                ", ".join(cmds[cmd][CMD_ALIASES])+". Access: "+access+'.')
        return None

    def _cmd_help_server(self, _from, to, msg, cmd):
        """
        Help for server command
        """
        cinfo = self.init_cmd(_from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        self.privmsg(cinfo[1], "Usage: server [<ip:opt_port> | <name> | add "\
                "<ip:opt_port> <name> | drop <name> | rename <old_name> <new_name> "\
                "| list]. Description: Manage ioq3 based game servers. Aliases: " +\
                ", ".join(cmds[cmd][CMD_ALIASES]) + ". Access: "+access+'.')
        return None

    def _cmd_help_hash(self, _from, to, msg, cmd):
        """
        Help for hash command
        """
        cinfo = self.init_cmd(_from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        self.privmsg(cinfo[1], "Usage: hash [md5 | sha1 | sha256 | sha512] <data>. "\
                "Description: Hash <data> using the specified algorithm. "\
                "Aliases: " + ", ".join(cmds[cmd][CMD_ALIASES]) +\
                ". Access: "+access+'.')
        return None

    def _cmd_help_uptime(self, _from, to, msg, cmd):
        """
        Help for uptime command
        """
        cinfo = self.init_cmd(_from, to, msg)
        access = "all"

        if cmds[cmd][CMD_LEVEL] == 4:
            access = "root"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['o']:
            access = "op"
        elif cmds[cmd][CMD_LEVEL] == irc.LEVEL_MASKS['v']:
            access = "voice"

        self.privmsg(cinfo[1], "Usage: uptime. "\
                "Description: Display risc's uptime. "\
                "Aliases: " + ", ".join(cmds[cmd][CMD_ALIASES]) +\
                ". Access: "+access+'.')
        return None

    def cmd_quit(self, _from, to, msg):
        """
        Simply leave
        quit
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        self.risc.stop()
        return None

    def cmd_google(self, _from, to, msg):
        """
        Query google
        google <query>
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
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

        if len(json.loads(res.text)['responseData']['results']):
            self.privmsg(cinfo[1], "Top hits:")
        else:
            self.privmsg(cinfo[1], "No results.")
            return None

        for hit in json.loads(res.text)["responseData"]["results"]:
            self.privmsg(cinfo[1], hit["url"])
            i+=1
            if i > 4:
                break
        return None

    def cmd_server(self, _from, to, msg):
        """
        Display game information about the specified server
        server [<ip:opt_port> | <name> | add <ip:opt_port> <name> | drop <name> | rename <old_name> <new_name> | list]
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
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
                    VALUES ('%s', %d, '%s', '%s')""" %(ip, port, mysql.escape_string(name), _from))
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
            self.privmsg(cinfo[1], COLOR["boldgreen"]+"Current servers:"+COLOR["rewind"])
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

        if sv.clients != -1:
            nb_cl = sv.clients
        elif sv.cl_list != []:
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

        status = COLOR['boldgreen'] + sv.hostname + COLOR['rewind'] +\
                ': Playing:' + COLOR['boldblue'] + ' ' + str(nb_cl - nb_bot) + (('+' +\
                str(nb_bot)) if nb_bot != 0 else '') + COLOR['rewind'] + '/' + str(sv.max_clients) +\
                ', map:' + COLOR['boldblue'] + ' ' + sv.map + COLOR['rewind'] +\
                ', nextmap:' + COLOR['boldblue'] + ' ' + sv.nextmap + COLOR["rewind"] +\
                ', gametype:' + COLOR['boldblue'] + ' ' + sv.gametype2str(sv.gametype) + COLOR['rewind'] +\
                ', version:' + COLOR['boldblue'] + ' ' + sv.version + COLOR['rewind'] +\
                ", IP:" + COLOR["boldblue"] + ' ' + sv.ip + ':' + str(sv.port) + COLOR["rewind"]

        self.privmsg(cinfo[1], status)

        if nb_cl == 0:
            self.privmsg(cinfo[1], "Server is currently empty.")
        else:
            self.privmsg(cinfo[1], "Playing (" + str(nb_cl - nb_bot) +\
                    ('+' + str(nb_bot) if nb_bot != 0 else '') + '/' +\
                    str(sv.max_clients) + "):" + ','.join(players))
        return None

    def cmd_hash(self, _from, to, msg):
        """
        Hash data using the specified hash algotithm
        hash [md5 | sha1 | sha256 | sha512] <data>
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
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

    def cmd_uptime(self, _from, to, msg):
        """
        Display risc's uptime
        uptime
        """
        cinfo = self.init_cmd(_from, to, msg)

        if self.irc.get_user_level(_from) < cinfo[0]:
            self.privmsg(self.risc.channel, COLOR["boldred"]+_from+COLOR["rewind"]+\
                    ": Access denied. Check "+self.risc.cmd_prefix+"help "+self.get_cmd(msg)+'.')
            return None

        self.privmsg(cinfo[1], "Uptime: " + str(datetime.timedelta(seconds=int(time.time()) - risc.init_time)))
        return None
