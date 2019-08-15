from lib.internals.structures.enums import ComponentStatus
from lib.internals.structures.enums import IncidentStatus


germanComponentVerbalStatuses = {
    ComponentStatus.Operational: "Funktionsfähig",
    ComponentStatus.PerformanceIssues: "Leistungsprobleme",
    ComponentStatus.PartialOutage: "Teilweiser Ausfall",
    ComponentStatus.MajorOutage: "Schwerer Ausfall"
}

englishComponentVerbalStatuses = {
    ComponentStatus.Operational: "Operational",
    ComponentStatus.PerformanceIssues: "Performance Issues",
    ComponentStatus.PartialOutage: "Partial Outage",
    ComponentStatus.MajorOutage: "Major Outage"
}

germanIncidentVerbalStatuses = {
    IncidentStatus.Investigating: "Untersuchungen laufen",
    IncidentStatus.Identified: "Identifiziert",
    IncidentStatus.Watching: "Unter Beobachtung",
    IncidentStatus.Fixed: "Behoben"
}

englishIncidentVerbalStatuses = {
    IncidentStatus.Investigating: "Investigating",
    IncidentStatus.Identified: "Identified",
    IncidentStatus.Watching: "Watching",
    IncidentStatus.Fixed: "Fixed"
}

