#!/usr/bin/python2
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

__author__ = 'Preacher'
__version__ = '1.6-dev'


import time
import ConfigParser
import re
import MySQLdb as mysql
from warnings import filterwarnings
from mechanize import Browser
import debug
import irc
import ioq3
import cmd

INIPATH = "risc.ini"
init_time = int(time.time())
MAX_Q3_SERVERS = 32

class Risc():
    """
    Main class containing the event dispatcher
    """
    def __init__(self):
        try:
            self.debug = debug.Debug(0, "risc")
            self.load_config()
            self.irc = irc.Irc(self.host, self.port, self.channel, self.nick)
            self.cmd = cmd.Cmd(self)
            filterwarnings("ignore", category = mysql.Warning)
        except:
            self.debug.critical("Risc.__init__: Exception caught while loading config settings - Make sure there's no missing field")
            raise SystemExit

    def load_config(self):
        """
        Load config settings
        """
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(INIPATH)

        # Gather config info
        self.host = self.cfg.get('irc', 'host')
        self.port = int(self.cfg.get('irc', 'port'))
        self.channel = self.cfg.get("irc", "channel")
        self.nick = self.cfg.get("irc", "nick")
        self.db_host = self.cfg.get('db', 'host')
        self.db_user = self.cfg.get('db', 'user')
        self.db_passwd = self.cfg.get('db', 'passwd')
        self.db_name = self.cfg.get('db', 'self_db')                                    # db for risc settings (admins etc)
        self.anti_spam_threshold = int(self.cfg.get("risc", "anti_spam_threshold"))
        self.on_kick_delay = int(self.cfg.get("risc", "on_kick_delay"))
        self.on_timeout_delay = int(self.cfg.get("risc", "on_timeout_delay"))
        self.svs = self.cfg.get('var', 'servers').split(',')                            # Get servers, their dbs
        self.auth = self.cfg.get('irc', 'auth')
        self.auth_passwd = self.cfg.get('irc', 'auth_passwd')
        self.cmd_prefix = self.cfg.get('risc', 'cmd_prefix')
        self.cmd_prefix_global = self.cfg.get('risc', 'cmd_prefix_global')

        if len(self.svs) > MAX_Q3_SERVERS:
            self.debug.error('Too many servers. Max: %u' %(MAX_Q3_SERVERS))

        if len(self.cmd_prefix) != 1:
            self.cmd_prefix = '!'

        if len(self.cmd_prefix_global) != 1:
            self.cmd_prefix_global = '@'

        self.load_cmd_levels()
        return None

    def load_cmd_levels(self):
        """
        Load cmd levels from config
        """
        for c in cmd.cmds:
            lvl = ''
            if self.cfg.has_option("levels", "cmd_"+c):
                lvl = self.cfg.get("levels", "cmd_"+c).lower()
                if lvl in ("root", "r"):
                    cmd.cmds[c][cmd.CMD_LEVEL] = 4
                elif lvl in ("op", "o"):
                    cmd.cmds[c][cmd.CMD_LEVEL] = 2
                elif lvl in ("voice", "v"):
                    cmd.cmds[c][cmd.CMD_LEVEL] = 1
                else:
                    cmd.cmds[c][cmd.CMD_LEVEL] = 0
        return None

    def start(self):
        """
        Launch the bot: connect, start event dispatcher, join
        """
        self.irc.set_callback("on_welcome", self.on_welcome)
        self.irc.set_callback("on_privmsg", self.on_privmsg)
        self.irc.start()
        return None

    def stop(self):
        """
        Stop the IRC module and leave
        """
        self.debug.info("Exiting")
        self.irc.stop()
        return None

    def clean_list(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != "" and e != ' ':
                ret.append(e)
        return ret

    def on_privmsg(self, _from, to, msg):
        """
        Called on PRIVMSG
        """
        if msg[0] in (self.cmd_prefix, self.cmd_prefix_global):
            self.cmd.process(_from, to, msg)
        else:
            self.process_irc(_from, to, msg)
        return None

    def on_welcome(self, host, welcome_msg):
        """
        Called after we successfully connected to the server
        """
        self.irc._send("PRIVMSG Q@CServe.quakenet.org :AUTH "+self.auth+" "+self.auth_passwd)
        self.irc.mode(self.nick, "+x")
        time.sleep(0.8)
        self.debug.info("Joining " + self.channel + " ...")
        self.irc.join()
        self.debug.info("Done")
        return None

    def xurls(self, raw_msg):
        """
        Extract URLs from str to a list
        """
        raw_msg = self.clean_list(raw_msg.split(' '))
        re_url = re.compile(r'(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}'\
                '[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}'\
                '\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[?[A-F0-9]*:[A-F0-9:]+\]?)(?::\d+)?(?:'\
                '/?|[/?]\S+)$', re.IGNORECASE)
        ret = []
        for s in raw_msg:
            if re.match(re_url, s):
                ret.append(s)
        return ret

    def process_irc(self, _from, to, msg):
        """
        Handle IRC messages
        """
        # Process URLs posting
        for url in self.xurls(msg):
            try:
                br = Browser()
                br.set_handle_robots(False)
                br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')]
                br.open(url)
                self.privmsg(self.channel, "Title: " + br.title())
            except Exception, e:
                self.debug.error("process_irc: Exception caught: '%s'." % e)
        return None

def main():
    print "[+] Running ..."
    try:
        inst = Risc()
        inst.start()
    except KeyboardInterrupt:
        inst.debug.warning('Caught <c-c>. Exiting.')
        inst.stop()
    except SystemExit:
        inst.stop()
    except TypeError:
        inst.debug.critical('Caught TypeError exception on Risc.start(): Contact an admin to fix this asap.')
        inst.stop()
    except NameError:
        inst.debug.critical('Caught NameError exception on Risc.start(): Contact an admin to fix this asap.')
        inst.stop()
    except UnicodeDecodeError:
        inst.debug.critical('Caught UnicodeDecodeError exception on Risc.start().')
    except Exception, e:
        if str(e) == "risc_exception_irc_timeout":
            main()
        else:
            inst.debug.critical("Unhandled exception on Risc(): '%s'. Exiting." % e)
            inst.stop()

if __name__ == "__main__":
    main()
