OrientExpress for Kodi
==========
Script for controlling some of the options provided by the ExpressVPN command line tool, from within Kodi. As such, this tool is merely a graphical interface for using that command line tool, it is not a replacement or addon.

Not all options of the command line tool are available through this Kodi addon, just some basic use cases are provided.

Note that this tool is in no way affiliated with, or endorsed by, ExpressVPN ([https://www.expressvpn.com/])

The geolocation code is provided by the upstream code (OpenVPN for Kodi)

This code is currently more of a quick hack of the original OpenVPN code, so there is plenty of room for improvements if you feel so inclined.

Most of the code is probably copryrighted by the upstream author. The only file in this tool that is written more or less from scratch is resources/lib/orientexpress.py but even that file is heavily inspired by the original file resources/lib/openvpn.py

The logo comes from a website with rights-free images (forgot which one: contact me if you feel that this is an error)

Features
-----
- Start and stop ExpressVPN from with Kodi.
- Select VPN server (exit point)
- Display current geo-location.

Screenshots
-----
For now, please use your own imagination...

Prerequisites
------
This addon is merely a graphical interface for the ExpressVPN unix command line tool, so first visit the ExpressVPN website ([https://www.expressvpn.com/]) to download the installer of the command line tool for your operating system. Next install and configure the tool on the system where you run Kodi: verify that you have a working ExpressVPN tunnel before using this addon.

Installation
------
The quickest way is to download this repository as a ZIP file, then install the addon from that ZIP. See [http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file][1] for more details on installing addons from zip file. Just be sure that the ZIP file contains the directory script.orientexpress in its root (Kodi expects all files below directory "script." + the name of the Kodi addon)

If you want to create your own ZIP file, run shell script package_zip.sh from within the root directory of this repo. No special software is required: just a working bash and zip command line tool. As the addon is written in Python, there is nothing to compile or build.

Usage
------

The tool is rather self-explanatory. The following functions are available:

**Show the current VPN IP configuration (same functionality as the OpenVPN parent tool)

**Show a list of available VPN endpoints (exit servers)

**Connect to a specific endpoint

**Disconnect from VPN

**Connect to the last active VPN endpoint

For any other manipulation of the ExpressVPN setup, please use SSH to connect to your Kodi box and use the expressvpn command line tool.

Settings
--------
For now no configurable settings are implemented.

FAQ
---

**Is this plugin available in a Kodi addons repository?** No

**I can't get the OrientExpress plugin to work on Raspberry Pi?** Before asking me for help I suggest reading the following [guide][3].

License
------
OrientExpress is a fork of OpenVPN for Kodi.

OpenVPN for Kodi is licensed under the [GPL 3.0 license][2].

[1]: http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file
[2]: http://www.gnu.org/licenses/gpl-3.0.html
[3]: http://forums.tvaddons.ag/threads/24769-How-to-set-up-your-VPN-on-raspberry-pi-using-Brain-Hornsby-Openvpn-for-XBMC
