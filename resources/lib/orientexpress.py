# /*
# *
# * OrientExpress for Kodi.
# *
# * Glue code to use the external expressvpn command line tool from
# * within Kodi.
# *
# * For now error handling is almost non-existant.
# */

import os
import re
import sys
import subprocess
import time
import socket

#
# Hardcoded for now (works on OSMC)
#
# TODO: get these values from settings
#
EXPRESSVPN_CMD = "/usr/bin/expressvpn"


def do_vpn_command(prog, args):
    """
    Execute ExpressVPN command with specified arguments. 
    """
    command = [prog] + args
    p = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate()
    return stdout.decode()


def is_running():
    """
    See if the ExpressVPN tunnel is up or not. If up, return the full name of the exit server.
    """
    try:
        data = do_vpn_command(EXPRESSVPN_CMD, ["status"])
        regex = r"Connected to +(.*)\n"
        res = re.search(regex, data, re.MULTILINE)
        if res:
            return res.group(1)
        else:
            return False
    except Exception:
        raise ExpressvpnError(3, "Unable to get Expressvpn status")


def disconnect():
    """
    Take down ExpressVPN tunnel. If success, return True.
    """
    try:
        data = do_vpn_command(EXPRESSVPN_CMD, ["disconnect"])
        regex = r"Disconnected."
        res = re.search(regex, data, re.MULTILINE)
        if res:
            return True
        else:
            return False
    except Exception:
        raise ExpressvpnError(3, "Unable to disconnect Expressvpn")


def connect():
    """
    Create ExpressVPN tunnel. If success, return the full name of the exit server.
    """
    try:
        data = do_vpn_command(EXPRESSVPN_CMD, ["connect"])
        regex = r"Connected to +(.*)\n"
        res = re.search(regex, data, re.MULTILINE)
        if res:
            return res.group(1)
        else:
            return False
    except Exception:
        raise ExpressvpnError(3, "Unable to connect Expressvpn")


def connect_specific(exit_node):
    """
    Create ExpressVPN tunnel. If success, return the full name of the exit server.
    """
    try:
        data = do_vpn_command(EXPRESSVPN_CMD, ["connect", exit_node])
        regex = r"Connected to +(.*)\n"
        res = re.search(regex, data, re.MULTILINE)
        if res:
            return res.group(1)
        else:
            return False
    except Exception:
        raise ExpressvpnError(3, "Unable to connect Expressvpn")


class ExitNode:
    def __init__(self, alias, country, location, recommended):
        self.alias = alias
        self.country = country
        self.location = location
        self.recommended = recommended

    def to_kodi(self):
        if self.recommended:
            return self.alias + " -- " + self.location + " (Recommended)"
        else:
            return self.alias + " -- " + self.location


def list_all_exitnodes():
    """
    Return array with all available exit nodes to choose from.
    """
    try:
        data = do_vpn_command(EXPRESSVPN_CMD, ["list", "all"])
        regex = r"(ALIAS\s+COUNTRY\s+LOCATION\s+RECOMMENDED.*)"
        res = re.search(regex, data, re.MULTILINE | re.DOTALL)
        if res:
            #
            # Parsing is rather rigorous as country and location fields can
            # contain whitespace
            #
            lines = res.group().split("\n")
            titles = lines.pop(0)
            ofs_alias = titles.index("ALIAS")
            ofs_country = titles.index("COUNTRY")
            ofs_location = titles.index("LOCATION")
            ofs_recommended = titles.index("RECOMMENDED")
            #
            # Remove underline chars
            #
            line = lines.pop(0)
            #
            # Now parse the rest of the output...
            #
            nodes = []
            for line in lines:
                if len(line.strip()) <= 0:
                    continue
                raw_alias = line[ofs_alias:ofs_country]
                raw_country = line[ofs_country:ofs_location]
                raw_location = line[ofs_location:ofs_recommended]
                if len(line) >= ofs_recommended:
                    raw_recommended = line[ofs_recommended : ofs_recommended + 1]
                else:
                    raw_recommended = "N"
                nodes.append(
                    ExitNode(
                        raw_alias.strip(),
                        raw_country.strip(),
                        raw_location.strip(),
                        (raw_recommended == "Y"),
                    )
                )
            return nodes
        else:
            return False
    except Exception:
        raise ExpressvpnError(3, "Unable to obtain Expressvpn exit nodes")


def get_all_exitnodes_for_display():
    nodes = list_all_exitnodes()
    lines = []
    for node in nodes:
        lines.append(node.to_kodi())
    return lines


class ExpressvpnError(Exception):
    def __init__(self, errno, string):
        self.errno = errno
        self.string = string

    def __str__(self):
        return "[%d]: %s" % (self.errno, self.string)
