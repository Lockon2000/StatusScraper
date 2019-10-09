#!/bin/bash
### BEGIN SCRIPT INFO
# Scriptname:           statusscraper.sh
# Author:               Mohamed Abdelwahab
# Email:                mabdelwahab@dtad.de
# Last Changes:         05.09.2019
# Description:          StatusScraper is a utility which gathers information about service provider statuses
#                       and posts or synchronizes them to a configured output valve.
### END SCRIPT INFO


# Save the start time of the program
startTime=$(date +%s)

# Change current directory to the directory of this script, inhibit all output
cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

# Make sure the ./logs directory is present for (at least) basic logging, if not, create it
if [[ ! -d ./logs ]]; then
    mkdir ./logs

    # Check whether the creation of the ./logs directory was successfull, if not, then exit
    if [[ $? -ne 0 ]]; then
        1>&2 echo "Basic logging could not be ensured. Exiting program!"
        exit 1
    fi
fi

# Get the configured log path
logDir=$(./bin/statusscraper-cli get logPath 2>>./logs/output.log)

# Check whether the logPath variable was retrieved successfully
if [[ $? -ne 0 ]]; then
     2>>./logs/output.log 1>&2 echo "Log directory couldn't be retrieved. Exiting program!"
    exit 1
fi

# Make sure the log directory exists, otherwise create it
if [[ ! -d $logDir ]]; then
    mkdir $logDir

    # Check whether the The creation of the log directory was successfull, if not then exit
    if [[ $? -ne 0 ]]; then
         2>>./logs/output.log 1>&2 echo "Log directory is not present and couldn't be created. Exiting program!"
        exit 1
    fi
fi

# As of now, the configured $logDir is available, so log there

# Log the starting time
echo "Started ($(date -d "@$startTime"))" >>$logDir/runs.log

# This is the call to the actuall program. It is invoked in a specific python virtual environment.
# The program should have no direct output at all. Any such output is a critical error or a bug that should
# be resolved. Thus this output is catched in a seperate file to help observing and resolving it.
/usr/local/bin/pipenv run python3 ./main.py >>$logDir/output.log 2>&1

# Log the ending time
echo -e "Ended $(if [[ $? -eq 0 ]]; then echo "Normally"; else echo "Abnormally"; fi)" \
        "($(date +"%X") - Execution Time (in sec.): $(bc <<< $(date +%s)-$startTime))\n" \
        "----------------------------------" >>$logDir/runs.log

