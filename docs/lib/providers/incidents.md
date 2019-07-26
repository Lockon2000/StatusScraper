Although some providers list maintenances (or other objects) syntactically simmilar to the incidents it lies upon scrapeIncidents to supply only the incidents
to its caller.

# Specification for Scraped Incidents

After successfully scraping an incident from some providers status site, a dict representing the incident should
returned with the following keys:
- `'name'`:
    - Type: `string`
    - Description: This key should hold a string with the name of the component.
- `'updates'`:
    - Type: `list.dict`
    - Description: Holds a list with all the updates of the incident represented by dicts.
- `'componentNames'`:
    - Type: `list.string` or `NoneType`
    - Description: Holds the names of the affected components. If there are no effected components then this key should hold `None`.
                   We chose to include the names of the components and not the IDs because the components could still be new and have no ID.
                   It could be possible that not all components at the providers status site are needed or desired. In that case only relevent
                   components should be included in this list, if any.
- `'componentStatuses'`:
    - Type: `list.enum:ComponentStatus` or `NoneType`
    - Description: Holds the statuses of the the correspondet components. The statuses order should match the components order. If there are no
                   components or at least no relevant ones then this should contain `None`.
- `'CreationDate'`:
    - Type: `datetime.datetime`
    - Description: Holds the date this incidents was created at.
- `'lastUpdateDate'`:
    - Type: `datetime.datetime`
    - Description: Holds the date when this incident was last updated.
- `'provider'`:
    - Type: `string`
    - Description: Holds the name of the provider to which this incident belongs in the correct format.
- `'link'`:
    - Type: `string`
    - Description: This holds the absolute http link to the dedicated page of the inident if it has one. Otherwise it should hold a link to the
                   providers status site.
- `'language'`:
    - Type: `string`
    - Description: This key should hold the language of the status site to which this component belongs.

# Specification for Scraped Incident Updates:

- `'type'`:
    - Type: `enum:IncidentType`
    - Description: This specifies the type of the update, it describes if the provider is e.g. investigating or monitoring the incident.
- `'date'`:
    - Type: `datetime.datetime`
    - Description: The time when this update was published.
- `'incidentStatus'`:
    - Type: `enum:IncidentStatus`
    - Description: The incident status according to this upate.
- `'rawBody'`:
    - Type: `string`
    - Description: The actuall information supllied by the status site in this update. (Notice that even if the very first update isn't treated by
                   all status sites as an update, we will standardize this and treat even the information supplied at the creation of the incidnet
                   as an update. If there is no obvious status tied to this first update then we will give it a default of IncidentStatus.Investigating)

