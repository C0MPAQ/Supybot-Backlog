###
# Copyright (c) 2002-2121, 1337 C0MPAQ
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE. FUCK PYTHON.
###

import os
import time
import copy

from time import gmtime, strftime

import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
import supybot.ircdb as ircdb
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.utils.structures import TimeoutQueue
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('Backlog')

filename = conf.supybot.directories.data.dirize('Backlog.db')

class Arrrr(object):
    def __init__(self, numba):
        self.numba = numba
        self.items = []

    def push(self, item):
        self.items.append(item)
        if len(self.items) > self.numba:
            # memory management, python style
            self.items = self.items[1:]

    def shift(self):
        if len(self.items) <= 0:
            return False
        # Yesshh
        retval = self.items[:1]
        self.items = self.items[1:]
        return retval.pop()

class Dick(object):
    def __init__(self, numba):
        self.items = {}
        self.numba = numba+5
    def push(self, key, value):
        if not key in self.items:
            self.items[key] = Arrrr(self.numba)
        self.items[key].push(value)
    def get(self, key):
        if not key in self.items:
            self.items[key] = Arrrr(self.numba)
        # I don't even know if I need this!
        return copy.deepcopy(self.items[key])
    
class BacklogDB(plugins.ChannelUserDB):
    def serialize(self, v):
        return [v]

    def deserialize(self, channel, id, L):
        if len(L) != 1:
            raise ValueError
        return L[0]


class Backlog(callbacks.Plugin):
    """This plugin will private message backlogs of X lines to users who join a
        channel."""
    def __init__(self, irc):
        self.__parent = super(Backlog, self)
        self.__parent.__init__(irc)
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write('')
                f.close()
        self.db = BacklogDB(filename)
        world.flushers.append(self.db.flush)
        self.lastParts = plugins.ChannelUserDictionary()
        splitTimeout = conf.supybot.plugins.Backlog.throttle.afterSplit
        self.splitters = TimeoutQueue(splitTimeout)
        self.lastBacklog = plugins.ChannelUserDictionary()

        self.logck = Dick(int(self.registryValue('maxlines')))

    def die(self):
        if self.db.flush in world.flushers:
            world.flushers.remove(self.db.flush)
        self.db.close()
        self.__parent.die()

