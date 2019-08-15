Although some providers list maintenances (or other objects) syntactically simmilar to the incidents it lies upon
scrapeIncidents to supply only the incidents to its caller.

# Specification for Scraped Incidents

After successfully scraping an incident from some providers status site, a dict representing the incident should
returned with the following keys:
- `'title'`:
    - Type: `string`
    - Inclusion: Mandatory
    - Existence: guaranteed - The implementor of the provider must guarantee its existence. Everyone can use this info
                 without checking for its existence first.
    - Description: This key should hold a string with the title of the incident.
- `'updates'`:
    - Type: `list.dict`
    - Inclusion: Mandatory
    - Existence: guaranteed - The implementor of the provider must guarantee its existence. Everyone can use this info
                 without checking for its existence first.
    - Description: Holds a list with all the updates of the incident represented by dicts.
- `'components'`:
    - Type: `list.string` or `NoneType`
    - Inclusion: Mandatory
    - Existence: guaranteed - The implementor of the provider must guarantee its existence. Everyone can use this info
                 without checking for its existence first.
    - Description: Holds the names of the affected components. If there are no affected components then this key should
                   hold `None`. We chose to include the names of the components and not the IDs because the components
                   could still be new and have no ID.
                   It could be possible that not all components at the providers status site are needed or desired. In
                   that case only relevent components should be included in this list, if any.
- `'componentStatuses'`:
    - Type: `list.enum:ComponentStatus` or `NoneType`
    - Inclusion: Mandatory
    - Existence: guaranteed - The implementor of the provider must guarantee its existence. Everyone can use this info
                 without checking for its existence first.
    - Description: Holds the statuses of the the correspondet components. The statuses order should match the
                   components order. If there are no components or at least no relevant ones then this should contain 
                   `None`.
- `'link'`:
    - Type: `string`
    - Inclusion: Optional
    - Existence: not guaranteed - Everyone who uses this info must first check its existence.
    - Description: This holds the absolute http link to the dedicated page of the inident if it has one. Otherwise it
                   should hold a link to the providers status site.
- `'locations'`:
    - Type: `list.string`
    - Inclusion: Optional
    - Existence: not guaranteed - Everyone who uses this info must first check its existence.
    - Description: Holds the affected locations by the incident.


# Specification for Scraped Incident Updates:

- `'action'`:
    - Type: `enum:IncidentUpdateType`
    - Description: This specifies the action the provider is taking with this update, it describes if the provider is
                   e.g. investigating or monitoring the incident. For more information about the IncidentUpdateType
                   enum, see the docs under enums.
- `'date'`:
    - Type: `datetime.datetime`
    - Description: The time when this update was published.
- `'info'`:
    - Type: `string`
    - Description: The actuall information supplied by the status site in this update. (Notice that even if the very
                   first update isn't treated by all status sites as an update, we will standardize this and treat even
                   the information supplied at the creation of the incidnet as an update. If there is no obvious status
                   tied to this first update then we will give it a default of `IncidentStatus.Investigating`)

