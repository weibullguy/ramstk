# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class ResistorAssessmentInputs(AssessmentInputs):
    """
    Display Resistor assessment input attribute data in the RAMSTK Work Book.

    The Resistor assessment input view displays all the assessment inputs for
    the selected resistor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Resistor assessment input view are:

    :cvar dict _dic_specifications: dictionary of resistor MIL-SPECs.  Key is
                                    resistor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of resistor styles defined in the
                            MIL-SPECs.  Key is resistor subcategory ID; values
                            are lists of styles.

    :ivar cmbSpecification: select and display the governing specification of
                            the resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
                           resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a
                        resistor network or the number of potentiometers taps.

    Callbacks signals in _lst_handler_id:

    +-------+------------------------------+
    | Index | Widget - Signal              |
    +=======+==============================+
    |   0   | cmbQuality - `changed`       |
    +-------+------------------------------+
    |   1   | cmbSpecification - `changed` |
    +-------+------------------------------+
    |   2   | cmbType - `changed`          |
    +-------+------------------------------+
    |   3   | cmbStyle - `changed`         |
    +-------+------------------------------+
    |   4   | cmbConstruction - `changed`  |
    +-------+------------------------------+
    |   5   | txtResistance - `changed`    |
    +-------+------------------------------+
    |   6   | txtNElements - `changed`     |
    +-------+------------------------------+
    """

    # Define private dict attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'specification_id',
        2: 'type_id',
        3: 'family_id',
        4: 'construction_id',
        5: 'resistance',
        6: 'n_elements',
    }

    _dic_quality = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-R-11"], [_("Lower")]],
        2: [
            ["S"], ["R"], ["P"], ["M"], ["MIL-R-10509"], ["MIL-R-22684"],
            [_("Lower")],
        ],
        3: [["MIL-SPEC"], [_("Lower")]],
        4: [["MIL-SPEC"], [_("Lower")]],
        5: [["S"], ["R"], ["P"], ["M"], ["MIL-R-93"], [_("Lower")]],
        6: [["S"], ["R"], ["P"], ["M"], ["MIL-R-26"], [_("Lower")]],
        7: [["S"], ["R"], ["P"], ["M"], ["MIL-R-18546"], [_("Lower")]],
        8: [["MIL-SPEC"], [_("Lower")]],
        9: [["S"], ["R"], ["P"], ["M"], ["MIL-R-27208"], [_("Lower")]],
        10: [["MIL-SPEC"], [_("Lower")]],
        11: [["MIL-SPEC"], [_("Lower")]],
        12: [["MIL-SPEC"], [_("Lower")]],
        13: [["S"], ["R"], ["P"], ["M"], ["MIL-R-22097"], [_("Lower")]],
        14: [["MIL-SPEC"], [_("Lower")]],
        15: [["MIL-SPEC"], [_("Lower")]],
    }
    # Key is subcategory ID; index is specification ID.
    _dic_specifications = {
        2: [
            ["MIL-R-10509"], ["MIL-R-22684"], ["MIL-R-39017"],
            ["MIL-R-55182"],
        ],
        6: [["MIL-R-26"], ["MIL-R-39007"]],
        7: [["MIL-R-18546"], ["MIL-R-39009"]],
        15: [["MIL-R-23285"], ["MIL-R-39023"]],
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
        1: [["RCR"], ["RC"]],
        2: [["RLR"], ["RL"], ["RNR"], ["RN"]],
        5: [["RBR"], ["RB"]],
        6: [["RWR"], ["RW"]],
        7: [["RER"], ["RE"]],
        9: [["RTR"], ["RT"]],
        11: [["RA"], ["RK"]],
        13: [["RJR"], ["RJ"]],
        15: [["RO"], ["RVC"]],
    }
    # First key is subcategory ID; second key is specification ID.
    # Index is style ID.
    _dic_styles = {
        6: {
            1: [
                ["RWR 71"], ["RWR 74"], ["RWR 78"], ["RWR 80"], ["RWR 81"],
                ["RWR 82"], ["RWR 84"], ["RWR 89"],
            ],
            2:
            [
                ["RW 10"], ["RW 11"], ["RW 12"], ["RW 13"], ["RW 14"], ["RW 15"],
                ["RW 16"], ["RW 20"], ["RW 21 "], ["RW 22"], ["RW 23"], ["RW 24"],
                ["RW 29"], ["RW 30"], ["RW 31"], ["RW 32"], ["RW 33"], ["RW 34"],
                ["RW 35"], ["RW 36"], ["RW 37"], ["RW 38"], ["RW 39"], ["RW 47"],
                ["RW 55"], ["RW 56"], ["RW 67"], ["RW 68"], ["RW 69"], ["RW 70"],
                ["RW 74"], ["RW 78"], ["RW 79"], ["RW 80"], ["RW 81"],
            ],
        },
        7: {
            1: [
                ["RE 60/RER 60"], ["RE 65/RER 65"], ["RE 70/RER 70"],
                ["RE 75/RER 75"], ["RE 77"], ["RE 80"],
            ],
            2: [
                ["RE 60/RER40"], ["RE 65/RER 45"], ["RE 70/ RER 50"],
                ["RE 75/RER 55"], ["RE 77"], ["RE 80"],
            ],
        },
    }
    # Key is subcategory ID; index is construction ID.
    _dic_construction = {
        10: [
            ["RR0900A2A9J103"], ["RR0900A3A9J103"], ["RR0900A4A9J103"],
            ["RR0900A5A9J103"],
        ],
        12: [[_("Enclosed")], [_("Unenclosed")]],
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Resistance (\u03A9):"),
        _("Specification:"),
        _("Type:"),
        _("Style:"),
        _("Construction:"),
        _("Number of Elements:"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Resistor assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentInputs.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbSpecification = RAMSTKComboBox(
            tooltip=_("The governing specification for the resistor."),
        )
        self.cmbType = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbStyle = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbConstruction = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.txtResistance = RAMSTKEntry()
        self.txtNElements = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Resistor class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.txtResistance, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbType, _x_pos, _y_pos[3])
        self.put(self.cmbStyle, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtNElements, _x_pos, _y_pos[6])

        self.show_all()

    def __set_callbacks(self):
        """
        Set callback methods for Resistor assessment input widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self.on_combo_changed, 0),
        )
        self._lst_handler_id.append(
            self.cmbSpecification.connect(
                'changed', self.on_combo_changed,
                1,
            ),
        )
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self.on_combo_changed, 2),
        )
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self.on_combo_changed, 3),
        )
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self.on_combo_changed, 4),
        )
        self._lst_handler_id.append(
            self.txtResistance.connect('changed', self.on_focus_out, 5),
        )
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self.on_focus_out, 6),
        )

    def __set_properties(self):
        """
        Set properties for Resistor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.do_set_properties(
            tooltip=_("The governing specification for the resistor."),
        )
        self.cmbType.do_set_properties(
            tooltip=_("The type of thermistor."),
        )
        self.cmbStyle.do_set_properties(
            tooltip=_("The style of resistor."),
        )
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the resistor."),
        )
        self.txtResistance.do_set_properties(
            width=125,
            tooltip=_("The resistance (in \u03A9) of the resistor."),
        )
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_(
                "The number of active resistors in a resistor network "
                "or the number of potentiometer taps.",
            ),
        )

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the Resisotr RKTComboBox()s.

        :param int subcategory_id: the newly selected resistor subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                _data = ["S", "R", "P", "M", ["MIL-SPEC"], [_("Lower")]]
            else:
                _data = self._dic_quality[subcategory_id]
        except KeyError:
            _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the specification RAMSTKComboBox().
        try:
            _data = self._dic_specifications[subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the type RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                _data = self._dic_types[subcategory_id]
            else:
                _data = [[_("Bead")], [_("Disk")], [_("Rod")]]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        # Load the style RAMSTKComboBox().
        _specification_id = int(self.cmbSpecification.get_active())
        try:
            _data = self._dic_styles[subcategory_id][_specification_id]
        except (KeyError, IndexError):
            _data = []
        self.cmbStyle.do_load_combo(_data)

        # Load the construction RAMSTKComboBox().
        try:
            _data = self._dic_construction[subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

    def _do_load_page(self, attributes):
        """
        Load the Resistor assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Resistor.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        if self._hazard_rate_method_id == 2:
            self.cmbSpecification.handler_block(self._lst_handler_id[1])
            self.cmbSpecification.set_active(attributes['specification_id'])
            self.cmbSpecification.handler_unblock(self._lst_handler_id[1])

            self.cmbStyle.handler_block(self._lst_handler_id[3])
            self.cmbStyle.set_active(attributes['family_id'])
            self.cmbStyle.handler_unblock(self._lst_handler_id[3])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtResistance.handler_block(self._lst_handler_id[5])
            self.txtResistance.set_text(
                str(self.fmt.format(attributes['resistance'])),
            )
            self.txtResistance.handler_unblock(self._lst_handler_id[5])

            self.txtNElements.handler_block(self._lst_handler_id[6])
            self.txtNElements.set_text(
                str(self.fmt.format(attributes['n_elements'])),
            )
            self.txtNElements.handler_unblock(self._lst_handler_id[6])

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)
        self.cmbSpecification.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.cmbStyle.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtResistance.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id in [1, 2, 5, 6, 7, 9, 11, 13, 15]:
                self.cmbType.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.txtResistance.set_sensitive(True)
            if self._subcategory_id in [2, 6, 7, 15]:
                self.cmbSpecification.set_sensitive(True)
            if self._subcategory_id in [6, 7]:
                self.cmbStyle.set_sensitive(True)
            if self._subcategory_id == 8:
                self.cmbType.set_sensitive(True)
            if self._subcategory_id in [10, 12]:
                self.cmbConstruction.set_sensitive(True)
            else:
                self.cmbConstruction.set_sensitive(False)
            if self._subcategory_id in [4, 9, 10, 11, 12, 13, 14, 15]:
                self.txtNElements.set_sensitive(True)
            else:
                self.txtNElements.set_sensitive(False)



class ResistorAssessmentResults(AssessmentResults):
    """
    Display Resistor assessment results attribute data in the RAMSTK Work Book.

    The Resistor assessment result view displays all the assessment results
    for the selected resistor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a Resistor assessment result view are:

    :ivar txtPiR: displays the resistance factor for the resistor.
    :ivar txtPiT: displays the temperature factor for the resistor.
    :ivar txtPiNR: displays the number of resistors factor for the resistor.
    :ivar txtPiTAPS: displays the potentiometer taps factor for the resistor.
    :ivar txtPiV: displays the voltage factor for the resistor.
    :ivar txtPiC: displays the construction class factor for the resistor.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Resistor assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>R</sub>:")
        self._lst_labels.append("\u03C0<sub>T</sub>:")
        self._lst_labels.append("\u03C0<sub>NR</sub>:")
        self._lst_labels.append("\u03C0<sub>TAPS</sub>")
        self._lst_labels.append("\u03C0<sub>V</sub>:")
        self._lst_labels.append("\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiR = RAMSTKEntry()
        self.txtPiT = RAMSTKEntry()
        self.txtPiNR = RAMSTKEntry()
        self.txtPiTAPS = RAMSTKEntry()
        self.txtPiV = RAMSTKEntry()
        self.txtPiC = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the resistor Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for resistors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiR, _x_pos, _y_pos[3])
        self.put(self.txtPiT, _x_pos, _y_pos[4])
        self.put(self.txtPiNR, _x_pos, _y_pos[5])
        self.put(self.txtPiTAPS, _x_pos, _y_pos[6])
        self.put(self.txtPiV, _x_pos, _y_pos[7])
        self.put(self.txtPiC, _x_pos, _y_pos[8])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Resistor assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the resistor "
                "failure rate.",
            ),
        )

        self.txtPiR.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The resistance factor for the resistor."),
        )
        self.txtPiT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The temperature factor for the resistor."),
        )
        self.txtPiNR.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The number of resistors factor for the resistor."),
        )
        self.txtPiTAPS.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The potentiometer taps factor for the resistor."),
        )
        self.txtPiV.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The voltage factor for the resistor."),
        )
        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction class factor for the resistor."),
        )

    def _do_load_page(self, attributes):
        """
        Load the Resistor assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Resistor.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiR.set_text(str(self.fmt.format(attributes['piR'])))
        self.txtPiT.set_text(str(self.fmt.format(attributes['piT'])))
        self.txtPiNR.set_text(str(self.fmt.format(attributes['piNR'])))
        self.txtPiTAPS.set_text(str(self.fmt.format(attributes['piTAPS'])))
        self.txtPiV.set_text(str(self.fmt.format(attributes['piV'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiR.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtPiNR.set_sensitive(False)
        self.txtPiTAPS.set_sensitive(False)
        self.txtPiV.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id != 8:
                self.txtPiR.set_sensitive(True)
            if self._subcategory_id == 4:
                self.txtPiT.set_sensitive(True)
                self.txtPiNR.set_sensitive(True)
            if self._subcategory_id in [9, 10, 11, 12, 13, 14, 15]:
                self.txtPiTAPS.set_sensitive(True)
                self.txtPiV.set_sensitive(True)
            if self._subcategory_id in [10, 12]:
                self.txtPiC.set_sensitive(True)