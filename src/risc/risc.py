#!/usr/bin/python2
# -*- coding: utf-8 -*-

# CHANGELOG
#
#       - Add !status/!st command [OK]
#       - Fix update_hist() [OK]
#       - Add !players <serverName> command [OK]
#       - Minor bug fixed [OK]
#       - Add colors [OK]
#       - Fix colors not working on non-console client [OK]
#       - Remove ^1 etc from map names [ok]
#       - Add aliases for args [ok]
#       - Add !base64 / !sha1 / !md5 [OK]
#       - Change lastposts to lastthreads / lt [OK]
#       - Add bold colors [OK]
#       - Add thread author [OK]
# ------- 1.1 - Preacher
#       - Use UDP instead of qstat stuff [OK]
#       - Add !search <player> [OK]
#       - Add !disasm [OK]
#       - Add !hi <user> [OK]
#       - Add <server> optional arg to !search && add limit of user output to !search [OK]
#       - Make the distinction between players & bots [OK]
#       - Fix server auth stuff [OK]
# ------- 1.2 - Preacher
#       - Add !ikick (in irc kick) [OK]
#       - !lt now returns a link to the last post in the thread [OK]
#       - Write irc_is_admin(): returns auth + level from *nick* [OK]
#       - Add required rights to help command [OK]
#       - Add !ilt / ileveltest command [OK]
#       - Updated irc_is_admin [OK]
#       - Fixed time response in TIME ctcp [OK]
#       - Fixed unicode char causing crash [OK]
#       - Improved debug info [OK]
#       - irc_is_on_channel() [OK]
#       - irc_is_authed() [OK] FIXME: too slow
#       - Set cmd output in pm [OK]
#       - Add support for pm cmds [OK]
#       - Add support for @ prefixed cmd's [OK]
#       - Add support for in-game calladmin cmd [OK]
#       - Removed disasm [OK]
#       - Add threading support for game events [OK]
# ------- 1.3 - Preacher
#       - Minor change in colors [OK]
#       - Added chat ability (IRC to game, other side implemented in riscb3 plugin) [OK]
#       - q3_to_IRC_color() [OK]
#       - PEP8: LF between functions and classes [OK]
#       - PEP8: Removed file encoding [OK]
#       - PEP8: Updated comments [OK]
#       - PEP8: Multiple fixes (comments, functions) [OK]
#       - PEP8: Global var, constant [OK]
#       - PEP8: Fixed all (except 79 chars standard) [OK]
#       - Fix reason chars on game events (^[0-9]) [OK]
#       - Set th.daemon = True for game_watcher thread [OK]
#       - More accurate time for ban [OK]
#       - Added cmd description for !chat [OK]
#       - Add seen cmd - 10/08/2014: fixed exception [OK]
#       - Cleaned up very long lines [OK]
#       - Fix version field for !st cmd (rm "\^[0-9]") [OK]
#       - Removed mysql warnings output [OK]
#       - Fix (again) crash for unicode chars [OK]
#       - Temp. disabled cmds until fixed: st, players, search [OK]
#       - Typo fixed for help cmds [OK]
# ------- 1.4 - Preacher - 08/18/2014
#       - Removed bot cred. from risc.ini [OK]
#       - Make sh added [OK]
# ------- 1.4.1 - Preacher - 08/19/2014
#       - Fixed 'make-nix.sh' [OK]
# ------- 1.4.2 - Preacher - 08/20/2014
#       - Fixed major bug in Sv [OK]
#       - Fix: use only one db & table for admins [OK]
#       - Bot auth credentials in risc.ini [OK]
#       - Remove !lt cmd from help <cmd> cmd [OK]
#       - Section in risc.ini for server alias [OK]
# ------- 1.4.3 - Preacher - 09/04/2014
#       - Add cmd levels to ini conf file [OK]
#       - Add admin init list to ini conf file [OK]
#       - Add ability to use custom cmd prefixes [OK]
#       - Allow chat in one server at a time only [OK]
#       - Dynamic help msg [OK]
#       - Update README file [OK]
# ------- 1.4.4 - Preacher - 09/07/2014
#       - Fix minor dbg code [OK]
#       - Fixed Sv failling -> crash [OK]
#       - Added cmd 'say' for admins [OK]
#       - Fix typo in help & help say [OK]
#       - Fix typo in cmd_status [OK]
#       - Added cmd google [OK]
#       - Fix bug for is_global_cmd [OK]
#       - Add cmd 'server' [OK]
#       - Small changes in cmd hello [OK]
#       - Minor bug fixes [OK]
#       - Add cmd 'uptime' [OK]
#       - Anti-spam [OK]
#       - Add cmd 'version' [OK]
# ------- 1.4.5 - Preacher - 10/12/2014
#       - Added server hostname for cmd 'server' [OK]
#       - Added player list to cmd 'server' [OK]
#       - Info on link posting [OK]
#       - Fix error handling for Sv class [OK]
#       - Fixed: "status all" was failling even if not all serv failed querying [OK]
#       - Do not start game_watcher callback when risb3 ain't running [OK]
#       - Add "roulette" cmd [OK]
#       - Improved server data parsing: prevent some possible 'exploit' by user msgs [OK]
#       - Implement on_kick & auto join on kick [OK]
#       - Fix cmd 'search' with server specified [OK]
#       - Fix for 'sv' cmd when no port specified [OK]
#       - Fix for reason param. in cmd "ikick" [OK]
#       - Use lib 'requests' [OK]
#       - Add some headers for http req [OK]
#       - Use lib 'requests' for cmd google [OK]
#       - Add server IP for cmd 'st <sv>' [OK]
#       - Minor changes for cmd_status() [OK]
#       - Minor fix to set_evt_callbacks() [OK]
#       - Removed some useless libs [OK]
#       - Added cmd_duck [OK]
#       - Fix 'search <cl> <sv>' when <sv> is down -> crash [OK]
# ------- 1.5 - Preacher - 12/04/2014
#       - Slightly updated russian roulette game (thx @MrYay) [OK]
#       - Fix for russian roulette [OK]
#       - Fix bug with some player colored names in cmd_players [OK]
#       - Applied & fixed @MrYay patch cmd_kill [OK]
#       - Fixed (again) cmd_kill [OK]
#       - Updated cmd_players [OK]
#       - Updated cmd_server [OK]
#       - Improved server-client data processing [OK]
#       - Keep an irc userlist & update it as users join/leave/nick/kick [OK]
#       - Auto change nick on nick in use [OK]
#       - Add cmd raw [cmd] [OK]
#       - Add ability to completely disable riscb3 related functions/threads [OK]
#       - Don't stop on Exception in cmd_search [OK]
#       - Add cmd todo /add/rm/list [OK]
#       - Fix the whole admin management system [OK]
#       - Drop hello cmd [OK]
#       - Fix roulette cmd (yes, again) [OK]
#       - Add ability to "sv add/rm/rename/list" [OK]
#       - Fix "Title: <empty>" bug on some links [OK]
#       - Fix utf issues [OK]
#       - Fix sv rename bug [OK]
#       - Add server IP to cmd_sv [OK]
#       - Add auto reconnect when timeout [OK]
#       - Allow partial name in sv [TEST]
#       - Add cmd_remindme
# ------- 1.6 - Preacher - MM/DD/YYYY


__author__ = 'Preacher'
__version__ = '1.6-dev'


import socket
import threading
import time
import sys
import ConfigParser
import re
import base64
import hashlib
import MySQLdb as mysql
from warnings import filterwarnings
import json
import datetime
import lxml.html
import tld
import random
import requests
from irc_rpl import *
from mechanize import Browser

init_time = int(time.time())
last_cmd_time = 0
HELP = None
CMDS = "help,ishowadmins,disconnect,status,players,base64,sha1,md5,search,ikick,iputgroup,ileveltest,seen,chat,say,google,server,uptime,version,roulette,duck,kill,raw,todo"
chat_set = {}
INIPATH = "risc.ini"
is_global_msg = 0  # Set if the command starts with '@' instead of '!'
users = {}         # {"user.lower()" :{"chan_lvl": "operator|voice"}} # Can't rely on chan_lvl: 'bug' on rename ...
debug_mode = 1
THREADS_STOP = 0

# used by cmd_roulette()
roulette_shot = random.randint(1, 6)
roulette_cur = random.randint(1, 6)

# IRC color codes
COLOR = {'white': '\x030', 'boldwhite': '\x02\x030', 'green': '\x033', 'red': '\x035',
        'magenta': '\x036', 'boldmagenta': '\x02\x036', 'blue': '\x032',
        'boldred': '\x02\x034', 'boldblue': '\x02\x032', 'boldgreen': '\x02\x033',
        'boldyellow': '\x02\x038', 'boldblack': '\x02\x031', 'rewind': '\x0f'}

##########################################################################################################
#                                                                                                        #
#                                                                                                        #
#                                       START HERE                                                       #
#                                                                                                        #
#                                                                                                        #
##########################################################################################################


class Debug:
    """
    Set of functions to write to the log file
    """
    def __init__(self, use__stdout__):
        t = time.time()

        if not use__stdout__:
            sys.stdout = open("risc_"+str(int(t))+'.log', "w+", 0)

    def info(self, info_msg):
        t = time.localtime()
        print '%d/%d %d:%d:%d INFO %s' % (t[1], t[2], t[3], t[4], t[5], info_msg)
        return None

    def debug(self, debug_msg):
        t = time.localtime()
        print '%d/%d %d:%d:%d DEBUG %s' % (t[1], t[2], t[3], t[4], t[5], debug_msg)
        return None

    def warning(self, warning_msg):
        t = time.localtime()
        print '%d/%d %d:%d:%d WARNING %s' % (t[1], t[2], t[3], t[4], t[5], warning_msg)
        return None

    def error(self, error_msg):
        t = time.localtime()
        print '%d/%d %d:%d:%d ERROR %s' % (t[1], t[2], t[3], t[4], t[5], error_msg)
        return None

    def critical(self, critical_msg):
        t = time.localtime()
        print '%d/%d %d:%d:%d CRITICAL %s' % (t[1], t[2], t[3], t[4], t[5], critical_msg)
        return None


