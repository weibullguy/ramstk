# -*- coding: utf-8 -*-
#
#       ramstk.logger.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Logger Module."""

# Standard Library Imports
import logging
import os
import sys

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import file_exists

LOGFORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(lineno)s : %(message)s')


class RAMSTKLogManager:
    """Class to manage logging of RAMSTK messages."""
    def __init__(self, log_file: str) -> None:
        """
        Initialize an instance of the LogManager.

        :param str log_file: the absolute path to the log file to use with this
            log manager.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.loggers = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.log_file = log_file

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_log_fail_message,
                      'fail_connect_program_database')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_environment')
        pub.subscribe(self._do_log_fail_message,
                      'fail_delete_failure_definition')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_fmea')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_function')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_hazard')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_mission')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_mission_phase')
        pub.subscribe(self._do_log_fail_message, 'fail_delete_revision')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_action')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_cause')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_control')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_environment')
        pub.subscribe(self._do_log_fail_message,
                      'fail_insert_failure_definition')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mechanism')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mission')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mission_phase')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_mode')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_function')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_hazard')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_hardware')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_validation')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_stakeholder')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_revision')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_requirement')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_opload')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_opstress')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_record')
        pub.subscribe(self._do_log_fail_message, 'fail_insert_test_method')
        pub.subscribe(self._do_log_fail_message, 'fail_update_fmea')
        pub.subscribe(self._do_log_fail_message, 'fail_update_function')
        pub.subscribe(self._do_log_fail_message, 'fail_update_hardware')
        pub.subscribe(self._do_log_fail_message, 'fail_update_record')
        pub.subscribe(self._do_log_fail_message, 'fail_update_requirement')
        pub.subscribe(self._do_log_fail_message, 'fail_update_revision')

        if file_exists(self.log_file):
            os.remove(self.log_file)

        # Create a logger for the pypubsub fail_* messages.
        self.do_create_logger(__name__, "WARN")

    #// TODO: Update fail messages to pass error_message
    #//
    #// The logger._do_log_fail_message() method takes the argument
    #// error_message.  Several data managers broadcast error_msg instead.
    #// These need to be updated so all fail_XX_XX messages broadcast an
    #// error_message.
    def _do_log_fail_message(self, error_message: str) -> None:
        """
        Log PyPubSub broadcast fail messages.

        :param str error_message: the error message that was part of the
            broadcast package.
        :return: None
        :rtype: None
        """
        self.loggers[__name__].warning(error_message)

    @staticmethod
    def _get_console_handler() -> logging.Handler:
        """
        Create the log handler for console output.

        :return: _c_handler
        :rtype: :class:`logging.Handler`
        """
        _c_handler = logging.StreamHandler(sys.stdout)
        _c_handler.setFormatter(LOGFORMAT)

        return _c_handler

    def _get_file_handler(self) -> logging.Handler:
        """
        Create the log handler for file output.

        :return: _f_handler
        :rtype: :class:`logging.Handler`
        """
        _f_handler = logging.FileHandler(self.log_file)
        _f_handler.setFormatter(LOGFORMAT)

        return _f_handler

    def do_create_logger(self,
                         logger_name: str,
                         log_level: str,
                         to_tty: bool = False) -> None:
        """
        Create a logger instance.

        :param str logger_name: the name of the logger used in the application.
        :param str log_level: the level of messages to log.
        :param str log_file: the full path of the log file for this logger
            instance to write to.
        :keyword boolean to_tty: boolean indicating whether this logger will
            also dump messages to the terminal.
        :return: None
        :rtype: None
        """
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(log_level)

        _logger.addHandler(self._get_file_handler())
        if to_tty:
            _logger.addHandler(self._get_console_handler())

        self.loggers[logger_name] = _logger

    def do_log_debug(self, logger_name: str, message: str) -> None:
        """
        Log DEBUG level messages.

        :param str logger_name: the name of the logger used in the application.
        :param str message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].debug(message)

    def do_log_exception(self, logger_name: str, exception: object) -> None:
        """
        Log EXCEPTIONS.

        :param str logger_name: the name of the logger used in the application.
        :param str exception: the exception to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].exception(exception)

    def do_log_info(self, logger_name: str, message: str) -> None:
        """
        Log INFO level messages.

        :param str logger_name: the name of the logger used in the application.
        :param str message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].info(message)

    def do_log_warning(self, logger_name: str, message: str) -> None:
        """
        Log WARN level messages.

        :param str logger_name: the name of the logger used in the application.
        :param str message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].warning(message)

    def do_log_error(self, logger_name: str, message: str) -> None:
        """
        Log ERROR level messages.

        :param str logger_name: the name of the logger used in the application.
        :param str message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].error(message)

    def do_log_critical(self, logger_name: str, message: str) -> None:
        """
        Log CRITICAL level messages.

        :param str logger_name: the name of the logger used in the application.
        :param str message: the message to log.
        :return: None
        :rtype: None
        """
        self.loggers[logger_name].critical(message)