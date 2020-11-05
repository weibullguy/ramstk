# Standard Library Imports
from typing import Any, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .widget import RAMSTKWidget as RAMSTKWidget

def do_make_buttonbox(view: Any,
                      **kwargs: Any) -> Union[Gtk.HButtonBox, Gtk.VButtonBox]:
    ...


class RAMSTKButton(Gtk.Button, RAMSTKWidget):
    def __init__(self, label: str = ...) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...


class RAMSTKCheckButton(Gtk.CheckButton, RAMSTKWidget):
    def __init__(self, label: str = ...) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: int, signal: str = ...) -> None:
        ...


class RAMSTKOptionButton(Gtk.RadioButton, RAMSTKWidget):
    def __init__(self, group: Gtk.RadioButton = ..., label: str = ...) -> None:
        ...


class RAMSTKSpinButton(Gtk.SpinButton, RAMSTKWidget):
    def __init__(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: int, signal: str = ...) -> None:
        ...