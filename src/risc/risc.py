#!/usr/bin/python2

# CHANGELOG
#
#       - add !status/!st command [OK]
#       - fix update_hist() [OK]
#       - add !players <serverName> command [OK]
#       - minor bug fixed [OK]
#       - add colors [OK]
#       - fix colors not working on non-console client [OK]
#       - remove ^1 etc from map names [OK]
#       - add aliases for args [OK]
#       - add !base64 / !sha1 / !md5 [OK]
#       - change lastposts to lastthreads / lt [OK]
#       - add bold colors [OK]
#       - add thread author [OK]
#       - v1.1 - Pr3acher
# -------
#       - use UDP instead of qstat stuff [OK]
#       - add !search <player> [OK]
#       - add !disasm [OK]
#       - add !hi <user> [OK]
#       - add <server> optional arg to !search && add limit of user output to !search [OK]
#       - make the distinction between players & bots [OK]
#       - fix server auth stuff [OK]
#       - v1.2 - Pr3acher
# -------
#       - add !ikick (in irc kick) [OK]
#       - !lt now returns a link to the last post in the thread [OK]
#       - write irc_is_admin(): returns auth + level from *nick* [OK]
#       - add required rights to help command [OK]
#       - add !ilt / ileveltest command [OK]
#       - updated irc_is_admin [OK]
#       - fixed time response in TIME ctcp [OK]
#       - fixed unicode char causing crash [OK]
#       - improved debug info [OK]
#       - irc_is_on_channel() [OK] XXX: NEED FIX (too slow)
#       - irc_is_authed() [OK] XXX: NEED FIX (too slow)
#       - set cmd output in pm [OK]
#       - add support for pm cmds [OK]
#       - add support for @ prefixed cmd's [OK]
#       - add support for in-game calladmin cmd [OK]
#       - removed disasm [OK]
#       - add threading support for game events [OK]
#       - v1.3 - Pr3acher
# -------
#       - minor change in colors [OK]
#       - added chat ability (IRC to game, other side implemented in riscb3 plugin) [OK]
#       - q3_to_IRC_color() [OK]
#       - PEP8: LF between functions and classes [OK]
#       - PEP8: Removed file encoding [OK]
#       - PEP8: Updated comments [OK]
#       - PEP8: Multiple fixes (comments, functions) [OK]
#       - PEP8: Global var, constant [OK]
#       - PEP8: Fixed all (except 79 chars standard) [OK]
#       - fix reason chars on game events (^[0-9]) [OK]
#       - set th.daemon = True for game_watcher thread [OK]
#       - more accurate time for ban [OK]
#       - Added cmd description for !chat [OK]
#       - add seen cmd - 10/08/2014: fixed exception [OK]
#       - cleaned up very long lines [OK]
#       - fix version field for !st cmd (rm "\^[0-9]") [OK]
#       - removed mysql warnings output [OK]
#       - fix (again) crash for unicode chars [OK]
#       - temp. disabled cmds until fixed: st, players, search [OK]
#       - typo fixed for help cmds [OK]
#       - v1.4 - Pr3acher - 08/18/2014
# -------
#       - removed bot cred. from risc.ini [OK]
#       - make sh added [OK]
# ------- v1.4.1 - Pr3acher - 08/19/2014
#       - fixed 'make-nix.sh' [OK]
# ------- v1.4.2 - Pr3acher - 08/20/2014
#       - fixed major bug in Sv [OK]
#       - fix: use only one db & table for risc_irc_admins [OK]
#       - bot auth credentials in risc.ini [OK]
#       - remove !lt cmd from help <cmd> cmd [OK]
#       - section in risc.ini for server alias [OK]
# ------- v1.4.3 - Pr3acher - 09/04/2014
#       - add cmd levels to ini conf file [OK]
#       - add admin init list to ini conf file [OK]
#       - add ability to use custom cmd prefixes [OK]
#       - allow chat in one server at a time only [OK]
#       - dynamic help msg [OK]
#       - update README file [OK]
# ------- v1.4.4 - Pr3acher - 09/07/2014
#       - fix minor dbg code [OK]
#       - fixed Sv failling -> crash [OK]
#       - cmd google
#       - Add cmd: playerinfo/pi
#       - add commands to set/get Cvars


