#
# OrientExpress for Kodi.
# /*
# *
# * OpenVPN for Kodi.
# *
# * Copyright (C) 2015 Brian Hornsby
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# */

import os
import shutil
import sys
import subprocess
import threading
import time
import urllib2
import xbmc
from BeautifulSoup import BeautifulSoup

import resources.lib.orientexpress as vpn
import resources.lib.kodisettings as settings
import resources.lib.kodiutils as utils

# Set some global values.
_addonid = "script.orientexpress"

# Initialise settings.
_settings = settings.KodiSettings(_addonid, sys.argv)

# Get addon information.
_addonname = _settings.get_name()
_version = _settings.get_version()


def log_debug(msg):
    if _settings["debug"] == "true":
        print "script.orientexpress: DEBUG: %s" % msg


def log_error(msg):
    print "script.orientexpress: ERROR: %s" % msg


log_debug("Addon Id:   [%s]" % (_addonid))
log_debug("Addon Name: [%s]" % (_addonname))
log_debug("Version:    [%s]" % (_version))

# 'enum' of connection states
(disconnected, failed, connecting, disconnecting, connected) = range(5)
_state = disconnected
if vpn.is_running():
    _state = connected

# Get addon settings values.
_userdata = _settings.get_datapath()
_args = _settings["args"]


def get_geolocation():
    try:
        url = "http://api.ipinfodb.com/v3/ip-city/?key=24e822dc48a930d92b04413d1d551ae86e09943a829f971c1c83b7727a16947f&format=xml"
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        return BeautifulSoup(result)
    except:
        return None


def display_location():
    geolocation = get_geolocation()
    if geolocation is not None:
        image = _settings.get_path(
            "%s%s%s"
            % (
                "resources/images/",
                geolocation.response.countrycode.string.lower(),
                ".png",
            )
        )
        utils.notification(
            _addonname,
            _settings.get_string(4000)
            % (
                geolocation.response.ipaddress.string,
                geolocation.response.countryname.string.title(),
            ),
            image=image,
        )


def display_notification(text, subtext=False):
    image = _settings.get_path("icon.png")
    if subtext:
        text = text + ": " + subtext
    utils.notification(_addonname, text, image=image)


def disconnect_orientexpress():
    log_debug("Disconnecting ExpressVPN")
    global _state
    try:
        _state = disconnecting
        response = vpn.is_running()
        if response:
            vpn.disconnect()
        _state = disconnected
        log_debug("Disconnect ExpressVPN successful")
    except vpn.ExpressvpnError as exception:
        utils.ok(
            _settings.get_string(3002), _settings.get_string(3011), exception.string
        )
        _state = failed


def connect_orientexpress():
    log_debug("Connecting Expressvpn")
    global _state

    try:
        if vpn.is_running():
            vpn.disconnect()
            _state = disconnected
        res = vpn.connect()
        display_notification(_settings.get_string(4002) % res)
        _state = connected
    except vpn.ExpressvpnError as exception:
        if exception.errno == 1:
            _state = connected
            if utils.yesno(
                _settings.get_string(3002),
                _settings.get_string(3009),
                _settings.get_string(3010),
            ):
                log_debug("User has decided to restart Expressvpn")
                connect_orientexpress()
            else:
                log_debug("User has decided not to restart Expressvpn")
        else:
            utils.ok(
                _settings.get_string(3002), _settings.get_string(3011), exception.string
            )
            _state = failed


def select_exit_node():
    list = vpn.get_all_exitnodes_for_display()
    choice = utils.select(_settings.get_string(3000), list)
    if choice >= 0:
        node = list[choice]
        log_debug("Select: [%s]" % node)
        idx = node.index(" ")
        alias = node[0:idx]
        if vpn.is_running():
            vpn.disconnect()
        vpn.connect_specific(alias)
        display_location()


if __name__ == "__main__":
    if _settings.get_argc() != 1:
        if _settings.get_argv(1) == "select":
            select_exit_node()
        elif _settings.get_argv(1) == "connect":
            connect_expressvpn()
        elif _settings.get_argv(1) == "location":
            display_location()
        elif _settings.get_argv(1) == "disconnect":
            disconnect_expressvpn()
        else:
            select_exit_node()
    else:
        select_exit_node()
