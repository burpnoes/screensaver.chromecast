#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 smuto ()
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#



import xbmcaddon
import xbmcgui
import xbmc



addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('id')
addon_path = addon.getAddonInfo('path')

addon_music = addon.getSetting('music')
addon_datetime = addon.getSetting('datetime')

class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def _set_prop(self, name, value):
        self.winid.setProperty('slideview.%s' % name, value)
        self.log('slideview.' + name + ' = ' + value)

    def _clear_prop(self, name):
        self.winid.clearProperty('slideview.%s' % name)
        self.log('clear slideview.' + name)

    def onInit(self):
        self.abort_requested = False
        self.started = False
        self.exit_monitor = self.ExitMonitor(self.exit)
        self.winid = xbmcgui.Window(xbmcgui.getCurrentWindowDialogId())
        if addon_music == 'true':
            self._set_prop('music', 'show')
        if addon_datetime == 'true':
            self._set_prop('datetime', 'show')

    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        self._clear_prop('music')
        self._clear_prop('datetime')
        self.log('exit')
        self.close()

    def log(self, msg):
        xbmc.log(u'Chromecast Screensaver: %s' % msg)


if __name__ == '__main__':
    screensaver = Screensaver(
        'script-%s-main.xml' % addon_name,
        addon_path,
        'default',
    )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()
