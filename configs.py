dtadCachetAPI = "http://cachet.workxl.de/api/v1"
APIKey = "Y9uZZFxfk61FacpuxyWc"
logFile = "logs/statusscrapper.log"
logLevel = "Normal"


# Blacklist for components
componentsBlacklist = {
    "NFON": [

    ],

    "DomainFactory": [

    ],

    "HubSpot": [

    ],

    "CloudFlare": [

    ]
}

# Blacklist for incidents
incidentsBlacklist = {
    "NFON": [
        r"nhospitality",
        r"ncontrol"
    ],

    "DomainFactory": [
        r"wartungsarbeiten",
        r"wartung",
        r"jiffybox",
        r"webslave",
        r"bank",
        r"cloud backup"
    ],

    "HubSpot": [
        r"maintenance"
    ],

    "CloudFlare": [

    ]
}

# Blacklist for maintenances
maintenancesBlacklist = {
    "NFON": [

    ],

    "DomainFactory": [

    ],

    "HubSpot": [

    ],

    "CloudFlare": [

    ]
}


if __name__ == "__main__":
    # Test configs
    print("No Tests yet!")
