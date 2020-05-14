# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.combo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Combo Module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, Gtk


class RAMSTKComboBox(Gtk.ComboBox):
    """This is the RAMSTK ComboBox class."""
    def __init__(self, index: int = 0, simple: bool = True) -> None:
        r"""
        Create RAMSTK ComboBox widgets.

        :keyword int index: the index in the RAMSTKComboBox Gtk.ListView() to
            display.  Default is 0.
        :keyword bool simple: indicates whether to make a simple (one item) or
            complex (three item) RAMSTKComboBox.  Default is True.
        """
        GObject.GObject.__init__(self)

        self._index: int = index

        if not simple:
            _list = Gtk.ListStore()
            _list.set_column_types([GObject.TYPE_STRING, GObject.TYPE_STRING,
                                    GObject.TYPE_STRING])
        else:
            _list = Gtk.ListStore()
            _list.set_column_types([GObject.TYPE_STRING])
        self.set_model(_list)

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, 'text', self._index)

        self.show()

    def do_get_options(self) -> Dict[int, Any]:
        """
        Retrieve all the options in the RAMSTK Combo.

        :return: _options
        :rtype: dict
        """
        _options = {}

        _model = self.get_model()
        _iter = _model.get_iter_first()

        i = 0
        while _iter is not None:
            _options[i] = _model.get_value(_iter, self._index)
            _iter = _model.iter_next(_iter)
            i += 1

        return _options

    # noinspection PyIncorrectDocstring
    def do_load_combo(self, entries: List[List[str]],
                      simple: bool = True, **kwargs) -> None:
        """
        Load RAMSTK ComboBox widgets.

        :param list entries: the information to load into the Gtk.ComboBox().
            This is always a list of lists where each internal list contains
            the information to be displayed and there is one internal list for
            each RAMSTKComboBox line.
        :keyword bool simple: indicates whether this is a simple (one item) or
            complex (three item) RAMSTKComboBox.  A simple (default)
            RAMSTKComboBox contains and displays one field only.  A 'complex'
            RAMSTKComboBox contains three str fields, but only displays the
            first field.  The other two fields are hidden and used to store
            information associated with the items displayed in the
            RAMSTKComboBox.  For example, if the name of an item is displayed,
            the other two fields might contain a code and an index.  These
            could be extracted for use in the RAMSTK Views.
        :return: None
        :rtype: None
        :raise: TypeError if attempting to load other than string values.
        """
        # TODO: Remove this try block when requirements 305.7 and 305.8 are
        #  implemented in the RAMSTKComboBox.
        try:
            _handler_id = kwargs['handler_id']
            self.handler_block(_handler_id)
        except KeyError:
            _handler_id = -1

        _model = self.get_model()
        _model.clear()

        if not simple:
            _model.append(["", "", ""])
            for __, _entry in enumerate(entries):
                _model.append(list(_entry))
        else:
            _model.append([""])
            for __, _entry in enumerate(entries):
                _model.append([_entry[self._index]])

        if _handler_id > -1:
            self.handler_unblock(_handler_id)

    # noinspection PyIncorrectDocstring
    #// TODO: add handler_id as an editable widget attribute
    #//
    #// Add an attribute to hold the value of the signal handler ID
    #// associated with RAMSTK widgets that are editable.  This attribute would
    #// be set in the __set_callbacks() methods in each class.  Use the
    #// attribute in the RAMSTK widget methods that make changes to the
    #// contents of the widget.
    #//
    #// See requirements 305.7 and 305.8.
    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK combobox.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.ComboBox() widget.
                Default is 30.
            * *tooltip* (str) -- the tooltip, if any, for the combobox.
                Default is an empty string.
            * *width* (int) -- width of the Gtk.ComboBox() widget.  Default is
                200.
        :return: None
        :rtype: None
        """
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 30
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ("Missing tooltip, please file a quality type issue to "
                        "have one added.")
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200

        if _height == 0:
            _height = 30
        if _width == 0:
            _width = 200

        self.set_property('height-request', _height)
        self.set_property('tooltip-markup', _tooltip)
        self.set_property('width-request', _width)

    def do_update(self, value: int, handler_id: int) -> None:
        """
        Update the RAMSTK Combo with a new value.

        :param str value: the information to update the RAMSTKCombo() to
            display.
        :param int handler_id: the handler ID associated with the
            RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self.handler_block(handler_id)
        self.set_active(value)
        self.handler_unblock(handler_id)

    def get_value(self, index: int = 0) -> str:
        """
        Return the value in the RAMSTKComboBox model at the index position.

        :keyword int index: the column in the RAMSTKComboBox() model whose
            value is to be retrieved.  Defaults to zero which will always
            read a 'simple' RAMSTKComboBox().
        :return: _value
        :rtype: str
        """
        _model = self.get_model()
        _row = self.get_active_iter()

        _value: str = _model.get_value(_row, index)

        return _value
