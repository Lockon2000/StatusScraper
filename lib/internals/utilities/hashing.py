from re import search


# Global options
debug = False


def setIncidentMarker(incident):
    assert 'message' in incident

    incident['message'] += "\n\n[//]: # ({marker})".format(marker=incident['provider_created_at'])

def getIncidentMarker(incident):
    assert 'message' in incident

    match = search(r"\[//\]: # \((.*)\)", incident['message'])
    assert match
    marker = match.group(1)

    return marker

def hashIncident(incident):
    # Make sure the incident has got the information required for hashing
    assert 'name' in incident

    marker = getIncidentMarker(incident)
    assert marker

    result = "".join([incident['name'], marker])

    return result


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    pprint("No Tests yet!")
