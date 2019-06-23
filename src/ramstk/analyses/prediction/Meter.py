# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Reliability Calculations Module."""

# Standard Library Imports
import gettext

_ = gettext.gettext

PI_F = [1.0, 1.0, 2.8]


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id.  Current subcategory IDs are:
    #
    #    1. Elapsed Time
    #    2. Panel
    #
    # These keys return a list of base hazard rate lists.  The proper internal
    # list is selected by the type ID.  The hazard rate to use is selected from
    # the list depending on the active environment.
    _dic_lambda_b = {
        1: [
            [
                10.0,
                20.0,
                120.0,
                70.0,
                180.0,
                50.0,
                80.0,
                160.0,
                250.0,
                260.0,
                5.0,
                140.0,
                380.0,
                0.0,
            ],
            [
                15.0,
                30.0,
                180.0,
                105.0,
                270.0,
                75.0,
                120.0,
                240.0,
                375.0,
                390.0,
                7.5,
                210.0,
                570.0,
                0.0,
            ],
            [
                40.0,
                80.0,
                480.0,
                280.0,
                720.0,
                200.0,
                320.0,
                640.0,
                1000.0,
                1040.0,
                20.0,
                560.0,
                1520.0,
                0.0,
            ],
        ],
        2: [
            [
                0.09,
                0.36,
                2.3,
                1.1,
                3.2,
                2.5,
                3.8,
                5.2,
                6.6,
                5.4,
                0.099,
                5.4,
                0.0,
                0.0,
            ],
            [
                0.15,
                0.61,
                2.8,
                1.8,
                5.4,
                4.3,
                6.4,
                8.9,
                11.0,
                9.2,
                0.17,
                9.2,
                0.0,
                0.0,
            ],
        ],
    }
    _msg = ''

    # Select the base hazard rate.
    try:
        attributes['lambda_b'] = _dic_lambda_b[attributes['subcategory_id']][
            attributes['type_id'] - 1
        ][attributes['environment_active_id'] - 1]
    except (IndexError, KeyError):
        attributes['lambda_b'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = (
            "RAMSTK WARNING: Base hazard rate is 0.0 when calculating "
            "meter, hardware ID: {0:d}, subcategory ID: {1:d}, type "
            "ID: {3:d}, and active environment ID: {2:d}."
        ).format(
            attributes['hardware_id'],
            attributes['subcategory_id'],
            attributes['environment_active_id'],
            attributes['type_id'],
        )

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_lambda_b = {1: [20.0, 30.0, 80.0], 2: 0.09}
    _msg = ''

    # Calculate the temperature ratio.
    try:
        _temperature_ratio = (
            attributes['temperature_active'] /
            attributes['temperature_rated_max']
        )
    except ZeroDivisionError:
        _temperature_ratio = 1.0

    # Calculate the base hazard rate.
    if attributes['subcategory_id'] == 1:
        attributes['lambda_b'] = _dic_lambda_b[1][attributes['type_id'] - 1]
    elif attributes['subcategory_id'] == 2:
        attributes['lambda_b'] = _dic_lambda_b[2]
    else:
        attributes['lambda_b'] = 0.0

    if attributes['lambda_b'] <= 0.0:
        _msg = (
            "RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, "
            "hardware ID: {0:d}.\n"
        ).format(attributes['hardware_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + (
            "RAMSTK WARNING: piQ is 0.0 when calculating meter, hardware ID: "
            "{0:d}, quality ID: {1:d}.\n"
        ).format(
            attributes['hardware_id'],
            attributes['quality_id'],
        )

    if attributes['piE'] <= 0.0:
        _msg = _msg + (
            "RAMSTK WARNING: piE is 0.0 when calculating meter, hardware ID: "
            "{0:d}.\n"
        ).format(attributes['hardware_id'])

    # Determine the application factor (piA) and function factor (piF).
    if attributes['subcategory_id'] == 2:
        attributes['piA'] = (1.7 if (attributes['type_id']) - (1) else 1.0)
        attributes['piF'] = PI_F[attributes['application_id'] - 1]

    # Determine the temperature stress factor (piT).
    if attributes['subcategory_id'] == 1:
        if 0.0 < _temperature_ratio <= 0.5:
            attributes['piT'] = 0.5
        elif 0.5 < _temperature_ratio <= 0.6:
            attributes['piT'] = 0.6
        elif 0.6 < _temperature_ratio <= 0.8:
            attributes['piT'] = 0.8
        elif 0.8 < _temperature_ratio <= 1.0:
            attributes['piT'] = 1.0

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piF'] * attributes['piQ']
        )
    elif attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piT']
        )

    return attributes, _msg
