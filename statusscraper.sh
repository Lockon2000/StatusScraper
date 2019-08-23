#!/bin/bash
### BEGIN SCRIPT INFO
# Scriptname:           statusscraper.sh
# Author:               Mohamed Abdelwahab
# Email:                mabdelwahab@dtad.de
# Last Changes:         22.08.2019
# Description:          StatusScraper is a utility which gathers information about service provider statuses
#                       and posts or synchronizes them to a configured output valve.
### END SCRIPT INFO


# Save the start time of the program
startTime=$(date +%s)

# Change current directory to the directory of this script, inhibit all output
cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

# Make sure the logs directory exists
logDir=$(./bin/statusscraper-cli get logPath)
if [[ ! -d $logDir ]]; then
    mkdir $logDir
fi

echo -e "Started ($(date -d "@$startTime"))" >>$logDir/runs.log

# This is the call to the actuall program. It is invoked in a specific python virtual environment.
# The program should have no direct output at all. Any such output is a bug that should be solved.
# And thus this output is catched in a seperate file to help observing it.
/usr/local/bin/pipenv run python3 ./main.py >>$logDir/output.log 2>&1


echo -e "Ended $(if [[ $? -eq 0 ]]; then echo "Normally"; else echo "Abnormally"; fi)" \
        "($(date +"%X") - Execution Time (in sec.): $(bc <<< $(date +%s)-$startTime))\n" \
        "----------------------------------" >>$logDir/runs.log

