from sys import argv
from importlib import import_module
from pprint import pprint

from lib.internals.utilities.verification import verifyConfigurations
from lib.internals.utilities.verification import verifyAdapters


# This is needed in order to make it possible to specify the imported adapter from the command line.
# If it is not specified on the command line if will take the configured one in configs.py as default.
if len(argv) == 2:
    adapter = argv[1]
else:
    from conf.configs import adapter

# Verify all needed components for module testing
#
# We verify all configurations
verifyConfigurations()
# We only verify the adapter being tested right now
verifyAdapters(adapter)

# Import the adapter module and make it accessible withr the variable adapterModule
adapterModule = import_module("lib.adapters."+adapter)
# Make all attributes of adapterModule directly accessible (Simulation for from <module> import *)
globals().update(
    {n: getattr(adapterModule, n) for n in adapterModule.__all__} if hasattr(adapterModule, '__all__') 
    else 
    {k: v for (k, v) in adapterModule.__dict__.items() if not k.startswith('_')
})

# Testing the Groups API
# 1. Test createGroups
print("# createGroup")
print("= Create a group called 'test'")
responseData = createGroup('test')
print("= response data:")
pprint(responseData)
# 2. Test readGroups
print("# readGroups")
print("= Read groups with the format 'group: ID'")
pprint(readGroups("group: ID"))
print("= Read groups with the format 'ID: group'")
pprint(readGroups("ID: group"))
print("= Read groups with the format 'group: False'")
pprint(readGroups("group: False"))
print("= Read groups with the format 'list'")
pprint(readGroups("list"))
# 3. Test deleteGroups
print("# deleteGroup")
print("= Delete the group 'test' previously created")
deleteGroup(responseData['id'])
print("= Read groups to make sure 'test' was deleted")
pprint(readGroups("list"))
print("------------------\n\n")

# # Testing readComponents
# print("# readComponents")
# print("## group: {component: ID}")
# pprint(readComponents("group: {component: ID}"))
# print("## group: {component: False}")
# pprint(readComponents("group: {component: False}"))
# print("## groupID: {component: ID}")
# pprint(readComponents("groupID: {component: ID}"))
# print("## groupID: {component: False}")
# pprint(readComponents("groupID: {component: False}"))
# print("## ID: status")
# pprint(readComponents("ID: status"))
# print("## group: components list")
# pprint(readComponents("group: components list"))
# print("------------------\n\n")

# # Testing readIncidents
# print("# readIncidents")
# print("## incidentHash: ID")
# pprint(readIncidents("incidentHash: ID"))
# print("## ID: status")
# pprint(readIncidents("ID: status"))
# print("------------------\n\n")

