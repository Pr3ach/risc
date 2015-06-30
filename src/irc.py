# -*- coding: utf-8 -*-

import socket

class Irc():
    def __init__(self, host, port=6667, channel, nick):
        self.host = host
        self.port = port
        self.channel = channel
        self.nick = nick
        self.debug_mode = 0

    def _send(self, data):
        """
        sock.send wrapper for the IRC protocol
        for internal use
        """
        self.sock.send(data+'\r\n')
        return None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
        self.sock.connect((self.host, self.port))
        self._send("NICK " + self.nick)
        self._send("USER %s 0 * :%s" % (self.nick, self.nick))
        return None

    def join(self):
        """
        Join a channel once connected
        """
        self._send("JOIN " + self.channel)
        return None

    def part(self, message="Be right back"):
        """
        Leave the current channel
        """
        self._send("QUIT :%s" %(message))
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

    def event_dispatcher(self):
        """
        Main and general event dispatcher
        """
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
                    self.debug.debug(line)

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

                elif re.search(' '+RPL_WELCOME+' '+self.nick+' ', line):
                    self.on_welcome()

                elif re.search(' '+RPL_NAMEREPLY+' '+self.nick+' ', line):
                    self.on_namereply(line)

                elif re.search(' '+ERR_NICKNAMEINUSE+' ', line):
                    self.on_nicknameinuse(line)

                elif re.search("ERROR :Closing Link: "+self.nick+" by .* \(Ping timeout\)", line):
                    self.on_timeout(line)
