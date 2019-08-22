# Needed variables for the CRUD function:
providers = {
    "modules":[
        import_module("lib.providers."+provider.lower())      # lower cased providers to provide for
        for provider in enabledProviders                      # case insensitve configuration
    ]
}

providers.update({
    "componentFunctions": [
        componentsGetterWrapper(module.providerName)(module.getComponents)
        for module in providers["modules"]
    ],
    "incidentFunctions": [
        incidentsGetterWrapper(module.providerName)(module.getIncidents)
        for module in providers["modules"]
    ]
})

return providers