# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.Export.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007, 2018 Doyle "weibullguy" Rowland
"""Export Assistant Module."""

# Standard Library Imports
import os

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKFileChooser, RAMSTKMessageDialog
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _


class RAMSTKExport(RAMSTKFileChooser):
    """Assistant to walk user through the process of exporting records."""

    def __init__(self, controller, module, tree):
        """
        Initialize an instance of the Export Assistant.

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        :param str module: the RAMSTK module to export.
        """
        RAMSTKFileChooser.__init__(
            self, _("RAMSTK Export"),
            controller.RAMSTK_CONFIGURATION.RAMSTK_PROG_DIR,
        )

        # Initialize private dict variables.

        # Initialize private list variables.

        # Initialize private scalar variables.
        self._mdcRAMSTK = controller
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers['exports']
        self._module = module
        self._tree = tree

        # Initialize public dict variables.

        # Initialize public list variables.

        # Initialize public scalar variables.

        self._do_select_file()

    def _do_quit(self):
        """
        Quit the RAMSTK Export Assistant.

        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_request_export(self, filetype, filename):
        """
        Request the data controller insert new records.

        :param str filetype: the type of file to export data.  Current options
                             are:

                             - Text
                             - Excel

        :param str filename: the absolute path to the file to export data.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)

        self._dtc_data_controller.request_do_load_output(
            self._module, self._tree,
        )
        self._dtc_data_controller.request_do_export(filetype, filename)

        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_select_file(self):
        """
        Select the input file to export data to.

        :return: None
        :rtype: None
        """
        _cansave = False
        (_filename, _extension) = self.do_run()

        if _filename is not None:
            if _extension == '.csv':
                _filetype = 'csv'
            elif _extension == '.txt':
                _filetype = 'text'
            elif _extension in ['.xls', '.xlsm', '.xlsx']:
                _filetype = 'excel'

            if os.path.exists(_filename):
                _prompt = _(
                    "File {0:s} already exists.  "
                    "Overwrite?",
                ).format(_filename)
                _icon = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
                        '/32x32/warning.png'
                _dialog = RAMSTKMessageDialog(_prompt, _icon, 'question')
                _response = _dialog.do_run()
                if _response == Gtk.ResponseType.YES:
                    _dialog.destroy()
                    _cansave = True
                else:
                    _dialog.destroy()
            else:
                _cansave = True

            if _cansave:
                self._do_request_export(_filetype, _filename)
            else:
                self._do_select_file()

        self._do_quit()