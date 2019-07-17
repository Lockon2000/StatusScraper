import sys
import importlib
from pathlib import Path

from lib.utilities.tools import moduleSyntaxCorrect


# Global options
debug = False


enabledProvidersDirectory = Path('enabledProviders')
providerFiles = [file.name[:-3] for file in enabledProvidersDirectory.iterdir() if file.is_file()]
providerFiles.remove('__init__')
providerFiles.remove('__main__')
modules = [
    importlib.import_module("enabledProviders.{}".format(providerFile))
    for providerFile in providerFiles
]

componentFunctions = [
    (module.providerName, module.getComponents)
    for module in modules
    if moduleSyntaxCorrect(module)
]
incidentFunctions = [
    (module.providerName, module.getIncidents)
    for module in modules
    if moduleSyntaxCorrect(module)
]
maintenanceFunctions = [
    (module.providerName, module.getMaintenances)
    for module in modules
    if moduleSyntaxCorrect(module)
]
