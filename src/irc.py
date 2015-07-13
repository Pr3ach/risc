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

__author__ = "Preacher"
__version__ = "1.0"

import socket
import re
import time

RPL_WELCOME                 = "001"             # :Welcome_msg... <nick>!<user>@<host>
RPL_TOPIC                   = "332"             # <channel> :<topic>
RPL_TOPICWHOTIME            = "333"
RPL_NAMEREPLY               = "353"             # ( '='|'*'|'@' ) <channel> ' ' : ['@'|'+'] <nick> *( ' ' ['@'|'+'] <nick> )
RPL_ENDOFNAMES              = "366"             # <channel> :<info>
RPL_MOTD                    = "372"             # :- <string>
ERR_NICKNAMEINUSE           = "433"             # <nick> :<reason>

COLOR = {'white': '\x030', 'boldwhite': '\x02\x030', 'green': '\x033', 'red': '\x035',
        'magenta': '\x036', 'boldmagenta': '\x02\x036', 'blue': '\x032',
        'boldred': '\x02\x034', 'boldblue': '\x02\x032', 'boldgreen': '\x02\x033',
        'boldyellow': '\x02\x038', 'boldblack': '\x02\x031', 'rewind': '\x0f'}

USER_ALIASES = 0
USER_MASK = 1
LEVEL_MASKS = {'o': 2, 'v': 1}

DATA_PROCESSED = 0x539

IRC_STOP = 0

