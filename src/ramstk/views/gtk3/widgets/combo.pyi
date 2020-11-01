# Standard Library Imports
from typing import Any, Dict, List, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .widget import RAMSTKWidget as RAMSTKWidget

class RAMSTKComboBox(Gtk.ComboBox, RAMSTKWidget):
    def __init__(self, index: int = ..., simple: bool = ...) -> None:
        ...

    def do_get_options(self) -> Dict[int, Any]:
        ...

    def do_load_combo(self,
                      entries: List[List[Union[str, int]]],
                      signal: str = ...,
                      simple: bool = ...) -> None:
        ...

    def do_update(self, value: int, signal: str = ...) -> None:
        ...

    def get_value(self, index: int = ...) -> str:
        ...
