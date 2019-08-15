#!/bin/bash
### BEGIN SCRIPT INFO
# Scriptname:           statusscraper.sh
# Author:               Mohamed Abdelwahab
# Email:                mabdelwahab@dtad.de
# Last Changes:         14.08.2019
### END SCRIPT INFO


cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

startTime=$(date +%s)

if [[ ! -d logs ]]; then
    mkdir logs
fi

echo -e "||||||||||||||||||||||||||||||| Started ($(date -d "@$startTime")) ||||||||||||||||||||||||||||||||\n" >>logs/statusscraper.log

/usr/local/bin/pipenv run python3 ./main.py >>logs/statusscraper.log 2>>logs/error.log

if [[ $? -eq 0 ]]; then
    echo -e "||||||||||||||||||||||||||||||| Ended Normally ($(date +"%X") - Execution Time: $(bc <<< $(date +%s)-$startTime)) ||||||||||||||||||||||||||||||||\n" >>logs/statusscraper.log
else
    echo -e "||||||||||||||||||||||||||||||| Ended Abnormally ($(date +"%X") - Execution Time: $(bc <<< $(date +%s)-$startTime)) ||||||||||||||||||||||||||||||||\n" >>logs/statusscraper.log
fi
