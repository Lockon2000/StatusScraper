# Specification for the created incidents at a status site

a successfully created incident with `createIncident` should return a dict with the following keys:
- `'ID'`:
    - Type: `int`
    - Description: This key should hold the newly created incidents ID.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'` in the context of an incident and `'incident_id'` in other contexts.


# Specification for the retrieved incidents from a status site

a successful retrieval of an incident from the status site with `readIncident` should return a dict which represents the incident and contains the
following keys (In the case of retrieving all incidents with `readIncidents` it should return a list the dicts representing the incidents):
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
    - Type: `enum:IncidentStatus`
    - Description: This key should hold the incident status as an IncidentStatus enum. See the docs for enums under structures for more information.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'status'` in the context of a component and `'component_status'` in all other contexts.
- `'body'`:
    - Type: `string`
    - Description: This key should hold the main body (the part of the incident where the marker is secretly embedded) of the incident.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'message'`.


# Specification for the retrieved incident updates from a status site

a successful retrieval of all incident updates at the status site with `readIncidentUpdates` should return a list containing dicts where each
dict represents an incident update and contains the following keys:
- `'ID'`:
    - Type: `int`
    - Description: This key should hold the ID of the incident udpate.
    - Remarks Specific to an employed Status Site:
        - Cachet:
            - The cachet API calls this piece of information `'id'`.