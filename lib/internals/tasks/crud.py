from lib.adapters import *
from lib.utilities.hashing import hashIncident


# The CRUD function is the main brain fo the Scraper. Here it actually gets the different scraped
# information and then processes it and finally decides how to deal with it.
def CRUD(providers):
    # Step 1:
    # At the beginning we make sure all automated groups exist. A group is automated if it corresponds
    # to an enabled provider. If an automated group is missing we create it.
    #
    # NOTE: No groups Are deleted!!! It lies upon the admins to make sure there are no unwanted groups.
    scrapedGroups = [module.providerName for module in providers["modules"]]
    ensureAutomatedGroups(scrapedGroups)

    # Step 2:
    # Now we sync the automated components. Components are automated if theire provider is enabled and
    # they are not filtered and also if they are not configured as manual components to be ignored by
    # the scraper. We only care for the existence of the components, not their status. So no
    # stauts updates are made. If a component is newly created it will be created with the status 
    # found upon scraping. Also we only care about automated components, which can only be
    # be found in automated groups. Components which are not under automated groups are ignored.
    #
    # NOTE: Components which are not found at the provider and are not configured by the admins
    # will be deleted!!!
    scrapedComponents = [scrapedComponent
                         for scrapeComponents in providers["componentFunctions"]
                         for scrapedComponent in scrapeComponents()]
    # ignoredComponents are the configured components to be ignored within the area of jurisdiction.
    # The case of the provider and component names is lowered so as to allow case insensitive configuration.
    ignoredComponents = {provider.lower(): list(map(lambda x: x.lower(), components))
                         for provider, components in manualComponents.items()}
    # automatedGroups is needed so that the function knows where its area of jurisdiction lies.
    automatedGroups = scrapedGroups
    syncAutomatedComponents(scrapedComponents, ignoredComponents, automatedGroups)

    # Step 3:
    # Current automated component statuses are saved from the scraped components. This also includes
    # newly created ones. Note that all automated components should be present in the scraped components.
    # The format of latestAutomatedComponentStatuses is {componentID: status, ...}.
    latestAutomatedComponentStatuses = readScrapedComponentStatuses(scrapedComponents)

    # Step 4:
    # Now we sync all automated incidents. Incidents are automated if their provider is enabled and
    # they are not filtered and also if they possess the specific marker confirming they are automated.
    #
    # NOTE: All unresolved incidents which are branded with the specific marker will be deleted if they are
    # not found at the correspondent provider, so as to prevent dangling incidents!!!
    #
    # Note that we set the marker on all scraped incidents
    scrapedIncidents = [scrapedIncident
                        for scrapeIncidents in providers["incidentFunctions"]
                        for scrapedIncident in scrapeIncidents()]
    syncAutomatedIncidents(scrapedIncidents)

    # Step 5:
    # Now we update the latestAutomatedComponentStatuses after the incidents are now up to date.
    saveAutomatedComponentStatusesFromUnresolvedIncidents(latestAutomatedComponentStatuses)

    # Step 6:
    # At last we update the automated component statuses at the status site with latest found statuses
    # from both scraped components and scraped incidents.
    updateAutomatedComponentStatuses(latestAutomatedComponentStatuses)


# Helper Functions -----------------------------------------------------------------
def ensureAutomatedGroups(scrapedGroups):
    # Input:
    #   scrapedGroups: A list with the correctly formated names of the enabled providers.
    # Output:
    #   Nothing. The function acts purely through its side effects.

    # Get the groups already in the status site.
    currentGroups = readGroups("list")

    # Check which groups are already there. If a group is not found if will be created.
    for group in scrapedGroups:
        if group not in currentGroups:
            createGroup(group)

def syncAutomatedComponents(scrapedComponents, ignoredComponents, automatedGroups):
    # Input:
    #   scrapedComponents: A list with the dicts of the scraped components of all providers. The dicts
    #                      contain all necessary information to handle the components. For a reference
    #                      of all contained information see the docs for components under adapters.
    #   ignoredComponents: A dict with automated group names as keys and values corresponding to the
    #                      configured comoponents to be ignored by the scraper and not deleted.
    #                      All strings are in lower case so as to provide case insensitive configuration.
    #   automatedGroups:   A list with the correctly formated names of the enabled providers.
    # Output:
    #   Nothing. The function acts purely through its side effects.

    # List all the components already on the status site with an initial synced attribute of false.
    # caseSensitivity is set to false to provide case insensitive configuration.
    currentComponentsSyncronisation = readComponents("group: {component: False}", caseSensitivity=False)

    # Check which scraped components are already there. If a component is not found if will be created
    # and added to currentComponentsSyncronisation.
    for component in scrapedComponents:
        name = component['name']
        group = component['provider']       # component['provider'] == component group
        if name in currentComponentsSyncronisation[group]:
            # As the component exists it is synced so we change its synced attribute to true
            currentComponentsSyncronisation[group][name] = True
        else:       # The component is not in the status site
            createComponent(component)

            # After creating the component it is synced so we add the component to the 
            # currentComponentsSyncronisation dict with a synced attribute of true.
            currentComponentsSyncronisation[group][name] = True

    # Also mark all ignored components as synced in order to not delete them. Note that we don't do
    # anything if the components are not actually present in the status site. That is because it doesn't
    # lie upon us to ensure its existence. All we care about is that it is not deleted if it is indeed there.
    for group in ignoredComponents:
        for name in ignoredComponents[group]:
            if name in currentComponentsSyncronisation[group]:
                currentComponentsSyncronisation[group][name] = True

    # Now we delete every asynchronous component, but only in the automated groups
    #
    # Get component IDs as they are needed for deleting the components
    componentIDs = readComponents("group: {component: id}", caseSensitivity=False)
    for group in automatedGroups:
        for name, syncStatus in currentComponentsSyncronisation[group].items():
            if syncStatus == False:
                deleteComponent(componentIDs[group][name])

