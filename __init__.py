###
# Copyright (c) 2002-2121, 1337 C0MPAQ
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

"""
Backlog: Displays last X lines of chat to new users on query
"""

import supybot
import supybot.world as world

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = ""

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.authors.unknown

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = ''

from . import config
from . import plugin
from imp import reload
# In case we're being reloaded.
reload(config)
reload(plugin)
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
