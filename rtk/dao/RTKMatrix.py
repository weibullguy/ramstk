#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMatrix.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKMatrix Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKMatrix(RTK_BASE):
    """
    Class to represent the rtk_matrix table in the RTK Program database.
    Matrix types are one of the following:

    +------+------------+-------------+
    | Type |    Rows    |   Columns   |
    +======+============+=============+
    |   0  | Function   | Hardware    |
    +------+------------+-------------+
    |   1  | Function   | Software    |
    +------+------------+-------------+
    |   2  | Function   | Testing     |
    +------+------------+-------------+
    |   3  | Requirement| Hardware    |
    +------+------------+-------------+
    |   4  | Requirement| Software    |
    +------+------------+-------------+
    |   5  | Requirement| Validation  |
    +------+------------+-------------+
    |   6  | Hardware   | Testing     |
    +------+------------+-------------+
    |   7  | Hardware   | Validation  |
    +------+------------+-------------+

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_matrix'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    matrix_id = Column('fld_matrix_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    column_id = Column('fld_column_id', Integer, default=0)
    column_item_id = Column('fld_column_item_id', Integer, default=0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    row_id = Column('fld_row_id', Integer, default=0)
    row_item_id = Column('fld_row_item_id', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)
    value = Column('fld_value', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='matrix')

    def get_attributes(self):
        """
        Method to retrieve the current values of the TKMatrix data model
        attributes.

        :return: (revision_id, matrix_id, column_id, column_item_id, parent_id,
                  row_id, row_item_id, type_id, value)
        :rtype: tuple
        """

        _values = (self.revision_id, self.matrix_id, self.column_id,
                   self.column_item_id, self.parent_id, self.row_id,
                   self.row_item_id, self.type_id, self.value)

        return _values

    def set_attributes(self, values):
        """
        Method to set the RTKMatrix data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMatrix {0:d} attributes.". \
               format(self.matrix_id)

        try:
            self.column_id = int(values[0])
            self.column_item_id = int(values[1])
            self.parent_id = int(values[2])
            self.row_id = int(values[3])
            self.row_item_id = int(values[4])
            self.type_id = int(values[5])
            self.value = float(values[6])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMatrix.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMatrix attributes."

        return _error_code, _msg
