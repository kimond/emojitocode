# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Kim Desrosiers <kimdesro@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# (This script requires WeeChat 0.3.0 or higher).
#
# WeeChat script that convert emoticons to their unicode version.
#
#
# Commands:
# /emojitocode - List supported emoticons in the current buffer

SCRIPT_NAME = "emojitocode"
SCRIPT_AUTHOR = "Kim Desrosiers <kimdesro@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Convert emoticons to their unicode version"
SCRIPT_COMMAND = "emojitocode"

import_ok = True

try:
    import weechat
    import re
except ImportError:
    print "This script must be run under WeeChat."
    import_ok = False

ICONS = {
    '^^': u'\U0001F601', '^_^': u'\U0001F601',  # GRINNING FACE WITH SMILING EYES
    ':)': u'\U0001F603', ':-)': u'\U0001F603', '=)': u'\U0001F603',  # SMILING FACE WITH OPEN MOUTH
    ':D': u'\U0001F604', '=D': u'\U0001F604',  # SMILING FACE WITH OPEN MOUTH AND SMILING EYES
    ';)': u'\U0001F609', ';-)': u'\U0001F609',  # WINKING FACE
    ':|': u'\U0001F612', '=|': u'\U0001F612', '>_>': u'\U0001F612', '<_<': u'\U0001F612',  # UNAMUSED FACE
    ':S': u'\U0001F615', ':/': u'\U0001F615', ':\\': u'\U0001F615', '=S': u'\U0001F615', '=/': u'\U0001F615',
    '=\\': u'\U0001F615',  # CONFUSED FACE
    ':P': u'\U0001F61B', ':p': u'\U0001F61B', '=P': u'\U0001F61B', '=p': u'\U0001F61B',  # FACE WITH STUCK-OUT TONGUE
    ';P': u'\U0001F61C', ';-P': u'\U0001F61C',  # FACE WITH STUCK-OUT TONGUE AND WINKING EYE
    ':(': u'\U0001F61E', ':-(': u'\U0001F61E', '=(': u'\U0001F61E', '=-(': u'\U0001F61E',  # DISAPPOINTED FACE
    '>_<': u'\U0001F623',  # PERSEVERING FACE
}

ICON_PATTERN = re.compile(r"(?<!\S)([>;:=8B\^]\S{1,2})")


def icon(match):
    global ICONS
    emoticon = match.group(0)

    if emoticon in ICONS:
        return "%s " % ICONS[emoticon].encode("utf-8")

    return emoticon


def emoji_input_replacer(data, buffer, command):
    global ICON_PATTERN

    input_string = weechat.buffer_get_string(buffer, 'input')
    if re.match('^/set ', input_string):
        return weechat.WEECHAT_RC_OK
    weechat.buffer_set(buffer, 'input', ICON_PATTERN.sub(icon, input_string))
    return weechat.WEECHAT_RC_OK


def list_icons_cb(data, buf, args):
    global ICONS

    l = dict()
    for key, val in ICONS.items():
        if val in l:
            l[val] += ", " + key
        else:
            l[val] = key

    weechat.prnt(buf, "%s - list of supported emoticons:" % SCRIPT_NAME)
    [weechat.prnt(buf, " %s  = %s" % (key.encode("utf-8"), l[key])) for key in l.keys()]

    return weechat.WEECHAT_RC_OK


if __name__ == "__main__" and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        weechat.hook_command_run("/input return", "emoji_input_replacer", "")
        weechat.hook_command(SCRIPT_COMMAND, "List supported emoticons", "", "", "", "list_icons_cb", "")
