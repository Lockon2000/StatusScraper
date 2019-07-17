# Test package
from pprint import pprint

from enabledProviders import providerFiles
from enabledProviders import modules
from enabledProviders import componentFunctions
from enabledProviders import incidentFunctions
from enabledProviders import maintenanceFunctions


debug = True


print("Provider Files:")
pprint(providerFiles)
print("\nProvider Modules:")
pprint(modules)
print("\n")
pprint(componentFunctions)
pprint(incidentFunctions)
pprint(maintenanceFunctions)

