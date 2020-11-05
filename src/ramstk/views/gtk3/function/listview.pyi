# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView

class FunctionHardware(RAMSTKListView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _view_type: str = ...
    _lst_tooltips: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...