#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKRPN.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKRPN module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RAMSTKRPN import RAMSTKRPN

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKRPN(unittest.TestCase):
    """
    Class for testing the RAMSTKRPN class.
    """

    attributes = (1, 'None', 'No effect.', 'severity', 1)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKRPN class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKRPN).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.rpn_type = self.attributes[3]
        self.DUT.value = self.attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RAMSTKRPN_create(self):
        """
        (TestRAMSTKRPN) __init__ should create an RAMSTKRPN model
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKRPN))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_rpn')
        self.assertEqual(self.DUT.rpn_id, 1)
        self.assertEqual(self.DUT.description, 'No effect.')
        self.assertEqual(self.DUT.name, 'None')
        self.assertEqual(self.DUT.rpn_type, 'severity')
        self.assertEqual(self.DUT.value, 1)

    @attr(all=True, unit=True)
    def test01_RAMSTKRPN_get_attributes(self):
        """
        (TestRAMSTKRPN) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RAMSTKRPN_set_attributes(self):
        """
        (TestRAMSTKRPN) set_attributes should return a zero error code on success
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity', 8)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKRPN {0:d} " \
                               "attributes.".format(self.DUT.rpn_id))

    @attr(all=True, unit=True)
    def test02b_RAMSTKRPN_set_attributes_to_few(self):
        """
        (TestRAMSTKRPN) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKRPN.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RAMSTKRPN_set_attributes_wrong_type(self):
        """
        (TestRAMSTKRPN) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity', 'eight')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more RAMSTKRPN " \
                               "attributes.")
