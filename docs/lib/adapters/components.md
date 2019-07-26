# Specification for the created components at a status site

a successfully created component with createComponent should return a dict with the following keys:
- `'ID'`:
    - Type: `int`
    - Description: This key should hold the newly created components ID.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'` in the context of a component and `'component_id'` in other contexts.


# Specification for the retrieved components from a status site

a successful retrieval of all components at the status site with readComponents should return a list containing dicts where each
dict represents a component and contains the following keys:
- `'name'`:
    - Type: `string`
    - Description: This key should hold a string with the name of the group.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'name'`.
- `'ID'`:
    - Type: `int`
    - Description: This key should hold the group ID of the group.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'` in the context of a group and `'group_id'` in other contexts.
- `'status'`:
    - Type: `enum:ComponentStatus`
    - Description: This key should hold the component status as a ComponentStatus enum. See the docs for enums under structures for more information.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'status'` in the context of a component and `'component_status'` in all other contexts.
- `'groupID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the group ID of the group to which this component belongs. Normaly it is ensured that this group
                   is already created. Under certain circumstances (e.g. testing) this could not be the case. In this situation it should
                   return `None`.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'` in the context of a group and `'group_id'` in other contexts.

