#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.__main__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RAMSTK application."""

# Standard Library Imports
from time import sleep
from typing import Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk import RAMSTKProgramManager
from ramstk.configuration import (
    RAMSTK_CRITICALITY, RAMSTK_FAILURE_PROBABILITY,
    RAMSTKSiteConfiguration, RAMSTKUserConfiguration
)
from ramstk.controllers import (
    amFMEA, amHardware, amHazards, amStakeholder, amValidation,
    dmFailureDefinition, dmFMEA, dmFunction, dmHardware, dmHazards, dmOptions,
    dmPoF, dmRequirement, dmRevision, dmStakeholder, dmUsageProfile,
    dmValidation, mmFunction, mmHardware, mmRequirement, mmValidation
)
from ramstk.db.base import BaseDatabase
from ramstk.db.common import do_load_variables
from ramstk.exim import Export, Import
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, RAMSTKDesktop


def do_connect_to_site_db(conn_info, logger) -> BaseDatabase:
    """Connect to the site (common) database.

    :param dict conn_info: the site database connection information.
    :param logger: the RAMSTKLogManager() to use for logging status.
    :type logger: :class:`RAMSTKLogManager`
    :return:
    """
    logger.do_log_info(
        __name__, "Connecting to the RAMSTK common database {0:s}.".format(
            conn_info['database']))
    _site_db = BaseDatabase()
    _site_db.do_connect(conn_info)
    logger.do_log_info(
        __name__, "Connected to the RAMSTK common database {0:s}.".format(
            conn_info['database']))

    return _site_db


def do_copy_configuration_values(
        user_configuration: RAMSTKUserConfiguration,
        site_configuration: RAMSTKSiteConfiguration
) -> RAMSTKUserConfiguration:
    """Copy some values from the site configuration to the user configuration.

    :param user_configuration: the instance of the RAMSTKUserConfiguration()
        to add volatile data to.
    :type user_configuration: :class:`RAMSTKUserConfiguration`
    :param site_configuration: the instance of the RAMSTKSiteConfiguration() to
        add volatile data from.
    :type site_configuration: :class:`RAMSTKSiteConfiguration`
    :return: None
    :rtype: None
    """
    user_configuration.RAMSTK_ACTION_CATEGORY = \
        site_configuration.RAMSTK_ACTION_CATEGORY
    user_configuration.RAMSTK_ACTION_STATUS = \
        site_configuration.RAMSTK_ACTION_STATUS
    user_configuration.RAMSTK_AFFINITY_GROUPS = \
        site_configuration.RAMSTK_AFFINITY_GROUPS
    user_configuration.RAMSTK_CATEGORIES = \
        site_configuration.RAMSTK_CATEGORIES
    user_configuration.RAMSTK_CRITICALITY = RAMSTK_CRITICALITY
    user_configuration.RAMSTK_DAMAGE_MODELS = \
        site_configuration.RAMSTK_DAMAGE_MODELS
    user_configuration.RAMSTK_FAILURE_PROBABILITY = RAMSTK_FAILURE_PROBABILITY
    user_configuration.RAMSTK_HAZARDS = site_configuration.RAMSTK_HAZARDS
    user_configuration.RAMSTK_LOAD_HISTORY = \
        site_configuration.RAMSTK_LOAD_HISTORY
    user_configuration.RAMSTK_MANUFACTURERS = \
        site_configuration.RAMSTK_MANUFACTURERS
    user_configuration.RAMSTK_MEASURABLE_PARAMETERS = \
        site_configuration.RAMSTK_MEASURABLE_PARAMETERS
    user_configuration.RAMSTK_MEASUREMENT_UNITS = \
        site_configuration.RAMSTK_MEASUREMENT_UNITS
    user_configuration.RAMSTK_REQUIREMENT_TYPE = \
        site_configuration.RAMSTK_REQUIREMENT_TYPE
    user_configuration.RAMSTK_RPN_DETECTION = \
        site_configuration.RAMSTK_RPN_DETECTION
    user_configuration.RAMSTK_RPN_OCCURRENCE = \
        site_configuration.RAMSTK_RPN_OCCURRENCE
    user_configuration.RAMSTK_RPN_SEVERITY = \
        site_configuration.RAMSTK_RPN_SEVERITY
    user_configuration.RAMSTK_STAKEHOLDERS = \
        site_configuration.RAMSTK_STAKEHOLDERS
    user_configuration.RAMSTK_SUBCATEGORIES = \
        site_configuration.RAMSTK_SUBCATEGORIES
    user_configuration.RAMSTK_USERS = site_configuration.RAMSTK_USERS
    user_configuration.RAMSTK_VALIDATION_TYPE = \
        site_configuration.RAMSTK_VALIDATION_TYPE
    user_configuration.RAMSTK_WORKGROUPS = site_configuration.RAMSTK_WORKGROUPS

    return user_configuration


def do_read_site_configuration(logger: RAMSTKLogManager) -> \
        RAMSTKSiteConfiguration:
    """Create a site configuration instance.

    :param logger: the logging.Logger() instance to use for writing to the
        runtime log file.
    :type logger: :class:`logging.Logger`
    :return: _configuration; the RAMSTKSiteConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKSiteConfiguration`
    """
    def on_fail_create_site_configuration(error_message: str) -> None:
        """Logs the error message when there's a failure to create the site
        conf.

        :param str error_message: the error message raised by the failure.
        :return: None
        :rtype: None
        """
        logger.do_log_error(__name__, error_message)

    pub.subscribe(on_fail_create_site_configuration,
                  'fail_create_site_configuration')

    logger.do_log_info(__name__, "Reading the site configuration file.")

    _configuration = RAMSTKSiteConfiguration()
    _configuration.set_site_directories()
    _configuration.get_site_configuration()

    logger.do_log_info(__name__, "Read the site configuration file.")

    return _configuration


