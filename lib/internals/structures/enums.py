from enum import IntEnum
from enum import unique

@unique
class ComponentStatus(IntEnum):
    Operational = 1
    PerformanceIssues = 2
    PartialOutage = 3
    MajorOutage = 4

@unique
class IncidentStatus(IntEnum):
    Investigating = 1
    Identified = 2
    Watching = 3
    Fixed = 4

@unique
class IncidentUpdateType(IntEnum):
    Investigating = 1
    Identified = 2
    Watching = 3
    Fixed = 4
    Update = 5

