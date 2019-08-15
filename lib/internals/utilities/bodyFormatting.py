from re import search
from re import findall


datetimeFormatString = "%d.%m.%Y, %H:%M"


def constructIncidentBody(**arguments):
    provider = arguments['provider']
    link = arguments['link']
    components = arguments['components']
    componentVerbalStatuses = arguments['componentVerbalStatuses']

    body = "**{provider}** - [Link]({link})\n\n".format(provider=provider, link=link)
    for component, componentVerbalStatus in zip(components, componentVerbalStatuses):
        body += "{component}: {componentVerbalStatus}\n\n".format(component=component,
                                                                  componentVerbalStatus=componentVerbalStatus)
            
    return body

def deconstructIncidentBody(incidentBody):
    result = {}

    # Get provider name
    match = search(r"\*\*([\w ]*)\*\*", incidentBody)
    assert match, "Couldn't extract provider name from incident body"
    result['provider'] = match.group(1)

    # Get link
    match = search(r"\[Link\]\((.*)\)", incidentBody)
    assert match, "Couldn't extract incident link from incident body"
    result['link'] = match.group(1)

    # get components and their verbal statuses
    matches = findall(r"([\w ]*): ([\w ]*)", incidentBody)
    if matches:
        result['components'] = []
        result['componentVerbalStatuses'] = []
        for match in matches:
            result['components'].append(match[0])
            result['componentVerbalStatuses'].append(match[1])
    
    return result

def constructIncidentUpdateBody(update):
    date = update['date'].strftime(datetimeFormatString)
    action = update['action'].name
    info = update['info']

    body = "{date} - **[{action}]** {info}".format(date=date, action=action, info=info)

    return body

