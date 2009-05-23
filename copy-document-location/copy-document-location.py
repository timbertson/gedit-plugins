# -*- coding: utf8 -*
#
#  Gedit plugin to copy the location of the current file to the clipboard.

# Copyright (C) 2009 Tim Cuthbertson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os 
import os.path

import gedit
import gtk
import gconf
import urllib2


COPY_DOCUMENT_LOCATION_UI = """
<ui>
  <menubar name="MenuBar">
    <menu name="FileMenu" action="File">
      <placeholder name="FileOps_2">
        <menuitem name="Copy document location" action="CopyDocumentLocation"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""


class CopyDocumentLocationPlugin(gedit.Plugin):

	def __init__(self):
		gedit.Plugin.__init__(self)
		self.conf_client = gconf.client_get_default()

	def copy_location_cb(self, window):
		active_doc = window.get_active_document()
		document_uri = active_doc.get_uri()
		if document_uri is None:
			return
		document_path = urllib2.unquote(document_uri.replace("file://", ""))
		gtk.Clipboard().set_text(document_path)

	def activate(self, window):	
		action = ("CopyDocumentLocation",
		          None,
		          "_Copy Document Location",
		          "<Shift><Control>c",
		          "Copy Document Location",
		          lambda x, y: self.copy_location_cb(y))
		
		action_group = gtk.ActionGroup("CopyDocumentLocationPluginActions")
		action_group.add_actions([action], window)
		
		ui_manager = window.get_ui_manager()
		ui_manager.insert_action_group(action_group, 0)
		ui_id = ui_manager.add_ui_from_string(COPY_DOCUMENT_LOCATION_UI)
		
		windowdata = dict()
		windowdata["action_group"] = action_group
		windowdata["ui_id"] = ui_id
		
		window.set_data("CopyDocumentLocationPluginInfo", windowdata)


	def deactivate(self, window):
		windowdata = window.get_data("CopyDocumentLocationPluginInfo")
		
		ui_manager = window.get_ui_manager()
		ui_manager.remove_ui(windowdata["ui_id"])
		ui_manager.remove_action_group(windowdata["action_group"])
		ui_manager.ensure_update()


	def is_valid_doc(self, doc):
		return bool(doc and
				    doc.get_uri() and
					doc.get_uri().startswith("file://"))


	def update_ui(self, window):
		windowdata = window.get_data("CopyDocumentLocationPluginInfo")
		active_doc = window.get_active_document()
		windowdata["action_group"].set_sensitive(self.is_valid_doc(active_doc))

