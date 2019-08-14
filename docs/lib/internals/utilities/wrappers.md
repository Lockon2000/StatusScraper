As it is desired to make provider implementation as simple and as fast as possible, a lot of the steps needed to guarantee the
required interface are handled behind the scenes for the scraped objects. The scraped objects need only provide a specified format.
While deriving this format we had two points in mind: minimality, as the required data is not independent of each other and one
could be derived from another, and semantical cleanliness, which makes the code more understandable or provides drastically more
elegant solutions to some problems. After that all remaining work like processing or adding information to the objects to conform to
the specification are done through wrappers for the scraping functions.

To summerize: The process of scraping information is divided into two parts:
1. '''The provider specific implementation''' which gathers only the seemingly necessary information from the provider status site.
2. '''The wrappers to the scraping functions''' which uses this provided information to derive other information to conform to the
specification and also process the scraped objects, e.g. filtering.

# Components Scraper Wrapper

The scrapeComponents wrapper function, roughly, does the following:
- It handles the exceptions possibly produced by the scrape function
- It completes the needed data for every component to conform to the specification, see below for the completed data.
- It Filters the blacklisted components
- It logs all necessary information

## Data to be Completed for The Components
- `'ID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the component ID if it is no new component. Otherwise it should hold `None`.
- `'description'`:
    - Type: `string`
    - Description: This key should hold the description of the component. A summirised insight to what it denotes.
- `'groupName'`:
    - Type: `string` or `NoneType`
    - Description: Holds the name of the group this component belongs to. Normally the group to which this component belongs will already have been 
                   created by the point this information is required, but in certain cases, e.g. "Testing", it can happen that the component still
                   doesn't have a group. 
- `'groupID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the group ID of the group to which this component belongs. Normally the group to which this component
                   belongs will already have been created by the point this information is required, but in certain cases, e.g. "Testing", it can
                   happen that the component still doesn't have a group.
- `'verbalStatus'`:
    - Type: `string`
    - Description: Holds the "German" verbal status of a component.
- `'provider'`:
    - Type: `string`
    - Description: Holds the name of the provider to which this component belongs in the correct format.


# Incidents Scraper Wrapper

The scrapeIncidents wrapper function, roughly, does the following:
- It handles the exceptions possibly produced by the scrape function
- It completes the needed data for every incidents and its updates to conform to the specification, see below for the completed data.
- It Filters the blacklisted incidents
- It embeds the marker in the main body
- It logs all necessary information

## Data to be Completed for The Incidents
- `'ID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the incident ID if it is no new incident. Otherwise it should hold `None`.
- `'status'`:
    - Type: `enum:IncidentStatus`
    - Description: This key should hold the incident status as an IncidentStatus enum. See the docs for enums under structures for more information.
- `'verbalStatus'`:
    - Type: `string`
    - Description: Holds the language speicfic verbal status of the incident.
- `'body'`:
    - Type: `string`
    - Description: holds the formated main body of the incident ready for presentation. This is where the marker is embedded.
- `'componenIDs'`:
    - Type: `list.string` or `NoneType`
    - Description: Holds the IDs of the affected components. If there are no affected components (either because there aren't any at the provider
                   or because the components don't have any like in testing scenarios. Notice that normally the commponents should already have
                   been created and be present at the point of executing this wrapper) then this key should hold `None`.
- `'componentVerbalStatuses'`:
    - Type: `list.enum:ComponentStatus` or `NoneType`
    - Description: Holds the language specific verbal statuses of the the correspondet components. The statuses order should match the components
                   order. If there are no components or at least no relevant ones then this should contain `None`.
- `'creationDate'`:
    - Type: `datetime.datetime`
    - Description: Holds the date this incidents was created at.
- `'lastUpdateDate'`:
    - Type: `datetime.datetime`
    - Description: Holds the date when this incident was last updated.
- `'provider'`:
    - Type: `string`
    - Description: Holds the name of the provider to which this incident belongs in the correct format.
- `'language'`:
    - Type: `string`
    - Description: This key should hold the language of the status site to which this component belongs.

## Data to be Completed for The Incidents Updates
- `'ID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the incident update ID if it is no new incident update. Otherwise it should hold `None`.
- `'incidentID'`:
    - Type: `int` or `NoneType`
    - Description: This key should hold the incident ID of the incident to which this incident update belongs. Normally the incident to which this
                   update belongs will already have been created by the point this information is required, but in certain cases,
                   e.g. "Testing", it can happen that the incident update still doesn't have an incident.
- `'incidentStatus'`:
    - Type: `enum:IncidentStatus`
    - Description: This key should hold the incident status according to this update as an IncidentStatus enum. See the docs for enums under
                   structures for more information.
- `'formatedBody'`:
    - Type: `'string'`
    - Description: Holds the formated body ready for presentation.