def do_read_user_configuration(
) -> Tuple[RAMSTKUserConfiguration, RAMSTKLogManager]:
    """Create a user configuration instance.

    :return: _configuration; the RAMSTKUserConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKUserConfiguration`
    """
    def on_fail_create_user_configuration(error_message: str) -> None:
        """Logs the error message when there's a failure to create the user
        conf.

        :param str error_message: the error message raised by the failure.
        :return: None
        :rtype: None
        """
        print(error_message)

    pub.subscribe(on_fail_create_user_configuration,
                  'fail_create_user_configuration')

    _configuration = RAMSTKUserConfiguration()
    _configuration.set_user_directories()
    _configuration.get_user_configuration()

    _logger: RAMSTKLogManager = RAMSTKLogManager(
        _configuration.RAMSTK_USER_LOG)
    _logger.do_create_logger(__name__,
                             _configuration.RAMSTK_LOGLEVEL,
                             to_tty=False)

    return _configuration, _logger


def the_one_ring() -> None:
    """Execute the main function for RAMSTK."""
    #// TODO: Implement splash screen.
    #//
    #// Add a splash screen to the launch of RAMSTK.
    #//
    #// labels: globalbacklog, normal
    # splScreen = SplashScreen()

    # Read the user configuration file and create a logger.  The user
    # configuration file contains information needed to create the logger so
    # it must come first.
    user_configuration, _logger = do_read_user_configuration()
    site_configuration = do_read_site_configuration(_logger)

    site_db = do_connect_to_site_db(site_configuration.RAMSTK_COM_INFO,
                                    _logger)

    _logger.do_log_debug(__name__, "Validating the RAMSTK license.")
    _logger.do_log_debug(__name__, "Validated the RAMSTK license.")

    _logger.do_log_info(__name__,
                        "Loading global RAMSTK configuration variables.")
    do_load_variables(site_db, site_configuration)
    _logger.do_log_info(__name__,
                        "Loaded global RAMSTK configuration variables.")

    # Copy some site-level configuration variables to the user-level
    # configuration.  These are used to load RAMSTKComboBox widgets with
    # information during initialization.  This is the easiest way to make
    # this information available without refactoring all the views to pass
    # the site configuration object in addition to the user configuration
    # object.
    user_configuration = do_copy_configuration_values(user_configuration,
                                                      site_configuration)

    _logger.do_log_info(__name__, "Initializing the RAMSTK application.")
    _program_mgr = RAMSTKProgramManager()
    _program_mgr.dic_managers['revision']['data'] = dmRevision()
    _program_mgr.dic_managers['function']['data'] = dmFunction()
    _program_mgr.dic_managers['function']['matrix'] = mmFunction()
    _program_mgr.dic_managers['hazards']['analysis'] = amHazards(
        user_configuration)
    _program_mgr.dic_managers['hazards']['data'] = dmHazards()
    _program_mgr.dic_managers['requirement']['data'] = dmRequirement()
    _program_mgr.dic_managers['requirement']['matrix'] = mmRequirement()
    _program_mgr.dic_managers['stakeholder']['analysis'] = amStakeholder(
        user_configuration)
    _program_mgr.dic_managers['stakeholder']['data'] = dmStakeholder()
    _program_mgr.dic_managers['hardware']['analysis'] = amHardware(
        user_configuration)
    _program_mgr.dic_managers['hardware']['data'] = dmHardware()
    _program_mgr.dic_managers['hardware']['matrix'] = mmHardware()
    _program_mgr.dic_managers['failure_definition']['data'] = \
        dmFailureDefinition()
    _program_mgr.dic_managers['fmea']['analysis'] = amFMEA(user_configuration)
    _program_mgr.dic_managers['fmea']['data'] = dmFMEA()
    _program_mgr.dic_managers['pof']['data'] = dmPoF()
    _program_mgr.dic_managers['usage_profile']['data'] = dmUsageProfile()
    _program_mgr.dic_managers['validation']['analysis'] = amValidation(
        user_configuration)
    _program_mgr.dic_managers['validation']['data'] = dmValidation()
    _program_mgr.dic_managers['validation']['matrix'] = mmValidation()
    # noinspection PyTypeChecker
    _program_mgr.dic_managers['options']['data'] = dmOptions(
        common_dao=site_db,
        site_configuration=site_configuration,
        user_configuration=user_configuration)
    _program_mgr.dic_managers['exim']['export'] = Export()
    _program_mgr.dic_managers['exim']['import'] = Import()
    _program_mgr.user_configuration = user_configuration
    _logger.do_log_info(__name__, "Initialized the RAMSTK application.")

    _logger.do_log_info(__name__, "Launching RAMSTK GUI.")

    # If you don't do this, the splash screen will show, but won't render it's
    # contents
    # while Gtk.events_pending():
    #     Gtk.main_iteration()

    sleep(1)
    # splScreen.window.destroy()

    # Create the RAMSTK Book.  This needs to be initialized after reading the
    # configuration and creating the logger.
    RAMSTKDesktop([user_configuration, site_configuration], _logger)

    _logger.do_log_info(__name__, "Launched RAMSTK GUI.")

    Gtk.main()