# This function gets the scraped statuses of the scraped components in the format {componentID: status, ...}
# Note that these are the statuses that were scraped with the component. They are not the same as the statuses
# on the status page.
def readScrapedComponentStatuses(scrapedComponents):
    # Input:
    #   scrapedComponents: A list with the dicts of the scraped components of all providers. The dicts
    #                      contain all necessary information to handle the components. For a reference
    #                      of all contained information see the docs for components under adapters.
    # Output:
    #   A dict with the component statuses keyed by their IDs.

    # Get all component IDs after the components existances were synced
    ComponentIDs = readComponents("group: {component: id}")

    result = {}
    for component in scrapedComponents:
        componentID = ComponentIDs[component['provider']][component['name']]
        result[componentID] = component['status']

    return result

def syncAutomatedIncidents(scrapedIncidents):
    # Input:
    #   scrapedIncidents: A list with the dicts of the scraped incidents. The dicts contain all necessary
    #                     information to handle the incident. For a reference of all contained information 
    #                     see the docs for incidents under adapters. Note that the marker for the incidents
    #                     has already been set.
    # Output:
    #   Nothing. The function acts purely through its side effects.

    # List all the automated incidents already on the status site with an initial synced attribute of false.
    currentAutomatedIncidentsSyncronisation = readAutomatedIncidents("incidentHash: False")
    # Get incident IDs as they are needed for updating and deleting the incident
    incidentIDs = readAutomatedIncidents("incidentHash: ID")

    # Check which of the scraped incidents is already there and if it includes all the updates upto this point.
    # If an incident is not found if will be created and populated with all updates upto this point.
    for incident in scrapeIncidents:
        hashValue = hashIncident(incident)
        if hashValue in currentAutomatedIncidentsSyncronisation:
            ID = incidentIDs[hashValue]
            # First update incidents main body (Note that there is no elegent way for determining if
            # the body has changed so that we only update the body when necessary, so we do it always)
            updateIncidentMainBody(ID, incident)
            # Now sync the incident updates. We begin by determining the number of updates there are. Then there are
            # three possibilities:
            # Number of scraped updates > Number of updates at status site: -----
            # Number of scraped updates == Number of updates at status site: -----
            # Number of scraped updates < Number of updates at status site: -----
            # (Note that there is no elegent way for determining if the body of the updates has changed so that we only update the body when necessary,
            # so we do it always)
            ########################### NOT YET IMPLEMENTED !!!!!!!! ############################################

            # Now the incident is synced so mark it as synced
            currentAutomatedIncidentsSyncronisation[hashValue] = True
        else:       # The incident is new and not in the status site
            # First create the main body of the incident and get the ID of the newly created incident
            result = createIncident(incident)
            ID = result['ID']
            # Then determine the number of all already posted updates and apply them all
            numberOfUpdates = readIncidentUpdatesNumber(ID)
            for nthLastUpdate in range(numberOfUpdates,0,-1):
                updateIncident(ID, incident, nthLastUpdate)

            # After creating the incident and all its updates, it is now synced, so mark it accordingly
            currentAutomatedIncidentsSyncronisation[hashValue] = True

    # Now we delete every asynchronous automated incident
    for hashValue, syncStatus in currentAutomatedIncidentsSyncronisation.items():
        if syncStatus == False:
            ID = incidentIDs[hashValue]
            deleteIncident(ID)

def saveAutomatedComponentStatusesFromUnresolvedIncidents(latestAutomatedComponentStatuses):
    pass

def updateAutomatedComponentStatuses(latestAutomatedComponentStatuses):
    pass


# Helper Functions -----------------------------------------------------------------------------------------------------
def readAutomatedIncidents(form):
    pass