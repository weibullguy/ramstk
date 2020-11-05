# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTK_CONTROL_TYPES as RAMSTK_CONTROL_TYPES
from ramstk.configuration import RAMSTK_CRITICALITY as RAMSTK_CRITICALITY
from ramstk.configuration import (
    RAMSTK_FAILURE_PROBABILITY as RAMSTK_FAILURE_PROBABILITY
)
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.assistants import AddControlAction as AddControlAction
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

def do_request_insert(attributes: Dict[str, Any], level: str,
                      parent_id: str) -> None:
    ...


def get_indenture_level(record_id: str) -> str:
    ...


class MethodPanel(RAMSTKPanel):
    chkCriticality: Any = ...
    chkRPN: Any = ...
    txtItemCriticality: Any = ...

    def __init__(self) -> None:
        ...


class FMEAPanel(RAMSTKPanel):
    dic_action_category: Any = ...
    dic_action_status: Any = ...
    dic_detection: Any = ...
    dic_icons: Any = ...
    dic_occurrence: Any = ...
    dic_severity: Any = ...
    dic_users: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_combobox(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...


class FMEA(RAMSTKWorkView):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...