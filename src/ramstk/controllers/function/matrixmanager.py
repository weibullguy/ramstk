# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Controller Package matrix manager."""

# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import RAMSTKFunction, RAMSTKHardware


class MatrixManager(RAMSTKMatrixManager):
    """
    Contain the attributes and methods of the Function matrix manager.

    This class manages the function matrices for Hardware and Validation.
    Attributes of the function Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the function item being analyzed.
    """
    def __init__(self) -> None:
        """Initialize an instance of the function matrix manager."""
        super().__init__(
            column_tables={
                'fnctn_hrdwr':
                [RAMSTKHardware, 'hardware_id', 'comp_ref_des']
            },
            row_table=RAMSTKFunction)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_functions')
        pub.subscribe(self._do_create_function_matrix_columns,
                      'succeed_retrieve_hardware')
        pub.subscribe(self._on_delete_function, 'succeed_delete_function')
        pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_insert_function, 'succeed_insert_function')
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')

    def _do_create_function_matrix_columns(self, tree: treelib.Tree) -> None:
        """
        Create the Function data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        # If the row tree has already been loaded, we can build the matrix.
        # Otherwise the matrix will be built when the row tree is loaded.
        if tree.get_node(0).tag == 'hardware':
            self._col_tree['fnctn_hrdwr'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('fnctn_hrdwr')
                pub.sendMessage('request_select_matrix',
                                matrix_type='fnctn_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_function(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Delete the matrix row associated with the deleted function.

        :param int node_id: the treelib Tree() node ID associated with the
            deleted function.
        :param tree: the treelib Tree() containing the remaining function data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_delete_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """
        Delete the node ID column from the Function::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that was deleted.
            Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['fnctn_hrdwr'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'fnctn_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_function(self, node_id: int, tree: treelib.Tree) -> None:
        """

        :param int node_id: the treelib Tree() node ID associated with the
            inserted function.
        :param tree: the treelib Tree() containing the remaining function data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)

    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """
        Insert the node ID column to the Function::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that is to be
            inserted.  Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['fnctn_hrdwr'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'fnctn_hrdwr')