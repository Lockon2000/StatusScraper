# Global options
debug = False


def buildLogEntry(date ,logType, message):
    entry = "### {date} - {logType} - {message}\n\n".format(date=date, logType=logType, message=message)

    return entry

def buildIncidentMessage(**arguments):
    linkMarkdown = "[Link]({link})".format(link=arguments['link'])

    message = "**{provider}**\n\n{verbalComponents}: {description} - {linkMarkdown}\n\n".format(
                                                provider=arguments['provider'],
                                                verbalComponents=arguments['verbalComponents'], 
                                                description=arguments['description'],
                                                linkMarkdown=linkMarkdown
                                            )

    return message

def buildIncidentUpdateMessage(date, verbalStatus, info):
    message = "{date} - **[{verbalStatus}]** {info}".format(date=date, verbalStatus=verbalStatus, info=info)

    return message


if __name__ == '__main__':
    # Test module
    from pprint import pprint
    debug = True

    pprint("No Tests yet!")
