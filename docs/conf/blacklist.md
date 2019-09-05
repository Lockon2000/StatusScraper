This Documentation explains for Administrators how to configure the blacklisting for StatusScraper.

# Configurations:

- `componentsBlacklist`:
    - Description: Tells the program which components to ignore.
    - Rules:
        - This configuration is given through an associative array with zero or more entries.
        - The key should be the provider name.
        - The value should be a list where each entry is a regex matching a component which is undesired.
        - Neither the provder name or the regexes are case sensitive.
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
    - Optional!
- `incidentsBlacklist`:
    - Description: Tells the program which incidents to ignore.
    - Rules:
        - This configuration is given through an associative array with zero or more entries.
        - The key should be the provider name.
        - The value should be a list where each entry is a regex matching an incident which is undesired.
        - Neither the provder name or the regexes are case sensitive.
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
    - Optional!

