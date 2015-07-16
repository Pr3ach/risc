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
__version__ = "1.2"

import socket
import re

GAMETYPES = {1: "LMS",
             2: "FFA",
             3: "TDM",
             4: "TS",
             5: "FTL",
             6: "CNH",
             7: "CTF",
             8: "BM",
             9: "JUMP",
             10: "FT"}

class Ioq3():
    """
    Get info about a game server running an IoQ3 engine
    """
    def __init__(self, ip, port, name="server"):
        if re.match('^([0-9]{1,3}\.){3}[0-9]{1,3}$', ip) is None:
            raise Exception('Invalid IP address')

        self.ip = ip
        self.port = port
        self.name = name
        self.cl_pings = []

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((ip, port))
            self.sock.settimeout(2)
        except Exception, e:
            if self.sock:
                self.sock.close()
            raise Exception("Couldn't connect to the given server: '%s'" % e)

        if not self.getstatus():
            if self.sock:
                self.sock.close()
            raise Exception("getstatus failed")

        if not self.getinfo():
            if self.sock:
                self.sock.close()
            raise Exception("getinfo failed")

        if self.sock:
            self.sock.close()

    def list_clean(self, l):
        """
        Clean a list after a split
        """
        ret = []
        for e in l:
            if e != "" and e != ' ':
                ret.append(e)
        return ret

    def clean_color_string(self, s):
        return re.sub('\^.', '', s)

    def get_client_list(self, raw):
        """
        Return the player list and set the ping list
        """
        cl = re.findall('".+', raw[-1])         # Find nicks, which are surrounded by "
        if not cl:
            return -1                           # No players
        for i in range(len(cl)):
            cl[i] = self.clean_color_string(cl[i])[1:][:-1]

        # Retrieve pings in the same order of players
        pings = re.findall('\\n[0-9]{1,3}\s[0-9]{1,3}\s', raw[-1])
        if len(pings) > 0:
            for i in range(len(pings)):
                pings[i] = pings[i].split(' ')[1]
            self.cl_pings = pings
        return cl

    def get_var(self, l, var):
        """
        Return the content of the requested cvar if available in the buffer, otherwise return -1
        """
        for i in range(len(l)):
            if l[i] == var:
                return l[i+1]
        return -1

    def getstatus(self):
        try:
            self.sock.send(b'\xff'*4+b'getstatus')
            raw_status = str(self.sock.recv(4096))
            list_status = self.list_clean(raw_status.split('\\'))
        except Exception, e:
            return 0
        self.allowvote = self.get_var(list_status, 'g_allowvote')
        self.version = self.clean_color_string(self.get_var(list_status, 'version'))
        self.gametype = self.get_var(list_status, 'g_gametype')
        self.nextmap = self.clean_color_string(self.get_var(list_status, 'g_NextMap'))
        self.cl_list = self.get_client_list(list_status)
        self.hostname = self.clean_color_string(self.get_var(list_status, 'sv_hostname'))
        return 1

    def getinfo(self):
        try:
            self.sock.send(b'\xff'*4+b'getinfo')
            raw_info = str(self.sock.recv(2048))
            list_info = self.list_clean(raw_info.split('\\'))
        except Exception, e:
            return 0
        self.clients = self.get_var(list_info, 'clients')
        self.auth = self.get_var(list_info, 'auth_notoriety')
        self.max_clients = self.get_var(list_info, "sv_maxclients")
        self.map = self.clean_color_string(self.get_var(list_info, 'mapname'))
        return 1

    def gametype2str(self, gametype):
        """
        Return a gametype string from gametype id
        """
        if gametype in GAMETYPES:
            return GAMETYPES[gametype]
        return ""
