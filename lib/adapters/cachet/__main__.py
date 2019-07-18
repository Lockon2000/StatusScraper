from sys import argv
from pprint import pprint

from lib.adapters.cachet import *


if argv[1] == "groups":
    # Testing readGroups
    print("# readGroups")
    print("## group: id")
    pprint(readGroups("group: id"))
    print("## id: group")
    pprint(readGroups("id: group"))
    print("## group: False")
    pprint(readGroups("group: False"))
    print("## list")
    pprint(readGroups("list"))
    print("------------------\n\n")

elif argv[1] == "components":
    # Testing readComponents
    print("# readComponents")
    print("## group: {component: id}")
    pprint(readComponents("group: {component: id}"))
    print("## group: {component: False}")
    pprint(readComponents("group: {component: False}"))
    print("## groupID: {component: id}")
    pprint(readComponents("groupID: {component: id}"))
    print("## groupID: {component: False}")
    pprint(readComponents("groupID: {component: False}"))
    print("## id: status")
    pprint(readComponents("id: status"))
    print("## group: components list")
    pprint(readComponents("group: components list"))
    print("------------------\n\n")

elif argv[1] == "incidents":
    # Testing readIncidents
    print("# readIncidents")
    print("## incidentHash: id")
    pprint(readIncidents("incidentHash: id"))
    print("## id: status")
    pprint(readIncidents("id: status"))
    print("------------------\n\n")