#    def doQuit(self, irc, msg):
#        # Netsplit measure
#        if ircmsgs.isSplit(msg):
#            self.splitters.enqueue(msg.nick)
#            try:
#                id = ircdb.users.getUserId(msg.prefix)
#                self.splitters.enqueue(id)
#            except KeyError:
#                pass
#

    def doJoin(self, irc, msg):
        channel = msg.args[0]
        if self.registryValue('enabled', channel):
            if not ircutils.strEqual(irc.nick, msg.nick):
        #        if msg.nick in self.splitters:
        #            self.log.debug('Not messaging %s, recent split.', msg.nick)
        #            return # Recently split.
                irc = callbacks.SimpleProxy(irc, msg)

                id = msg.nick

                now = time.time()
                throttle = self.registryValue('throttle', channel)
                if now - self.lastBacklog.get((channel, id), 0) > throttle:
                    if (channel, id) in self.lastParts:
                       i = self.registryValue('throttle.afterPart', channel)
                       if now - self.lastParts[channel, id] < i:
                           return
                self.lastBacklog[channel, id] = now
                
                try:    
                    lines = int(self.db["1337allthechannels1337", id])
                except:
                    lines = int(self.registryValue('lines'))
                    
                if lines != 0:
                    irc.queueMsg(ircmsgs.privmsg(msg.nick, "Hello "+msg.nick+". I will now show you up to "+str(lines)+" messages from "+channel+", before you joined. To change this behavior, write me: @setbackloglines [0-25]. Setting it to zero disables this feature. Time is GMT."))
                    logg = self.logck.get(channel)
                    for i in range(1, lines):
                        msgg = logg.shift()
                        if msgg == False: 
                            break;
                        else:
                            irc.queueMsg(ircmsgs.privmsg(msg.nick, str(msgg)))

            self.doLog(irc, channel, '*** %s <%s> has joined %s', msg.nick, msg.prefix, channel)

    def doLog(self, irc, channel, s, *args):
        if not self.registryValue('enabled', channel):
            return
        self.logck.push(channel, strftime("%H:%M:%S", gmtime())+" "+str(format(s, *args)))

    def doNotice(self, irc, msg):
        (recipients, text) = msg.args
        for channel in recipients.split(','):
            if irc.isChannel(channel):
                self.doLog(irc, channel, '-%s- %s', msg.nick, text)

    def doNick(self, irc, msg):
        oldNick = msg.nick
        newNick = msg.args[0]
        for (channel, c) in irc.state.channels.iteritems():
            if newNick in c.users:
                self.doLog(irc, channel,
                           '*** %s is now known as %s', oldNick, newNick)

    def doPrivmsg(self, irc, msg):
        (recipients, text) = msg.args
        for channel in recipients.split(','):
            if irc.isChannel(channel):
                nick = msg.nick or irc.nick
                if ircmsgs.isAction(msg):
                    self.doLog(irc, channel,
                               '* %s %s', nick, ircmsgs.unAction(msg))
                else:
                    self.doLog(irc, channel, '<%s> %s', nick, text)

    def doKick(self, irc, msg):
        if len(msg.args) == 3:
            (channel, target, kickmsg) = msg.args
        else:
            (channel, target) = msg.args
            kickmsg = ''
        if kickmsg:
            self.doLog(irc, channel,
                       '*** %s was kicked by %s (%s)',
                       target, msg.nick, kickmsg)
        else:
            self.doLog(irc, channel,
                       '*** %s was kicked by %s', target, msg.nick)

    def doTopic(self, irc, msg):
        if len(msg.args) == 1:
            return # It's an empty TOPIC just to get the current topic.
        channel = msg.args[0]
        self.doLog(irc, channel,
                   '*** %s changes topic to "%s"', msg.nick, msg.args[1])

    def doPart(self, irc, msg):
        for channel in msg.args[0].split(','):
            self.doLog(irc, channel,
                       '*** %s <%s> has left %s',
                       msg.nick, msg.prefix, channel)

    def doQuit(self, irc, msg):
        if not isinstance(irc, irclib.Irc):
            irc = irc.getRealIrc()
        for (channel, chan) in self.lastStates[irc].channels.iteritems():
            if msg.nick in chan.users:
                self.doLog(irc, channel,
                           '*** %s <%s> has quit IRC\n',
                           msg.nick, msg.prefix)

    def outFilter(self, irc, msg):
        # Gotta catch my own messages *somehow* :)
        # Let's try this little trick...
        if msg.command in ('PRIVMSG', 'NOTICE'):
            # Other messages should be sent back to us.
            m = ircmsgs.IrcMsg(msg=msg, prefix=irc.prefix)
            self(irc, m)
        return msg

    @internationalizeDocstring
    def setbackloglines(self, irc, msg, args, lines):
        """<number of lines 0-100>

        Sets how many lines of backlog are returned to you upon join
        """
        try:
            line = int(lines)
            if line >= 0 and line < self.registryValue('maxlines')+1:
#                irc.reply("Will now private-message you "+str(line)+" lines of backlog on join.", prefixNick=True)
                id = msg.nick
                self.db["1337allthechannels1337", id] = line
                irc.replySuccess()
            else: 
                raise ZeroDivisionError('')
        except ValueError:
                irc.error(lines+" is not an integer", prefixNick=True)
        except ZeroDivisionError:
                irc.error(lines+" is not within 0-"+str(self.registryValue('maxlines')), prefixNick=True)
            
    setbackloglines = wrap(setbackloglines, ['text'])

Class = Backlog

# vim:set shiftwidth=4 softtabstop=4  tabstop=4 expandtab textwidth=79:
