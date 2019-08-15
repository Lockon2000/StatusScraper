from re import search

from lib.internals.structures.exceptions import NoMarkerFound

# This function takes an incident and builds from the information in the incident a hash value that uniqly identifies
# the incident.
def buildIncidentHash(incident):
    # Make sure the incident has got the information required for hashing
    assert 'title' in incident
    assert 'link' in incident

    hashValue = hash(incident['title']+incident['link'])

    return hashValue

# This function embeds a marker in the incident, which identifies this incident as being programmatically managed.
def setIncidentMarker(incident):
    assert 'body' in incident
    assert 'hashValue' in incident

    marker = incident['hashValue']

    incident['body'] += "\n\n[//]: # ({marker})".format(marker=marker)

def getIncidentMarker(incident):
    assert 'body' in incident

    match = search(r"\[//\]: # \((.*)\)", incident['body'])
    if match:
        marker = match.group(1)
    else:
        raise NoMarkerFound

    return marker

