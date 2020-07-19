# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK base FME(C)A Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (RAMSTK_CONTROL_TYPES, RAMSTK_CRITICALITY,
                                  RAMSTK_FAILURE_PROBABILITY,
                                  RAMSTKUserConfiguration)
from ramstk.logger import RAMSTKLogManager
from ramstk.models.programdb import (RAMSTKAction, RAMSTKCause, RAMSTKControl,
                                     RAMSTKMechanism, RAMSTKMode)
from ramstk.views.gtk3 import Gdk, GdkPixbuf, Gtk, _
from ramstk.views.gtk3.assistants import AddControlAction
from ramstk.views.gtk3.widgets import (RAMSTKCheckButton, RAMSTKLabel,
                                       RAMSTKMessageDialog, RAMSTKTextView,
                                       RAMSTKTreeView, RAMSTKWorkView)


class FMEA(RAMSTKWorkView):
    """
    Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :cvar list _lst_control_type: list containing the types of controls that
        can be implemented.
    :cvar list _lst_fmea_data: list containing the FMEA row data.

    :ivar dict _dic_missions: a dict containing all this missions associated
        with the selected Revision.
    :ivar dict _dic_mission_phases: a dict containing all the mission phases
        associated with each mission in _dic_missions.
    :ivar float _item_hazard_rate: the hazard rate of the Function or Hardware
        item associated with the FMEA.
    """

    # Define private class dict attributes.
    _dic_keys = {
        1: "description",
        2: "mission",
        3: "mission_phse",
        4: "effect_local",
        5: "effect_next",
        6: "effect_end",
        7: "detection_method",
        8: "other_indications",
        9: "isolation_method",
        10: "design_provisions",
        11: "operator_actions",
        12: "severity_class",
        13: "hazard_rate_source",
        14: "mode_probability",
        15: "effect_probability",
        16: "mode_ratio",
        17: "mode_hazard_rate",
        18: "mode_op_time",
        19: "mode_criticality",
        20: "type_id",
        21: "rpn_severity",
        22: "rpn_occurrence",
        23: "rpn_detection",
        24: "rpn",
        25: "action_category",
        26: "action_owner",
        27: "action_due_date",
        28: "action_status",
        29: "action_taken",
        30: "action_approved",
        31: "action_approve_date",
        32: "action_closed",
        33: "action_close_date",
        34: "rpn_severity_new",
        35: "rpn_occurrence_new",
        36: "rpn_detection_new",
        37: "rpn_new",
        38: "critical_item",
        39: "single_point",
        40: "pof_include",
        41: "remarks"
    }
    _dic_column_keys = _dic_keys

    # Define private class list attributes.
    _lst_control_type: List[bool] = [_("Prevention"), _("Detection")]
    _lst_mode_mask: List[bool] = [
        True, True, True, True, True, True, True, True, True, True, True, True,
        True, True, True, True, True, True, True, True, False, True, False,
        False, False, False, False, False, False, False, False, False, False,
        False, True, False, False, False, True, True, False, True, False, False
    ]
    _lst_mechanism_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, True, True, True, False, False, False, False, False,
        False, False, False, False, False, True, True, True, False, False,
        True, True, False, False
    ]
    _lst_cause_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, True, True, True, False, False, False, False, False,
        False, False, False, False, False, True, True, True, False, False,
        False, True, False, False
    ]
    _lst_control_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        True, False, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, True, False, False
    ]
    _lst_action_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, False, False, False, True, True, True, True, True, True,
        True, True, True, False, False, False, False, False, False, False,
        True, False, False
    ]
    _lst_labels: List[str] = ["", "", _("Item Criticality:")]

    # Define private class scalar attributes.
    _pixbuf: bool = True

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'fmea') -> None:
        """
        Initialize the Work View for the FMEA.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_mission_phases: Dict[str, List[str]] = {"": [""]}

        # Initialize private list attributes.
        self._lst_fmea_data: List[Any] = [
            0, "Description", "Mission", "Mission Phase", "Effect, Local",
            "Effect, Next", "Effect, End", "Detection Method", "Other "
            "Indications", "Isolation Method", "Design Provision",
            "Operator Actions", "Severity Class", "h(t) Data Source",
            "Failure Probability", 0.0, 0.0, 0.0, 0.0, 0.0, "Control Type",
            "RPN Severity", "RPN Occurrence", "RPN Detection", 0, "Action "
            "Category", "Action Owner", "Action Due Date", "Action Status",
            "Action Taken", 0, "Action Approval Date", 0,
            "Action Closure Date", "RPN New Severity", "RPN New Occurrence",
            "RPN New Detection", 0, 0, 0, 0, "Remarks", None, ""
        ]
        self._lst_missions: List[str] = [""]

        # Initialize private scalar attributes.
        self._item_hazard_rate: float = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkCriticality: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate Criticality"))
        self.chkRPN: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate RPNs"))
        self.txtItemCriticality: RAMSTKTextView = RAMSTKTextView(
            Gtk.TextBuffer())

        self._lst_widgets = [
            self.chkCriticality, self.chkRPN, self.txtItemCriticality
        ]

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_missions,
                      'succeed_get_usage_profile_attributes')
        pub.subscribe(self._do_load_tree, 'succeed_retrieve_hardware_fmea')

    def __do_load_action_category(self) -> None:
        """
        Load the action category Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[25])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY[_item][1]
            ])

    def __do_load_control_type(self) -> None:
        """
        Load the control type Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[20])
        for _item in RAMSTK_CONTROL_TYPES:
            _model.append([_item])

    def __do_load_failure_probability(self) -> None:
        """
        Load the failure probability Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[14])
        for _item in RAMSTK_FAILURE_PROBABILITY:
            _model.append([_item[0]])

    def __do_load_rpn_detection(self) -> None:
        """
        Load the RPN detection Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _detection = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION

        for _position in [23, 36]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_detection):
                _model.append([_detection[_item]['name']])

    def __do_load_rpn_occurrence(self) -> None:
        """
        Load the RPN occurrence Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _occurrence = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE

        for _position in [22, 35]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_occurrence):
                _model.append([_occurrence[_item]['name']])

    def __do_load_rpn_severity(self) -> None:
        """
        Load the RPN severity Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _severity = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY

        for _position in [21, 34]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_severity):
                _model.append([_severity[_item]['name']])

    def __do_load_severity_class(self) -> None:
        """
        Load the severity classification Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[12])
        for _item in RAMSTK_CRITICALITY:
            _model.append([_item[0]])

    def __do_load_status(self) -> None:
        """
        Load the action status Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[28])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS[_item][0]
            ])

    def __do_load_users(self) -> None:
        """
        Load the RAMSTK users Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[26])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS:
            _user = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS[_item][0]
                     + ", "
                     + self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS[_item][1])
            _model.append([_user])

    def __load_combobox(self) -> None:
        """
        Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        self.__do_load_action_category()
        self.__do_load_control_type()
        self.__do_load_failure_probability()
        self.__do_load_rpn_detection()
        self.__do_load_rpn_occurrence()
        self.__do_load_rpn_severity()
        self.__do_load_severity_class()
        self.__do_load_status()
        self.__do_load_users()

    def __make_ui(self) -> None:
        """
        Make the FMEA Work View page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        #
        # +-----+-----+---------------------------------+
        # |  B  |  W  |                                 |
        # |  U  |  I  |                                 |
        # |  T  |  D  |                                 |
        # |  T  |  G  |          SPREAD SHEET           |
        # |  O  |  E  |                                 |
        # |  N  |  T  |                                 |
        # |  S  |  S  |                                 |
        # +-----+-----+---------------------------------+
        #                                    buttons -----+--> self
        #                                                 |
        #  RAMSTKFixed ---+-->Gtk.VPaned -->RAMSTKFrame --+
        #                 |
        #  RAMSTKFrame ---+
        # Make the buttons.
        super().make_toolbuttons(
            icons=["insert_sibling", "insert_child", "remove", "calculate"],
            tooltips=[
                _("Add a new (D)FME(C)A entity at the same level as the "
                  "currently selected entity."),
                _("Add a new (D)FME(C)A entity one level below the currently "
                  "selected entity."),
                _("Remove the selected entity from the (D)FME(C)A."),
                _("Calculate the Task 102 criticality and/or risk priority "
                  "number (RPN).")
            ],
            callbacks=[
                self.do_request_insert_sibling, self.do_request_insert_child,
                self._do_request_delete, self._do_request_calculate
            ])
        super().make_ui_with_treeview(title=[
            "",
            _("(Design) Failure Mode, Effects, (and Criticality) Analysis "
              "[(D)FME(C)A]")
        ])

        # Set the tab label.
        _label = RAMSTKLabel(_("FMEA"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays failure mode and effects analysis (FMEA) "
                      "information for the selected Hardware"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions for the common FMEA widgets.

        :return: None
        :rtype: None
        """
        super().do_set_cell_callbacks('wvw_editing_fmea',
                                      self._lst_col_order[2:])

        self._lst_handler_id.append(
            self.treeview.connect("button_press_event", self._on_button_press))

    def __set_properties(self) -> None:
        """
        Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        # By default, calculate both Task 102 and RPN.
        self.chkCriticality.set_active(True)
        self.chkRPN.set_active(True)
        self.chkCriticality.do_set_properties(tooltip=_(
            "Select this option to calculate the MIL-STD-1629, Task 102 "
            "criticality analysis."))
        self.chkRPN.do_set_properties(tooltip=_(
            "Select this option to calculate the risk priority numbers "
            "(RPN)."))

        # ----- ENTRIES
        self.txtItemCriticality.do_set_properties(
            editable=False,
            height=75,
            tooltip=_(
                "Displays the MIL-STD-1629A, Task 102 item criticality for "
                "the selected hardware item."))

        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the (Design) Failure Mode and Effects "
              "(and Criticality) Analysis [(D)FME(C)A] for the "
              "currently selected Hardware item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the FMEA.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

    def _do_load_action(self, entity: RAMSTKAction,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load an action record into the RAMSTKTreeView().

        :param entity: the FMEA entity containing the data to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKAction`
        :param row: the parent row of the action to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with action data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["action"], 22, 22)

        _attributes = [
            str(entity.action_id), entity.action_recommended, "", "", "", "",
            "", "", "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "",
            "", "", "", 0, entity.action_category, entity.action_owner,
            entity.action_due_date.strftime('%Y-%m-%d'), entity.action_status,
            entity.action_taken, entity.action_approved,
            entity.action_approve_date.strftime('%Y-%m-%d'),
            entity.action_closed,
            entity.action_close_date.strftime('%Y-%m-%d'), "", "", "", 0, 0, 0,
            0, "", _icon,
            str(entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Actions had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "FMEA.")
            _debug_msg = (
                "Data for Action ID {0:s} for Hardware ID {1:s} is the wrong "
                "type for one or more columns.".format(str(entity.action_id),
                                                       str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Actions was missing some of it's "
                          "data and is not displayed in the FMEA.")
            _debug_msg = ("Too few fields for Action ID {0:s} for Hardware "
                          "ID {1:s}.".format(str(entity.action_id),
                                             str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_cause(self, entity: RAMSTKCause,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure cause record into the RAMSTKTreeView().

        :param entity: the FMEA entity containing the data to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKCause`
        :param row: the parent row of the cause to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with cause data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self._get_rpn_values(entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["cause"], 22, 22)

        _attributes = [
            str(entity.cause_id), entity.description, "", "", "", "", "", "",
            "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, entity.rpn_new, 0, 0, 0,
            "", _icon,
            str(entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Causes had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "FMEA.")
            _debug_msg = (
                "Data for Cause ID {0:s} for Hardware ID {1:s} is the wrong "
                "type for one or more columns.".format(str(entity.cause_id),
                                                       str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Causes was missing some of it's "
                          "data and is not displayed in the FMEA.")
            _debug_msg = ("Too few fields for Cause ID {0:s} for Hardware "
                          "ID {1:s}.".format(str(entity.cause_id),
                                             str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_control(self, entity: RAMSTKControl,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a control record into the RAMSTKTreeView().

        :param entity: the FMEA entity containing the data to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKControl`
        :param row: the parent row of the control to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with control data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["control"], 22, 22)

        _attributes = [
            str(entity.control_id), entity.description, "", "", "", "", "", "",
            "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0,
            entity.type_id, "", "", "", 0, "", "", "", "", "", 0, "", 0, "",
            "", "", "", 0, 0, 0, 0, "", _icon,
            str(entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Controls had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "FMEA.")
            _debug_msg = (
                "Data for Control ID {0:s} for Hardware ID {1:s} is the wrong "
                "type for one or more columns.".format(str(entity.control_id),
                                                       str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Controls was missing some of it's "
                          "data and is not displayed in the FMEA.")
            _debug_msg = ("Too few fields for Control ID {0:s} for Hardware "
                          "ID {1:s}.".format(str(entity.control_id),
                                             str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mechanism(self, entity: RAMSTKMechanism,
                           row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param entity: the FMEA entity containing the data to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKMechanism`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self._get_rpn_values(entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["mechanism"], 22, 22)

        _attributes = [
            str(entity.mechanism_id), entity.description, "", "", "", "", "",
            "", "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, entity.rpn_new,
            entity.pof_include, 0, 0, "", _icon,
            str(entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Mechanisms had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "FMEA.")
            _debug_msg = (
                "Data for Mechanism ID {0:s} for Hardware ID {1:s} is the "
                "wrong type for one or more columns.".format(
                    str(entity.mechanism_id), str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Mechanisms was missing some of it's "
                          "data and is not displayed in the FMEA.")
            _debug_msg = ("Too few fields for Mechanism ID {0:s} for Hardware "
                          "ID {1:s}.".format(str(entity.mechanism_id),
                                             str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_missions(self, attributes: treelib.Tree) -> None:
        """
        Load the mission and mission phase dicts.

        :param attributes: the treelib Tree() containing the usage profile.
        :type attributes: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _nid = attributes.root
        _model = self._get_cell_model(self._lst_col_order[2])
        _model.clear()

        self._lst_missions = [""]
        _model.append([""])
        for _node in attributes.children(_nid):
            _model.append([_node.tag])
            self._lst_missions.append(_node.tag)

    def _do_load_mission_phases(self, mission: str) -> None:
        """
        Load the mission phase Gtk.CellRendererCombo().

        :param str mission: the mission that was selected.
        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[3])
        _model.clear()
        _model.append([""])

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append([_phase])
        except KeyError:
            pass

    def _do_load_mode(self, entity: RAMSTKMode,
                      row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mode record into the RAMSTKTreeView().

        :param entity: the FMEA entity containing the data to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKMode`
        :param row: the parent row of the mode to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        _severity = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY[
            entity.rpn_severity]['description']
        _severity_new = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY[
            entity.rpn_severity_new]['description']
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self._dic_icons["mode"],
                                                       22, 22)

        _attributes = [
            str(entity.mode_id), entity.description, entity.mission,
            entity.mission_phase, entity.effect_local, entity.effect_next,
            entity.effect_end, entity.detection_method,
            entity.other_indications, entity.isolation_method,
            entity.design_provisions, entity.operator_actions,
            entity.severity_class, entity.hazard_rate_source,
            entity.mode_probability, entity.effect_probability,
            entity.mode_ratio, entity.mode_hazard_rate, entity.mode_op_time,
            entity.mode_criticality, "", _severity, "", "", 0, "", "", "", "",
            "", 0, "", 0, "", _severity_new, "", "", 0, entity.critical_item,
            entity.single_point, 0, entity.remarks, _icon,
            str(entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more failure modes had the wrong data type "
                          "in it's data package and is not displayed in the "
                          "FMEA.")
            _debug_msg = (
                "Data for Mode ID {0:s} for Hardware ID {1:s} is the wrong "
                "type for one or more columns.".format(str(entity.mode_id),
                                                       str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more failure modes was missing some of it's "
                          "data and is not displayed in the FMEA.")
            _debug_msg = ("Too few fields for Mode ID {0:s} for Hardware ID "
                          "{1:s}.".format(str(entity.mode_id),
                                          str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_tree(self, tree: treelib.Tree,
                      row: Gtk.TreeIter = None) -> None:
        """
        Iterate through tree and load the FMEA RAMSTKTreeView().

        :param tree: the treelib.Tree() containing the data packages for the
            (D)FME(C)A.
        :type tree: :class:`treelib.Tree`
        :param row: the last row to be loaded with FMEA data.
        :type row: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _new_row = None
        _model = self.treeview.get_model()

        _node = tree.nodes[list(tree.nodes.keys())[0]]
        _entity = _node.data
        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        if _entity is None:
            self._do_clear_page()
        else:
            [[__, _entity]] = _node.data.items()

        try:
            if _entity.is_mode:
                self._get_mission(_entity)
                _new_row = self._do_load_mode(_entity, row)
            elif _entity.is_mechanism:
                _new_row = self._do_load_mechanism(_entity, row)
            elif _entity.is_cause:
                _new_row = self._do_load_cause(_entity, row)
            elif _entity.is_control:
                _new_row = self._do_load_control(_entity, row)
            elif _entity.is_action:
                _new_row = self._do_load_action(_entity, row)
        except AttributeError:
            _user_msg = _("One or more FMEA line items was missing it's data "
                          "package and is not displayed in the FMEA.")
            _debug_msg = (
                "There is no data package for FMEA ID {0:s} for Hardware ID "
                "{1:s}.".format(str(_node.identifier), str(self._record_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        super().do_expand_tree()

    def _do_refresh_view(self, model: Gtk.TreeModel, __path: str,
                         row: Gtk.TreeIter) -> None:
        """
        Refresh the FMEA Work View after a successful calculation.

        :return: None
        :rtype: None
        """
        # if row is not None:
        #    _node_id = model.get_value(row, 43)

        #    _level = self._get_level(_node_id)
        #    _node = self._dtc_data_controller.request_do_select(_node_id)

        #    if _level == "mode":
        #        model.set_value(
        #            row,
        #            self._lst_col_order[17],
        #            _node.mode_hazard_rate,
        #        )
        #        model.set_value(
        #            row,
        #            self._lst_col_order[19],
        #            _node.mode_criticality,
        #        )
        #    elif _level in ["mechanism", "cause"]:
        #        model.set_value(row, self._lst_col_order[24], _node.rpn)
        #        model.set_value(row, self._lst_col_order[37], _node.rpn_new)
        # if not self._functional:
        #    _str_item_crit = ""
        #    _dic_item_crit = self._dtc_data_controller.request_item_criticality(
        #    )

        #    for _key in _dic_item_crit:
        #        _str_item_crit = _str_item_crit + _("{0:s}: {1:g}\n").format(
        #            _key,
        #            _dic_item_crit[_key],
        #        )

        #    self.txtItemCriticality.do_get_buffer().set_text(
        #        str(_str_item_crit), )

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Calculate the FMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()

        pub.sendMessage("request_calculate_dfmeca",
                        node_id=_model.get_value(_row, 43),
                        item_hr=self._item_hazard_rate,
                        criticality=self.chkCriticality.get_active(),
                        rpn=self.chkRPN.get_active())

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 43)

        pub.sendMessage("request_delete_fmea", node_id=_node_id)

    def _do_request_insert(self, **kwargs: Dict[str, Any]) -> None:
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _sibling = kwargs["sibling"]

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 43)
            _level = self._get_level(_node_id)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _level = "mode"
            _prow = None

        # Dict to hold the set of arguments to use for flow control.
        # Outer key is FMEA level.  Inner key determines whether sibling or
        # child is requested for insert.  Value is the entity ID, parent ID,
        # whether to raise ActionControl dialog, and if an undefined condition
        # exists (no child for control or action).
        _dic_args = {
            "mode": {
                True: [self._parent_id, _node_id, False, False],
                False: [_model.get_value(_prow, 0), _node_id, False, False]
            },
            "mechanism": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43), False, False
                ],
                False: [_model.get_value(_row, 0), _node_id, False, False]
            },
            "cause": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43), False, False
                ],
                False: [_model.get_value(_row, 0), _node_id, True, False]
            },
            "control": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43), True, False
                ],
                False: [_model.get_value(_row, 0), _node_id, True, True]
            },
            "action": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43), True, False
                ],
                False: [_model.get_value(_row, 0), _node_id, True, True]
            }
        }

        # The _entity_id is the RAMSTK Program database Hardware ID, Mode ID,
        # Mechanism ID, or Cause ID to add the new entity to.  The _parent_id
        # is the Node ID of the parent node in the treelib Tree().
        (_entity_id, _parent_id, _choose,
         _undefined) = _dic_args[_sibling][_level]

        if _undefined:
            _prompt = _(
                "A FMEA control or an action cannot have a child entity.")
            _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons["error"],
                                          "error")

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        if _choose:
            _dialog = AddControlAction()

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _control = _dialog.rdoControl.get_active()
                _action = _dialog.rdoAction.get_active()

                if _control:
                    _level = "control"
                elif _action:
                    _level = "action"

            _dialog.do_destroy()

        if not _undefined:
            pub.sendMessage("request_insert_fmea",
                            entity_id=_entity_id,
                            parent_id=_parent_id,
                            level=_level)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected entity in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 43)

        self.do_set_cursor(Gdk.CursorType.WATCH)
        if self._functional:
            pub.sendMessage("request_update_ffmea", node_id=_node_id)
        else:
            pub.sendMessage("request_update_dfmeca", node_id=_node_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_update_all_fmea")
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_set_headings(self, node_id: str) -> List[bool]:
        """
        Set the heading text for the FMEA columns.

        :return: _set_visible; a list of True/False for the columns to be
            set visible.
        :rtype: list
        """
        _set_visible = []

        if node_id.count(".") == 0:
            self._record_id = int(node_id)
            self.treeview.headings[self._lst_col_order[0]] = _("Mode ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Failure\nMode")
            _set_visible = self._do_set_visible_columns(self._lst_mode_mask)
        elif node_id.count(".") == 1:
            self.treeview.headings[self._lst_col_order[0]] = _("Mechanism ID")
            self.treeview.headings[self._lst_col_order[1]] = _(
                "Failure\nMechanism")
            _set_visible = self._do_set_visible_columns(
                self._lst_mechanism_mask)
        elif node_id.count(".") == 2:
            self.treeview.headings[self._lst_col_order[0]] = _("Cause ID")
            self.treeview.headings[self._lst_col_order[1]] = _(
                "Failure\nCause")
            _set_visible = self._do_set_visible_columns(self._lst_cause_mask)
        elif node_id.count(".") == 4 and node_id[-1] == "c":
            self.treeview.headings[self._lst_col_order[0]] = _("Control ID")
            self.treeview.headings[self._lst_col_order[1]] = _(
                "Existing\nControl")
            _set_visible = self._do_set_visible_columns(self._lst_control_mask)
        elif node_id.count(".") == 4 and node_id[-1] == "a":
            self.treeview.headings[self._lst_col_order[0]] = _("Action ID")
            self.treeview.headings[self._lst_col_order[1]] = _(
                "Recommended\nAction")
            _set_visible = self._do_set_visible_columns(self._lst_action_mask)

        return _set_visible

    def _do_set_visible_columns(self, mask: List[bool]) -> List[bool]:
        """
        Set the list of True/False for the visible FMEA columns.

        :param list mask: the list of True/False mask for the type of FMEA
            object selected.
        :return: _set_visible; a list of True/False for the columns to be
            set visible.
        :rtype: list
        """
        return self.treeview.visible and mask

    def _get_cell_model(self, column: int) -> Gtk.TreeModel:
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property("model")
        _model.clear()

        return _model

    def _get_mission(self, entity: object) -> None:
        """
        Retrieve the mission information.

        :param entity: the FMEA entity to get the mission information.
        :return: None
        :rtype: None
        """
        try:
            self._lst_fmea_data[2] = self._dic_missions[entity.mission]
        except (AttributeError, KeyError):
            self._lst_fmea_data[2] = ""

        try:
            self._lst_fmea_data[3] = self._dic_mission_phases[
                entity.mission_phase]
        except (AttributeError, KeyError):
            self._lst_fmea_data[3] = ""

    def _get_rpn_values(self, entity: object) -> Tuple[str, str, str, str]:
        """
        Retrieve the RPN category for the selected mechanism or cause.

        :param entity: the RAMSTKMechanism or RAMSTKCause object to be read.
        :type entity: :class:`ramstk.models.programdb.RAMSTKMechanism` or
            :class:`ramstk.models.programdb.RAMSTKCause`
        :return: (_occurrence, _detection, _occurrence_new, _detection_new)
        :rtype: tuple
        """
        _occurrence = str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[
            entity.rpn_occurrence]['description'])
        _detection = str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION[
            entity.rpn_detection]['description'])
        _occurrence_new = str(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[
                entity.rpn_occurrence_new]['description'])
        _detection_new = str(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION[
                entity.rpn_detection_new]['description'])

        return (_occurrence, _detection, _occurrence_new, _detection_new)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the FMEA Work View RAMSTKTreeView().

        :param treeview: the FMEA TreeView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.

        if event.button == 3:
            _icons = [
                "insert_sibling", "insert_child", "remove", "calculate", "save"
            ]
            _labels = [
                _("Insert Sibling"),
                _("Insert Child"),
                _("Remove"),
                _("Calculate"),
                _("Save")
            ]
            _callbacks = [
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_delete, self._do_request_calculate,
                self._do_request_update_all
            ]
            RAMSTKWorkView.on_button_press(self,
                                           event,
                                           icons=_icons,
                                           labels=_labels,
                                           callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the FMEA RAMSTKTreeView().
        :type treeview: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()
        try:
            _node_id = _model.get_value(_row, 0)
            _mission = _model.get_value(_row, 2)
        except TypeError:
            _node_id = '0'
            _mission = ""

        self._do_load_mission_phases(_mission)
        _set_visible = self._do_set_headings(_node_id)

        _columns = self.treeview.get_columns()
        i = 0
        for _heading in self.treeview.headings:
            _label = RAMSTKLabel(_heading)
            _label.do_set_properties(height=-1,
                                     justify=Gtk.Justification.CENTER,
                                     wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(_set_visible[self._lst_col_order[i]])

            i += 1

        selection.handler_unblock(self._lst_handler_id[0])
