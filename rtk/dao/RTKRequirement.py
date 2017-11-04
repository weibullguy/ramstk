# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRequirement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKRequirement Table
===============================================================================
"""

from datetime import date
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKRequirement(RTK_BASE):
    """
    Class to represent the rtk_requirement table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_requirement'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    requirement_id = Column('fld_requirement_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    derived = Column('fld_derived', Integer, default=0)
    description = Column('fld_description', BLOB, default='')
    figure_number = Column('fld_figure_number', String(256), default='')
    owner_id = Column('fld_owner_id', Integer, default=0)
    page_number = Column('fld_page_number', String(256), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    priority = Column('fld_priority', Integer, default=0)
    requirement_code = Column('fld_requirement_code', String(256), default='')
    specification = Column('fld_specification', String(256), default='')
    type_id = Column('fld_type_id', Integer, default=0)
    validated = Column('fld_validated', Integer, default=0)
    validated_date = Column('fld_validated_date', Date,
                            default=date.today())

    # Clarity of requirement questions.
    q_clarity_0 = Column('fld_clarity_0', Integer, default=0)
    q_clarity_1 = Column('fld_clarity_1', Integer, default=0)
    q_clarity_2 = Column('fld_clarity_2', Integer, default=0)
    q_clarity_3 = Column('fld_clarity_3', Integer, default=0)
    q_clarity_4 = Column('fld_clarity_4', Integer, default=0)
    q_clarity_5 = Column('fld_clarity_5', Integer, default=0)
    q_clarity_6 = Column('fld_clarity_6', Integer, default=0)
    q_clarity_7 = Column('fld_clarity_7', Integer, default=0)
    q_clarity_8 = Column('fld_clarity_8', Integer, default=0)

    # Completeness of requirement questions.
    q_complete_0 = Column('fld_complete_0', Integer, default=0)
    q_complete_1 = Column('fld_complete_1', Integer, default=0)
    q_complete_2 = Column('fld_complete_2', Integer, default=0)
    q_complete_3 = Column('fld_complete_3', Integer, default=0)
    q_complete_4 = Column('fld_complete_4', Integer, default=0)
    q_complete_5 = Column('fld_complete_5', Integer, default=0)
    q_complete_6 = Column('fld_complete_6', Integer, default=0)
    q_complete_7 = Column('fld_complete_7', Integer, default=0)
    q_complete_8 = Column('fld_complete_8', Integer, default=0)
    q_complete_9 = Column('fld_complete_9', Integer, default=0)

    # Consitency of requirement questions.
    q_consistent_0 = Column('fld_consistent_0', Integer, default=0)
    q_consistent_1 = Column('fld_consistent_1', Integer, default=0)
    q_consistent_2 = Column('fld_consistent_2', Integer, default=0)
    q_consistent_3 = Column('fld_consistent_3', Integer, default=0)
    q_consistent_4 = Column('fld_consistent_4', Integer, default=0)
    q_consistent_5 = Column('fld_consistent_5', Integer, default=0)
    q_consistent_6 = Column('fld_consistent_6', Integer, default=0)
    q_consistent_7 = Column('fld_consistent_7', Integer, default=0)
    q_consistent_8 = Column('fld_consistent_8', Integer, default=0)

    # Verifiablity of requirement questions.
    q_verifiable_0 = Column('fld_verifiable_0', Integer, default=0)
    q_verifiable_1 = Column('fld_verifiable_1', Integer, default=0)
    q_verifiable_2 = Column('fld_verifiable_2', Integer, default=0)
    q_verifiable_3 = Column('fld_verifiable_3', Integer, default=0)
    q_verifiable_4 = Column('fld_verifiable_4', Integer, default=0)
    q_verifiable_5 = Column('fld_verifiable_5', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='requirement')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Requirement data model
        attributes.

        :return: (revsion_id, requirement_id, description, requirement_code,
                  requirement_type, priority, specification, page_number,
                  figure_number, derived, owner, validated, validated_date,
                  parent_id, q_clarity_0, q_clarity_1, q_clarity_2,
                  q_clarity_3, q_clarity_4, q_clarity_5, q_clarity_6,
                  q_clarity_7, q_clarity_8, q_complete_0, q_complete_1,
                  q_complete_2, q_complete_3, q_complete_4, q_complete_5,
                  q_complete_6, q_complete_7, q_complete_8, q_complete_9,
                  q_consistent_0, q_consistent_1, q_consistent_2,
                  q_consistent_3, q_consistent_4, q_consistent_5,
                  q_consistent_6, q_consistent_7, q_consistent_8,
                  q_verifiable_0, q_verifiable_1, q_verifiable_2,
                  q_verifiable_3, q_verifiable_4, q_verifiable_5)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.requirement_id, self.derived,
                       self.description, self.figure_number, self.owner_id,
                       self.page_number, self.parent_id, self.priority,
                       self.requirement_code, self.specification,
                       self.type_id, self.validated, self.validated_date,
                       self.q_clarity_0, self.q_clarity_1, self.q_clarity_2,
                       self.q_clarity_3, self.q_clarity_4, self.q_clarity_5,
                       self.q_clarity_6, self.q_clarity_7, self.q_clarity_8,
                       self.q_complete_0, self.q_complete_1, self.q_complete_2,
                       self.q_complete_3, self.q_complete_4, self.q_complete_5,
                       self.q_complete_6, self.q_complete_7, self.q_complete_8,
                       self.q_complete_9,
                       self.q_consistent_0, self.q_consistent_1,
                       self.q_consistent_2, self.q_consistent_3,
                       self.q_consistent_4, self.q_consistent_5,
                       self.q_consistent_6, self.q_consistent_7,
                       self.q_consistent_8, self.q_verifiable_0,
                       self.q_verifiable_1, self.q_verifiable_2,
                       self.q_verifiable_3, self.q_verifiable_4,
                       self.q_verifiable_5)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the Requirement data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRequirement {0:d} attributes.". \
               format(self.requirement_id)

        try:
            self.derived = int(none_to_default(attributes[0], 0))
            self.description = str(none_to_default(attributes[1], ''))
            self.figure_number = str(none_to_default(attributes[2], ''))
            self.owner_id = int(none_to_default(attributes[3], 0))
            self.page_number = str(none_to_default(attributes[4], ''))
            self.parent_id = int(none_to_default(attributes[5], 0))
            self.priority = int(none_to_default(attributes[6], 0))
            self.requirement_code = str(none_to_default(attributes[7], ''))
            self.specification = str(none_to_default(attributes[8], ''))
            self.type_id = int(none_to_default(attributes[9], 0))
            self.validated = int(none_to_default(attributes[10], 0))
            self.validated_date = none_to_default(attributes[11], date.today())
            self.q_clarity_0 = int(none_to_default(attributes[12], 0))
            self.q_clarity_1 = int(none_to_default(attributes[13], 0))
            self.q_clarity_2 = int(none_to_default(attributes[14], 0))
            self.q_clarity_3 = int(none_to_default(attributes[15], 0))
            self.q_clarity_4 = int(none_to_default(attributes[16], 0))
            self.q_clarity_5 = int(none_to_default(attributes[17], 0))
            self.q_clarity_6 = int(none_to_default(attributes[18], 0))
            self.q_clarity_7 = int(none_to_default(attributes[19], 0))
            self.q_clarity_8 = int(none_to_default(attributes[20], 0))
            self.q_complete_0 = int(none_to_default(attributes[21], 0))
            self.q_complete_1 = int(none_to_default(attributes[22], 0))
            self.q_complete_2 = int(none_to_default(attributes[23], 0))
            self.q_complete_3 = int(none_to_default(attributes[24], 0))
            self.q_complete_4 = int(none_to_default(attributes[25], 0))
            self.q_complete_5 = int(none_to_default(attributes[26], 0))
            self.q_complete_6 = int(none_to_default(attributes[27], 0))
            self.q_complete_7 = int(none_to_default(attributes[28], 0))
            self.q_complete_8 = int(none_to_default(attributes[29], 0))
            self.q_complete_9 = int(none_to_default(attributes[30], 0))
            self.q_consistent_0 = int(none_to_default(attributes[31], 0))
            self.q_consistent_1 = int(none_to_default(attributes[32], 0))
            self.q_consistent_2 = int(none_to_default(attributes[33], 0))
            self.q_consistent_3 = int(none_to_default(attributes[34], 0))
            self.q_consistent_4 = int(none_to_default(attributes[35], 0))
            self.q_consistent_5 = int(none_to_default(attributes[36], 0))
            self.q_consistent_6 = int(none_to_default(attributes[37], 0))
            self.q_consistent_7 = int(none_to_default(attributes[38], 0))
            self.q_consistent_8 = int(none_to_default(attributes[39], 0))
            self.q_verifiable_0 = int(none_to_default(attributes[40], 0))
            self.q_verifiable_1 = int(none_to_default(attributes[41], 0))
            self.q_verifiable_2 = int(none_to_default(attributes[42], 0))
            self.q_verifiable_3 = int(none_to_default(attributes[43], 0))
            self.q_verifiable_4 = int(none_to_default(attributes[44], 0))
            self.q_verifiable_5 = int(none_to_default(attributes[45], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKRequirement.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKRequirement attributes."

        return _error_code, _msg
