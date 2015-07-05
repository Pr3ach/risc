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

cmds = {"quit": ["quit", "leave", "disconnect", "q"],
        "help": ["h", "help"],
        "status": ["status", "st"],
        "players": ["players", "p"],
        "base64": ["b64", "base64"],
        "search": ['search', 's'],
        "google": ["google", "g"],
        "uptime": ["uptime"],
        "version": ["version", "v"],
        "roulette": ["roulette", 'r'],
        "kill": ['kill', 'k'],
        "raw": ["raw"]}

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

        elif command in self.commands["server"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" [<ip:port> | add <ip> <name> | rm <name> | rename <old_name> <new_name> | list]: Aliases: "+', '.join(self.commands["server"])+\
                    ". Display info about the specified server. If no port is specified, assume 27960. Add, remove, rename or list all the available servers."

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

        elif command in self.commands["showadmins"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": Aliases: "+', '.join(self.commands["showadmins"])+". Show all "+\
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

        elif command in self.commands["getlevel"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ": <user> Aliases: " + ', '.join(self.commands["getlevel"]) +\
                    ". Returns the level of the user <user> if he's registered as admin with risc. If you don't specify a <user> parameter,"+\
                    " the command will return your level. You're required to be registered as admin[" +\
                    str(self.commandLevels['getlevel'])+"] with "+self.nick+" to access this command."

        elif command in self.commands["md5"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+" <string>: Aliases: "+', '.join(self.commands["md5"])+\
                    ". Returns the md5 of the string <string>."

        elif command in self.commands["status"]:
            return COLOR['boldgreen'] + command + COLOR['rewind'] + ' <serverName>' + ": Aliases: " + ', '.join(self.commands["status"])+\
                    ". Diplays information about the <serverName> server. Available args/server-name: "+', '.join(self.args['status'])

        elif command in self.commands["setlevel"]:
            return COLOR['boldgreen'] + command + COLOR['rewind']+": <user> <level> Aliases: "+', '.join(self.commands["setlevel"])+\
                    ". Set an admin level <level> to the user <user>. You need to be registered as admin[" + str(self.commandLevels['setlevel'])+\
                    "] with risc. Valid values for <level> include "+', '.join(str(x) for x in self.args['setlevel'])+". Use <level> = 0 to drop an admin."

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
