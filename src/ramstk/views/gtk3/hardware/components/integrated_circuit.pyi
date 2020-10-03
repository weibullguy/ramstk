# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel as RAMSTKAssessmentInputPanel
from .panels import RAMSTKAssessmentResultPanel as RAMSTKAssessmentResultPanel

class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    cmbApplication: Any = ...
    cmbConstruction: Any = ...
    cmbECC: Any = ...
    cmbManufacturing: Any = ...
    cmbPackage: Any = ...
    cmbTechnology: Any = ...
    cmbType: Any = ...
    txtArea: Any = ...
    txtFeatureSize: Any = ...
    txtNActivePins: Any = ...
    txtNCycles: Any = ...
    txtNElements: Any = ...
    txtOperatingLife: Any = ...
    txtThetaJC: Any = ...
    txtVoltageESD: Any = ...
    txtYearsInProduction: Any = ...
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...

class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    txtC1: Any = ...
    txtC2: Any = ...
    txtLambdaBD: Any = ...
    txtLambdaBP: Any = ...
    txtLambdaCYC: Any = ...
    txtLambdaEOS: Any = ...
    txtPiA: Any = ...
    txtPiCD: Any = ...
    txtPiL: Any = ...
    txtPiMFG: Any = ...
    txtPiPT: Any = ...
    txtPiT: Any = ...
    def __init__(self) -> None: ...
