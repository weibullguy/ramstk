# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

class GoalMethodPanel(RAMSTKPanel):
    cmbAllocationGoal: Any = ...
    cmbAllocationMethod: Any = ...
    txtHazardRateGoal: Any = ...
    txtMTBFGoal: Any = ...
    txtReliabilityGoal: Any = ...

    def __init__(self) -> None:
        ...


class AllocationPanel(RAMSTKPanel):
    def __init__(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...


class Allocation(RAMSTKWorkView):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...