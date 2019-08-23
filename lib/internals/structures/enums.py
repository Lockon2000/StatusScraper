from enum import IntEnum
from enum import unique

@unique
class ComponentStatus(IntEnum):
    Operational = 1
    PerformanceIssues = 2
    PartialOutage = 3
    MajorOutage = 4
    Current = 5         # Special value indicating that the current status of the configured adapter should be used.
    Unknown = -1

@unique
class IncidentStatus(IntEnum):
    Investigating = 1
    Identified = 2
    Watching = 3
    Fixed = 4
    Unknown = -1

@unique
class IncidentUpdateAction(IntEnum):
    Investigating = 1
    Identified = 2
    Watching = 3
    Fixed = 4
    Update = 5
    Unknown = -1

