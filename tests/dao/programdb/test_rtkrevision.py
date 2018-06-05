# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkrevision.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKRevision module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKRevision import RTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


ATTRIBUTES = {
            'revision_id': 1,
            'availability_logistics': 1.0,
            'availability_mission': 1.0,
            'cost': 0.0,
            'cost_per_failure': 0.0,
            'cost_per_hour': 0.0,
            'hazard_rate_active': 0.0,
            'hazard_rate_dormant': 0.0,
            'hazard_rate_logistics': 0.0,
            'hazard_rate_mission': 0.0,
            'hazard_rate_software': 0.0,
            'mmt': 0.0,
            'mcmt': 0.0,
            'mpmt': 0.0,
            'mtbf_logistics': 0.0,
            'mtbf_mission': 0.0,
            'mttr': 0.0,
            'name': 'Test Revision',
            'reliability_logistics': 1.0,
            'reliability_mission': 1.0,
            'remarks': '',
            'n_parts': 0,
            'revision_code': '',
            'program_time': 0.0,
            'program_time_sd': 0.0,
            'program_cost': 0.0,
            'program_cost_sd': 0.0
        }


@pytest.mark.integration
def test_rtkrevision_create(test_dao):
    """ __init__() should create an RTKRevision model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    assert isinstance(DUT, RTKRevision)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_revision'
    assert DUT.revision_id == 1
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.cost == 0.0
    assert DUT.cost_failure == 0.0
    assert DUT.cost_hour == 0.0
    assert DUT.hazard_rate_active == 0.0
    assert DUT.hazard_rate_dormant == 0.0
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.hazard_rate_software == 0.0
    assert DUT.mmt == 0.0
    assert DUT.mcmt == 0.0
    assert DUT.mpmt == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mttr == 0.0
    assert DUT.name == 'Test Revision'
    assert DUT.reliability_logistics == 1.0
    assert DUT.reliability_mission == 1.0
    assert DUT.remarks == ''
    assert DUT.total_part_count == 1
    assert DUT.revision_code == ''
    assert DUT.program_time == 0.0
    assert DUT.program_time_sd == 0.0
    assert DUT.program_cost == 0.0
    assert DUT.program_cost_sd == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of {attr name:attr value} pairs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    _values = DUT.get_attributes()

    assert _values['availability_logistics'] == ATTRIBUTES['availability_logistics']


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKRevision {0:d} "
                    "attributes.".format(DUT.revision_id))


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """ set_attributes() should return a 40 error code when passed an attribute dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    ATTRIBUTES.pop('name')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'name' in attribute "
                    "dictionary passed to RTKRevision.set_attributes().")
