# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# CHANGELOG
#
# 01/08/2014 - 1.0 - Pr3acher
# * init 
# 03/08/2014 - 1.1 - Pr3acher
# * fix color for '/' in evt_game_map_change
# * added event notification for kick / ban / tban / map change
# * bug fix: get_last_calladmin
# * added possibility to skip calladmin threshold
# * minor bug fixes
# * added chat ability (game to IRC) 
# * set b3 name in config file
# 08/12/2014 - 1.2 - Pr3acher
# * Disable calladmin cmd when client count is < ini_var 
# 08/18/2014 - 1.2.1 - Pr3acher
# * Slightly updated for risc v1.4.4
# 09/07/2014 - 1.2.2 - Pr3acher
# * add possibility to set/get Cvar (TODO)
# * handle wrong settings using defaults (TODO)

import b3
import b3.events
import b3.plugin
import time
import MySQLdb as mysql
import threading

__author__ = 'Pr3acher'
__version__ = '1.2.2'


class Riscb3Plugin(b3.plugin.Plugin):
    requiresConfigFile = True

    def onLoadConfig(self):
        """
        Load settings from config file
        """
        try:
            self.calladmin_threshold = int(self.config.get('calladmin','threshold'))
            self.db_host = self.config.get('db','host')
            self.db_user = self.config.get('db','user')
            self.db_passwd = self.config.get('db','passwd')
            self.db_name = self.config.get('db','name')
            self.db_table = 'risc_'+(self.config.get('riscb3','server_name'))
            self.calladmin_level = int(self.config.get('calladmin','level'))
            self.calladmin_bypass_level = int(self.config.get('calladmin','bypassthresholdlevel'))
            self.calladmin_min_players = int(self.config.get('calladmin','minplayers'))
            self.b3_name = self.config.get('b3','name')
        except Exception, e:
            self.error('onLoadConfig: Error while loading config - Make sure all options are set and using a proper type: %s' % e)
        return None

    # <user> <msg>
    def on_ichat(self, ID, data):
        """
        (Internal) - Handle incomming IRC messages: send them over UrT and set the msg state to processed
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()
        cur.execute("""UPDATE %s SET processed = 1 WHERE ID = %d""" % (self.db_table, ID))
        con.commit()
        con.close()

        data_list = data.split('\r\n')
        user = data_list[0]
        msg = data_list[1]

        self.console.say('[IRC.'+user+']: '+msg)
        return None

    def set_cvar(self, ID, data):
        """
        Set a Cvar value
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()
        cur.execute("""UPDATE %s SET processed = 1 WHERE ID = %d""" % (self.db_table, ID))
        con.commit()
        con.close()

        data_list = data.split('\r\n')
        cvar, value = data_list[0], data_list[1]

        self.console.setCvar(cvar, value)
        return None

    def irc_watcher(self):
        """
        (Internal) - Main IRC event watcher & dispatcher thread
        """
        try:
            while 1:
                time.sleep(0.5)

                con = mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
                cur = con.cursor()
                cur.execute("""SELECT ID,evt,data FROM %s WHERE processed = 0""" % (self.db_table))
                query = cur.fetchall()
                con.close()

                if len(query) >= 1:
                    for row in query:
                        if row[1] == 'EVT_ICHAT' and self.chat_state():
                            self.on_ichat(row[0], row[2])
                        elif row[1] == 'EVT_CVAR_SET':
                            # data: <cvar> <value>
                            self.debug('type '+str(type(row[0])))
                            self.set_cvar(row[0], row[2])
                        else:
                            pass
        except Exception, e:
            self.error('irc_watcher: Caught exception: %s - Passing' %e )
            pass

    def onStartup(self):
        """
        Called on startup to register our cmd's and events
        """
        self.admin_plugin = self.console.getPlugin('admin')

        # start our main IRC event watcher thread
        th = threading.Thread(None,self.irc_watcher,None,(),None)
        th.daemon = True
        th.start()

        try:
            con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS %s(ID INT AUTO_INCREMENT PRIMARY KEY,\
                                                   evt VARCHAR(40) NOT NULL DEFAULT '',\
                                                   data VARCHAR(255) NOT NULL DEFAULT '',\
                                                   time BIGINT NOT NULL DEFAULT 0,\
                                                   processed TINYINT NOT NULL DEFAULT 0)""" % (self.db_table))
            con.commit()
            con.close()

        except Exception, e:
            self.error('onStartup: There was an error initializing plugin: %s' %e)
            if con:
                con.rollback()
                con.close()
            return None

        if not self.admin_plugin:
            self.error("Couldn't load admin plugin.")
            return None
        self.admin_plugin.registerCommand(self,"calladmin",self.calladmin_level,self.cmd_calladmin)

        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)
        self.registerEvent(b3.events.EVT_CLIENT_KICK)
        self.registerEvent(b3.events.EVT_CLIENT_BAN_TEMP)
        self.registerEvent(b3.events.EVT_CLIENT_BAN)
        self.registerEvent(b3.events.EVT_CLIENT_SAY)
        self.registerEvent(b3.events.EVT_CLIENT_TEAM_SAY)
        return None

    def _store_event(self,evt,data,t):
        """
        (Internal) - Store the event evt and it's data data into the database
        """
        try:
            con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
            cur = con.cursor()

            cur.execute("""INSERT INTO %s(evt,data,time,processed) VALUES('%s','%s',%d,0)""" % (self.db_table,evt,data,int(t)))

            con.commit()
            con.close()
        except Exception, e:
            self.error('_store_event: Error storing event %s: %s - Passing' % (evt,e))
            if con: 
                con.close()
                pass
        return None

    def _get_last_calladmin(self):
        """
        (Internal) - Returns the last time the calladmin cmd was issued in sec.
        """
        try:
            con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
            cur = con.cursor()

            cur.execute("""SELECT time FROM %s WHERE evt = 'EVT_CALLADMIN' AND ID = (SELECT MAX(ID) FROM %s)""" % (self.db_table,self.db_table))

            res = cur.fetchall()
            con.close()
        except:
            self.error('get_last_calladmin: Error retrieving last calladmin cmd time')
            if con:
                con.close()
            return 0

        if not len(res):
            return 0

        return int(res[0][0])

    def _timetostr(self,t):
        """
        (Internal) - Converts an ammount of time in seconds into a string (minutes & sec only)
        """
        self.debug('t=='+str(t))
        m = int(t / 60)
        s = int(t - (60 * m))

        m_str = 'minute'
        s_str = 'second'

        if m > 1:
            m_str += 's'
        if s > 1:
            s_str += 's'

        if m > 0:
            return str(m)+' '+m_str+' '+str(s)+' '+s_str
        else:
            return str(s)+' '+s_str

    def cmd_calladmin(self,data,client,cmd=None):
        """
        <reason> - Sends an admin request on the IRC channel
        """
        if len(self.console.clients.getList()) < self.calladmin_min_players:
            client.message('Command disabled: player count too low.')
            return None

        cur_time = int(time.time())
        len_data = len(data)
        last_calladmin = self._get_last_calladmin()

        if ((cur_time - last_calladmin) > self.calladmin_threshold) or client.maxLevel >= self.calladmin_bypass_level:
            if len_data <= 135 and len_data > 1:
                # <client> <reason>
                self._store_event('EVT_CALLADMIN',client.name+'\r\n'+data,cur_time)
                client.message('Admins have been made aware of your request.')
            else:
                client.message('Invalid reason: either no reason specified or too many characters.')
        else:
            client.message('You have to wait another %s before you can call an admin.' % (self._timetostr(self.calladmin_threshold-(cur_time-last_calladmin))))
        return None

    def on_map_change(self,event):
        """
        Called when the map get cycled
        """
        cl_count = len(self.console.clients.getList())
        try:
            max_cl_count = self.console.getCvar("sv_maxclients").getInt()
        except TypeError:
            max_cl_count = 0

        # <map_name> <cl_count> <max_cl_count>
        self._store_event('EVT_GAME_MAP_CHANGE',event.data['new']+'\r\n'+str(cl_count)+'\r\n'+str(max_cl_count),event.time)
        return None

    def on_kick(self,event):
        """
        Called when an admin kicks someone
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()

        # get admin ID and name
        cur.execute("""SELECT clients.name, penalties.admin_id, penalties.client_id  FROM penalties INNER JOIN clients ON \
                    penalties.time_add = %d AND clients.id = penalties.admin_id AND penalties.type = 'Kick'""" % (event.time))

        query = cur.fetchall()
        con.close()

        if len(query) != 1:
            self.debug('on_kick: Something wrong in the query.')
            return None

        if len(query[0]) != 3:
            self.debug('on_kick: Something wrong in the query.')
            return None

        admin, admin_id, client_id = query[0][0], str(query[0][1]), str(query[0][2])
        reason = ''

        if len(event.data) >= 2:
            reason = event.data

        # <admin> <admin_id> <client> <client_id> <reason=''>
        self._store_event('EVT_CLIENT_KICK',admin+'\r\n'+admin_id+'\r\n'+event.client.name+'\r\n'+client_id+'\r\n'+reason,event.time)
        return None

    def on_tempban(self,event):
        """
        Called when an admin ban someone
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()

        # get admin ID and name
        cur.execute("""SELECT clients.name, penalties.admin_id, penalties.client_id, penalties.duration FROM penalties INNER JOIN clients ON \
                    penalties.time_add = %d AND clients.id = penalties.admin_id AND penalties.type = 'TempBan'""" % (event.time))

        query = cur.fetchall()
        con.close()

        if len(query) != 1:
            self.debug('on_tempban: Something wrong in the query.')
            return None

        if len(query[0]) != 4:
            self.debug('on_tempban: Something wrong in the query.')
            return None

        admin, admin_id, client_id, duration = query[0][0], str(query[0][1]), str(query[0][2]), str(query[0][3])
        reason = ''

        if len(event.data['reason']) >= 1:
            reason = event.data['reason']

        # <admin> <admin_id> <client> <client_id> <duration_min> <reason=''>
        self._store_event('EVT_CLIENT_BAN_TEMP',admin+'\r\n'+admin_id+'\r\n'+event.client.name+'\r\n'+client_id+'\r\n'+duration+'\r\n'+reason,event.time)
        return None

    def on_ban(self,event):
        """
        Called when an admin perm-ban someone
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()

        # get admin id and name
        cur.execute("""SELECT clients.name, penalties.admin_id, penalties.client_id  FROM penalties INNER JOIN clients ON \
                    penalties.time_add = %d AND clients.id = penalties.admin_id AND penalties.type = 'Ban'""" % (event.time))

        query = cur.fetchall()
        con.close()

        if len(query) != 1:
            self.debug('on_ban: Something wrong in the query.')
            return None

        if len(query[0]) != 3:
            self.debug('on_ban: Something wrong in the query.')
            return None

        admin, admin_id, client_id = query[0][0], str(query[0][1]), str(query[0][2])
        reason = ''

        if len(event.data['reason']) >= 2:
            reason = event.data['reason']

        # <admin> <admin_id> <client> <client_id> <reason=''>
        self._store_event('EVT_CLIENT_BAN',admin+'\r\n'+admin_id+'\r\n'+event.client.name+'\r\n'+client_id+'\r\n'+reason,event.time)
        return None

    def chat_state(self):
        """
        (Internal) - Returns 1 if chat is enabled for the current server, else returns 0
        """
        con = mysql.connect(self.db_host,self.db_user,self.db_passwd,self.db_name)
        cur = con.cursor()

        cur.execute("""SELECT data FROM %s WHERE ID = (SELECT MAX(ID) FROM %s WHERE evt = 'EVT_CHAT_SET')""" % (self.db_table,self.db_table))
        query = cur.fetchall()
        con.close()

        if len(query) > 1 or not len(query):
            return 0
        return int(query[0][0])

    def onEvent(self,event):
        """
        Handle events here
        """
        try:

            if event.type == b3.events.EVT_GAME_MAP_CHANGE:
                self.on_map_change(event)

            elif event.type == b3.events.EVT_CLIENT_KICK:
                self.on_kick(event)

            elif event.type == b3.events.EVT_CLIENT_BAN_TEMP:
                self.on_tempban(event)

            elif event.type == b3.events.EVT_CLIENT_BAN:
                self.on_ban(event)

            elif (event.type == b3.events.EVT_CLIENT_SAY or event.type == b3.events.EVT_CLIENT_TEAM_SAY) and self.chat_state() and event.client.name != self.b3_name:
                # <client> <msg>
                self._store_event('EVT_CHAT',event.client.name+'\r\n'+event.data,event.time)

            else:
                pass

        except Exception, e:
            self.error('onEvent: Could not handle a registered event: %s - Passing' % e)
            pass
        return None
