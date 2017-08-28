#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestCause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
This is the test class for testing the Cause class.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea.Cause import Model, Cause, OutOfRangeError
from dao import DAO
from dao import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class Test00CauseModel(unittest.TestCase):
    """
    Class for testing the Cause model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Cause model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKCause(), ], self.session)
        self.dao.db_add([RTKCause(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_cause_create(self):
        """
        (TestCauseModel) __init__ should return instance of Cause data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestCauseModel): select_all() should return a Tree() object populated
        with RTKCause instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKCause))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestCauseModel): select() should return an instance of the RTKCause data model on success.
        """

        self.DUT.select_all(1)
        _cause = self.DUT.select(1)

        self.assertTrue(isinstance(_cause, RTKCause))
        self.assertEqual(_cause.cause_id, 1)
        self.assertEqual(_cause.description, 'This is a failure cause.')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestCauseModel): select() should return None when a non-existent Cause ID is requested.
        """

        _cause = self.DUT.select(100)

        self.assertEqual(_cause, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestCauseModel): insert() should return a zero error code on success
        when inserting a hardware failure Cause.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mechanism_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestCauseModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestCauseModel): delete() should return a non-zero error code when
        passed a Cause ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2025)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Cause ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestCauseModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _cause = self.DUT.tree.get_node(1).data
        _cause.description = 'This is a failure cause.'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestCauseModel): update() should return a non-zero error code when
        passed a Cause ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2026)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Cause ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """
        (TestCauseModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_rpn_out_of_range_severity_inputs(self):
        """
        (TestCauseModel) calculate_rpn() raises OutOfRangeError for 11 < severity inputs < 0
        """

        self.DUT.select_all(1)

        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 0, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 11, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 0)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 11)

    @attr(all=True, unit=True)
    def test07b_calculate_rpn_out_of_range_occurrence_inputs(self):
        """
        (TestCauseModel) calculate_rpn() raises OutOfRangeError for 11 < occurrence inputs < 0
        """

        self.DUT.select_all(1)

        self.DUT.rpn_occurrence = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 1)
        self.DUT.rpn_occurrence = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 1)

    @attr(all=True, unit=True)
    def test07c_calculate_rpn_out_of_range_new_occurrence_inputs(self):
        """
        (TestCauseModel) calculate_rpn() raises OutOfRangeError for 11 < new occurrence inputs < 0
        """

        self.DUT.select_all(1)

        self.DUT.rpn_occurrence_new = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 1)
        self.DUT.rpn_occurrence_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 1)

    @attr(all=True, unit=True)
    def test07d_calculate_rpn_out_of_range_detection_inputs(self):
        """
        (TestCauseModel) calculate_rpn() raises OutOfRangeError for 11 < detection inputs < 0
        """

        self.DUT.select_all(1)

        self.DUT.rpn_detection = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 10)
        self.DUT.rpn_detection = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 10)

    @attr(all=True, unit=True)
    def test07e_calculate_rpn_out_of_range_new_detection_inputs(self):
        """
        (TestCauseModel) calculate_rpn raises OutOfRangeError for 11 < new detection inputs < 0
        """

        self.DUT.select_all(1)

        self.DUT.rpn_detection_new = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 10)
        self.DUT.rpn_detection_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1, 10)


class Test01CauseController(unittest.TestCase):
    """
    Class for testing the FMEA Cause data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Cause model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKCause(), ], self.session)
        self.dao.db_add([RTKCause(), ], self.session)

        self.DUT = Cause(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test_cause_create(self):
        """
        (TestCauseController) __init__ should return instance of Cause data controller
        """

        self.assertTrue(isinstance(self.DUT, Cause))
        self.assertTrue(isinstance(self.DUT._dtm_cause, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """
        (TestCauseController) request_select_all() should return a Tree of
        RTKCause models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKCause))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestCauseController) request_select() should return an RTKCause model.
        """

        self.DUT.request_select_all(1)

        _cause = self.DUT.request_select(1)

        self.assertTrue(isinstance(_cause, RTKCause))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """
        (TestCauseController) request_select() should return None when
        requesting a Cause that doesn't exist.
        """

        _cause = self.DUT.request_select(100)

        self.assertEqual(_cause, None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """
        (TestCauseController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(mechanism_id=1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestCauseController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.DUT.request_insert(mechanism_id=1)

        self.assertFalse(self.DUT.request_delete(
            self.DUT._dtm_cause.last_id))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestCauseController) request_delete() should return True when
        attempting to delete a non-existent Cause.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """
        (TestCauseController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """
        (TestCauseController) request_update() should return True when
        attempting to save a non-existent Cause.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestCauseController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_request_calculate_rpn(self):
        """
        (TestCauseController) request_calculate_rpn() should return False on success.
        """

        self.DUT.request_select_all(1)
        _cause = self.DUT.request_select(1)
        _cause.rpn_detection = 10
        _cause.rpn_detection_new = 5
        _cause.rpn_occurrence = 5
        _cause.rpn_occurrence_new = 4

        self.assertFalse(self.DUT.request_calculate_rpn(1, 10, 5))
        self.assertAlmostEqual(_cause.rpn, 500)
        self.assertAlmostEqual(_cause.rpn_new, 100)
