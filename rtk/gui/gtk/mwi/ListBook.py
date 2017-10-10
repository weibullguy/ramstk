# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.ListBook.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
PyGTK Multi-Window Interface List Book
===============================================================================
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub                              # pylint: disable=E0401

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.listviews.Revision import ListView as lvwRevision
from gui.gtk.listviews.Function import ListView as lvwFunction

_ = gettext.gettext


def destroy(__widget, __event=None):
    """
    Quits the RTK application when the X in the upper right corner is
    pressed.

    :param __widget: the gtk.Widget() that called this method.
    :type __widget: :py:class:`gtk.Widget`
    :keyword __event: the gtk.gdk.Event() that called this method.
    :type __event: :py:class:`gtk.gdk.Event`
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    gtk.main_quit()

    return False


class ListView(gtk.Window):                 # pylint: disable=R0904
    """
    This is the List View class for the pyGTK multiple window interface.
    """

    def __init__(self, controller):
        """
        Method to initialize an instance of the RTK List View class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.
        self.dic_list_view = {'revision': lvwRevision(controller),
                              'function': lvwFunction(controller)}

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        try:
            locale.setlocale(locale.LC_ALL,
                             self._mdcRTK.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_title(_(u"RTK Matrices & Lists"))
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((2 * _width / 3), 0)

        self.connect('delete_event', destroy)

        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Method to load the correct List View for the RTK module that was
        selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if self.get_child() is not None:
            self.remove(self.get_child())

        if self.dic_list_view[module] is not None:
            self.add(self.dic_list_view[module])
        else:
            _return = True

        return _return