__author__ = 'Pr3acher'
__version__ = '1.4.4'


import socket
import threading
import time
import sys
import os
import urllib
import ConfigParser
import re
import base64
import hashlib
import MySQLdb as mysql
from warnings import filterwarnings
import unicodedata
import json

HELP = None
CMDS = "help,ishowadmins,hello,disconnect,status,players,base64,sha1,md5,search,ikick,iputgroup,ileveltest,seen,chat,set"
is_global_msg = 0  # Set if the command starts with '@' instead of '!'
chat_set = {}
INIPATH = "risc.ini"

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
    def __init__(self, use__stdout__):
        t = time.time()
        if not use__stdout__:
            sys.stdout = open("risc_"+str(int(t))+'.log', "w+", 0)
        return None

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
    Gather info about a specific UrT 4.2 server
    """
    def __init__(self, ip, port, name, debug):
        self.debug = debug
        # Match a "valid" ip
        if re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', ip) is None:
            self.debug.warning('Sv.__init__: IP seems invalid - Returning 0')
            return 0
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
            self.debug.error("Sv.__init__: Couldn't connect to the given ip,port: %s - Ret 0" % e)
            return 0
        if not self.getstatus():
            raise Exception("Sv.getstatus()")
            if self.sock:
                self.sock.close()
            return 0
        if not self.getinfo():
            raise Exception("Sv.getinfo()")
            if self.sock:
                self.sock.close()
            return 0
        self.check_vars()
        if self.sock:
            self.sock.close()
        return None

    def list_clean(self, l):
        retList = []
        for i in l:
            if i != '' and i != ' ':
                retList.append(i)
        return retList

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
        return None

    def getstatus(self):
        try:
            self.sock.send(b'\xff'*4+b'getstatus')
            rawStatus = str(self.sock.recv(4096))
            listStatus = self.list_clean(rawStatus.split('\\'))
        except Exception, e:
            print 'Sv.getstatus: Exception: %s - Returning 0' % e
            return 0
        self.allowVote = self.get_var(listStatus, 'g_allowvote')
        self.version = self.get_var(listStatus, 'version')
        self.gameType = self.get_var(listStatus, 'g_gametype')
        self.nextMap = self.get_var(listStatus, 'g_NextMap')
        self.clientsList = self.get_clients_list(listStatus)
        return 1

    def getinfo(self):
        try:
            self.sock.send(b'\xff'*4+b'getinfo')
            rawInfo = str(self.sock.recv(2048))
            listInfo = self.list_clean(rawInfo.split('\\'))
        except Exception, e:
            print 'Sv.getinfo: Exception: %s - Returning 0' % e
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
            self.debug = Debug(0)
            filterwarnings("ignore", category = mysql.Warning)
            self.cfg = ConfigParser.ConfigParser()
            self.cfg.read(INIPATH)

            self.host = self.cfg.get('irc', 'host')
            self.port = int(self.cfg.get('irc', 'port'))
            self.channel = self.cfg.get("irc", "channel")
            self.nick = self.cfg.get("irc", "nick")

            self.db_host = self.cfg.get('db', 'host')
            self.db_user = self.cfg.get('db', 'user')
            self.db_passwd = self.cfg.get('db', 'passwd')
            self.db_name = self.cfg.get('db', 'self_db')  # db for risc settings (admins etc)

            # get servers, their dbs
            self.svs = self.cfg.get('var', 'servers').split(',')

            if len(self.svs) > 8:
                self.debug.error('Too many servers. Max of 8 servers can be supported.')

            self.dbs = self.cfg.get('db', 'databases').split(',')

            if len(self.dbs) != len(self.svs):
                self.debug.error('Number of databases does not match the number of servers.')

            # Get the servers on which the riscb3 plugin is running
            self.sv_running = (self.cfg.get('var', 'svrunning').split(','))

            # Get bot credentials to auth with Q
            self.auth = self.cfg.get('irc', 'auth')
            self.auth_passwd = self.cfg.get('irc', 'auth_passwd')

            self.cmd_prefix = self.cfg.get('risc', 'cmd_prefix')
            self.cmd_prefix_global = self.cfg.get('risc', 'cmd_prefix_global')

            self.init_help()

            if len(self.cmd_prefix) != 1:
                self.cmd_prefix = '!'

            if len(self.cmd_prefix_global) != 1:
                self.cmd_prefix_global = '@'

            for sv in self.sv_running:
                chat_set[sv] = 0
        except:
            self.debug.critical("Risc.__init__: Exception caugth while loading config settings - Make sure there's no missing field")
            raise SystemExit

        # Commands and their aliases
        self.commands = {"quit": ["quit", "leave", "disconnect", "q"],
                         "help": ["h", "help"],
                         "ishowadmins": ["isa", "ishowadmins"],
                         "hello": ["hi", "hello"],
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
                         "set": ["set"],
                         "google": ["google"],
                         "ileveltest": ['ileveltest', 'ilt']}

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
        return None

    def start(self):
        """
        Launch the bot: connect, start event dispatcher, join
        """
        self.init_irc_admins()
        self.connect()
        self.debug.info('[+] Connected on '+self.host+' port '+str(self.port))
        self.set_evt_callbacks()
        self.dispatcher()
        return None

    def exit_process(self, msg="exit_process: Exiting"):
        self.debug.info(msg)
        time.sleep(0.3)
        sys.exit(0)
        return None

    def init_help(self):
        global HELP
        global CMDS
        HELP = "Available cmds: "
        CMDS_list = CMDS.split(',')
        for cmd in CMDS_list:
            HELP += self.cmd_prefix+cmd+', '
        HELP += ". Type "+self.cmd_prefix+"help <cmd> for more info. Report bugs/suggestions at pr3acher777h@gmail.com."
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
        ret = {"quit": 80,
               "ikick": 80,
               "iputgroup": 100,
               "chat": 80,
               "set": 80,
               "ileveltest": 60}

        for cmd in ret:
            if self.cfg.has_option("levels", "cmd_"+cmd):
                lvl = int(self.cfg.get("levels", "cmd_"+cmd))
                if lvl in self.args["iputgroup"] or lvl == 100:
                    ret[cmd] = lvl
        return ret

    def on_welcome(self):
        """
        Called after we successfully connected to the server
        """
        self._send("PRIVMSG Q@CServe.quakenet.org :AUTH "+self.auth+" "+self.auth_passwd)  # Auth against Q
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
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "risc v" + __version__ + " by Pr3acher @__Pr3__" + "\001")

        elif msg[0].lower() == "ping":
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "PONG " + "\001")

        else:
            self._send("NOTICE " + sourceNick + " :\001" + msg[0].upper() + ' ' + "Error: " + msg[0] + " CTCP command is not supported." + "\001")

        return None

    def set_option(self, section, option, value):
        """
        Write to and flush the config file, since configparser only buffer it
        """
        try:
            self.cfg.read(INIPATH)
            self.cfg.set(section, option, value)
            self.cfg.write(open(INIPATH, "wb"))
        except:
            self.debug.warning("set_option: exception caught")
            pass
        return None

    # XXX: FIX NEEDED: too slow
    def irc_is_on_channel(self, nick):
        """
        Checks whether a user-nick is on the channel, return 0 if not, otherwise return 1
        """
        try:
            self.sock.send('WHOIS ' + nick + '\r\n')
            res = str(self.sock.recv(1024))
        except:
            self.debug.error('irc_is_on_channel: Exception caught')
            return 0
        if re.search(self.channel, res) is None or re.search(":No such nick", res):
            return 0
        return 1

    # XXX: FIX NEEDED: too slow
    def irc_is_authed(self, nick):
        """
        Check whether a user-nick is registered / has an account with quakenet, return 0 if not, otherwise return the account name
        """
        try:
            if not self.irc_is_on_channel(nick):
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
        for key in d:
            for val in d[key]:
                if val == searchValue.lower():
                    return key
        return 0

    def get_db(self, name):
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

            cur.execute("""SELECT level FROM risc_irc_admins WHERE auth = '%s'""" % auth)

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

    def cmd_iputgroup(self, source, msg):
        """
        Put an authed user in one of the admin group
        """
        cleanIpg = self.list_clean(msg.split(' '))

        # Check input
        if len(cleanIpg) != 3:
            return 0

        if len(cleanIpg[1]) > 19:
            return 0

        try:
            cleanIpg[2] = int(cleanIpg[2])
        except:
            return 0

        # Check rights
        sourceAuth, sourceLevel = self.irc_is_admin(source)
        if not sourceAuth or sourceLevel != 100:
            return 0

        targetAuth, targetLevel = self.irc_is_admin(cleanIpg[1])
        if not targetAuth or (cleanIpg[2] not in self.args['iputgroup'] and cleanIpg[2] != 0) or targetLevel == cleanIpg[2]:
            return 0

        try:
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
            cur = con.cursor()

            if targetLevel in self.args["iputgroup"] or cleanIpg[2] == 0:  # If already admin, delete the record before.
                cur.execute("""DELETE FROM risc_irc_admins WHERE auth = '%s'""" % targetAuth)

            if cleanIpg[2] in self.args['iputgroup']:
                cur.execute("""INSERT INTO risc_irc_admins(auth,level,addedOn,addedBy) VALUES('%s',%d,%d,'%s')""" % (targetAuth, cleanIpg[2], int(time.time()), sourceAuth))

            con.commit()
            con.close()

        except:
            self.debug.critical('cmd_iputgroup: Exception caught. Rolling back the db')
            if con:
                con.rollback()
                con.close()
            return 0

        if cleanIpg[2] == 0:
            return COLOR['boldgreen']+source+COLOR['rewind']+": User-auth "+COLOR['boldmagenta']+targetAuth+COLOR['rewind']+\
                         ', '+COLOR['boldmagenta']+'admin'+COLOR['rewind']+'['+str(targetLevel)+'], is no more.'

        return COLOR['boldgreen']+source+COLOR['rewind']+": User-auth "+COLOR['boldmagenta']+targetAuth+COLOR['rewind']+\
                     " was successfully added to "+COLOR['boldmagenta']+'admin'+COLOR['rewind']+'['+str(cleanIpg[2])+'] group.'

    def cmd_ileveltest(self, msg0, sourceNick):
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

            cur.execute("""SELECT auth FROM risc_irc_admins""")

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

    def cmd_hello(self, msg0, sourceNick):
        helloClean = self.list_clean(msg0.split(' '))
        lenHello = len(helloClean)

        if lenHello > 2:
            self.privmsg(sourceNick, 'Invalid arguments. Check '+self.cmd_prefix+'help hello.')
            return None

        if lenHello == 1:
            self.privmsg(self.channel, COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" says hi to "+self.channel)
            return None

        else:
            if len(helloClean[1]) > 28:
                self.privmsg(sourceNick, 'Nick has too many chars')
                return None
            elif sourceNick.lower() == helloClean[1].lower():
                self.privmsg(self.channel, COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" is feeling alone ...")
                return None
            else:
                if self.irc_is_on_channel(helloClean[1]) or helloClean[1].lower() == 'q':
                    self.privmsg(self.channel, COLOR["boldgreen"]+sourceNick+COLOR['rewind']+" says hi to "+helloClean[1])
                else:
                    self.privmsg(sourceNick, "No such nick")
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
            reason = ''.join(cleanKick[2:])

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
                         "You need to be admin["+str(self.commandLevels['ikick'])+"] to access this command."+COLOR['rewind'])

    def cmd_sha1(self, msg0, sourceNick):
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
        Turn ON or OFF the chat feature in the specified server
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
                         ": Invalid arguments, target server either doesn't exist or is not running riscb3")
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

            cur.execute("""INSERT INTO %s(evt,data,time,processed) VALUES('EVT_CHAT_SET','%s',%d,1)""" % ('risc_' + sv, state, int(time.time())))
            con.commit()
            con.close()
        except:
            if con:
                con.rollback()
                con.close()
            self.debug.error('cmd_chat: Error during db operations, trying roll back. Passing')
            self.privmsg(sourceNick, COLOR['boldred']+sourceNick+COLOR['rewind']+
                         ': There was an error changing the chat state for the '+COLOR['boldblue']+sv+COLOR['rewind']+' server.')
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
        self.cfg.read(INIPATH)
        ret = ''
        serv = serv.lower()

        if serv == 'all':
            for i in self.argAliases['servers']:
                fullIp = self.cfg.get('var', i).split(':')
                try:
                    sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
                except:
                    return COLOR['boldred']+"Error: Exception raised: Couldn't get "+i+" server status"+COLOR['rewind']

                if not sv:
                    return COLOR['boldred']+"Error: Couldn't get "+i+" server status"+COLOR['rewind']
                if sv.clientsList == -1:
                    nbClients = 0
                else:
                    nbClients = len(sv.clientsList)

                ret += COLOR['boldgreen']+i+COLOR['rewind']+' : Players: '+COLOR['boldblue']+' '+str(nbClients)+COLOR['rewind']+\
                             '/'+str(sv.maxClients)+', map: '+COLOR['boldblue']+re.sub('\^[0-9]', '', sv.mapName)+COLOR['rewind']+' - '
                del sv
            ret = ret[:-3]

        else:
            keyFromValue = self.get_dict_key(self.argAliases['servers'], serv)
            if not keyFromValue:
                return 'Invalid argument. Check '+self.cmd_prefix+'help status'

            fullIp = self.cfg.get('var', keyFromValue).split(':')
            try:
                sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
            except:
                return COLOR['boldred']+"Error: Exception raised: Couldn't get "+keyFromValue+" server status"+COLOR['rewind']
                
            if not sv:
                return COLOR['boldred']+"Error: Couldn't get "+keyFromValue+" server status"+COLOR['rewind']

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

            ret = COLOR['boldgreen'] + keyFromValue + COLOR['rewind'] + ' : Players: ' +\
                COLOR['boldblue'] + ' '+str(nbClients) + COLOR['rewind'] + '/' +\
                str(sv.maxClients) + ', map: '+COLOR['boldblue'] +\
                re.sub('\^[0-9]', '', sv.mapName)+COLOR['rewind'] +\
                ', nextmap: '+COLOR['boldblue']+re.sub('\^[0-9]', '', sv.nextMap) +\
                COLOR['rewind']+', version: '+COLOR['boldblue']+re.sub('\^[0-9]','',sv.version)+COLOR['rewind'] +\
                ', auth: '+sv.authNotoriety+', vote: '+sv.allowVote
            del sv
        return ret

    def cmd_help_(self, command):
        command = command.lower()

        if command in self.commands["quit"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: " + ', '.join(self.commands["quit"])+\
                         ". Tells risc to leave. You need to be registered as admin["+str(self.commandLevels['quit'])+\
                         "] with risc."

        elif command in self.commands["seen"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <player>: Aliases: "+', '.join(self.commands["seen"])+\
                         ". Return the last time a player was seen in the server set."

        elif command in self.commands["hello"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": <user> Aliases: " + ', '.join(self.commands["hello"])+\
                         ". Simply says hi to user <user>. Use without <user> argument to target the channel."

        elif command in self.commands["players"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <serverName>: Aliases: "+", ".join(self.commands["players"])+\
                         ". Shows all players on the <serverName> server. Available args/server-name: "+', '.join(self.args["players"])

        elif command in self.commands["search"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ": <playerNick> <server> Aliases: " + ', '.join(self.commands["search"])+\
                         ". Search for the player <playerNick> in the current server set if <server> is not specified,"+\
                         " else it performs the search in the <server> server."

        elif command in self.commands["ishowadmins"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["ishowadmins"])+". Shows all "+\
                         self.nick+" admins."

        elif command in self.commands["base64"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <utf8String>: Aliases: "+', '.join(self.commands["base64"])+\
                         ". Returns a base64 encoded string from the utf-8 string <utf8_String>."

        elif command in self.commands["sha1"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + " <string>: Aliases: " + ', '.join(self.commands["sha1"])+\
                         ". Returns the sha1 of the string <string>."

        elif command in self.commands["set"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + " <cvar> <value>: Aliases: " + ', '.join(self.commands["set"])+\
                         ". Set a value for the specified cvar."

        elif command in self.commands["chat"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + " <server> <on|off>: Aliases: " + ', '.join(self.commands["chat"])+\
                         ". Enable or disable the chat feature betwen IRC and the server <server>. Return the state of the chat feature"+\
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
                         str(self.commandLevels['ileveltest'])+"] with PerBot to access this command."

        elif command in self.commands["md5"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <string>: Aliases: "+', '.join(self.commands["md5"])+\
                         ". Returns the md5 of the string <string>."

        elif command in self.commands["status"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ' <serverName>' + ": Aliases: " + ', '.join(self.commands["status"])+\
                         ". Diplays information about the <serverName> server. Available args/server-name: "+', '.join(self.args['status'])

        elif command in self.commands["iputgroup"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": <user> <level> Aliases: "+', '.join(self.commands["iputgroup"])+\
                         ". Set an admin level <level> to the user <user>. You need to be registered as admin[" + str(self.commandLevels['iputgroup'])+\
                         "] with risc. <user> must have a quakenet account. Valid values for <level> include "+', '.join(str(x) for x in self.args['iputgroup'])+'.'

        else:
            return "Command not found: " + COLOR['boldmagenta']+command+COLOR['rewind']

    def cmd_players(self, serverName, rawRet=0):
        """
        Return the player list in the specified server
        """
        serverName = self.get_dict_key(self.argAliases['servers'], serverName.lower())
        ret = []
        if not serverName:
            return "Invalid arguments. Check "+self.cmd_prefix+"help players."

        self.cfg.read(INIPATH)
        fullIp = self.cfg.get('var', serverName).split(":")
        try:
            sv = Sv(fullIp[0], int(fullIp[1]), '', self.debug)
        except:
            return COLOR['boldred']+"Error: Exception raised: Couldn't get "+serverName+" server status"+COLOR['rewind']

        if not sv:
            return COLOR['boldred']+'Error retrieving '+serverName+' players'+COLOR['rewind']

        if sv.clients == 0 or sv.clientsList == -1:
            return serverName + ' server is currently empty.'

        usePings = False
        if len(sv.clientsPings) == len(sv.clientsList):
            usePings = True

        for i in range(len(sv.clientsList)):
            if usePings and sv.clientsPings[i] == '0':
                ping = COLOR['rewind']+' ('+COLOR['boldblue']+'BOT'+COLOR['rewind']+')'
            else:
                ping = ''

            ret.append(COLOR['boldgreen']+sv.clientsList[i]+COLOR['rewind']+ping)

        if rawRet:
            return ret

        ret.sort()
        # For some reason, sv.clients is innacurate here ...
        return 'Players on '+serverName+' ('+str(len(sv.clientsList))+'/'+str(sv.maxClients)+'): '+', '.join(ret)

    def cmd_seen(self, msg0, sourceNick):
        """
        Return the last time a user was seen in the specified server
        """
        cleanCmd = self.list_clean(msg0.split(' '))

        if len(cleanCmd) != 2:
            self.privmsg(sourceNick, "Invalid arguments, check "+self.cmd_prefix+"help seen.")
            return None
        
        # b3 uses 32 chars to store names
        if len(cleanCmd[1]) > 31:
            self.privmsg(sourceNick, "User nick too long, max length: 31 chars")

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

        self.privmsg(sourceNick, "No such player")
        return None

    def cmd_search(self, player, rawRet=0):
        """
        Search for a player in the entire server set
        """
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
            except:
                return COLOR['boldred']+"Error: Exception raised: Couldn't get "+server+" server status"+COLOR['rewind']
            if not sv:
                return COLOR['boldred']+'An error occured while processing your command: could not get '+server+' server status'+COLOR['rewind']
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

    def cmd_set(self, msg0, sourceNick):
        """
        Set a Cvar value to the specified server
        """
        cmd_clean = self.list_clean(msg0.split(' '))
        cmd_len = len(cmd_clean)

        if cmd_len != 4:
            self.privmsg(sourceNick,"Invalid arguments, check "+self.cmd_prefix+"help set.")
            return None

        sv = self.get_dict_key(self.argAliases['servers'], cmd_clean[1])
        
        if not sv or sv not in self.sv_running:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+
                         ": Invalid arguments, target server either doesn't exist or is not running riscb3")
            return None

        auth, level = self.irc_is_admin(sourceNick)

        if not auth or level < self.commandLevels['set']:
            self.privmsg(sourceNick, COLOR['boldmagenta']+sourceNick+COLOR['rewind']+": You need to be admin["+
                         str(self.commandLevels['set'])+'] to access this command.')
            return None

        try:
            data = cmd_clean[2]+'\r\n'+cmd_clean[3]
            db = self.get_db(sv)
            if not db:
                self.privmsg(sourceNick, COLOR['boldred']+sourceNick+COLOR['rewind']+
                         ': There was an error setting the Cvar for the '+COLOR['boldblue']+sv+COLOR['rewind']+' server.')
                return None
            con = mysql.connect(self.db_host, self.db_user, self.db_passwd, db)
            cur = con.cursor()

            # <Cvar> <value>
            cur.execute("""INSERT INTO %s(evt,data,time,processed) VALUES('EVT_CVAR_SET','%s',%d,0)""" % ('risc_' + sv, data, int(time.time())))
            con.commit()
            con.close()
        except Exception, e:
            self.debug.error('cmd_set: Exception: %s - Trying rollback db - Passing' % e)
            if con:
                con.rollback()
                con.close()
            self.privmsg(sourceNick, COLOR['boldred']+sourceNick+COLOR['rewind']+
                         ': There was an error setting the Cvar for the '+COLOR['boldblue']+sv+COLOR['rewind']+' server.')
            pass

        self.privmsg(sourceNick, COLOR['boldgreen']+sourceNick+COLOR['rewind']+
                         ': Setting the Cvar for the '+COLOR['boldblue']+sv+COLOR['rewind']+' server.')
        return None

    def cmd_google(self, msg0, nick):
        clean_msg = self.list_clean(msg0.split(' '))
        if len(clean_msg) <= 1:
            self.privmsg(nick, "Invalid arguments, check "+self.cmd_prefix+"help google.")
            return None
        API_url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
        query = urllib.urlencode({'q': searchfor})
        data_search = clean_msg[1]
        response = urllib.urlopen(API_url+query)
        results = response.read()
        res = json.loads(results)
        data = res['responseData']
        self.privmsg(nick, "nb_res: "+ data['cursor']['estimatedResultCount'])
        return None

    # -------------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------

    def search_accurate(self, p, serv):
        """
        Search for a player in the specified server
        """
        (cl, pings) = self.cmd_search(p, 1)
        servKey = self.get_dict_key(self.argAliases["servers"], serv.lower())
        ret = []
        count = 0

        if not servKey:
            return 'Invalid arguments: '+serv+'. Check '+self.cmd_prefix+'help search.'

        p = re.escape(p)

        if cl[servKey][0] == '' and len(cl[servKey][0]) == 1:
            return COLOR['boldmagenta'] + 'No such player in the specified server.' + COLOR['rewind']

        usePings = 0
        isBot = COLOR['rewind'] + ' (' + COLOR['boldblue'] + 'BOT' + COLOR['rewind'] + ')'

        if len(cl[servKey]) == len(pings[servKey]):
            usePings = 1

        for i in range(len(cl[servKey])):
            if re.search(p.lower(), cl[servKey][i].lower()):
                count += 1
                if usePings:
                    if pings[servKey][i] == '0':
                        ret.append(COLOR['boldgreen'] + cl[servKey][i] + isBot + COLOR['rewind'])
                    else:
                        ret.append(COLOR['boldgreen'] + cl[servKey][i] + COLOR['rewind'])
                else:
                    ret.append(COLOR['boldgreen'] + cl[servKey][i] + COLOR['rewind'])

        # 'not count' not giving the expecting result? ...
        if count == 0:
            return COLOR['boldmagenta']+'No such player in the specified server.'+COLOR['rewind']
        elif count == 1:
            return 'Found a player matching the request in the '+COLOR['boldwhite']+servKey+COLOR['rewind']+' server: '+ret[0]
        else:
            ret.sort()
            return 'Found '+str(count) + ' players matching the request in the ' + COLOR['boldwhite'] + servKey + COLOR['rewind'] + ' server: ' + ', '.join(ret)

    def list_clean(self, list):
        ret = []
        for e in list:
            if e != '' and e != ' ':
                ret.append(e)
        return ret

    def mintostr(self, m):
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
        Channel messages starting with the char '!' or '@' are processed here
        """
        global is_global_msg
        cmdTime = time.time()
        sourceNick = rawMsg[0].split('!')[0][1:]
        msg = []
        msg.append((' '.join(rawMsg[0].split(' ')[3:])[1:]))  # User full command
        msg[0] = msg[0][1:]

        global_msg = ''
        if is_global_msg:
            global_msg = ' (global output)'

        self.debug.info("on_pubmsg: Received command '"+msg[0]+"' from '"+sourceNick+"'"+global_msg)

        # Big switch where we handles received commands and eventually their args
        if msg[0].lower().split(' ')[0] in self.commands["hello"]:
            self.cmd_hello(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["iputgroup"]:
            retCmdIpg = self.cmd_iputgroup(sourceNick, msg[0])
            if not retCmdIpg:
                self.privmsg(self.channel, COLOR['boldred']+"Failed. Check "+self.cmd_prefix+"help iputgroup."+COLOR['rewind'])
            else:
                self.privmsg(sourceNick, retCmdIpg)

        elif msg[0].lower().split(' ')[0] in self.commands["ikick"]:
            self.cmd_ikick(msg[0], sourceNick)

        elif msg[0].lower().split(' ')[0] in self.commands["google"]:
            self.cmd_google(msg[0], sourceNick)

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

        elif msg[0].lower().split(' ')[0] in self.commands["set"]:
            self.cmd_set(msg[0], sourceNick)

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
        Watch for game event generated by the riscb3 plugin
        """
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

            while 1:
                time.sleep(0.5)

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

    def set_evt_callbacks(self):
        """
        Starts threads to watch specific events
        """
        self.debug.info("[+] Setting and starting event callbacks")
        th = threading.Thread(None, self.game_watcher, None, (), None)
        th.daemon = True  # So that the prog doesn't wait for the threads to exit
        th.start()
        return None

    def get_init_admins(self):
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

    def init_irc_admins(self):
        """
        Called on startup to init the irc admin table
        """
        # IRC-auth of some admins who can handle the bot
        d = self.get_init_admins()

        con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS risc_irc_admins(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                                                auth VARCHAR(20) NOT NULL DEFAULT '',\
                                                                level TINYINT NOT NULL DEFAULT 0,\
                                                                addedOn BIGINT NOT NULL DEFAULT 0,\
                                                                addedBy VARCHAR(20) NOT NULL DEFAULT '')""")

        for admin in d:
            cur.execute("""SELECT auth FROM risc_irc_admins WHERE auth = '%s'""" % (admin))
            q = cur.fetchall()

            if not len(q):
                cur.execute("""INSERT INTO risc_irc_admins(auth,level,addedOn,addedBy) VALUES('%s',%d,%d,'risc')""" % (admin, d[admin], int(time.time())))

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

    def disconnect(self, message="ducks"):
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
            is_global_msg = 0
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

    def process_irc(self, raw_msg):
        if len(raw_msg[0].split(':')) != 3:
            return None
        msg = raw_msg[0].split(':')[2]
        nick = raw_msg[0].split('!')[0][1:]
        url_re = re.compile(r'(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
                r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d'
                r'{1,3}|\[?[A-F0-9]*:[A-F0-9:]+\]?)(?::\d+)?(?:/?|[/?]\S+)$', re.IGNORECASE)

        is_url = re.match(url_re, msg)

        if is_url:
            url_dump = urllib.urlopen(is_url[0]).read()
            print "dump: "
            print url_dump
        print "no url"

        return None

    def _on_privmsg(self, msg):
        """
        Disptach PRIVMSG messages to the right functions
        """
        global is_global_msg
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
        onWelcome = 0
        while 1:
            res = self.sock.recv(512)

            # Split the buffer into lines, way more accurate, since the IRC protocol uses crlf separator
            for line in res.split('\r\n'):

                if not line:
                    continue

                if re.search('PRIVMSG', line):
                    self._on_privmsg(line)

                # Reply back to the server
                if re.search('PING :', line):
                    self._send('PONG :' + line.split(':')[1])

                # Indicate we're connected, we can now join the channel
                if re.search(':Welcome', line):
                    if not onWelcome:
                        self.on_welcome()
                        onWelcome = 1 

if __name__ == '__main__':
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
        inst.debug.critical('Unhandled exception on Risc(): %s. Exiting.' % e)
        inst.exit_process()
