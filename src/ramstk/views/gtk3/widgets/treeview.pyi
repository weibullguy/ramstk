# Stubs for ramstk.views.gtk3.widgets.treeview (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import treelib
from ramstk.views.gtk3 import Gtk
from typing import Any, List

def do_make_column(cells: List[Gtk.CellRenderer], **kwargs) -> \
        Gtk.TreeViewColumn: ...
    pass

def do_set_cell_properties(cell: Gtk.CellRenderer, **kwargs) -> None: ...
    pass


class RAMSTKTreeView(Gtk.TreeView):
    datatypes: List[str] = ...
    editable: List[int] = ...
    headings: List[str] = ...
    korder: List[int] = ...
    order: List[int] = ...
    visible: List[int] = ...
    widgets: List[str] = ...
    pixbuf_col: int = ...
    index_col: int = ...
    def __init__(self) -> None:
        self._resize_wrap = None
        self._format_cell = None
        ...
    def do_parse_format(self, fmt_path: str, fmt_file: str, pixbuf: bool=..., indexed: bool=...) -> None: ...
    def do_set_editable_columns(self) -> None: ...
    def do_set_visible_columns(self, **kwargs: Any) -> None: ...
    def do_load_tree(self, tree: treelib.Tree, tag: str, row: Gtk.TreeIter=...) -> bool: ...
    def do_edit_cell(self, cell: Gtk.CellRenderer, path: str, new_text: str, position: int) -> None: ...
    def get_cell_model(self, column: int, clear: bool=...) -> Gtk.TreeModel: ...
    def make_model(self, bg_color: str=..., fg_color: str=...) -> None: ...

    def handler_block(self, param: int) -> object:
        pass

    def handler_unblock(self, param: int) -> object:
        pass

    def _do_set_properties(self, _cell, bg_color, fg_color, param):
        pass

    def _do_make_cell(self, _widget):
        pass

    def _do_make_combo_cell(self):
        pass

    def _do_make_spin_cell(self):
        pass

    def _do_make_toggle_cell(self):
        pass

    def _do_make_text_cell(self, param):
        pass

    def connect(self, param, _on_button_press):
        pass

    def do_load_tree(self, tree, _tag):
        pass


class CellRendererML(Gtk.CellRendererText):
    textedit_window: Any = ...
    selection: Any = ...
    treestore: Any = ...
    treeiter: Any = ...
    textedit: Any = ...
    textbuffer: Any = ...
    def __init__(self) -> None:
        self._keyhandler = None
        ...
    def do_get_size(self, widget: Any, cell_area: Any): ...
    def do_start_editing(self, __event: Any, treeview: Any, path: Any, __background_area: Any, cell_area: Any, __flags: Any) -> None: ...

    def get_property(self, param):
        pass

    def emit(self, param, path, text):
        pass
