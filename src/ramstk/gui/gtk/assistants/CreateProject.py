# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.CreateProject.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Create Project Assistant Module."""

from os import remove

# Import other RAMSTK modules.
import ramstk.Utilities as Utilities
from ramstk.gui.gtk.ramstk.Widget import _, gtk, set_cursor
from ramstk.gui.gtk import ramstk

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2018 Doyle "weibullguy" Rowland'


class CreateProject(object):
    """This is the class used to create a new RAMSTK Project database."""

    def __init__(self, __button, controller):
        """
        Initialize an instance of the Create Project Assistant.

        :param __button: the gtk.ToolButton() that launched this class.
        :type __button: :class:`gtk.ToolButton`
        :param controller: the RAMSTK master data controller.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        set_cursor(self._mdcRAMSTK, gtk.gdk.WATCH)

        self._request_create_sqlite3_project()

        set_cursor(self._mdcRAMSTK, gtk.gdk.LEFT_PTR)

    def _request_create_sqlite3_project(self):
        """Create a RAMSTK Project database using SQLite3."""
        _dialog = gtk.FileChooserDialog(
            title=_(u"Create a RAMSTK Program Database"),
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_NEW, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
                     gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_DIR)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program + '.ramstk'

            if Utilities.file_exists(_new_program):
                _dlgConfirm = ramstk.RAMSTKDialog(
                    _(u"RAMSTK - Confirm Overwrite"),
                    dlgbuttons=(gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO,
                                gtk.RESPONSE_NO))

                _label = ramstk.RTLabel(
                    _(u"RAMSTK Program database already exists. "
                      u"\n\n{0:s}\n\nOverwrite?").format(_new_program),
                    width=-1,
                    height=-1,
                    bold=False,
                    wrap=True)
                _dlgConfirm.vbox.pack_start(_label)
                _label.show()

                if _dlgConfirm.run() == gtk.RESPONSE_YES:
                    _dlgConfirm.destroy()
                    remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()
                    return True

            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'] = \
                _new_program

        _dialog.destroy()

        self._mdcRAMSTK.request_do_create_program()

        return False

    def _cancel(self, __button):
        """
        Destroy the Create Project Assistant.

        :param __button: the gtk.Button() that called this method.
        :type __button: :class:`gtk.Button `
        :return: True
        :rtype: boolean
        """
        self.assistant.destroy()

        return True
