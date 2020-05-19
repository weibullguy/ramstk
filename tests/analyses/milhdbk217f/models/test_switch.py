# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_switch.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the switch module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import switch

ATTRIBUTES = {
    'category_id': 7,
    'subcategory_id': 1,
    'environment_active_id': 3,
    'construction_id': 1,
    'quality_id': 1,
    'application_id': 1,
    'contact_form_id': 2,
    'n_elements': 8,
    'current_ratio': 0.45,
    'n_cycles': 2.3,
    'piE': 2.0,
    'piQ': 1.3
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 5])
def test_get_part_count_lambda_b(subcategory_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = switch.get_part_count_lambda_b(subcategory_id, 3, 1)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.018, 5: 1.7}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = switch.get_part_count_lambda_b(27, 3, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_construction():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown construction ID."""
    with pytest.raises(KeyError):
        _lambda_b = switch.get_part_count_lambda_b(5, 3, 41)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = switch.get_part_count_lambda_b(2, 32, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float value for the base hazard rate on success."""
    _lambda_b = switch.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.018


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 5, 31])
@pytest.mark.parametrize("construction_id", [1, 2])
def test_calculate_part_stress_lambda_b(subcategory_id, construction_id):
    """calculate_part_stress_lambda_b() should return a float value for the part stress base hazard rate on success."""
    _lambda_b = switch.calculate_part_stress_lambda_b(subcategory_id, 1,
                                                      construction_id, 1, 8)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and construction_id == 1:
        assert _lambda_b == 0.00045
    elif subcategory_id == 1 and construction_id == 2:
        assert _lambda_b == 0.0027
    elif subcategory_id == 2 and construction_id == 1:
        assert _lambda_b == pytest.approx(0.1036)
    elif subcategory_id == 2 and construction_id == 2:
        assert _lambda_b == 0.1072
    elif subcategory_id == 4:
        assert _lambda_b == 0.5027
    elif subcategory_id == 5:
        assert _lambda_b == 0.02
    elif subcategory_id == 31:
        assert _lambda_b == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_quality():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown quality ID."""
    with pytest.raises(IndexError):
        _lambda_b = switch.calculate_part_stress_lambda_b(1, 21, 1, 1, 8)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_application():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown application ID."""
    with pytest.raises(IndexError):
        _lambda_b = switch.calculate_part_stress_lambda_b(5, 1, 1, 21, 8)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_construction():
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown construction ID."""
    with pytest.raises(KeyError):
        _lambda_b = switch.calculate_part_stress_lambda_b(1, 1, 41, 1, 8)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 5])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return the switch attributes dict with updated values."""
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = switch.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == 0.00045
        assert _attributes['piCYC'] == 2.3
        assert _attributes['piL'] == pytest.approx(1.372187594)
        assert _attributes['piC'] == 1.5
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0042606425)
    elif subcategory_id == 2:
        assert _attributes['lambda_b'] == pytest.approx(0.10360)
        assert _attributes['piCYC'] == 2.3
        assert _attributes['piL'] == pytest.approx(1.372187594)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.65392972)
    elif subcategory_id == 5:
        assert _attributes['lambda_b'] == 0.02
        assert _attributes['piC'] == 2.0
        assert _attributes['piU'] == 1.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.104)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_load_stress_resistive():
    """calculate_load_stress() should return a float when calculating resistive load stress."""
    _pi_l = switch.calculate_load_stress_factor(1, 0.2)

    assert _pi_l == pytest.approx(1.064494459)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_load_stress_inductive():
    """calculate_load_stress() should return a float when calculating inductive load stress."""
    _pi_l = switch.calculate_load_stress_factor(2, 0.2)

    assert _pi_l == pytest.approx(1.284025417)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_load_stress_capacitive():
    """calculate_load_stress() should return a float when calculating capacitive load stress."""
    _pi_l = switch.calculate_load_stress_factor(3, 0.2)

    assert _pi_l == pytest.approx(2.718281828)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_load_stress_nothing():
    """calculate_load_stress() should return 0.0 when calculating load stress for unknown load type."""
    _pi_l = switch.calculate_load_stress_factor(13, 0.2)

    assert _pi_l == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_picyc_one():
    """calculate_part_stress() should set piCYC=1.0 when n_cycles < 1.0."""
    ATTRIBUTES['n_cycles'] = 0.05
    _attributes = switch.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['piCYC'] == 1.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_base():
    """calculate_part_stress() should return an active h(t)=0.0 for subcategories>5."""
    ATTRIBUTES['piE'] = 6
    ATTRIBUTES['subcategory_id'] = 6
    _attributes = switch.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_active'] == 0.0
