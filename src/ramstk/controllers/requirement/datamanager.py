# -*- coding: utf-8 -*-
#
#       ramstk.controllers.requirement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRequirement


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Requirement data manager.

    This class manages the requirement data from the RAMSTKRequirement
    and RAMSTKStakeholder data models.
    """

    _tag = 'requirement'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Requirement data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'requirement': ['revision_id', 'requirement_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_requirement_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_requirement_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_requirement')
        pub.subscribe(super().do_update_all, 'request_update_all_requirements')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_requirement')
        pub.subscribe(self.do_get_tree, 'request_get_requirement_tree')
        pub.subscribe(self.do_create_code, 'request_create_requirement_code')
        pub.subscribe(self.do_create_all_codes,
                      'request_create_all_requirement_codes')

        pub.subscribe(self._do_delete_requirement,
                      'request_delete_requirement')
        pub.subscribe(self._do_insert_requirement,
                      'request_insert_requirement')

    def do_create_code(self, node_id: int, prefix: str) -> None:
        """Request to create the requirement code.

        :param int node_id: the Requirement ID to create the code for.
        :param str prefix: the code prefix to use for the requested code.
        :return: None
        :rtype: None
        """
        try:
            _requirement = self.tree.get_node(node_id).data['requirement']
            _requirement.create_code(prefix=prefix)

            pub.sendMessage('succeed_create_code')
            pub.sendMessage('succeed_create_requirement_code',
                            requirement_code=_requirement.get_attributes()
                            ['requirement_code'])
        except (TypeError, AttributeError):
            if node_id != 0:
                pub.sendMessage('fail_create_requirement_code',
                                error_message=('No data package found for '
                                               'requirement ID {0:s}.').format(
                                                   str(node_id)))

    def do_get_tree(self) -> None:
        """Retrieve the requirement treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_requirement_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Requirement data from the RAMSTK Program database.

        :param dict attributes: the attributes for the selected Requirement.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _requirement in self.dao.do_select_all(
                RAMSTKRequirement,
                key=RAMSTKRequirement.revision_id,
                value=self._revision_id,
                order=RAMSTKRequirement.requirement_id):
            _data_package = {'requirement': _requirement}

            self.tree.create_node(tag=_requirement.requirement_code,
                                  identifier=_requirement.requirement_id,
                                  parent=_requirement.parent_id,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_requirements', tree=self.tree)

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node (requirement) ID of the requirement to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['requirement'])

            pub.sendMessage('succeed_update_requirement', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_requirement',
                            error_message=('Attempted to save non-existent '
                                           'requirement with requirement ID '
                                           '{0:s}.').format(str(node_id)))
        except (KeyError, TypeError):
            if node_id != 0:
                pub.sendMessage('fail_update_requirement',
                                error_message=('No data package found for '
                                               'requirement ID {0:s}.').format(
                                                   str(node_id)))

    def _do_delete_requirement(self, node_id: int) -> None:
        """Remove a requirement.

        :param int node_id: the node (requirement) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'requirement')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_requirement',
                            node_id=node_id,
                            tree=self.tree)
        except DataAccessError:
            _error_msg = ("Attempted to delete non-existent requirement ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_requirement',
                            error_message=_error_msg)

    def _do_insert_requirement(self, parent_id: int = 0) -> None:
        """Add a new requirement.

        :param int parent_id: the parent (requirement) ID the new requirement
            will be a child (derived) of.
        :return: None
        :rtype: None
        """
        try:
            _requirement = RAMSTKRequirement()
            _requirement.revision_id = self._revision_id
            _requirement.requirement_id = self.last_id + 1
            _requirement.parent_id = parent_id
            _requirement.description = 'New Requirement'

            self.dao.do_insert(_requirement)

            self.last_id = _requirement.requirement_id
            self.tree.create_node(tag=_requirement.requirement_code,
                                  identifier=self.last_id,
                                  parent=parent_id,
                                  data={'requirement': _requirement})
            pub.sendMessage('succeed_insert_requirement',
                            node_id=self.last_id,
                            tree=self.tree)
        except NodeIDAbsentError:
            pub.sendMessage(
                "fail_insert_requirement",
                error_message=("Attempting to add child requirement "
                               "to non-existent requirement "
                               "{0:d}.").format(parent_id))
