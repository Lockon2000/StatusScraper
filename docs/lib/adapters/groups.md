# Specification for the created groups at a status site

a successfully created group with createGroup should return a dict with the following keys:
- `'ID'`:
    - Type: `int`
    - Description: This key should hold the newly created groups ID.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'` in the context of a group and `'group_id'` in other contexts.


# Specification for the retrieved groups from a status site

a successful retrieval of all groups at the status site with readGroups should return a list containing dicts where each
dict represents a group and contains the following keys:
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