class Irc():
    def __init__(self, host, port, channel, nick):
        self.host = host
        self.port = port
        self.channel = channel
        self.nick = nick
        self.users = {} # {"user": [["old_nick", "old_nick2" ...], mode_mask], ...}
        self.callbacks = {"all": None,
                "on_privmsg": None,
                "on_welcome": self.on_welcome,
                "on_kick": self.on_kick,
                "on_namereply": self.on_namereply,
                "on_join": self.on_join,
                "on_part": self.on_part,
                "on_nick": self.on_nick,
                "on_mode": self.on_mode,
                "on_nicknameinuse": self.on_nicknameinuse,
                "on_ping": self.on_ping,
                "on_timeout": None}
        return None

    def start(self):
        """
        Connect to the IRC server and start dispatching data
        """
        global IRC_STOP
        IRC_STOP = 0
        self.connect()
        self._data_dispatcher()
        return None

    def stop(self):
        """
        Leave the channel, close the connection and stop the IRC session
        """
        global IRC_STOP
        IRC_STOP = 1
        self.part()
        self.disconnect()
        self.sock.close()
        return None

    def get_user_level(self, user):
        """
        Return the maximum level of a user
        """
        if user not in self.users:
            return 0

        mask = self.users[user][USER_MASK]

        for s in LEVEL_MASKS:
            if LEVEL_MASKS[s] & mask:
                return LEVEL_MASKS[s]
        return 0

    def set_callback(self, cb_name, cb_function):
        """
        Set a callback function for an event
        """
        if cb_name.lower() in self.callbacks:
            self.callbacks[cb_name] = cb_function
        return None

    def on_ping(self, ping_data):
        """
        Default callback function for ping event
        """
        self._send("PONG :" + ping_data)
        return None

    def on_welcome(self, host, welcome_msg):
        """
        Default callback function for welcome event
        """
        self.join()
        return None

    def on_kick(self, kicker, kicked, reason):
        """
        Default callback function for kick event
        """
        if kicked in self.users:
            self.users.pop(kicked)
        if kicked == self.nick:
            self.join()
        return None

    def on_namereply(self, user_list):
        """
        Default callback function for namereply event
        """
        for user in user_list:
            level = 0
            if user[0] == '@':
                level = LEVEL_MASKS['o']
                user = user[1:]
            elif user[0] == '+':
                level = LEVEL_MASKS['v']
                user = user[1:]
            if user in self.users:
                continue
            self.users.setdefault(user)
            self.users[user] = [[], level]
        return None

    def on_join(self, user):
        """
        Default callback function for join event
        """
        if user not in self.users:
            self.users.setdefault(user)
            self.users[user] = [[], 0]
        return None

    def on_part(self, user, reason):
        """
        Default callback function for part event
        """
        if user in self.users:
            self.users.pop(user)
        return None

    def on_nick(self, prev_nick, new_nick):
        """
        Default callback function for nick event
        """
        if prev_nick not in self.users:
            self.users.setdefault(new_nick)
            self.users[new_nick] = [[prev_nick], 0]
        else:
            self.users[new_nick] = self.users.pop(prev_nick)
            self.users[new_nick][USER_ALIASES].append(prev_nick)
        return None

    def on_mode(self, mode, by, target):
        """
        Default callback function for mode event
        """
        if target not in self.users:
            return None

        cur = ''
        for i in mode:
            if i in ('+', '-'):
                cur = i
                continue

            if i not in ('v', 'o'):
                continue

            if cur == '+':
                self.users[target][USER_MASK] |= LEVEL_MASKS[i]
            else:
                self.users[target][USER_MASK] &= ~LEVEL_MASKS[i]
        return None

    def on_nicknameinuse(self, nick):
        """
        Default callback function for nicknameinuse event
        """
        self.stop()
        self.nick += '_'
        self.users = {}
        time.sleep(3)
        self.start()
        return None

    def call_cb_privmsg(self, line):
        """
        Call the on_privmsg callback function, if set
        """
        if self.callbacks["on_privmsg"] is not None:
            _from = line.split('!')[0][1:]
            if _from[0] in ('@', '+', '&'):
                _from = _from[1:]
            to = line.split(' ')[2]
            msg = ' '.join(line.split(' ')[3:])[1:]

            self.callbacks["on_privmsg"](_from, to, msg)
        return None

    def call_cb_ping(self, line):
        """
        Call the on_ping callback function if set, or pong back the server
        """
        if self.callbacks["on_ping"] is not None:
            ping_data = line.split(':')[1]
            self.callbacks["on_ping"](ping_data)
        return None

    def call_cb_kick(self, line):
        """
        Call the on_kick callback function, if set
        """
        if self.callbacks["on_kick"] is not None:
            kicker = line.split('!')[0][1:]
            kicked = line.split(' ')[3]
            reason = ' '.join(line.split(' ')[4:])[1:]

            self.callbacks["on_kick"](kicker, kicked, reason)
        return None

    def call_cb_part(self, line):
        """
        Call the on_part callback function, if set
        """
        if self.callbacks["on_part"] is not None:
            user = line.split('!')[0][1:]
            reason = ' '.join(line.split(' ')[3:])[1:]

            self.callbacks["on_part"](user, reason)
        return None

    def call_cb_join(self, line):
        """
        Call the on_join callback function, if set
        """
        if self.callbacks["on_join"] is not None:

            user = line.split('!')[0][1:]

            self.callbacks["on_join"](user)
        return None

    def call_cb_nick(self, line):
        """
        Call the on_nick callback function, if set
        """
        if self.callbacks["on_nick"] is not None:
            prev_nick = line.split('!')[0][1:]
            new_nick = ' '.join(line.split(' ')[2:])[1:]

            self.callbacks["on_nick"](prev_nick, new_nick)
        return None

    def call_cb_mode(self, line):
        """
        Call the on_mode callback function, if set
        """
        if self.callbacks["on_mode"] is not None:
            if len(line.split(' ')) == 4:
                target = self.channel
            else:
                target = line.split(' ')[-1]
            by = line.split('!')[0][1:]
            mode = line.split(' ')[3]

            self.callbacks["on_mode"](mode, by, target)
        return None

    def call_cb_welcome(self, line):
        """
        Call the on_welcome callback function, if set
        """
        if self.callbacks["on_welcome"] is not None:
            host = line.split(' ')[0][1:]
            welcome_msg = ''.join(line.split(':')[2:])

            self.callbacks["on_welcome"](host, welcome_msg)
        return None

    def call_cb_namereply(self, line):
        """
        Call the on_namereply callback function, if set
        """
        if self.callbacks["on_namereply"] is not None:
            # user list with prefixes on nicks (@, +)
            user_list = line.split(':')[2:][0].split(' ')

            self.callbacks["on_namereply"](user_list)
        return None

    def call_cb_nicknameinuse(self, line):
        """
        Call the on_nicknameinuse callback function, if set
        """
        if self.callbacks["on_nicknameinuse"] is not None:
            self.callbacks["on_nicknameinuse"](self.nick)
        return None

    def call_cb_timeout(self, line):
        """
        Call the on_timeout callback function, if set
        """
        if self.callbacks["on_timeout"] is not None:
            self.callbacks["on_timeout"]()
        return None

    def connect(self):
        """
        Connect to the IRC server
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
        self.sock.connect((self.host, self.port))
        self._send("NICK " + self.nick)
        self._send("USER %s 0 * :%s" % (self.nick, self.nick))
        return None

    def disconnect(self, msg="Bye."):
        """
        Close the connection to the server
        """
        self._send("QUIT :%s" %(msg))
        return None

    def join(self):
        """
        Join a channel once connected
        """
        self._send("JOIN " + self.channel)
        return None

    def part(self, msg="Bye."):
        """
        Leave the current channel
        """
        self._send("PART %s :%s" %(self.channel, msg))
        return None

    def mode(self, target, command):
        """
        Set a mode for a specified target
        """
        self._send("MODE %s %s" % (target, command))
        return None

    def privmsg(self, target, msg):
        """
        Send a PRIVMSG message
        """
        self._send('PRIVMSG %s :%s' % (target, msg))
        return None

    def _send(self, data):
        """
        sock.send wrapper for the IRC protocol
        for internal use
        """
        self.sock.send(data+'\r\n')
        return None

    def _data_dispatcher(self):
        """
        Dispatch incomming data
        """
        last_chunk = ''

        while not IRC_STOP:
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
                    continue

                if self.callbacks["all"] is not None:
                    if self.callbacks["all"](line) == DATA_PROCESSED:
                        continue

                if re.search(" PRIVMSG ", line):
                    self.call_cb_privmsg(line)

                    # Reply back to the server
                elif re.search("^PING :", line):
                    self.call_cb_ping(line)

                elif re.search(" KICK ", line):
                    self.call_cb_kick(line)

                elif re.search(" PART ", line):
                    self.call_cb_part(line)

                elif re.search(" JOIN ", line):
                    self.call_cb_join(line)

                elif re.search(" NICK ", line):
                    self.call_cb_nick(line)

                elif re.search(" MODE ", line):
                    self.call_cb_mode(line)

                elif re.search(' '+RPL_WELCOME+' '+self.nick+' ', line):
                    self.call_cb_welcome(line)

                elif re.search(' '+RPL_NAMEREPLY+' '+self.nick+' ', line):
                    self.call_cb_namereply(line)

                elif re.search(' '+ERR_NICKNAMEINUSE+' ', line):
                    self.call_cb_nicknameinuse(line)

                elif re.search("ERROR :Closing Link: "+self.nick+" by .* \(Ping timeout\)", line):
                    self.call_cb_timeout(line)
