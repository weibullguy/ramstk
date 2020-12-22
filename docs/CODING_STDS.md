# Coding Conventions

This document describes the coding standards to be adhered to by developers on
the [RAMSTK Project](https://github.com/weibullguy/ramstk).  It is a working document
and suggested changes shall be submitted as issues in the RAMSTK GitHub issue
tracker with an Enhancement label attached.

[Naming Conventions](#naming-conventions)
  * [Constants and Variables](#constants-and-variables)
  * [Classes and Modules](#classes-and-modules)
  * [Attributes](#attributes)
  * [Functions and Methods](#functions-and-methods)
  * [Tags](#tags)
[Design Conventions](#design-conventions)
  * [Data Models](#data-models)
  * [Data Controllers](#data-controllers)
  * [GUI Components](#gui-components)
    * [List Views](#list-views)
    * [Matrix Views](#matrix-views)
    * [Module Views](#module-views)
    * [Work Views](#work-views)


## Naming Conventions

Naming conventions shall, generally, follow the guidance provided in PEP8.
Where appropriate, the pylintrc code for checking these conventions is
included in each section.

### Constants and Variables

  1. All RAMSTK global constants shall be defined in the configuration module.
  2. Constants shall be:
      - All UPPERCASE with spaces replaced by underscores (_).
      - Prefaced by RAMSTK_ to identify it as an RAMSTK constant.
      - A minimum of twelve characters (RAMSTK_ is 7) and a maximum of 30 characters.

      ```
      pylintrc: const-rgx=RAMSTK_[A-Z_]{12,30}$
      ```

  3. Variables shall be:
      - All lowercase with spaces replaced by underscores (_).
      - A minimum of three characters and a maximum of 30 characters.
      - A descriptive name when used for program flow control (e.g., for or
        while loops).  For example, _index rather than i or _key rather than k.
      - Preceded by a single underscore when private in scope.

      ```
      pylintrc: variable-rgx=[a-z_][a-z_]{3,30}$
      ```

### Classes and Modules

  1. Module names shall be:
      - All lowercase with spaces replaced by underscores (_).
  2. Class names shall be:
      - In the CapWords format.
      - Alpha characters only.
      - Prefaced by RAMSTK.
      - A minimum of eight characters (RAMSTK is 3) and a maximum of 30 characters.
      - Suffixed by 'Error' when defining an exception class.

      ```
      pylintrc: module-rgx=(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$
      pylintrc: class-rgx=RAMSTK[A-Z][a-z]{8,30}$
      ```

### Attributes

  1. Class attributes shall be:
      - All lowercase with spaces replaced by underscores (_).
      - Prefaced by a double underscore (__).

  2. Private instance attribute shall be:
      - All lowercase with spaces replaced by underscores (_).
      - Prefaced by a single underscore (_).
      - Identified by the data type the attribute holds as follows:

      ```
      _dic to indicate a dictionary
      _lst to indicate a list
      _tpl to indicate a tuple
      _int to indicate a scalar integer
      _flt to indicate a scalar float
      _str to indicate a scalar string
      ```

  3. Public instance attributes shall be:
      - All lowercase with spaces replaced by underscores (_).
      - Identified by the data type the attribute holds as follows:

      ```
      dic to indicate a dictionary
      lst to indicate a list
      tpl to indicate a tuple
      int to indicate a scalar integer
      flt to indicate a scalar float
      str to indicate a scalar string
      ```

      ```
      pylintrc: attr-rgx=[_a-z_?][a-z0-9_?]{3,30}$
      ```

### Functions and Methods

  1. Functions and methods shall be:
      - All lowercase with underscores (_) replacing spaces.
      - A minimum of five characters and a maximum of 50 characters.
      - Prefaced by a single underscore (_) if not a public function or method.

      ```
      pylintrc: function-rgx=[_a-z0-9][_a-z0-9]{5,50}$
      pylintrc: method-rgx=[_a-z0-9][_a-z0-9]{5,50}$
      ```

  2. Function and method arguments shall be:
      - All lowercase with underscores (_) replacing spaces.
      - A minimum of five characters and a maximum of 30 characters.
      - Prefaced by a double underscore (__) if it is unused in the function
        or methods (e.g., in widget callback methods).

      ```
      pylintrc: argument-rgx=[a-z0-9][_a-z0-9]{5,30}$
      ```

### Tags

  1. Tags may be used to assist in placeholding during development.
      - FIXME to indicate non-working code that needs to be re-worked before
        check-in.
      - TODO to indicate missing code/functionality that needs to be added.
      - ISSUE to point to the RAMSTK GitHub project issue tracking the condition.

  2. FIXME tags shall:
      - **NOT** be included in any code checked in to the RAMSTK git repository.
      - Be converted to an ISSUE tag when an issue is created to track the
        condition.

  3. TODO tags shall:
      - **NOT** be included in any code checked in to the RAMSTK git repository.
      - Be converted to an ISSUE tag when an issue is created to track the
        condition.

  4. ISSUE tags shall:
      - Include the issue number and brief decription.  For example,

          ISSUE 88: Handle Errors in FMEA WorkView _do_load_tree() Method

      - Be printed to the console when encountered in the code.


## Design Conventions

### Data Models

  1. All data models shall have the following public methods:


      ```
      do_delete(self, node_id)
      do_insert(self, **kwargs)
      do_select(self, node_id, **kwargs)
      do_select_all(self, **kwargs)
      do_update(self, node_id)
      do_update_all(self, **kwargs)
      get_attributes(self, node_id)
      set_attributes(self, node_id, attributes)
      ```

  2. All data models shall have the following private methods:

      ```
      __init__(self, dao)
      ```

  3. Data models may have the following public/private methods/functions:

      ```
      do_calculate(self, node_id, **kwargs)
      do_calculate_all(self, **kwargs)
      do_select_children(self, node_id)
      _do_calculate_availability_metrics(attributes)
      _do_calculate_cost_metrics(attributes)
      _do_calculate_metric_variances(attributes)
      _do_calculate_reliability_metrics(attributes)
      ```

  4. For data model functions or methods unique to a particular RAMSTK module,
naming shall adhere to the following conventions:
      - If the function or method responds to a user request, it shall begin
        with do_ (public) or _do_ (private).  For example:

      ```
      _do_add_actions(self, cause_id, parent_id)
      _do_calculate_rpn(self)
      ```

      - If the function or method retrieves something, it shall begin with get_
        (public) or _get_ (private).  For example:

      ```
      get_actual_burndown(self)
      get_assessment_points(self)
      get_planned_burndown(self)
      ```

      - If the function or method does something, it should begin with set_
        (public) or _set_ (private).  For example:

      ```
      _set_assessment_points(self, **kwargs)
      ```

      - Conform with all naming convetions.

### Data Controllers

  1. All data controllers shall have the following public methods:

      ```
      do_handle_results(self, error_code, error_msg, pub_msg=None)
      request_do_delete(self, node_id)
      request_do_insert(self, **kwargs)
      request_do_select(self, node_id, **kwargs)
      request_do_select_all(self, parent_id, **kwargs)
      request_do_update(self, node_id)
      request_do_update_all(self, **kwargs)
      request_get_attributes(self, node_id)
      request_get_last_id(self, **kwargs)
      request_set_attributes(self, node_id, attributes)
      ```

  2. All data controllers shall have the following private methods:

      ```
      __init__(self, dao, configuration, **kwargs)
      ```

  3. Data controllers may have the following public/private methods/functions:

      ```
      request_do_calculate(self, **kwargs)
      request_do_calculate_all(self, **kwargs)
      request_do_calculate_availability(self, node_id)
      request_do_calculate_costs(self, node_id)
      request_do_calculate_hazard_rate(self, node_id)
      request_do_calculate_mtbf(self, node_id)
      request_do_calculate_reliability(self, node_id)
      request_do_select_children(self, node_id)
      ```

  4. For data controller functions or methods unique to a particular RAMSTK
module, naming shall adhere to the following conventions:
      - All methods should be named the same as the data model method and
        prefaced with request_.  For example:

      ```
      request_do_calculate_rpn(self)
      request_get_planned_burndown(self)
      ```

      - Shall be public in scope.
      - Conform with all naming conventions.

### GUI Components

  1. If the function or method creates a simple or aggregate widget, it shall
begin with make (public) or _make_ (private).

      ```
      _make_assessment_inputs_page(self)
      _make_buttonbox(self)
      ```

  2, If the function or method is a callback signal that is not a user request,
it should begin with on (public) or _on_ (private).

      ```
      _on_focus_out(self, entry, new_text)
      _on_edit(self, __cell, path, new_text, position)
      ```

  3. If the function or method is a callback signal that is a user request
(button press, etc.), it should be begin with do_request_ (public) or
_do_request_ (private).

      ```
      _do_request_calculate(self, __button)
      _do_request_update(self, __button)
      ```

  4. View functions and methods should, generally, be "private" (prefaced by a
single underscore '_') as they would only need to be called by other View
functions and methods and would not be part of the public API.  See paragraph 2.3.8.2 for an exception.

#### List Views

  1. All List Views shall have the following public methods:

  2. All List Views shall have the following private methods:

      ```
      __init__(self, controller, module=None)
      _do_change_row(self, treeview)
      _do_edit_cell(__cell, path, new_text, position, model)
      _do_load_page(self, tree, row=None)
      _do_request_delete(self, __button)
      _do_request_insert(self, __button)
      _do_request_update(self, __button)
      _do_request_update_all(self, __button)
      _make_buttonbox(self)
      _make_cell(self, cell, editable, position, model)
      _make_treeview(self)
      _on_button_press(self, treeview, event)
      _on_select_revision(self, module_id)
      ```

  3. For List View functions or methods unique to a particular RAMSTK module,
naming shall adhere to the following conventions:
      - Conform with requirements 2.3.1 through 2.3.4.  For example:

      ```
      _do_request_calculate(self)
      ```

      - Be private in scope.
      - Conform with all naming conventions.

#### Matrix Views

  1. All Matrix Views shall have the following public methods:


  2. All Matrix Views shall have the following private methods:

      ```
      __init__(self, controller, **kwargs)
      _do_request_update(self, __button)
      _make_buttonbox(self)
      _on_select_revision(self, module_id)
      ```

  3. For Matrix View functions or methods unique to a particular RAMSTK module,
naming shall adhere to the following conventions:
      - Conform with requirements 2.3.1 through 2.3.4.  For example:

      ```
      _do_request_calculate(self)
      ```

      - Be private in scope.
      - Conform with all naming conventions.

#### Module Views

  1. All Module Views shall have the following public methods:


  2. All Module Views shall have the following private methods:

      ```
      __init__(self, controller, module=None)
      _do_change_row(self, treeview)
      _do_edit_cell(self, __cell, path, new_text, position, model)
      _do_request_delete(self, __button)
      _do_request_insert(self, **kwargs)
      _do_request_insert_sibling(self, __button, **kwargs)
      _do_request_update(self, __button)
      _do_request_update_all(self, __button)
      _make_buttonbox(self)
      _make_treeview(self)
      _on_button_press(self, treeview, event)
      _on_edit(self, position, new_text)
      _on_select_revision(self, **kwargs)
      ```

  3. Module Views may have the following public/private methods/functions:

      ```
      _do_request_calculate_all(self, __button)
      _do_request_insert_child(self, __button, **kwargs)
      _on_calculate(self)
      ```

  4. Module View functions or methods unique to a particular RAMSTK module, naming
shall adhere to the following conventions:
      - Conform with requirements 2.3.1 through 2.3.4.  For example:

      ```
      _do_request_calculate_all(self)
      ```

      - Be private in scope.
      - Conform with all naming conventions.

#### Work Views

  1. All Work Views shall have the following public methods:


  2. Work Views that are embedded in a higher-level Work View (e.g.,
component-specific work views are embedded into the Hardware BoM Work View)
require their methods to be public so they can be called by the higher level
(private) method of the same name.  The following methods may be used by a Work
View that meets this criterion:

      ```
      do_load_comboboxes(self, subcategory_id)
      do_load_page(self)
      do_set_sensitive(self)
      make_assessment_input_page(self)
      make_assessment_results_page(self)
      on_combo_changed(self, combo, index)
      on_select(self, module_id)
      ```

  3. All Work Views shall have the following private methods:

      ```
      __init__(self, controller, **kwargs)
      _do_load_page(self, **kwargs)
      _do_refresh_view(self)
      _do_request_update(self, __button)
      _do_request_update_all(self, __button)
      _on_select(self, module_id, **kwargs)
      ```

  4. Work Views containing or consisting of a RAMSTKTreeView shall have the
following private methods:

      ```
      _do_change_row(self, treeview)
      _do_edit_cell(self, __cell, path, new_text, position, model)
      _do_request_delete(self, __button)
      _do_request_insert(self, **kwargs)
      _do_request_insert_sibling(self, __button)
      _get_cell_model(self, column)
      _make_treeview(self)
      _on_button_press(self, treeview, event)
      ```

  5. Work Views may contain one or more of the following private methods as
needed:

      ```
      _do_load_comboboxes(self, **kwargs)
      _do_request_calculate(self, __button)
      _do_request_calculate_all(self, __button)
      _do_request_plot(self, __button=None)
      _do_select_date(__button, __event, entry)
      _do_set_sensitive(self, **kwargs)
      _make_assessment_input_page(self)
      _make_assessment_results_page(self)
      _make_buttonbox(self)
      _make_general_data_page(self)
      _on_combo_changed(self, combo, index)
      _on_edit(self, index, new_text)
      _on_focus_out(self, entry, index)
      _on_toggled(self, togglebutton, index)
      _on_value_changed(self, spinbutton, index)
      ```

  6. For Work View functions or methods unique to a particular RAMSTK module,
naming shall adhere to the following conventions:
      - Conform with requirements 2.3.1 through 2.3.4.  For example:

      ```
      _do_load_planned_burndown(self, module_id=None)
      _do_load_subcategory(self, category_id)
      _do_request_edit_function(self, __button)
      _do_request_make_comp_ref_des(self, __button)
      _make_burndown_curve_page(self)
      _make_requirement_analysis_page(self)
      _make_stress_input_page(self)
      _make_stress_results_page(self)
      ```

      - Be private in scope.
      - Conform with all naming conventions.
