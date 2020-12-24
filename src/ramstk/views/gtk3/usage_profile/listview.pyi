# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

class UsageProfilePanel(RAMSTKPanel):
    _module: str = ...
    _dic_attributes: Any = ...
    _dic_element_keys: Any = ...
    _dic_headings: Any = ...
    _dic_row_loader: Any = ...
    _dic_visible: Any = ...
    _title: Any = ...
    dic_icons: Any = ...
    dic_units: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_combobox(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...
    _dic_attribute_keys: Any = ...
    _dic_attribute_updater: Any = ...

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        ...

    def __do_load_environment(self, node: treelib.Node,
                              row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_mission(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_phase(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...


class UsageProfile(RAMSTKListView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _lst_col_order: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlPanel: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        ...

    _record_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def __make_ui(self) -> None:
        ...