class Sv():
    """
    Gather info about a specific UrT 4.2 server (ioq3 engine)
    """
    def __init__(self, ip, port, name, debug):
        self.debug = debug

        # Match a "valid" ip
        if re.match('^([0-9]{1,3}\.){3}[0-9]{1,3}$', ip) is None:
            self.debug.warning('Sv.__init__(): IP seems invalid.')
            raise Exception('Sv.__init__(): Invalid IP.')
        self.ip = ip
        self.port = port
        self.name = name
        self.clientsPings = []
        try:
            # Using UDP for UrT
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((ip, port))
            self.sock.settimeout(3)
        except Exception, e:
            if self.sock:
                self.sock.close()
            self.debug.error("Sv.__init__(): Couldn't connect to the given ip,port: '%s'" % e)
            raise Exception("Sv.__init__(): Couldn't connect to the given ip,port: '%s'" % e)
        if not self.getstatus():
            if self.sock:
                self.sock.close()
            raise Exception("Sv.getstatus() failure.")
        if not self.getinfo():
            if self.sock:
                self.sock.close()
            raise Exception("Sv.getinfo() failure.")
        self.check_vars()
        if self.sock:
            self.sock.close()

    def list_clean(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != '' and e != ' ':
                ret.append(e)
        return ret

    def get_clients_list(self, raw):
        """
        Return the player list and set the ping list
        """
        cl = re.findall('".+', raw[len(raw)-1])  # Find nicks, which are surrounded by "
        if not cl:
            return -1                            # No players
        for i in range(len(cl)):
            cl[i] = re.sub('\^.', '', cl[i])[1:][:-1]

        # Retrieve pings in the same order of players
        pings = re.findall('\\n[0-9]{1,3}\s[0-9]{1,3}\s', raw[len(raw)-1])
        if len(pings) > 0:
            for i in range(len(pings)):
                pings[i] = pings[i].split(' ')[1]
            self.clientsPings = pings

        return cl

    def get_var(self, l, var):
        """
        Return the content of the requested cvar if available in the buffer, otherwise return -1
        """
        for i in range(len(l)):
            if l[i] == var:
                return l[i+1]
        return -1

    def check_vars(self):
        """
        Check whether a Cvar was set on the server or not, ie: if it was in the buffer. If not, set it to 'Not set'
        """
        if self.allowVote == -1:
            self.allowVote = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.version == -1:
            self.version = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.gameType == -1:
            self.gameType = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.nextMap == -1:
            self.nextMap = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.clients == -1:
            self.clients = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.maxClients == -1:
            self.maxClients = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.mapName == -1:
            self.mapName = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        if self.hostname == -1:
            self.hostname = COLOR['boldmagenta']+'Not set'+COLOR['rewind']
        return None

    def getstatus(self):
        try:
            self.sock.send(b'\xff'*4+b'getstatus')
            rawStatus = str(self.sock.recv(4096))
            listStatus = self.list_clean(rawStatus.split('\\'))
        except Exception, e:
            self.debug.error('Sv.getstatus: Exception: %s - Returning 0' % e)
            return 0
        self.allowVote = self.get_var(listStatus, 'g_allowvote')
        self.version = self.get_var(listStatus, 'version')
        self.gameType = self.get_var(listStatus, 'g_gametype')
        self.nextMap = self.get_var(listStatus, 'g_NextMap')
        self.clientsList = self.get_clients_list(listStatus)
        self.hostname = self.get_var(listStatus, 'sv_hostname')
        return 1

    def getinfo(self):
        try:
            self.sock.send(b'\xff'*4+b'getinfo')
            rawInfo = str(self.sock.recv(2048))
            listInfo = self.list_clean(rawInfo.split('\\'))
        except Exception, e:
            self.debug.error('Sv.getinfo: Exception: %s - Returning 0' % e)
            return 0
        self.clients = self.get_var(listInfo, 'clients')
        self.authNotoriety = self.get_var(listInfo, 'auth_notoriety')
        self.maxClients = self.get_var(listInfo, "sv_maxclients")
        self.mapName = self.get_var(listInfo, 'mapname')
        return 1


class Risc():
    """
    Main class containing the event dispatcher
    """
    def __init__(self):
        try:
            global chat_set
            global INIPATH

            self.debug = Debug(0)

            filterwarnings("ignore", category = mysql.Warning)

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

            if len(self.svs) > 8:
                self.debug.error('Too many servers. Max of 8 servers can be supported.')

            self.dbs = self.cfg.get('db', 'databases').split(',')

            if len(self.dbs) != len(self.svs):
                self.debug.error('Number of databases does not match the number of servers.')

            # Get the servers on which the riscb3 plugin is running
            self.sv_running = (self.cfg.get('var', 'svrunning').split(','))

            self.auth = self.cfg.get('irc', 'auth')
            self.auth_passwd = self.cfg.get('irc', 'auth_passwd')
            self.cmd_prefix = self.cfg.get('risc', 'cmd_prefix')
            self.cmd_prefix_global = self.cfg.get('risc', 'cmd_prefix_global')
            self.use_riscb3 = int(self.cfg.get('risc', 'use_riscb3'))

            self.init_help()

            if len(self.cmd_prefix) != 1:
                self.cmd_prefix = '!'

            if len(self.cmd_prefix_global) != 1:
                self.cmd_prefix_global = '@'

            for sv in self.sv_running:
                chat_set[sv] = 0
        except:
            self.debug.critical("Risc.__init__: Exception caught while loading config settings - Make sure there's no missing field")
            raise SystemExit

        # Commands and their aliases
        self.commands = {"quit": ["quit", "leave", "disconnect", "q"],
                "help": ["h", "help"],
                "ishowadmins": ["isa", "ishowadmins"],
                "status": ["status", "st"],
                "players": ["players", "p"],
                "base64": ["b64", "base64"],
                "sha1": ["sha1"],
                "md5": ["md5"],
                "search": ['search', 's'],
                "ikick": ["ikick", "ik"],
                "iputgroup": ["iputgroup", "ipg"],
                "chat": ["chat"],
                "seen": ["seen"],
                "say": ["say"],
                "google": ["google", "g"],
                "server": ["server", "sv"],
                "uptime": ["uptime"],
                "version": ["version", "v"],
                "roulette": ["roulette", 'r'],
                "duck": ["duck"],
                "ileveltest": ['ileveltest', 'ilt'],
                "kill": ['kill', 'k'],
                "raw": ["raw"],
                "todo": ["todo"]}

        # Valid argument for each commands
        tmp = ["all"]
        tmp.extend(self.svs)
        self.args = {"status": tmp,
                "players": self.svs,
                "search": self.svs,
                "iputgroup": [60, 80]}

        # Commands that need some rights
        self.commandLevels = self.get_cmd_levels()

        # Commands arguments aliases
        self.argAliases = {'servers': self.get_sv_aliases()}

    def start(self):
        """
        Launch the bot: connect, start event dispatcher, join
        """
        self.init_db()
        self.connect()
        self.debug.info('[+] Connected on '+self.host+' port '+str(self.port))
        self.set_evt_callbacks()
        self.dispatcher()
        return None

    def exit_process(self, msg="exit_process: Exiting"):
        global THREADS_STOP
        self.debug.info(msg)
        THREADS_STOP = 1
        time.sleep(0.5)
        sys.exit(0)

    def init_help(self):
        """
        Build the main help message
        """
        global HELP
        global CMDS
        HELP = "Available cmds: "
        CMDS_list = CMDS.split(',')
        for cmd in CMDS_list:
            HELP += self.cmd_prefix+cmd+', '
        HELP = HELP[:-2]
        HELP += ". Type "+self.cmd_prefix+"help <cmd> for more info."
        return None

    def get_sv_aliases(self):
        """
        Return a dict containing server aliases, sourced from ini file
        """
        ret = {}
        for sv in self.svs:
            ret.setdefault(sv)
            ret[sv] = [sv]
            if self.cfg.has_option('aliases', sv):
                ret[sv].extend(self.cfg.get('aliases', sv).split(','))
        return ret

    def get_cmd_levels(self):
        """
        Init the different command access levels
        """
        ret = {"quit": 80,
                "ikick": 80,
                "iputgroup": 100,
                "chat": 80,
                "set": 80,
                "say": 60,
                "ileveltest": 60,
                "raw": 100,
                "todo_add": 80,
                "todo_rm": 100,
                "server_add" : 60,
                "server_rm": 100,
                "server_rename": 60,
                "server_ls": 60}

        for cmd in ret:
            if self.cfg.has_option("levels", "cmd_"+cmd):
                lvl = int(self.cfg.get("levels", "cmd_"+cmd))
                if lvl in self.args["iputgroup"] or lvl == 100:
                    ret[cmd] = lvl
        return ret

    def repr_int(self, s):
        if not s:
            return 0
        for ch in s:
            if ord(ch) < 0x30 or ord(ch) > 0x39:
                return 0
        return 1

    def on_welcome(self):
        """
        Called after we successfully connected to the server
        """
        self._send("PRIVMSG Q@CServe.quakenet.org :AUTH "+self.auth+" "+self.auth_passwd)  # Auth with Q
        self.mode(self.nick, "+x")
        time.sleep(0.8)
        self.debug.info("[+] Joining " + self.channel + " ...")
        self.join()
        self.debug.info("[*] OK - Now processing\n")
        return None

    def on_ctcp(self, rawMsg):
        """
        Handle CTCP messages from the users
        """
        ltime = time.localtime()
        msg = []
        msg.append((' '.join(rawMsg[0].split(' ')[3:])[2:][:-1]))
        sourceNick = rawMsg[0].split('!')[0][1:]

        self.debug.info("on_ctcp: Received CTCP '"+msg[0] + "' from '" + sourceNick+"'")

        if msg[0].lower() == "version":
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "risc v" + __version__ + "\001")

        elif msg[0].lower() == "time":
            formatTime = str(ltime[1]) + '/' + str(ltime[2]) + '/' + str(ltime[0]) + ' ' + str(ltime[3]) + ':' + str(ltime[4]) + ':' + str(ltime[5])
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + formatTime + "\001")

        elif msg[0].lower() == "userinfo":
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "stalk much?" + "\001")

        elif msg[0].lower() == "ping":
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "PONG " + "\001")

        else:
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "Error: " + msg[0] + " CTCP command is not supported." + "\001")

        return None

    def user_add(self, user):
        """
        Add a user to the IRC user list
        """
        if not user:
            return None
        elif user[0] == '@':
            user = user[1:]
            level = "operator"
        elif user[0] == '+':
            user = user[1:]
            level = "voice"
        else:
            level = "none"
        if not user:
            return None
        user = user.lower()
        global users
        if user not in users:
            users[user] = {"chan_lvl": level}
        return None

    def user_remove(self, user):
        """
        Remove a user from the IRC user list
        """
        global users
        if not user:
            return None
        elif user.lower() in users:
            users.pop(user.lower())
        return None

    def init_users(self, line):
        """
        Called on namereply - Init IRC user list
        """
        line = self.list_clean(line.split(" :")[1].split(' '))
        for user in line:
            self.user_add(user)
        return None

    def is_on_channel(self, user):
        """
        Check whether a given user is on the channel
        """
        global users
        if not user:
            return None
        elif user.lower() in users:
            return True
        return None

    def set_option(self, section, option, value):
        """
        Write to and flush the config file, since configparser only buffer it
        """
        global INIPATH
        try:
            self.cfg.read(INIPATH)
            self.cfg.set(section, option, value)
            self.cfg.write(open(INIPATH, "wb"))
        except:
            self.debug.warning("set_option: exception caught")
            pass
        return None

    # TODO: FIX NEEDED: too slow
    def irc_is_authed(self, nick):
        """
        Check whether a user-nick is registered / has an account with quakenet, return 0 if not, otherwise return the account name
        """
        try:
            if not self.is_on_channel(nick):
                return 0
            self.sock.send('WHOIS ' + nick + '\r\n')
            res = str(self.sock.recv(1024))
        except:
            self.debug.error("irc_is_authed: Caught exception")
            return 0
        res = res.split(':')
        for i in range(len(res)):
            if re.search('is authed as', res[i]):
                tmp = self.list_clean(res[i-1].split(' '))
                auth = tmp[len(tmp)-1].strip()
                if nick.lower() == tmp[len(tmp)-2].strip().lower():  # some more precautions
                    return auth
        return 0

    def get_dict_key(self, d, searchValue):
        """
        Return the dict key from a value
        """
        for key in d:
            for val in d[key]:
                if val == searchValue.lower():
                    return key
        return 0

    def get_db(self, name):
        """
        Return the db associated with the given server name
        """
        name = name.lower()
        if name in self.svs:
            return self.dbs[self.svs.index(name)]
        return 0

    def irc_is_admin(self, nick):
        """
        Check whether a user is a risc admin or not, if he is, return the tuple auth,level, otherwise return 0
        """
        try:

            auth = self.irc_is_authed(nick)

            if not auth:
                return (0, 0)

            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            cur = con.cursor()

            cur.execute("""SELECT level FROM admins WHERE auth = '%s'""" % auth)

            con.commit()
            query = cur.fetchall()
            con.close()

        except:
            self.debug.critical("irc_is_admin: Exception. Rolling back db. Returning (0,0)")
            if con:
                con.rollback()
                con.close()
            return (auth, 0)

        # This makes the function fail if there're several records of the admin in the table
        if len(query) != 1:
            return (auth, 0)

        if query[0][0] is None:
            return (auth, 0)

        return (auth, int(query[0][0]))

    #############################################################################################################################
    #                                                                                                                           #
    #                                                                                                                           #
    #                                                CMD FUNCTIONS                                                              #
    #                                                                                                                           #
    #                                                                                                                           #
    #############################################################################################################################

    def cmd_iputgroup(self, nick, msg):
        """
        Put an authed user in one of the admin group
        """
        argv = self.list_clean(msg.split(' '))

        # Check input
        if len(argv) != 3:
            self.privmsg(nick, COLOR['boldmagenta']+nick+COLOR['rewind']+': Invalid arguments. Check '+self.cmd_prefix+'help iputgroup.')
            return None

        if len(argv[1]) > 19:
            self.privmsg(nick, COLOR['boldmagenta']+nick+COLOR['rewind']+': Invalid target.')
            return None

        try:
            argv[2] = int(argv[2])
        except:
            self.privmsg(nick, COLOR['boldmagenta']+nick+COLOR['rewind']+': Invalid arguments. Check '+self.cmd_prefix+'help iputgroup.')
            return None

        # Check rights
        nick_auth, nick_lvl = self.irc_is_admin(nick)
        if not nick_auth or nick_lvl != 100:
            self.privmsg(nick, "You need to be admin[100] to access this command.")
            return None

        if argv[2] not in self.args["iputgroup"] and argv[2] != 0:
            self.privmsg(nick, COLOR['boldmagenta']+nick+COLOR['rewind']+': Invalid arguments. Check '+self.cmd_prefix+'help iputgroup.')
            return None

        target_auth = self.irc_is_authed(argv[1])
        if not target_auth:
            self.privmsg(nick, COLOR['boldmagenta']+nick+COLOR['rewind']+": Target isn't authed.")
            return None

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()

            if not argv[2]:
                c.execute("""DELETE FROM admins WHERE auth = '%s'""" % target_auth)
                if c.rowcount == 1:
                    con.commit()
                    con.close()
                    self.privmsg(nick, "User-auth "+COLOR["boldgreen"]+target_auth+COLOR["rewind"]+" has been dropped from the admin groups.")
                    return None
                else:
                    self.debug.warning("cmd_iputgroup: Failure dropping admin - rolling back ...")
                    con.rollback()
                    con.close()
                    self.privmsg(nick, "Operation failed.")
                    return None
            else:
                c.execute("""SELECT * FROM admins WHERE auth = '%s'""" % target_auth)
                if c.rowcount == 1:
                    c.execute("""UPDATE admins SET level = %d WHERE auth = '%s'""" % (argv[2], target_auth))
                    con.commit()
                    con.close()
                    self.privmsg(nick, "User-auth "+COLOR["boldgreen"]+target_auth+COLOR["rewind"]+" has been moved to the admin["+str(argv[2])+"] group.")
                    return None
                elif c.rowcount > 1:
                    self.debug.critical("Errors detected in the admin DB: auth duplicated (%s)." % target_auth)
                    self.privmsg(self.channel, COLOR["boldred"]+"Operation failed: Errors detected in the admin DB! Contact an admin."+COLOR["rewind"])
                    con.close()
                    return None
                else:
                    c.execute("""INSERT INTO admins(auth,level,addedOn,addedBy) VALUES('%s',%d,%d,'%s')""" % (target_auth, argv[2], int(time.time()), nick_auth))
                    con.commit()
                    con.close()
                    self.privmsg(nick, "User-auth "+COLOR["boldgreen"]+target_auth+COLOR["rewind"]+" has been added to the admin["+str(argv[2])+"] group.")
                    return None

        except Exception, e:
            self.debug.critical("cmd_iputgroup: Exception caught: '%s'. Rolling back the db" % e)
            self.privmsg(self.channel, COLOR["boldred"]+"Exception caught: Operation failed."+COLOR["rewind"])
            if con:
                con.rollback()
                con.close()
        return None

    def cmd_ileveltest(self, msg0, sourceNick):
        """
        Check whether the given user is in the admin group
        """
        cleanLt = self.list_clean(msg0.split(" "))
        testNick = sourceNick

        if len(cleanLt) > 2:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+': Invalid arguments. Check '+self.cmd_prefix+'help ileveltest.')
            return None

        sourceAuth, sourceLevel = self.irc_is_admin(sourceNick)

        if sourceLevel < self.commandLevels['ileveltest'] or not sourceAuth:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": You cannot access this command. Check "+self.cmd_prefix+"help ileveltest.")
            return None

        if len(cleanLt) == 2:
            testNick = cleanLt[1]

        targetAuth, targetLevel = self.irc_is_admin(testNick)

        if targetAuth and (targetLevel in self.args['iputgroup'] or targetLevel == 100):
            if sourceNick.lower() == testNick.lower():
                self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": You're a "+self.nick+" admin["+str(targetLevel)+'].')
            else:
                self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": User "+COLOR['boldblue']+testNick+COLOR['rewind']+
                        " is a "+self.nick+" admin["+str(targetLevel)+'].')
        else:
            if sourceNick.lower() == testNick.lower():
                self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": You're not a "+self.nick+" admin.")
            else:
                self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": User "+COLOR['boldblue']+
                        testNick+COLOR['rewind']+' is not a '+self.nick+" admin.")
                return None

    def cmd_ishowadmins(self, msg0, sourceNick):
        """
        Show the risc admin list
        """
        cleanSA = self.list_clean(msg0.split(' '))
        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            cur = con.cursor()

            cur.execute("""SELECT auth FROM admins""")

            admins = cur.fetchall()
            con.close()
        except Exception, e:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": Error: Couldn't retrieve the "+self.nick+" admin list")
            self.debug.critical("cmd_ishowadmins: Exception: %s." % e)
            if con:
                con.rollback()
                con.close()
            return None

        if len(admins) == 0:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+': The '+self.nick+' admin list is empty.')
            return None

        adminList = []
        for admin in admins:
            adminList.append(COLOR['boldgreen']+admin[0]+COLOR['rewind'])

        self.privmsg(sourceNick, self.nick+' admin list: '+', '.join(adminList))

        return None

    def cmd_ikick(self, msg0, sourceNick):
        """
        Kick a user out of the channel
        """
        cleanKick = self.list_clean(msg0.split(' '))
        lenKick = len(cleanKick)
        reason = sourceNick

        if lenKick < 2:
            self.privmsg(sourceNick, "Invalid arguments. Check "+self.cmd_prefix+"help ikick.")
            return None

        if lenKick >= 3:
            reason = ' '.join(cleanKick[2:])

        sourceAuth, sourceLevel = self.irc_is_admin(sourceNick)
        targetAuth, targetLevel = self.irc_is_admin(cleanKick[1])

        if sourceAuth and sourceLevel >= self.commandLevels['ikick'] and sourceLevel > targetLevel:
            try:
                self.sock.send('KICK '+self.channel+' '+cleanKick[1]+' :'+reason+'\r\n')
            except:
                self.privmsg(sourceNick, "Couldn't kick the requested user!")
                self.debug.warning("cmd_ikick: Couldn't kick user!")
                return None
        else:
            self.privmsg(self.channel, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": "+COLOR['boldred']+
                    "You need to be admin["+str(self.commandLevels['ikick'])+"] to access this command, or the target admin"+\
                            " group is higher or equal to yours."+COLOR['rewind'])

            def cmd_sha1(self, msg0, sourceNick):
                """
        Give the SHA1 for the given string
        """
        cleanSha1Data = ''.join(msg0[6:])  # In case we have spaces in the string, they're taken into account

        if len(cleanSha1Data) > 150:
            self.privmsg(sourceNick, "Input too large.")
        else:
            try:
                sha1 = hashlib.sha1(cleanSha1Data).hexdigest()
            except:
                self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+': '+
                        COLOR['boldred']+'There was an error while computing. Check your input.'+COLOR['rewind'])
                return None
            self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+': '+sha1)
        return None

    def cmd_md5(self, msg0, sourceNick):
        """
        Give the MD5 for the given string
        """
        cleanMd5Data = ''.join(msg0[5:])

        if len(cleanMd5Data) > 150:
            self.privmsg(sourceNick, "Input too large.")
        else:
            try:
                md5 = hashlib.md5(cleanMd5Data).hexdigest()
            except:
                self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+': '+COLOR['boldred']+
                        'There was an error processing your command. Check your input.'+COLOR['rewind'])
                return None
            self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+': '+md5)
        return None

    def cmd_quit(self, msg0, sourceNick):
        """
        Tell risc to quit
        """
        sourceAuth, sourceLevel = self.irc_is_admin(sourceNick)
        if sourceAuth and sourceLevel >= self.commandLevels['quit']:
            self.disconnect("%s killed me" % sourceNick)
            time.sleep(0.8)
            self.exit_process("Exiting now: %s" % sourceNick)
        else:
            self.privmsg(self.channel, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": "+COLOR['boldred']+
                    "You need to be admin["+str(self.commandLevels["quit"])+"] to access this command."+COLOR['rewind'])
            return None

    def cmd_help(self, msg0, sourceNick):
        """
        Display the main help message
        """
        global HELP
        cleanHelp = self.list_clean(msg0.split(' '))
        lenCleanHelp = len(cleanHelp)

        if lenCleanHelp == 1:
            self.privmsg(sourceNick, HELP)
        elif lenCleanHelp == 2:
            self.privmsg(sourceNick, self.cmd_help_(cleanHelp[1]))
        else:
            self.privmsg(sourceNick, "Too many arguments. Check "+self.cmd_prefix+"help.")
        return None

    def cmd_chat(self, msg0, sourceNick):
        """
        Turn ON | OFF the chat feature in the specified server
        """
        global chat_set
        clean_cmd = self.list_clean(msg0.split(' '))
        len_cmd = len(clean_cmd)

        if len_cmd not in (1, 2, 3):
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": Invalid arguments, check "+self.cmd_prefix+"help chat.")
            return None

        if len_cmd == 1:
            ret = COLOR['boldgreen']+sourceNick+COLOR['rewind']+': Chat state: '
            for sv in chat_set:
                cur_state = COLOR['boldred']+'OFF'+COLOR['rewind']
                if chat_set[sv]:
                    cur_state = COLOR['boldgreen']+'ON'+COLOR['rewind']
                ret += sv+': '+cur_state+', '
            self.privmsg(sourceNick, ret[:-2])
            return None

        sv = self.get_dict_key(self.argAliases['servers'], clean_cmd[1])

        if not sv or sv not in self.sv_running:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+
                    ": Invalid arguments, target server either doesn't exist or is not running riscb3.")
            return None

        if len_cmd == 2:
            if chat_set[sv]:
                self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": Chat for the "+sv+
                        " server is currently"+COLOR['boldgreen']+' ON'+COLOR['rewind'])
            else:
                self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": Chat for the "+sv+
                        " server is currently"+COLOR['boldred']+' OFF'+COLOR['rewind'])
                return None

        auth, level = self.irc_is_admin(sourceNick)

        if not auth or level < self.commandLevels['chat']:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": You need to be admin["+
                    str(self.commandLevels['chat'])+'] to access this command.')
            return None


        try:
            state = '0'

            if clean_cmd[2].lower() in ('enable', 'on', '1'):
                state = '1'

            # Do not turn chat on in several server at a time
            if 1 in chat_set.values() and state == '1':
                self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": Chat is already enabl"\
                        "ed in a server, only one server at a time is allowed.")
                return None

            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.get_db(sv))
            cur = con.cursor()

            cur.execute("""INSERT INTO %s(evt, data, time, processed) VALUES('EVT_CHAT_SET','%s',%d,1)""" % ('risc_' + sv, state, int(time.time())))
            con.commit()
            con.close()
        except:
            self.debug.error('cmd_chat: Error during db operations, trying roll back. Passing')
            self.privmsg(sourceNick, COLOR['boldred']+sourceNick+COLOR['rewind']+
                    ': There was an error changing the chat state for the '+COLOR['boldblue']+sv+COLOR['rewind']+' server.')
            if con:
                con.rollback()
                con.close()
            return None

        chat_set[sv] = int(state)

        if chat_set[sv]:
            self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": Chat for the "+COLOR['boldblue']+sv+
                    COLOR['rewind']+" server is now"+COLOR['boldgreen']+' ON'+COLOR['rewind'])
        else:
            self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+": Chat for the "+COLOR['boldblue']+sv+
                    COLOR['rewind']+" server is now"+COLOR['boldred']+' OFF'+COLOR['rewind'])
            return None

    def cmd_status(self, serv):
        """
        Return info about the specified server, or all the servers in the server set
        """
        global INIPATH
        self.cfg.read(INIPATH)
        ret = ''
        serv = serv.lower()

        if serv == 'all':
            for i in self.argAliases['servers']:
                fullIp = self.cfg.get('var', i).split(':')
                try:
                    sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
                except Exception, e:
                    self.debug.warning("cmd_status: Failure for server '"+i+"'. Ignoring.")
                    continue

                if sv.clientsList == -1:
                    nbClients = 0
                else:
                    nbClients = len(sv.clientsList)

                ret += COLOR['boldgreen']+i+COLOR['rewind']+': Playing:'+COLOR['boldblue']+' '+str(nbClients)+COLOR['rewind']+\
                        '/'+str(sv.maxClients)+', map: '+COLOR['boldblue']+re.sub('\^[0-9]', '', sv.mapName)+COLOR['rewind']+' - '
                del sv
            if len(ret) >= 3:
                ret = ret[:-3]

        else:
            keyFromValue = self.get_dict_key(self.argAliases['servers'], serv)
            if not keyFromValue:
                return 'Invalid argument. Check '+self.cmd_prefix+'help status'

            fullIp = self.cfg.get('var', keyFromValue).split(':')
            try:
                sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
            except Exception, e:
                return COLOR['boldred']+"Exception for server '"+keyFromValue+"': %s" % e +COLOR['rewind']

            if sv.clientsList == -1:
                nbClients = 0
            else:
                nbClients = len(sv.clientsList)
            if int(sv.authNotoriety) >= 10:
                sv.authNotoriety = COLOR['boldgreen']+'ON'+COLOR['rewind']
            else:
                sv.authNotoriety = COLOR['boldred']+'OFF'+COLOR['rewind']
            if sv.allowVote == '1':
                sv.allowVote = COLOR['boldgreen']+'ON'+COLOR['rewind']
            elif sv.allowVote == '0':
                sv.allowVote = COLOR['boldred']+'OFF'+COLOR['rewind']

            ret = COLOR['boldgreen'] + keyFromValue + COLOR['rewind'] + ': Playing:' +\
                    COLOR['boldblue'] + ' '+str(nbClients) + COLOR['rewind'] + '/' +\
                    str(sv.maxClients) + ', map: '+COLOR['boldblue'] +\
                    re.sub('\^[0-9]', '', sv.mapName)+COLOR['rewind'] +\
                    ', nextmap: '+COLOR['boldblue']+re.sub('\^[0-9]', '', sv.nextMap) +\
                    COLOR['rewind']+', version: '+COLOR['boldblue']+re.sub('\^[0-9]','',sv.version)+COLOR['rewind'] +\
                    ', auth: '+sv.authNotoriety+', vote: '+sv.allowVote+', IP:'+COLOR['boldblue']+' '+fullIp[0]+':'+\
                    str(fullIp[1])+COLOR['rewind']
            del sv
        return ret

    def cmd_help_(self, command):
        """
        Display the help message associated with the given command
        """
        command = command.lower()

        if command in self.commands["quit"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: " + ', '.join(self.commands["quit"])+\
                    ". Tells risc to leave. You need to be registered as admin["+str(self.commandLevels['quit'])+\
                    "] with "+self.nick+"."

        elif command in self.commands["seen"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <player>: Aliases: "+', '.join(self.commands["seen"])+\
                    ". Return the last time a player was seen in the server set."

        elif command in self.commands["todo"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" [add <todo> | rm <todo_id> | list]: Aliases: "+', '.join(self.commands["todo"])+\
                    ". add/remove/list todo."

        elif command in self.commands["raw"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" [cmd]: Aliases: "+', '.join(self.commands["raw"])+\
                    ". Sends [cmd] data to the irc server. You need to be admin["+str(self.commandLevels["raw"])+"] to access this command."

        elif command in self.commands["version"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["version"])+\
                    ". Return the bot version."

        elif command in self.commands["roulette"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["roulette"])+\
                    ". Russian roulette game."

        elif command in self.commands["duck"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["duck"])+\
                    ". Sometimes, words ain't enough."

        elif command in self.commands["server"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" [<ip:port> | add <ip> <name> | rm <name> | rename <old_name> <new_name> | list]: Aliases: "+', '.join(self.commands["server"])+\
                    ". Display info about the specified server. If no port is specified, assume 27960. Add, remove, rename or list all the available servers."

        elif command in self.commands["say"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <str>: Aliases: "+', '.join(self.commands["say"])+\
                    ". Makes "+self.nick+ " say <str>. You need to be registered as admin["+str(self.commandLevels['say'])+\
                    "] with "+self.nick+"."

        elif command in self.commands["uptime"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["uptime"])+". "+\
                    "Show "+self.nick+"'s uptime."

        elif command in self.commands["players"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <serverName>: Aliases: "+", ".join(self.commands["players"])+\
                    ". Shows all players on the <serverName> server. Available args/server-name: "+', '.join(self.args["players"])+'.'

        elif command in self.commands["search"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ": <playerNick> <server> Aliases: " + ', '.join(self.commands["search"])+\
                    ". Search for the player <playerNick> in the current server set if <server> is not specified,"+\
                    " else it performs the search in the <server> server."

        elif command in self.commands["ishowadmins"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["ishowadmins"])+". Show all "+\
                    self.nick+" admins."

        elif command in self.commands["google"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <str>: Aliases: "+', '.join(self.commands["google"])+". Perform a"+\
                    " google search and echo the top 4 hits."

        elif command in self.commands["base64"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <utf8String>: Aliases: "+', '.join(self.commands["base64"])+\
                    ". Returns a base64 encoded string from the utf-8 string <utf8String>."

        elif command in self.commands["sha1"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + " <string>: Aliases: " + ', '.join(self.commands["sha1"])+\
                    ". Returns the sha1 of the string <string>."

        elif command in self.commands["chat"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + " <server> <on|off>: Aliases: " + ', '.join(self.commands["chat"])+\
                    ". Enable or disable the chat feature betwen IRC and the game server <server>. Return the state of the chat feature"+\
                    " in the servers when no arg are specified, or the state of the chat feature in the specified server if any."+\
                    " You need to be admin["+str(self.commandLevels['chat'])+'] to access this command.'

        elif command in self.commands["ikick"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ": <user> <reason> Aliases: " + ', '.join(self.commands["ikick"]) +\
                    ". Kicks the channel user <user>. You need to registered as admin[" +\
                    str(self.commandLevels['ikick']) +\
                    "] with risc. Also you can't kick another admin unless your level is strictly higher than his."

        elif command in self.commands["ileveltest"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ": <user> Aliases: " + ', '.join(self.commands["ileveltest"]) +\
                    ". Returns the level of the user <user> if he's registered as admin with risc. If you don't specify a <user> parameter,"+\
                    " the command will return your level. You're required to be registered as admin[" +\
                    str(self.commandLevels['ileveltest'])+"] with "+self.nick+" to access this command."

        elif command in self.commands["md5"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <string>: Aliases: "+', '.join(self.commands["md5"])+\
                    ". Returns the md5 of the string <string>."

        elif command in self.commands["status"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ' <serverName>' + ": Aliases: " + ', '.join(self.commands["status"])+\
                    ". Diplays information about the <serverName> server. Available args/server-name: "+', '.join(self.args['status'])

        elif command in self.commands["iputgroup"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": <user> <level> Aliases: "+', '.join(self.commands["iputgroup"])+\
                    ". Set an admin level <level> to the user <user>. You need to be registered as admin[" + str(self.commandLevels['iputgroup'])+\
                    "] with risc. Valid values for <level> include "+', '.join(str(x) for x in self.args['iputgroup'])+". Use <level> = 0 to drop an admin."

        elif command in self.commands["kill"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": <user> <weapon> Alias(es): " + ', '.join(self.commands["kill"])+\
                    ". Performs a kill on the specified <user> with the desired <weapon>. Can be used without <weapon> argument."
        else:
            return "Command not found: " + COLOR['boldmagenta']+command+COLOR['rewind']

    def cmd_players(self, serverName, rawRet=0):
        """
        Return the player list in the specified server
        """
        global INIPATH
        serverName = self.get_dict_key(self.argAliases['servers'], serverName.lower())
        ret = []
        bot_count = 0
        if not serverName:
            return "Invalid arguments. Check "+self.cmd_prefix+"help players."

        self.cfg.read(INIPATH)
        fullIp = self.cfg.get('var', serverName).split(":")
        try:
            sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
        except Exception, e:
            return COLOR['boldred']+"Exception for server '"+serverName+"': %s" % e +COLOR['rewind']

        if sv.clients == 0 or sv.clientsList == -1:
            return serverName + ' server is currently empty.'

        usePings = False
        if len(sv.clientsPings) == len(sv.clientsList):
            usePings = True

        for i in range(len(sv.clientsList)):
            if usePings and sv.clientsPings[i] == '0':
                ping = COLOR['rewind']+' ('+COLOR['boldblue']+'BOT'+COLOR['rewind']+')'
                bot_count += 1
            else:
                ping = ''

            ret.append(COLOR['boldgreen']+' '+sv.clientsList[i]+COLOR['rewind']+ping)

        if rawRet:
            return ret

        ret.sort()
        # For some reason, sv.clients is innacurate here ...
        if usePings and bot_count:
            return 'Playing on '+serverName+' ('+str(len(sv.clientsList) - bot_count)+'+'+str(bot_count)+'/'+str(sv.maxClients)+'):'+','.join(ret)
        else:
            return 'Playing on '+serverName+' ('+str(len(sv.clientsList))+'/'+str(sv.maxClients)+'):'+','.join(ret)

    def cmd_seen(self, msg0, sourceNick):
        """
        Return the last time a user was seen in the server set
        """
        cleanCmd = self.list_clean(msg0.split(' '))

        if len(cleanCmd) != 2:
            self.privmsg(sourceNick, "Invalid arguments, check "+self.cmd_prefix+"help seen.")
            return None

        # b3 uses 32 chars to store names
        if len(cleanCmd[1]) > 31:
            self.privmsg(sourceNick, "User nick too long, max length: 31 chars.")

        try:
            last_seen = (0, 0)
            last_seen_sv = ''
            for sv in self.svs:
                query = ()
                db = self.get_db(sv)
                if not db:
                    continue
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
                cur = con.cursor()

                cur.execute("""SELECT id, time_edit FROM clients WHERE name = '%s' AND id = (SELECT MAX(id) FROM clients WHERE name = '%s')""" % (cleanCmd[1], cleanCmd[1]))
                query = cur.fetchone()
                con.close()

                if isinstance(query, tuple):
                    if len(query) == 2:
                        if query[1] > last_seen[1]:
                            last_seen_sv = sv
                            last_seen = query

            if last_seen != (0, 0) and last_seen_sv != '':
                t = time.gmtime(last_seen[1])
                self.privmsg(sourceNick, "Player %s%s%s @%d was last seen on the %s%s%s server on%s %d/%d/%d %sat%s %d:%d %s(GMT)" % (\
                        COLOR['boldblue'], cleanCmd[1], COLOR['rewind'], last_seen[0], COLOR['boldblue'], last_seen_sv,\
                        COLOR['rewind'], COLOR['boldblue'], t[1], t[2], t[0], COLOR['rewind'],\
                        COLOR['boldblue'], t[3], t[4], COLOR['rewind']))
                return None
        except Exception, e:
            self.debug.error('cmd_seen: Caught exception: %s - Passing' % e)
            pass

        self.privmsg(sourceNick, "No such player.")
        return None

    def cmd_search(self, player, rawRet=0):
        """
        Search for a player in the entire server set
        """
        global INIPATH
        if len(player) >= 30:
            return 'Player name has too many chars.'

        player = re.escape(player)

        # Get all players on all servers into a dict
        clients = {}
        pings = {}
        self.cfg.read(INIPATH)
        for server in self.args['search']:
            fullIp = self.cfg.get('var', server).split(':')
            try:
                sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
            except Exception, e:
                continue
            if sv.clientsList != -1:
                clients.setdefault(server, sv.clientsList)
                pings.setdefault(server, sv.clientsPings)
            else:
                clients.setdefault(server, [''])

        if rawRet:
            return (clients, pings)

        # Search for the player
        ret = []
        count = 0
        for sv in clients:
            for i in range(len(clients[sv])):
                if re.search(player.lower(), clients[sv][i].lower()):
                    count += 1
                    if len(pings[sv]) == len(clients[sv]):
                        if pings[sv][i] == '0':
                            ret.append(COLOR['boldgreen'] + clients[sv][i] + COLOR['rewind'] + ' (' + COLOR['boldblue'] +
                                    'BOT' + COLOR['rewind'] + ',' + COLOR['boldblue'] + ' ' + sv + COLOR['rewind'] + ')')
                        else:
                            ret.append(COLOR['boldgreen'] + clients[sv][i] + COLOR['rewind'] + ' (' + COLOR['boldblue'] + sv + COLOR['rewind'] + ')')
                    else:
                        ret.append(COLOR['boldgreen'] + clients[sv][i] + COLOR['rewind'] + ' (' + COLOR['boldblue'] + sv + COLOR['rewind'] + ')')

        lenRet = len(ret)

        if lenRet == 0:
            return COLOR['boldmagenta'] + 'No such player in the server set.' + COLOR['rewind']
        elif lenRet == 1:
            return 'Found a player matching the request: ' + ret[0]
        elif count > 15:
            return COLOR['boldmagenta'] + "Too many players matching the request. Try to be more accurate." + COLOR['rewind']
        else:
            ret.sort()
            return 'Found ' + str(count) + ' players matching: ' + ', '.join(ret)

    def cmd_say(self, msg0, nick):
        """
        Tell risc to say something
        """
        auth, level = self.irc_is_admin(nick)

        if not auth or level < self.commandLevels['say']:
            self.privmsg(nick, "You must be at least in the admin["+str(self.commandLevels['say'])+"] group to access this command.")
            return None

        self.privmsg(self.channel, " ".join(msg0.split(' ')[1:]))
        return None

    def cmd_google(self, msg0, nick):
        """
        Display the google result of the given request
        """
        i = 0
        search_str = " ".join(msg0.split(' ')[1:])
        if len(search_str) >= 255:
            self.privmsg(nick, "Input too large.")
            return None

        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % search_str
        res = requests.get(url)
        if len(json.loads(res.text)['responseData']['results']):
            self.privmsg(nick, "Top hits: ")
        else:
            self.privmsg(nick, "No results.")
            return None
        for hit in json.loads(res.text)['responseData']['results']:
            self.privmsg(nick, hit["url"])
            i+=1
            if i >= 4:
                break
        return None

    def cmd_server_add(self, msg0, nick):
        """
        Add a server ip/name in the server database
        sv add <ip> <name>
        """
        argv = self.list_clean(msg0.split(' '))
        t = int(time.time())

        if len(argv) != 4:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help server.")
            return None

        re_full_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{5}$')
        re_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}$')

        if re.match(re_ip, argv[2]):
            ip = argv[2]+":27960"
        elif re.match(re_full_ip, argv[2]):
            ip = argv[2]
        else:
            self.privmsg(nick, "Invalid IP.")
            return None

        name = argv[3].encode("string_escape")

        if len(name) > 32:
            self.privmsg(nick, "Server name input too large.")
            return None

        auth, level = self.irc_is_admin(nick)
        if not auth or level < self.commandLevels["server_add"]:
            self.privmsg(nick, "You need to be admin["+str(self.commandLevels["server_add"])+"] to access this command.")
            return None

        try:
            sv = Sv(ip.split(':')[0], int(ip.split(':')[1]), '', self.debug)
        except Exception, e:
            self.debug.warning("cmd_server_add: Invalid ioq3 IP.")
            self.privmsg(nick, "Invalid ioq3 IP.")
            return None

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()

            c.execute("""SELECT * FROM server WHERE name = '%s' OR ip = '%s'""" % (name, ip))

            if c.rowcount:
                self.privmsg(nick, "Server already exists.")
                con.close()
                return None

            con.commit()
            c.execute("""SELECT * FROM server""")

            if c.rowcount > 20:
                self.privmsg(nick, "Too many servers in the DB.")
                con.close()
                return None

            c.execute("""INSERT INTO server(name, ip, author, time) VALUES('%s', '%s', '%s', %d)""" % (name, ip, nick, t))
            con.commit()
            con.close()
        except Exception, e:
            self.debug.warning(nick, "cmd_server_add: Error during DB operations. Rolling back.")
            self.privmsg(nick, "Error during DB operations.")
            con.rollback()
            return None

        self.privmsg(nick, "Operation successful.")
        return None

    def cmd_server_rm(self, msg0, nick):
        """
        Remove a server from the server database
        sv rm <name>
        """
        argv = self.list_clean(msg0.split(' '))

        if len(argv) != 3:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help server.")
            return None

        name = argv[2].encode("string_escape")

        if len(name) > 32:
            self.privmsg(nick, "Server name input too large.")
            return None

        auth, level = self.irc_is_admin(nick)
        if not auth or level < self.commandLevels["server_rm"]:
            self.privmsg(nick, "You need to be admin["+str(self.commandLevels["server_rm"])+"] to access this command.")
            return None

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()
            c.execute("""DELETE FROM server WHERE name = '%s'""" % name)
            con.commit()
            con.close()
        except Exception, e:
            self.debug.warning(nick, "cmd_server_rm: Error during DB operations. Rolling back.")
            self.privmsg(nick, "Error during DB operations.")
            con.rollback()
            return None

        self.privmsg(nick, "Operation successful")
        return None


    def cmd_server_rename(self, msg0, nick):
        """
        Rename a server in the server database
        sv rename <old_name> <new_name>
        """
        argv = self.list_clean(msg0.split(' '))

        if len(argv) != 4:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help server.")
            return None

        old_name = argv[2].encode("string_escape")
        new_name = argv[3].encode("string_escape")

        if len(old_name) > 32 or len(new_name) > 32:
            self.privmsg(nick, "Server name input too large.")
            return None

        auth, level = self.irc_is_admin(nick)
        if not auth or level < self.commandLevels["server_rename"]:
            self.privmsg(nick, "You need to be admin["+str(self.commandLevels["server_rename"])+"] to access this command.")
            return None

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()

            c.execute("""SELECT * FROM server WHERE name = '%s'""" % new_name)
            if c.rowcount:
                self.privmsg(nick, "Server name already exists.")
                con.close()
                return None
            c.execute("""UPDATE server SET name = '%s' WHERE name = '%s'""" % (new_name, old_name))
            con.commit()
            con.close()
        except Exception, e:
            self.debug.warning(nick, "cmd_server_rename: Error during DB operations. Rolling back.")
            self.privmsg(nick, "Error during DB operations.")
            con.rollback()
            return None

        self.privmsg(nick, "Operation successful")
        return None

    def cmd_server_list(self, msg0, nick):
        """
        List the available servers
        sv list
        """
        argv = self.list_clean(msg0.split(' '))

        if len(argv) != 2:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help server.")
            return None

        auth, level = self.irc_is_admin(nick)
        if not auth or level < self.commandLevels["server_ls"]:
            self.privmsg(nick, "You need to be admin["+str(self.commandLevels["server_ls"])+"] to access this command.")
            return None

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()
            c.execute("""SELECT name, ip, author FROM server LIMIT 20""")

            if not c.rowcount:
                self.privmsg(nick, "Server DB is empty.")
            elif c.rowcount <= 20:
                for r in c.fetchall():
                    self.privmsg(nick, COLOR["boldgreen"] + r[0] + COLOR["rewind"]+':'+COLOR["boldblue"]+' '+r[1]+COLOR["rewind"]+" (by "+r[2]+')')
            else:
                self.privmsg(nick, "Too many servers in the DB (%d)." % str(c.rowcount))    # Should never happen ...

            con.close()
        except Exception, e:
            self.debug.warning(nick, "cmd_server_list: Error during DB operations.")
            self.privmsg(nick, "Error during DB operations.")
        return None

    def cmd_server_from_db(self, sv_name, nick):
        """
        Return sv IP on success, "FAIL" on failure
        """
        sv_name = sv_name.encode("string_escape")

        if len(sv_name) > 32:
            return "FAIL"

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            c = con.cursor()
            c.execute("""SELECT ip FROM server WHERE name LIKE '%s'""" % ('%'+sv_name+'%'))

            if c.rowcount == 1:
                con.close()
                return c.fetchone()[0]

            con.close()
        except Exception, e:
            self.debug.warning(nick, "cmd_server_list: Error during DB operations.")
            self.privmsg(nick, "Error during DB operations.")
        return "FAIL"

    def cmd_server(self, msg0, nick):
        """
        Return info about the specified game server ip
        """
        clean_msg = self.list_clean(msg0.split(' '))
        sv = None

        if len(clean_msg) < 2:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help server.")
            return None

        ret = ''
        re_full_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{5}$')
        re_ip = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}$')
        ip = ""
        port = 27960

        if re.match(re_ip, clean_msg[1]):
            ip = clean_msg[1]
        elif re.match(re_full_ip, clean_msg[1]):
            ip = clean_msg[1].split(':')[0]
            port = int(clean_msg[1].split(':')[1])

        elif clean_msg[1].lower() == "add":
            self.cmd_server_add(msg0, nick)
            return None

        elif clean_msg[1].lower() in ("rm", "remove", "del", "delete", "drop"):
            self.cmd_server_rm(msg0, nick)
            return None

        elif clean_msg[1].lower() == "rename":
            self.cmd_server_rename(msg0, nick)
            return None

        elif clean_msg[1].lower() in ("ls", "list", "show"):
            self.cmd_server_list(msg0, nick)
            return None

        else:
            ip_db = self.cmd_server_from_db(clean_msg[1], nick)
            if ip_db == "FAIL":
                self.privmsg(nick, "No such server.")
                return None
            else:
                try:
                    sv = Sv(ip_db.split(':')[0], int(ip_db.split(':')[1]), '', self.debug)
                except Exception, e:
                    return COLOR["boldred"]+"Exception for server '"+ip_db+"': %s" % e + COLOR["rewind"]

        if sv is None:
            try:
                sv = Sv(ip, port, '', self.debug)
            except Exception, e:
                return COLOR["boldred"]+"Exception for server '"+ip+':'+str(port)+"': %s" % e + COLOR["rewind"]

        if sv.clientsList == -1:
            nbClients = 0
        else:
            nbClients = len(sv.clientsList)
        if int(sv.authNotoriety) >= 10:
            sv.authNotoriety = COLOR['boldgreen']+'ON'+COLOR['rewind']
        else:
            sv.authNotoriety = COLOR['boldred']+'OFF'+COLOR['rewind']
        if sv.allowVote == '1':
            sv.allowVote = COLOR['boldgreen']+'ON'+COLOR['rewind']
        elif sv.allowVote == '0':
            sv.allowVote = COLOR['boldred']+'OFF'+COLOR['rewind']

        if sv.clients == 0 or sv.clientsList == -1:
            ret2 = 'Server is currently empty.'
        else:
            usePings = False
            if len(sv.clientsPings) == len(sv.clientsList):
                usePings = True

            players = []
            bot_count = 0
            for i in range(len(sv.clientsList)):
                if usePings and sv.clientsPings[i] == '0':
                    ping = COLOR['rewind']+' ('+COLOR['boldblue']+'BOT'+COLOR['rewind']+')'
                    bot_count += 1
                else:
                    ping = ''
                players.append(COLOR['boldgreen']+' '+sv.clientsList[i]+COLOR['rewind']+ping)

            if usePings and bot_count:
                ret2 = "Playing ("+str(len(sv.clientsList) - bot_count)+'+'+str(bot_count)+"/"+str(sv.maxClients)+'): '+",".join(players)
            else:
                ret2 = "Playing ("+str(len(sv.clientsList))+"/"+str(sv.maxClients)+'): '+",".join(players)

        ret = COLOR['boldgreen'] + re.sub('\^[0-9]', '', sv.hostname) + COLOR['rewind'] + ': Playing:' +\
                COLOR['boldblue'] + ' '+str(nbClients) + COLOR['rewind'] + '/' +\
                str(sv.maxClients) + ', map: '+COLOR['boldblue'] +\
                re.sub('\^[0-9]', '', sv.mapName)+COLOR['rewind'] +\
                ', nextmap: '+COLOR['boldblue']+re.sub('\^[0-9]', '', sv.nextMap) +\
                COLOR['rewind']+', version: '+COLOR['boldblue']+re.sub('\^[0-9]','',sv.version)+COLOR['rewind'] +\
                ', auth: '+sv.authNotoriety+', vote: '+sv.allowVote+", IP:"+COLOR["boldblue"]+' '+\
                (str(sv.ip)+':'+str(sv.port))+COLOR["rewind"]
        return ret, ret2

    def cmd_uptime(self, msg0, nick):
        """
        Display risc's uptime
        """
        cmd = self.list_clean(msg0.split(' '))
        global init_time
        if len(cmd) != 1:
            return "Invalid usage, check "+self.cmd_prefix+"help uptime."
        return str(datetime.timedelta(seconds=int(time.time())-init_time))

    def cmd_roulette(self, msg0, nick):
        """
        Roulette game 6 chambers
        """
        cmd = self.list_clean(msg0.split(' '))

        if len(cmd) != 1:
            self.privmsg(self.channel, "Invalid usage, check "+self.cmd_prefix+"help roulette.")
            return None

        global roulette_shot
        global roulette_cur

        if roulette_cur == roulette_shot:
            self.privmsg(self.channel,COLOR['boldred']+"*BANG*"+COLOR['rewind']+" -"+COLOR['boldred']+' '+nick+" is no more ..."+COLOR['rewind'])
            roulette_shot = random.randint(1, 6)
            roulette_cur = random.randint(1, 6)
            self.sock.send('KICK '+self.channel+' '+nick+' :'+"got rekt"+'\r\n')
        else:
            roulette_cur = (roulette_cur + 1)%7
            self.privmsg(self.channel, COLOR['boldgreen']+"+click+"+COLOR['rewind']+" -"+COLOR['boldgreen']+' '+nick+" is safe."+COLOR['rewind'])
        return None

    def cmd_duck(self):
        """
        WTF?
        """
        duck_s = ["....................../??/)", "....................,/?../", ".................../..../",\
                "............./??/'...'/???`??", "........../'/.../..../......./??\\", "........('(...?...?.... ?~/'...')",\
                ".........\.................'...../", "..........''...\.......... _.??", "............\..............(",\
                "..............\.............\..."]
        for s in duck_s:
            self.privmsg(self.channel, s)
        return None

    def cmd_kill(self, msg0, sourceNick):
        """
        kill <opt_user> <opt_weapon>
        """
        killClean = self.list_clean(msg0.split(' '))
        lenKill = len(killClean)
        weapons = {"colt": [" was given a new breathing hole by ", "'s Colt 1911."],
                "spas": [" was turned into peppered steak by ", "'s SPAS blast."],
                "ump45": [" danced the ump tango to ", "'s sweet sweet music."],
                "mp5": [" was MP5K spammed without mercy by ", "'s MP5K."],
                "mac11": [" was minced to death by ", "'s Mac 11."],
                "lr300": [" played 'catch the shiny bullet with ", " LR-300 rounds."],
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

        if lenKill == 1:
            self.privmsg(self.channel, COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" has an urge to kill...")

        elif lenKill == 2:
            if len(killClean[1]) > 28:
                self.privmsg(sourceNick, 'Nick has too many chars.')

            elif killClean[1].lower() in ('all', 'everyone', 'channel', 'everybody'): # FIXME: what if sm1 is named "all", "everyone" etc?
                self.privmsg(self.channel, COLOR["boldred"]+random.choice(["The whole channel", "Everyone", "Everybody"])\
                        +COLOR['rewind']+" has been murdered by "+COLOR["boldgreen"]+sourceNick+COLOR['rewind']+".")

            elif sourceNick.lower() == killClean[1].lower():
                self.privmsg(self.channel, COLOR["boldred"]+sourceNick+COLOR['rewind']+" went an hero.")

            elif self.nick.lower() == killClean[1].lower(): # FIXME: write a safe kick function ...
                self.privmsg(self.channel, "You cannot kill me, "+COLOR['boldred']+"I KILL YOU!")
                self.sock.send('KICK '+self.channel+' '+sourceNick+' :'+"killed by risc"+'\r\n')

            elif self.is_on_channel(killClean[1]):
                self.privmsg(self.channel, COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" killed "+killClean[1]+".")

            else:
                self.privmsg(sourceNick, "This person doesn't exist.")

        elif lenKill == 3:
            if not self.is_on_channel(killClean[1]):
                self.privmsg(sourceNick, "This person doesn't exist.")

            elif killClean[2].lower() in weapons:
                self.privmsg(self.channel, COLOR["boldred"]+killClean[1]+COLOR['rewind']+weapons[killClean[2]][0]+COLOR["boldgreen"]+sourceNick+COLOR['rewind']+weapons[killClean[2]][1])
            else:
                self.privmsg(self.channel, COLOR["boldred"]+killClean[1]+COLOR['rewind']+" has been creatively killed by "+COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" using a "+killClean[2]+".")

        else:
            self.privmsg(sourceNick, 'Invalid arguments. Check '+self.cmd_prefix+'help kill.')
        return None

    def cmd_todo(self, msg0, nick):
        """
        todo [add <todo> | rm <num> | list]
        """
        todo_clean = self.list_clean(msg0.split(' '))
        t = int(time.time())

        if len(todo_clean) < 2:
            self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
            return None

        if todo_clean[1].lower() == "add":
            if len(todo_clean) < 3:
                self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
                return None

            auth, level = self.irc_is_admin(nick)

            if not auth or level < self.commandLevels["todo_add"]:
                self.privmsg(nick, "You need to be admin["+str(self.commandLevels["todo_add"])+"] to access this command.")
                return None

            todo_str = ' '.join(todo_clean[2:]).encode("string_escape")
            author = nick.encode("string_escape")

            if len(todo_str) > 127 or len(author) > 31:
                self.privmsg(nick, 'Input too large.')
                return None

            try:
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
                c = con.cursor()

                c.execute("""SELECT * FROM todo WHERE todo = '%s'""" % (todo_str))

                if c.rowcount:
                    self.privmsg(nick, 'Todo already exists.')
                    con.close()
                    return None

                c.execute("""SELECT COUNT(*) FROM todo""")

                if c.fetchall()[0][0] > 10:
                    self.privmsg(nick, 'Too many todo (Max. 10).')
                    con.close()
                    return None

                c.execute("""INSERT INTO todo(author, time, todo) VALUES('%s', '%d', '%s')""" % (author, t, todo_str))
                con.commit()
                con.close()
            except:
                self.privmsg(nick, 'Error during DB operations - Trying db rollback ...')
                con.rollback()
                con.close()
                return None
            self.privmsg(nick, "Operation successful")
        elif todo_clean[1].lower() in ("rm", "remove", "del", "delete"):
            if len(todo_clean) != 3:
                self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
                return None

            auth, level = self.irc_is_admin(nick)

            if not auth or level < self.commandLevels["todo_rm"]:
                self.privmsg(nick, "You need to be admin["+str(self.commandLevels["todo_rm"])+"] to access this command.")
                return None

            rm_id = todo_clean[2]

            if not self.repr_int(rm_id) and rm_id != '*':
                self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
                return None

            try:
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
                c = con.cursor()

                if rm_id != '*':
                    c.execute("""DELETE FROM todo WHERE id = %d""" % (int(rm_id)))
                else:
                    c.execute("""DELETE FROM todo""")

                con.commit()
                con.close
            except:
                self.privmsg(nick, 'Error during DB operations - Trying db rollback ...')
                con.rollback()
                con.close()
                return None
            self.privmsg(nick, "Operation successful")
        elif todo_clean[1].lower() in ("list", "ls", "show"):
            if len(todo_clean) != 2:
                self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
                return None

            try:
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
                c = con.cursor()

                c.execute("""SELECT id, todo, author FROM todo LIMIT 10""")
                res = c.fetchall()
                con.close()
            except:
                self.privmsg(nick, 'Error during DB operations - Trying db rollback ...')
                con.rollback()
                con.close()
                return None

            if not c.rowcount:
                self.privmsg(nick, "Todo list is empty.")
                return None

            for record in res:
                self.privmsg(nick, COLOR["boldgreen"]+'#'+str(record[0])+COLOR["rewind"]+' '+
                        record[1]+" (by "+COLOR["boldgreen"]+record[2]+COLOR["rewind"]+')')
        else:
            self.privmsg(nick, 'Invalid arguments. Check '+self.cmd_prefix+'help todo.')
        return None

    def cmd_raw(self, msg0, nick):
        """
        Sends raw data to the server
        """
        clean_raw = self.list_clean(msg0.split(' '))
        cmd = ' '.join(clean_raw[1:])
        auth, level = self.irc_is_admin(nick)
        if auth and level >= self.commandLevels["raw"]:
            self.sock.send(":risc!~risc@risc.users.quakenet.org "+cmd+"\r\n")
        else:
            self.privmsg(nick, "You need to be admin["+str(self.commandLevels["raw"])+"] to access this command.")
        return None

    def search_accurate(self, p, serv):
        """
        Search for a player in the specified server
        """
        try:
            (cl, pings) = self.cmd_search(p, 1)
        except:
            return COLOR['boldred']+"Error - Server may be unreachable."+COLOR['rewind']

        servKey = self.get_dict_key(self.argAliases["servers"], serv.lower())
        ret = []
        count = 0

        if not servKey:
            return 'Invalid arguments: '+serv+'. Check '+self.cmd_prefix+'help search.'

        p = re.escape(p)

        if cl[servKey] == ['']:
            return COLOR['boldmagenta'] + 'No such player in the specified server.' + COLOR['rewind']

        usePings = 0
        isBot = COLOR['rewind'] + ' (' + COLOR['boldblue'] + 'BOT' + COLOR['rewind'] + ')'

        if len(cl[servKey]) == len(pings[servKey]):
            usePings = 1

        for i in range(len(cl[servKey])):
            if p.lower() in cl[servKey][i].lower():
                count += 1
                if usePings:
                    if pings[servKey][i] == '0':
                        ret.append(COLOR['boldgreen'] + cl[servKey][i] + isBot + COLOR['rewind'])
                    else:
                        ret.append(COLOR['boldgreen'] + cl[servKey][i] + COLOR['rewind'])
                else:
                    ret.append(COLOR['boldgreen'] + cl[servKey][i] + COLOR['rewind'])

        if count == 0:
            return COLOR['boldmagenta']+'No such player in the specified server.'+COLOR['rewind']
        elif count == 1:
            return 'Found a player matching the request in the '+COLOR['boldwhite']+servKey+COLOR['rewind']+' server: '+ret[0]
        else:
            ret.sort()
            return 'Found '+str(count) + ' players matching the request in the ' + COLOR['boldwhite'] + servKey + COLOR['rewind'] + ' server: ' + ', '.join(ret)

    def list_clean(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != '' and e != ' ':
                ret.append(e)
        return ret

    def mintostr(self, m):
        """
        Convert minutes to a string
        """
        if not isinstance(m, int):
            return '0'

        if m < 60:
            return str(m)+' minute' if m == 1 else str(m)+' minutes'

        elif m < 1440:
            unit = ' hour'
            duration = str(round(float(m) / 60.0, 1))
            # If we have a float that actually represents an int, truncate it
            if duration[-1] == '0':
                duration = duration.split('.')[0]
            if int(duration.split('.')[0]) > 1:
                unit += 's'
            return duration+unit

        elif m < 10080:
            unit = ' day'
            duration = str(round(float(m) / 1440.0, 1))
            if duration[-1] == '0':
                duration = duration.split('.')[0]
            if int(duration.split('.')[0]) > 1:
                unit += 's'
            return duration+unit

        elif m < 40320:
            unit = ' week'
            duration = str(round(float(m) / 10080.0, 1))
            if duration[-1] == '0':
                duration = duration.split('.')[0]
            if int(duration.split('.')[0]) > 1:
                unit += 's'
            return duration+unit

        elif m < 483840:
            unit = ' month'
            duration = str(round(float(m) / 40320.0, 1))
            if duration[-1] == '0':
                duration = duration.split('.')[0]
            if int(duration.split('.')[0]) > 1:
                unit += 's'
            return duration+unit

        else:
            unit = ' year'
            duration = str(round(float(m) / 483840.0, 1))
            if duration[-1] == '0':
                duration = duration.split('.')[0]
            if int(duration.split('.')[0]) > 1:
                unit += 's'
            return duration+unit

    def on_ichat(self, rawMsg):
        """
        Called on IRC message
        """
        global chat_set
        sourceNick = rawMsg[0].split('!')[0][1:]
        msg = rawMsg[0].split(':')[2]

        # Store the event in the table of the servers which have chat enabled
        for sv in chat_set:
            if chat_set[sv]:
                db = self.get_db(sv)
                if not db:
                    continue
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
                cur = con.cursor()
                cur.execute("""INSERT INTO %s(evt,data,time,processed) VALUES('EVT_ICHAT','%s',%d,0)""" % ('risc_' + sv, sourceNick + '\r\n' + msg, int(time.time())))
                con.commit()
                con.close()
        return None

    ##############################################################################################################
    #                                                                                                            #
    #                                                                                                            #
    #                                       HANDLE COMMANDS HERE                                                 #
    #                                                                                                            #
    #                                                                                                            #
    ##############################################################################################################

    def on_pubmsg(self, rawMsg):
        """
        Channel messages starting with the char self.cmd_prefix/_global are processed here
        """
        global is_global_msg
        global last_cmd_time

        # Basic Anti-Spam stuff
        cur_time = time.time()
        if int(cur_time) - last_cmd_time <= self.anti_spam_threshold:
            last_cmd_time = int(cur_time)
            return None
        last_cmd_time = int(cur_time)

        sourceNick = rawMsg[0].split('!')[0][1:]
        msg = []
        msg.append((' '.join(rawMsg[0].split(' ')[3:])[1:]))  # User full command
        msg[0] = msg[0][1:]

        global_msg = ''
        if is_global_msg:
            global_msg = ' (global output)'

        self.debug.info("on_pubmsg: Received command '"+msg[0]+"' from '"+sourceNick+"'"+global_msg)

        # Big switch where we handles received commands and eventually their args
        if msg[0].lower().split(' ')[0] in self.commands["iputgroup"]:
            self.cmd_iputgroup(sourceNick, msg[0])

        elif msg[0].lower().split(' ')[0] in self.commands["ikick"]:
            self.cmd_ikick(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["say"]:
            self.cmd_say(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["kill"]:
            self.cmd_kill(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["google"]:
            self.cmd_google(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["roulette"]:
            self.cmd_roulette(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["duck"]:
            self.cmd_duck()

        elif msg[0].lower().split(' ')[0] in self.commands["raw"]:
            self.cmd_raw(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["todo"]:
            self.cmd_todo(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["server"]:
            ret_cmd = self.cmd_server(msg[0], sourceNick)
            if isinstance(ret_cmd, tuple):
                self.privmsg(sourceNick, ret_cmd[0])
                self.privmsg(sourceNick, ret_cmd[1])
            else:
                if str(ret_cmd) != "None":
                    self.privmsg(sourceNick, ret_cmd)

        elif msg[0].lower().split(' ')[0] in self.commands["version"]:
            self.privmsg(sourceNick, "risc v"+__version__+" by "+__author__)

        elif msg[0].lower().split(' ')[0] in self.commands["uptime"]:
            self.privmsg(sourceNick, self.cmd_uptime(msg[0], sourceNick))

        elif msg[0].lower().split(' ')[0] in self.commands["ileveltest"]:
            self.cmd_ileveltest(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["search"]:
            cleanSearch = self.list_clean(msg[0].lower().split(' '))
            if len(cleanSearch) == 2:
                self.privmsg(sourceNick, self.cmd_search(cleanSearch[1]))
            elif len(cleanSearch) == 3:
                self.privmsg(sourceNick, self.search_accurate(cleanSearch[1].lower(), cleanSearch[2].lower()))
            else:
                self.privmsg(sourceNick, 'Invalid arguments. Check '+self.cmd_prefix+'help search.')

        elif msg[0].lower().split(' ')[0] in self.commands["chat"]:
            self.cmd_chat(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["seen"]:
            self.cmd_seen(msg[0],sourceNick)

        elif msg[0].lower().strip().split(' ')[0] in self.commands["base64"]:
            cleanB64 = self.list_clean(msg[0].split(' '))[0]
            cleanB64Data = ''.join(msg[0][len(cleanB64)+1:])
            if len(cleanB64Data) > 120:
                self.privmsg(sourceNick, "Input too large.")
            else:
                self.privmsg(sourceNick, base64.b64encode(bytearray(cleanB64Data, 'utf-8')))

        elif msg[0].lower().strip().split(' ')[0] in self.commands["sha1"]:
            self.cmd_sha1(msg[0], sourceNick)

        elif msg[0].lower().strip().split(' ')[0] in self.commands["md5"]:
            self.cmd_md5(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["players"]:
            cleanPlayers = self.list_clean(msg[0].split(' '))
            if len(cleanPlayers) != 2:
                self.privmsg(sourceNick, "Invalid arguments. Check "+self.cmd_prefix+"help players.")
            else:
                self.privmsg(sourceNick, self.cmd_players(cleanPlayers[1]))

        elif msg[0].lower().split(' ')[0] in self.commands["status"]:
            cleanStatus = self.list_clean(msg[0].split(' '))
            lenStatus = len(cleanStatus)

            if lenStatus > 2:
                self.privmsg(sourceNick, "Invalid arguments. Check "+self.cmd_prefix+"help status.")
            elif lenStatus == 1:
                self.privmsg(sourceNick, self.cmd_status("all"))  # Consider "!status" == "!status all"
            else:
                self.privmsg(sourceNick, self.cmd_status(cleanStatus[1]))

        elif msg[0].lower().strip().split(' ')[0] in self.commands["help"]:
            self.cmd_help(msg[0], sourceNick)

        elif msg[0].lower().strip() in self.commands["ishowadmins"]:
            self.cmd_ishowadmins(msg[0], sourceNick)

        elif msg[0].lower().strip() in self.commands["quit"]:
            self.cmd_quit(msg[0], sourceNick)

        is_global_msg = 0
        return None

    # <client> <reason>
    def game_on_calladmin(self, sv, data):
        """
        Called when a player uses the calladmin command
        """
        data_list = data.split('\r\n')
        player = data_list[0]
        reason = data_list[1]

        self.privmsg(self.channel, COLOR['boldwhite'] + '[' + COLOR['rewind'] + COLOR['boldgreen']
                + sv + COLOR['rewind'] + COLOR['boldwhite'] + ']' + COLOR['rewind'] + COLOR['boldblue']
                + ' ' + player + COLOR['rewind'] + ' requested an admin: ' + COLOR['boldblue']
                + reason + COLOR['rewind'])
        return None

    # <map_name> <cl_count> <max_cl_count>
    def game_on_game_map_change(self, sv, data):
        """
        Called on map change
        """
        data_list = data.split('\r\n')
        map_name = data_list[0]
        cl_count = data_list[1]
        max_cl_count = data_list[2]

        self.privmsg(self.channel, COLOR['boldwhite'] + '['+COLOR['rewind'] + COLOR['boldgreen']
                + sv + COLOR['rewind'] + COLOR['boldwhite'] + ']' + COLOR['rewind'] + ' map: '
                + COLOR['boldblue'] + map_name + COLOR['rewind'] + ', players:' + COLOR['boldblue']
                + ' ' + cl_count + COLOR['rewind'] + '/' + str(max_cl_count))
        return None

    # <admin> <admin_id> <client> <client_id> <reason=''>
    def game_on_client_kick(self, sv, data):
        """
        Called on player kick
        """
        data_list = data.split('\r\n')
        admin = data_list[0]
        admin_id = data_list[1]
        client = data_list[2]
        client_id = data_list[3]

        if data_list[4] == '':
            reason = COLOR['boldmagenta']+'No reason specified'+COLOR['rewind']
        else:
            reason = COLOR['boldblue']+data_list[4]+COLOR['rewind']

        self.privmsg(self.channel, COLOR['boldwhite']+'['+COLOR['rewind']+COLOR['boldgreen'] + sv
                + COLOR['rewind'] + COLOR['boldwhite'] + ']' + COLOR['rewind']+COLOR['boldyellow']
                +' '+admin+' @' + admin_id + COLOR['rewind'] + ' kicked' + COLOR['boldyellow'] +
                ' '+client+' @'+client_id+COLOR['rewind']+': '+re.sub('\^[0-9]{1}', '', reason))
        return None

    # <admin> <admin_id> <client> <client_id> <duration_min> <reason=''>
    def game_on_client_ban_temp(self, sv, data):
        """
        Called on player temp-ban
        """
        data_list = data.split('\r\n')
        admin = data_list[0]
        admin_id = data_list[1]
        client = data_list[2]
        client_id = data_list[3]
        duration = COLOR['boldyellow'] + ' ' + self.mintostr(int(data_list[4])) + COLOR['rewind']

        if data_list[5] == '':
            reason = COLOR['boldmagenta']+'No reason specified'+COLOR['rewind']
        else:
            reason = COLOR['boldblue']+data_list[5]+COLOR['rewind']

        self.privmsg(self.channel, COLOR['boldwhite']+'['+COLOR['rewind']+COLOR['boldgreen']+sv+COLOR['rewind']
                +COLOR['boldwhite']+']' + COLOR['rewind']+COLOR['boldyellow']+' '+admin+' @'+admin_id
                +COLOR['rewind']+' banned'+COLOR['boldyellow']+' '+client+' @' + client_id
                + COLOR['rewind'] + ' for' + duration + ': '+re.sub('\^[0-9]{1}', '', reason))
        return None

    # <admin> <admin_id> <client> <client_id> <reason=''>
    def game_on_client_ban(self, sv, data):
        """
        Called on player ban
        """
        data_list = data.split('\r\n')
        admin = data_list[0]
        admin_id = data_list[1]
        client = data_list[2]
        client_id = data_list[3]

        if data_list[4] == '':
            reason = COLOR['boldmagenta']+'No reason specified'+COLOR['rewind']
        else:
            reason = COLOR['boldblue']+data_list[4]+COLOR['rewind']

        self.privmsg(self.channel, COLOR['boldwhite']+'['+COLOR['rewind']+COLOR['boldgreen']+sv+COLOR['rewind']+COLOR['boldwhite'] + ']' +
                COLOR['rewind']+COLOR['boldyellow']+' '+admin+' @'+admin_id+COLOR['rewind']+' banned'+COLOR['boldyellow']+' '+client +
                ' @'+client_id+COLOR['rewind']+': '+re.sub('\^[0-9]{1}', '', reason))
        return None

    def q3_to_IRC_color(self, msg):
        """
        Convert a ioq3 colored string into IRC one
        """
        q3_to_IRC_map = {0: COLOR['rewind']+COLOR['boldblack'],
                1: COLOR['rewind']+COLOR['boldred'],
                2: COLOR['rewind']+COLOR['boldgreen'],
                3: COLOR['rewind']+COLOR['boldyellow'],
                4: COLOR['rewind']+COLOR['boldblue'],
                5: COLOR['rewind']+COLOR['blue'],
                6: COLOR['rewind']+COLOR['boldmagenta'],
                7: COLOR['rewind']+COLOR['white']}

        for cd in range(8):
            msg = re.sub('\^%d' % cd, q3_to_IRC_map[cd], msg)
        return msg

    # <client> <msg>
    def on_chat(self, sv, ID, data):
        """
        Catch player messages and broadcast them on IRC
        """
        db = self.get_db(sv)
        if not db:
            return None
        con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
        cur = con.cursor()
        cur.execute("""UPDATE %s SET processed = 1 WHERE ID = %d""" % ('risc_'+sv, ID))
        con.commit()
        con.close()

        data_list = data.split('\r\n')
        cl = data_list[0]
        msg = data_list[1]

        self.privmsg(self.channel, COLOR['boldwhite']+'['+COLOR['rewind']+COLOR['boldgreen'] +
                sv+COLOR['rewind']+'.'+COLOR['boldblue']+re.sub('\^[0-9]{1}', '', cl)+COLOR['rewind'] +
                COLOR['boldwhite']+']: '+COLOR['rewind']+self.q3_to_IRC_color(msg))
        return None

    # Note: using crlf separator on db data
    def game_watcher(self):
        """
        Watch for game events sent by the riscb3 plugin
        """
        global chat_set
        global THREADS_STOP
        self.debug.info('[+] Started "game_watcher" event callback.')
        try:
            # in case the bot is ran before the plugin, init tables
            for sv in self.sv_running:
                db = self.get_db(sv)
                if not db:
                    continue
                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS %s(ID INT AUTO_INCREMENT PRIMARY KEY,\
                        evt VARCHAR(40) NOT NULL DEFAULT '',\
                        data VARCHAR(255) NOT NULL DEFAULT '',\
                        time BIGINT NOT NULL DEFAULT 0,\
                        processed TINYINT NOT NULL DEFAULT 0)""" % ('risc_' + sv))
                con.commit()
                con.close()

            while 1 and not THREADS_STOP:
                time.sleep(0.3)

                for sv in self.sv_running:
                    db = self.get_db(sv)
                    if not db:
                        continue
                    con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
                    cur = con.cursor()

                    cur.execute("""SELECT ID,evt,data FROM %s WHERE processed = 0""" % ('risc_'+sv))
                    res = cur.fetchall()
                    cur.execute("""UPDATE %s SET processed = 1 WHERE processed = 0 AND evt != 'EVT_CHAT' AND evt != 'EVT_ICHAT'""" % ('risc_'+sv))
                    con.commit()
                    con.close()

                    if len(res) >= 1:
                        for row in res:
                            if row[1] == 'EVT_CALLADMIN':
                                self.game_on_calladmin(sv, row[2])
                            elif row[1] == 'EVT_CHAT' and chat_set[sv]:  # Extra precautions
                                self.on_chat(sv, row[0], row[2])
                            elif row[1] == 'EVT_GAME_MAP_CHANGE':
                                self.game_on_game_map_change(sv, row[2])
                            elif row[1] == 'EVT_CLIENT_KICK':
                                self.game_on_client_kick(sv, row[2])
                            elif row[1] == 'EVT_CLIENT_BAN_TEMP':
                                self.game_on_client_ban_temp(sv, row[2])
                            elif row[1] == 'EVT_CLIENT_BAN':
                                self.game_on_client_ban(sv, row[2])
                            else:
                                pass
        except Exception, e:
            self.debug.error('game_watcher: Exception caught: %s - Passing' % e)
            pass
        return None

    def set_evt_callbacks(self):
        """
        Starts threads to watch specific events
        """
        self.debug.info("[+] Setting and starting event callbacks")

        # game_watcher event callback
        if self.use_riscb3:
            th = threading.Thread(None, self.game_watcher, None, (), None)
            th.daemon = True  # So that the prog doesn't wait for the threads to exit
            th.start()
        return None

    def get_init_admins(self):
        """
        Retrieve the init admin list
        """
        ret = {}
        l = self.cfg.get('irc', 'init_admins').split(',')
        if not len(l):
            return ret
        for a in l:
            data = a.split(':')
            admin = data[0]
            lvl = int(data[1])
            if lvl in self.args["iputgroup"] or lvl == 100:
                ret.setdefault(admin)
                ret[admin] = lvl
        return ret

    def init_db(self):
        """
        Called on startup to init the database
        """
        # IRC-auth of some admins who can handle the bot
        d = self.get_init_admins()

        con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS admins(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                auth VARCHAR(20) NOT NULL DEFAULT '',\
                level TINYINT NOT NULL DEFAULT 0,\
                addedOn BIGINT NOT NULL DEFAULT 0,\
                addedBy VARCHAR(20) NOT NULL DEFAULT '')""")

        for admin in d:
            cur.execute("""SELECT auth FROM admins WHERE auth = '%s'""" % (admin))
            q = cur.fetchall()

            if not len(q):
                cur.execute("""INSERT INTO admins(auth,level,addedOn,addedBy) VALUES('%s',%d,%d,'risc')""" % (admin, d[admin], int(time.time())))

        con.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS todo(id INT AUTO_INCREMENT PRIMARY KEY,
                                                       author VARCHAR(32) NOT NULL DEFAULT '',
                                                       time BIGINT NOT NULL DEFAULT 0,
                                                       todo VARCHAR(128) NOT NULL DEFAULT '')""")

        con.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS server(id INT AUTO_INCREMENT PRIMARY KEY,
                                                       name VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN',
                                                       ip VARCHAR(22) NOT NULL DEFAULT '0.0.0.0',
                                                       author VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN',
                                                       time BIGINT NOT NULL DEFAULT 0)""")

        con.commit()
        con.close()
        return None

    def _send(self, data):
        """
        Simply socket.send() method using crlf separator
        """
        self.sock.send(data+'\r\n')
        return None

    def join(self):
        """
        Join a channel once connected
        """
        self._send('JOIN '+self.channel)
        return None

    def disconnect(self, message="Be right back."):
        """
        Disconnect from the current channel
        """
        self._send("QUIT :%s" % message)
        return None

    def mode(self, target, command):
        """
        Set a mode for a specified target
        """
        self._send('MODE %s %s' % (target, command))
        return None

    def privmsg(self, target, msg):
        """
        Send a PRIVMSG message
        """
        global is_global_msg
        if is_global_msg:
            target = self.channel
        self._send('PRIVMSG %s :%s' % (target, msg))
        return None

    def connect(self):
        """
        Connect to the IRC server
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Use TCP
        self.sock.connect((self.host, self.port))
        self._send("NICK " + self.nick)
        self._send("USER %s 0 * :%s" % (self.nick, self.nick))
        return None

    def clean_unicode(self, s):
        l = []
        for ch in s:
            ascii_ch = ord(ch)
            if ascii_ch >= 0 and ascii_ch <= 0x7f:
                l.append(ch)
        return ''.join(l)

    def xurls(self, raw_msg):
        """
        Extract URLs from str to a list
        """
        raw_msg = self.list_clean(raw_msg.split(' '))
        re_url = re.compile(r'(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[?[A-F0-9]*:[A-F0-9:]+\]?)(?::\d+)?(?:/?|[/?]\S+)$', re.IGNORECASE)
        ret = []

        for s in raw_msg:
            if re.match(re_url, s):
                ret.append(s)

        return ret

    def process_irc(self, raw_msg):
        """
        Handle IRC messages
        """
        if not re.search(' PRIVMSG ', raw_msg[0]):
            return None

        msg = ':'.join(raw_msg[0].split(':')[2:])
        nick = raw_msg[0].split('!')[0][1:]

        # Process URLs posting
        url_list = self.xurls(msg)

        for url in url_list:
            try:
                br = Browser()
                br.set_handle_robots(False)
                br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')]
                br.open(url)
                self.privmsg(self.channel, "Title: " + br.title())
            except Exception, e:
                self.debug.error("process_irc: Exception caught: '%s'." % e)

        return None

    def on_kick(self, raw_msg):
        kicker = raw_msg.split('!')[0][1:]
        target = raw_msg.split(' ')[3]
        reason = ':'.join(raw_msg.split(':')[2:])

        if target == self.nick:
            self.debug.warning("on_kick: Got kicked by '%s' for '%s' - Joining again in %ss ..." % (kicker, reason, str(self.on_kick_delay)))
            time.sleep(self.on_kick_delay)
            self.join()
        else:
            self.debug.info("on_kick: '%s' kicked '%s' for '%s'" % (kicker, target, reason))
            self.user_remove(target)
        return None

    def on_namereply(self, line):
        """
        Called on NAMES reply
        """
        self.init_users(line)
        return None

    def on_join(self, line):
        """
        Called when someone joins the channel
        """
        if not line:
            return None
        user = line.split('!')[0][1:]
        self.user_add(user)
        return None

    def on_part(self, line):
        """
        Called when someone leaves the channel
        """
        if not line:
            return None
        user = line.split('!')[0][1:]
        self.user_remove(user)
        return None

    def on_nick(self, line):
        """
        Called when someone renames
        """
        if not line:
            return None
        old = line.split('!')[0][1:]
        new = line.split(' ')[2][1:]
        self.user_remove(old)
        self.user_add(new)
        return None

    def on_nicknameinuse(self, line):
        """
        Called when risc's nick is already used
        """
        self.debug.warning("Nick '%s' already in use - renaming to '%s'" %(self.nick, self.nick+'_'))
        self.nick = self.nick+'_'
        self.start()
        return None

    def on_timeout(self, line):
        """
        Called on ping timeout
        """
        global THREADS_STOP
        self.debug.info("Connection timedout. Starting another risc instance in "+str(self.on_timeout_delay)+"...")
        THREADS_STOP = 1
        time.sleep(self.on_timeout_delay)
        raise Exception("risc_exception_irc_timeout")
        return None

    def _on_privmsg(self, msg):
        """
        Disptach PRIVMSG messages to the right functions
        """
        global is_global_msg
        global chat_set
        msgList = []
        msgList.append(msg)

        l = msg.split(' ')
        target = l[2]                  # Target == channel | pm
        content = ' '.join(l[3:])[1:]  # Raw message from the user

        try:
            content = self.clean_unicode(content)
            if not len(content):
                return None
            b = bytearray(content, "utf-8")
            if re.search(b'[\0-\x0a]{1}[A-Z]+([\0-\x0a]){1}', b):  # matches ctcp command
                self.on_ctcp(msgList)
                return None
        except Exception, e:
            self.debug.warning('_on_privmsg: Caught exception: %s -  Could be ascii conversion of non-ascii'+
                    ' char (unicode) during regex process. Passing' % e)
            pass

        # Handle IRC msgs for chat feature
        # send the IRC message to the game servers where chat is turned on
        # ensure the message doesn't come from risc ...
        if 1 in chat_set.values() and msgList[0].split('!')[0][1:] != self.nick and content[0] not in (self.cmd_prefix, self.cmd_prefix_global):
            try:
                self.on_ichat(msgList)
            except Exception, e:
                self.debug.error('_on_privmsg: Called to on_ichat failed: %s - Passing' % e)
                pass
            return None

        if content[0] != self.cmd_prefix and content[0] != self.cmd_prefix_global:
            self.process_irc(msgList)
            return None

        if content[0] == self.cmd_prefix_global:
            msgList[0] = re.sub(' :'+self.cmd_prefix_global, ' :'+self.cmd_prefix, msgList[0])
            is_global_msg = 1

        self.on_pubmsg(msgList)  # Handle pm same way as 'normal' messages
        return None

    ########################################################################################################################
    #                                                                                                                      #
    #                                                                                                                      #
    #                                  EVENT DISPATCHER                                                                    #
    #                                                                                                                      #
    #                                                                                                                      #
    ########################################################################################################################

    def dispatcher(self):
        """
        Main and general event dispatcher
        """
        global debug_mode
        last_chunk = ''

        while 1:
            res = self.sock.recv(512)

            if not res:
                continue

            # Split the buffer into lines, way more accurate, since the IRC protocol uses crlf separator
            lines = res.split("\r\n")

            if last_chunk:
                lines[0] = last_chunk + lines[0]
                last_chunk = ''

            for line in lines:
                if not line:
                    continue

                # Unfinished server message
                if res[-1] != '\n' and res[-2] != '\r' and not last_chunk and line == lines[-1]:
                    last_chunk = lines[-1]
                    continue # Only treat unfinished msgs after they've been rebuilt

                if debug_mode:
                    print line

                if re.search(" PRIVMSG ", line):
                    self._on_privmsg(line)

                    # Reply back to the server
                elif re.search("^PING :", line):
                    self._send("PONG :" + line.split(':')[1])

                elif re.search(" KICK ", line):
                    self.on_kick(line)

                elif re.search(" PART ", line):
                    self.on_part(line)

                elif re.search(" JOIN ", line):
                    self.on_join(line)

                elif re.search(" NICK ", line):
                    self.on_nick(line)

                # Indicate we're connected, we can now join the channel
                elif re.search(' '+RPL_WELCOME+' '+self.nick+' ', line):
                    self.on_welcome()

                elif re.search(' '+RPL_NAMEREPLY+' '+self.nick+' ', line):
                    self.on_namereply(line)

                elif re.search(' '+ERR_NICKNAMEINUSE+' ', line):
                    self.on_nicknameinuse(line)

#FIXME?: may be someone else timeout-ing ?
                elif re.search("ERROR :Closing Link: "+self.nick+" by .* \(Ping timeout\)", line):
                    self.on_timeout(line)

def main():
    print "[+] Running ..."
    try:
        inst = Risc()  # Init config and stuff
        inst.start()
    except KeyboardInterrupt:
        inst.debug.warning('Caught <c-c>. Exiting.')
        inst.disconnect()
        inst.exit_process()
    except SystemExit:
        inst.disconnect()
        inst.exit_process("Caught SystemExit")
    except TypeError:
        inst.debug.error('Caught TypeError exception on Risc.start(): Contact an admin to fix this asap. Passing')
        pass
    except NameError:
        inst.debug.error('Caught NameError exception on Risc.start(): Contact an admin to fix this asap. Passing')
        pass
    except UnicodeDecodeError:
        inst.debug.error('Caught UnicodeDecodeError exception on Risc.start(). Passing')
        pass
    except Exception, e:
        if str(e) == "risc_exception_irc_timeout":
            main()
        else:
            inst.debug.critical("Unhandled exception on Risc(): '%s'. Exiting." % e)
            inst.exit_process("Unhandled exception")

if __name__ == "__main__":
    main()
