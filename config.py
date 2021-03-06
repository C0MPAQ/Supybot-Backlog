###
# Copyright (c) 2002-2005, Jeremiah Fincher
# All rights reserved.
# Copyright (c) 2015-2121, 1337 C0MPAQ
# GPLv3 license http://www.gnu.org/licenses/gpl-3.0.html
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
#  * g o a t s e x * g o a t s e x * g o a t s e x *
#  g                                               g  
#  o /     \             \            /    \       o
#  a|       |             \          |      |      a
#  t|       `.             |         |       :     t
#  s`        |             |        \|       |     s
#  e \       | /       /  \\\   --__ \\       :    e
#  x  \      \/   _--~~          ~--__| \     |    x  
#  *   \      \_-~                    ~-_\    |    *
#  g    \_     \        _.--------.______\|   |    g
#  o      \     \______// _ ___ _ (_(__>  \   |    o
#  a       \   .  C ___)  ______ (_(____>  |  /    a
#  t       /\ |   C ____)/      \ (_____>  |_/     t
#  s      / /\|   C_____) GPLv3 |  (___>   /  \    s
#  e     |   (   _C_____)\______/  // _/ /     \   e
#  x     |    \  |__   \\_________// (__/       |  x
#  *    | \    \____)   `----   --'             |  *
#  g    |  \_          ___\       /_          _/ | g
#  o   |              /    |     |  \            | o
#  a   |             |    /       \  \           | a
#  t   |          / /    |         |  \           |t
#  s   |         / /      \__/\___/    |          |s
#  e  |           /        |    |       |         |e
#  x  |          |         |    |       |         |x
#  * g o a t s e x * g o a t s e x * g o a t s e x *
#  
#   * You may NOT remove this disclaimer, it is part of the license agreement
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
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Backlog')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Backlog', True)


Backlog = conf.registerPlugin('Backlog')

conf.registerChannelValue(Backlog, 'enabled',
    registry.Boolean(True, _("""Determines whether the plugin is active in the
    channel""")))
conf.registerChannelValue(Backlog, 'lines',
    registry.PositiveInteger(10, _("""How many lines of backlog to paste to
    users.""")))
conf.registerGlobalValue(Backlog, 'maxlines',
    registry.PositiveInteger(25, _("""Maximum number of lines that can be
    backlogged.""")))

conf.registerChannelValue(Backlog, 'throttle',
    registry.PositiveInteger(10, _("""Determines the minimum number of seconds
    between messaging backlogs.""")))

# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Backlog, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
