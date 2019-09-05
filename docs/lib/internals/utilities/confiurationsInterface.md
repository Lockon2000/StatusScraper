This Documentation explains for Developers how to read the configurations in the conf directory.

# Variables:

- `adapter`:
    - Type: `string`
    - Description: Holds the `adapter` configuration.
    - Properties:
        - Will be all lower case. The casing is not preserved.
    - Guaranteed!
- `APIBaseURL`:
    - Type: `string`
    - Description: Holds the `APIBaseURL` configuration.
    - Properties:
        - Will not end with a forward slash.
        - Will be all lower case. The casing is not preserved.
    - Example: "http://cachet.workxl.de/api/v1"
    - Guaranteed!
- `APIKey`:
    - Type: `string`
    - Description: Holds the `APIKey` configuration.
    - Properties: Nothing
    - Example: "OapiYxvm8PxXHzYurpasdfwqpGHa"
    - Guaranteed!
- `logPath`:
    - Type: `string`
    - Description: Holds the `logPath` configuration.
    - Properties:
        - Will have a forward slash at the end.
        - Will be absolute.
    - Example: "/var/log/statusscraper/"
    - Guaranteed!
- `logFiles`:
    - Type: `list.tuple.string`
    - Description: Holds the `logFiles` configuration.
    - Properties:
        - Each entry will hold a log file name in position zero and will hold a severity level in position one from the
          list (`logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`).
    - Example: [
                   ("statusscraper.log", logging.INFO),
                   ("error.log", logging.ERROR),
                   ("debug.log", logging.DEBUG)
               ]
    - Guaranteed!
- `enabledProviders`:
    - Type: `list.string`
    - Description: Holds the `enabledProviders` configuration.
    - Properties:
        - Holds the name of a fully implemented provider in the lib/providers path.
        - The name will be in lower case.
    - Example: [
                   "nfon",
                   "domainfactory"
               ]
    - Guaranteed!
- `manualComponents`:
    - Type: `list.tuple.string`
    - Description: Holds the `manualComponents` configuration.
    - Properties:
        - Each entry will hold a provider name in position zero and the manual component to be ignored in position one.
    - Example:[
                  ("nfon", "DTAD Telecomunications"),
                  ("domainfactory", "DTAD Mails")
              ]
    - Guaranteed!
- `componentsBlacklist`:
    - Type: `CaseInsensitiveDict.list.string`
    - Description: Holds the `componentsBlacklist` configuration.
    - Properties:
        - The key will be the provider name.
        - The value will be a list where each entry is a regex matching a component which is undesired.
        - The implementation of `CaseInsensitiveDict` is found in lib/internals/structures/classes.py.
    - Example: {
                   "nfon": [
                       r"secondary telephony",
                       r"devices"
                   ],       
                   "hubspot": [
                       r"hubSpot crm",
                       r"cta delivery",
                   ]       
               }
    - Not Guaranteed!
- `incidentsBlacklist`:
    - Type: `CaseInsensitiveDict.list.string`
    - Description: Holds the `incidentsBlacklist` configuration.
    - Properties:
        - The key will be the provider name.
        - The value will be a list where each entry is a regex matching an incident which is undesired.
        - The implementation of `CaseInsensitiveDict` is found in lib/internals/structures/classes.py.
    - Example: {
                   "NFON": [
                       r"nhospitality",
                       r"ncontrol"
                   ],       
                   "DomainFactory": [
                       r"wartungsarbeiten",
                       r"wartung",
                   ],       
                   "HubSpot": [
                       r"maintenance"
                   ]
               }
    - Not Guaranteed!
