# Missing Cachet Documentaion

## Requiered Headers for API Endpoints
The header `Content-Type: application/json` must be set for all create and update requests.

## Date Fields Format
When dates are supplied to the API a certain format must be uphold. The current docs do not explicitly mention it. Only a test file shows how one should format a dates: **YYYY-MM-DD hh:mm**.


# Specification for Implementing a Service Provider

Here we describes the mandatory and recommended implementation details of a service provider e. g. interface, functionality and structure. Only the interface must conform to a preset layout in order for the program to function correctly. Functionality and structure are rather an aspect of standardization between the different provider implementations so that a common layout is present which simplifys the planning and understanding of every implementation.


## Functionality and Structure

This section describes the recommended structure and internal functionality of a provider implementation. It provides **one way** of doing things but one could very well divert from it. Refer to the template to see how it should look like.

### Layout
```
Imports

Global Variables

Components getter function

Incident getter function

Maintenence getter function

Provider specific helper functions

Module testing
```

### Imports
+ Import all helpers from the lib.utilities module into the main namespace.

### Global Variables
+ `providerName` : The name of the provider correctly cased
+ `statusURL` : The URL of the status page of the provider
+ `parsedWebPage` : The parsed web page which you get as a result of a call to the `getThenParse` helper function with the statusURL as the argument
+ `debug` : A debug mode flag which is set to False by default and only activated when desired e. g. in module testing

### Components getter function
+ Layout :
  ```
  Initializing the result

  Provider independent variables

  Provider dependent variables

  Gathering components

  Relevance check of the commponents

  Return results

  ```

### Incidents getter function
*Work in Progress*

### Maintenances getter function
*Work in Progress*

### Helper Functions
*Work in Progress*

### Module Testing
+ Import the pprint function and print using it.
+ set the Debug flag to true.
+ show the results of all getter functions sectioned and formatted.


## Interface

This sections describes the mandatory interface that every provider implementation should follow in order for the program to function as intended or even at all. It also includes subtle conceptual points to handle edge cases that have been gathered through bug fixes or carefull analysis.

### General details

+ The functionality of every provider implementation is accessed by importing the getter functions by name. So they must be named correctly in order to be found afterwards.

+ In order to provide provider independent functionality, e. g. logging, to the getter functions they are all decorated by decorators defined in lib.utilities. These decorators take the provider name as input.

+ All getter functions take no inputs.

+ All getter functions should return a list of dicts representing the objects (Components, incidents or maintenances) they gathered or an empty list.

+ The dicts returned by the getter functions need only have a specific set of key-value pairs which are later used but generaly try to store as much information as possible.

+ Only relevant objects should be returned as no further filtering is applied. Relevance check is implemented through helper functions defined in lib.utilties. They take the object as an argument and return a boolean value if the object is relevant or not.

+ The format of all dates in the dict should be : **YYYY-MM-DD hh:mm**

### Components getter function
+ Name : `getComponents`
+ Decorator : `componentsGetterWrapper`
+ Relevance Checker: `isRelevantComponent`
+ Input : None
+ Output : List of the components and an empty list if there are none
+ Every component need the following keys-value pairs:
  + name : The name of the component which will be displayed.
  + description : The description which will be displayed when someone hovers over the question mark.
  + status : The status code of the component 1 - 4.
  + group_id : The group ID of component.
    The groups are maintainted before the components of every group which means it should be garanteed that a corresponding group ID exists.

### Incidents getter function
+ Name : `getIncidents`
+ Decorator : `incidentsGetterWrapper`
+ Relevance Checker: `isRelevantIncident`
+ Input : None


### Maintenances getter function
+ Name : `getMaintenances`
+ Decorator : `maintenancesGetterWrapper`
+ Relevance Checker: `isRelevantMaintenance`
+ Input : None
