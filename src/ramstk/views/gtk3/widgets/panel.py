# pylint: disable=non-parent-init-called, too-many-public-methods
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 panel Module."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
import treelib
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gtk, _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton
from .combo import RAMSTKComboBox
from .entry import RAMSTKEntry, RAMSTKTextView
from .frame import RAMSTKFrame
from .label import do_make_label_group
from .matrixview import RAMSTKMatrixView
from .plot import RAMSTKPlot
from .scrolledwindow import RAMSTKScrolledWindow
from .treeview import RAMSTKTreeView

register_matplotlib_converters()


class RAMSTKPanel(RAMSTKFrame):
    """The RAMSTKPanel class.

    Implementations of the RAMSTKPanel() class should provide the following
    methods:

    __do_set_callbacks() to set the callback method for the widgets in the
        panel.  The use of the public methods on_changed_combo(),
        on_changed_entry(), on_focus_out(), and on_toggled() in this
        meta-class shall be the preferred callback methods.
    __do_set_properties() to set the properties of the widgets in the panel.

    Implementations of the RAMSTKPanel() class may provide the following
    methods:

    _do_clear_panel() to clear the contents of the widgets in the panel.
        Connect this as a listener for the 'closed_program' signal.
    _do_load_panel() to load the attribute data into the widgets in the
        panel.  Connect this as a listener for the 'selected_<module>' for
        the work stream module the panel is associated with.

    There are three types of panels that can be created.  These are:

        * fixed: a panel containing a Gtk.Fixed() populated with labels
            and widgets.
        * plot: a panel containing a RAMSTKPlot().
        * treeview: a panel containing a RAMSTKTreeView().

    The attributes of a RAMSTKPanel are:

    :ivar _dic_attribute_keys: contains key:value pairs where the key is
        the index of the widget displaying the associated attribute and the
        value is a list with the name of the attribute in position 0 and the
        attribute's data type in position 1.  An example entry in this dict
        might be:

        0: ['name', 'string']

    :ivar _dic_attribute_updater: contains key:value pairs where the
        key is the name of the attribute and the value is a list with the
        method used to update a widget's display in position 0, the
        name of the signal to block while updating the widget in position 1,
        and the column number in the RAMSTKTreeView() where the attribute data
        is displayed in position 2.  An example entry in this dict might be:

        'name': [self.txtName.do_update, 'changed', 0]

    :ivar _lst_labels: the list of text to display in the labels
        for each widget in a panel.
    :ivar _lst_widgets: the list of widgets to display in a panel.
    :ivar _record_id: the work stream module ID whose attributes
        this panel is displaying.
    :ivar _title: the title to place on the RAMSTKFrame() that is
        this panel's container.

    :ivar tvwTreeView: a RAMSTKTreeView() for the panels that embed a
        treeview.
    :ivar pltPlot: a RAMSTPlot() for the panels that embed a plot.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize private dict instance attributes.
        # TODO: _dic_attribute_keys renamed to _dic_index_attribute?
        # This may be more descriptive of the information the dict holds.
        self._dic_attribute_keys: Dict[int, List[str]] = {}
        self._dic_attribute_updater: Dict[str, Any] = {}

        # Initialize private list instance attributes.
        self._lst_col_order: List[int] = []
        self._lst_labels: List[str] = []
        self._lst_widgets: List[object] = []

        # Initialize private scalar instance attributes.
        self._parent_id: int = -1
        self._record_id: int = -1
        self._title: str = ''
        self._tree_loaded: bool = False

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = '{0:0.6}'

        self.pltPlot: RAMSTKPlot = RAMSTKPlot()
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

    def do_clear_tree(self) -> None:
        """Clear the contents of a RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

    def do_expand_tree(self) -> None:
        """Expand the RAMSTKTreeView.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _row = _model.get_iter_first()

        self.tvwTreeView.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwTreeView.get_column(0)
            self.tvwTreeView.set_cursor(_path, None, False)
            self.tvwTreeView.row_activated(_path, _column)

    def do_load_row(self, attributes: Dict[str, Any]) -> None:
        """Load the data into a RAMSTKTreeView row.

        :param attributes: the attributes dict for the row to be loaded.
        :return: None
        """
        _model = self.tvwTreeView.get_model()

        _data = []
        for _key in self.tvwTreeView.korder:
            _data.append(attributes[self.tvwTreeView.korder[_key]])

        # Only load items that are immediate children of the selected item and
        # prevent loading the selected item itself in the worksheet.
        if not _data[1] == self._record_id and not self._tree_loaded:
            _model.append(None, _data)

    def do_load_tree(self, tree: treelib.Tree) -> None:
        """Load the RAMSTKTreeView().

        :param tree: the treelib Tree containing the module to load.
        :return: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

        try:
            _tag = tree.get_node(0).tag
        except AttributeError:
            _tag = "UNK"

        try:
            self.tvwTreeView.do_load_tree(tree, _tag)
            self.tvwTreeView.expand_all()
            _row = _model.get_iter_first()
            if _row is not None:
                self.tvwTreeView.selection.select_iter(_row)
                self.show_all()
        except TypeError:
            _error_msg = _(
                "An error occurred while loading {1:s} data for Record "
                "ID {0:d} into the view.  One or more values from the "
                "database was the wrong type for the column it was trying to "
                "load.").format(self._record_id, _tag)
        except ValueError:
            _error_msg = _(
                "An error occurred while loading {1:s} data for Record "
                "ID {0:d} into the view.  One or more values from the "
                "database was missing.").format(self._record_id, _tag)

    def do_make_panel_fixed(self, **kwargs: Dict[str, Any]) -> None:
        """Create a panel with the labels and widgets on a Gtk.Fixed().

        :return: None
        :rtype: None
        """
        _justify = kwargs.get('justify', Gtk.Justification.RIGHT)

        _fixed: Gtk.Fixed = Gtk.Fixed()

        _y_pos: int = 5
        # noinspection PyTypeChecker
        (_x_pos, _labels) = do_make_label_group(
            self._lst_labels,
            bold=False,  # type: ignore
            justify=_justify,
            x_pos=5,  # type: ignore
            y_pos=5)  # type: ignore
        for _idx, _label in enumerate(_labels):
            _fixed.put(_label, 5, _y_pos)

            _minimum: Gtk.Requisition = self._lst_widgets[  # type: ignore
                _idx].get_preferred_size()[0]
            if _minimum.height <= 0:
                _minimum.height = self._lst_widgets[  # type: ignore
                    _idx].height

            # RAMSTKTextViews are placed inside a scrollwindow so that's
            # what needs to be placed on the container.
            if isinstance(self._lst_widgets[_idx], RAMSTKTextView):
                _fixed.put(
                    self._lst_widgets[_idx].scrollwindow,  # type: ignore
                    _x_pos + 5,
                    _y_pos)
                _y_pos += _minimum.height + 30
            else:
                _fixed.put(self._lst_widgets[_idx], _x_pos + 5, _y_pos)
                _y_pos += _minimum.height + 5

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)

        self.add(_scrollwindow)

    def do_make_panel_plot(self) -> None:
        """Create a panel with a RAMSTKPlot().

        :return: None
        :rtype: None
        """
        self._lst_widgets.append(self.pltPlot)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.pltPlot.canvas)

        self.add(_scrollwindow)

    def do_make_panel_matrixview(self, matrix: RAMSTKMatrixView) -> None:
        """Create a panel with a RAMSTKMatrixView().

        :param matrix: the matrix to display in the panel.
        :return: None
        """
        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(matrix)

        self.add(_scrollwindow)

    def do_make_panel_treeview(self) -> None:
        """Create a panel with a RAMSTKTreeView().

        :return: None
        """
        self._lst_widgets.append(self.tvwTreeView)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwTreeView)

        self.add(_scrollwindow)

    def do_make_treeview(self, **kwargs: Dict[str, Any]) -> None:
        """Make the RAMSTKTreeView() instance for this panel.

        :return: None
        :rtype: None
        """
        _bg_color: str = kwargs.get('bg_color', '#FFFFFF')  # type: ignore
        _fg_color: str = kwargs.get('fg_color', '#000000')  # type: ignore
        _fmt_file: str = kwargs.get('fmt_file', '')  # type: ignore

        self.tvwTreeView.do_parse_format(_fmt_file)
        self.tvwTreeView.do_make_model()
        self.tvwTreeView.do_make_columns(colors={
            'bg_color': _bg_color,
            'fg_color': _fg_color
        })

        self._lst_col_order = list(self.tvwTreeView.position.values())

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This method receives two dicts.  This first is from the
        workflow's workview module and is sent when a workview widget is
        edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The second dict is from the workflow's moduleview.

            `keys` key: `keys` value

        corresponds to:

            database field name: TreeModel default column position

        Since both dicts contain the same key values, this method can refresh
        the proper column of the RAMSTKTreeView with the new data.

        :param node_id: unused in this method.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        try:
            _position = self._lst_col_order[self._dic_attribute_updater[_key]
                                            [2]]

            _model, _row = self.tvwTreeView.get_selection().get_selected()
            _model.set(_row, _position, _value)
        except KeyError as _error:
            print(_error)

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKTreeView().

        :return: None
        """
        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

    def do_set_cell_callbacks(self, message: str, columns: List[int]) -> None:
        """Set the callback methods for RAMSTKTreeView() cells.

        :param message: the PyPubSub message to broadcast on a
            successful edit.
        :param columns: the list of column numbers whose cells should
            have a callback function assigned.
        :return: None
        """
        for _idx in columns:
            _cell = self.tvwTreeView.get_column(
                self._lst_col_order[_idx]).get_cells()
            try:
                _cell[0].connect('edited', self.on_cell_edit, message, _idx)
            except TypeError:
                _cell[0].connect('toggled', self.on_cell_edit, 'new text',
                                 message, _idx)

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**kwargs)

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_rubber_banding(True)

    def on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                     position: int, message: str) -> None:
        """Handle edits of the RAMSTKTreeview() in a treeview panel.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        try:
            _key = self._dic_attribute_keys[self._lst_column_order[position]]
            if not self.tvwTreeView.do_edit_cell(cell, path, new_text,
                                                 position):
                pub.sendMessage(message,
                                node_id=[self.parent_id, self._record_id, ''],
                                package={_key: new_text})
        except KeyError:
            pass

    # pylint: disable=unused-argument
    def on_cell_toggled(self, cell: Gtk.CellRenderer, path: str, position: int,
                        message: str) -> None:
        """Handle edits of the FMEA Work View RAMSTKTreeview() toggle cells.

        :param cell: the Gtk.CellRenderer() that was toggled.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was toggled.
        :param position: the column position of the toggled
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        :rtype: None
        """
        _new_text = boolean_to_integer(cell.get_active())
        _lst_column_order: List[int] = list(self.tvwTreeView.position.values())

        try:
            _key = self._dic_attribute_keys[_lst_column_order[position]]
            if not self.tvwTreeView.do_edit_cell(cell, path, _new_text,
                                                 position):
                pub.sendMessage(message,
                                node_id=[self.parent_id, self._record_id, ''],
                                package={_key: _new_text})
        except KeyError:
            pass

    def on_changed_combo(self, combo: RAMSTKComboBox, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKComboBox() widgets.

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param combo: the RAMSTKComboBox() that called the method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the attribute from the calling Gtk.Widget().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the work stream module's attribute name
            and the new value from the RAMSTKComboBox().  The value {'': -1}
            will be returned when a KeyError or ValueError is raised by this
            method.
        """
        _key: str = ''
        _new_text: int = -1

        combo.handler_block(combo.dic_handler_id['changed'])

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(combo.get_active())

            # Only if something is selected should we send the message.
            # Otherwise attributes get updated to a value of -1 which isn't
            # correct.  And it sucks trying to figure out why, so leave the
            # conditional unless you have a more elegant (and there prolly
            # is) solution.
            if _new_text > -1:
                pub.sendMessage(message,
                                node_id=[self._record_id, -1],
                                package={_key: _new_text})

        except (KeyError, ValueError):
            pass

        combo.handler_unblock(combo.dic_handler_id['changed'])

        return {_key: _new_text}

    def on_changed_entry(self, entry: RAMSTKEntry, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param entry: the RAMSTKEntry() that called the method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKEntry() or RAMSTKTextView().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': ''} will be returned when a KeyError or ValueError is raised
            by this method.
        :rtype: dict
        """
        entry.handler_block(entry.dic_handler_id['changed'])

        _package: Dict[str, Any] = self.__do_read_text(entry, index, message)

        entry.handler_unblock(entry.dic_handler_id['changed'])

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_changed_textview(
            self, buffer: Gtk.TextBuffer, index: int, message: str,
            textview: RAMSTKTextView) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKTextView() widgets.

        This method is called by:

            * Gtk.TextBuffer() 'changed' signal

        :param buffer: the Gtk.TextBuffer() calling this method.  This
            parameter is unused in this method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKTextView().
        :param message: the PyPubSub message to broadcast.
        :param textview: the RAMSTKTextView() calling this method.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKTextView(). The value {'': ''} will be
            returned when a KeyError or ValueError is raised by this method.
        """
        textview.handler_block(textview.dic_handler_id['changed'])

        _package: Dict[str, Any] = self.__do_read_text(textview, index,
                                                       message)

        textview.handler_unblock(textview.dic_handler_id['changed'])

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete(self, node_id: int, tree: treelib.Tree) -> None:
        """Update the RAMSTKTreeView after deleting a line item.

        :param node_id: the treelib Tree() node ID that was deleted.
        :param tree: the treelib Tree() containing the workflow module data.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()
        _model.remove(_row)

        _row = _model.get_iter_first()
        if _row is not None:
            self.tvwTreeView.selection.select_iter(_row)
            self.show_all()

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """Update the panel's Gtk.Widgets() when attributes are changed.

        This method is called whenever an attribute is edited in the module
        view.

        :param node_id: the list of IDs of the work stream module item
            being edited.  This unused parameter is part of the PyPubSub
            message data package that this method responds to so it must
            remain in the argument list.
        :param package: a dict containing the attribute name as key and
            the new attribute value as the value.
        :return: None
        """
        [[_key, _value]] = package.items()

        (_function,
         _signal) = self._dic_attribute_updater.get(_key)  # type: ignore
        _function(_value, _signal)  # type: ignore

    def on_insert(self, data: Any) -> None:
        """Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :return: None
        """
        _attributes = []
        _model, _row = self.tvwTreeView.selection.get_selected()

        try:
            if self._record_id == self._parent_id:
                _prow = _row
            else:
                _prow = _model.iter_parent(_row)
        except TypeError:
            _prow = None

        _attributes = self.tvwTreeView.get_aggregate_attributes(data)

        _row = _model.append(_prow, _attributes)

        self.tvwTreeView.selection.select_iter(_row)

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        """Get the attributes for the newly selected row.

        :param selection: the Gtk.TreeSelection() for the new row.
        :return: _attributes; the dict of attributes and value for the item
            in the selected row.  The key is the attribute name, the value is
            the attribute value.  Pulling them from the RAMSTKTreeView()
            ensures uncommitted changes are always selected.
        """
        selection.handler_block(self.tvwTreeView.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            for _key in self._dic_attribute_updater:
                _attributes[_key] = _model.get_value(
                    _row,
                    self._lst_col_order[self._dic_attribute_updater[_key][2]])

        selection.handler_unblock(self.tvwTreeView.dic_handler_id['changed'])

        return _attributes

    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int,
                   message: str) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKCheckButton() widgets.

        :param checkbutton: the RAMSTKCheckButton() that was toggled.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKCheckButton().
        :param message: the PyPubSub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': -1} will be returned when a KeyError is raised by this method.
        """
        _key: str = ''
        _new_text: int = -1

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(checkbutton.get_active())
            checkbutton.do_update(_new_text, signal='toggled')

            pub.sendMessage(message,
                            node_id=[self._record_id, -1, ''],
                            package={_key: _new_text})

        except KeyError:
            pass

        return {_key: _new_text}

    def __do_read_text(self, entry: RAMSTKEntry, index: int,
                       message: str) -> Dict[str, Any]:
        """Read the text in a RAMSTKEntry() or Gtk.TextBuffer().

        :param entry: the RAMSTKEntry() or Gtk.TextBuffer() to read.
        :param index: the position in the attribute key dict for the
            attribute being updated.
        :param message: the PyPubSub message to send along with the data
            package.
        :return: {_key, _new_text}; a dict containing the attribute key and
            the new value (text) for that key.
        """
        _key: str = ''
        _new_text: Any = ''
        _type: str = 'string'

        try:
            _key = self._dic_attribute_keys[index][0]
            _type = self._dic_attribute_keys[index][1]

            _new_text = {
                'float': float(entry.do_get_text()),
                'integer': int(entry.do_get_text()),
                'string': str(entry.do_get_text()),
            }[_type]

            pub.sendMessage(message,
                            node_id=[self._record_id, -1, -1],
                            package={_key: _new_text})
        except (KeyError, ValueError):
            pass

        return {_key: _new_text}