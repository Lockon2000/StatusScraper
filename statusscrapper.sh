#!/bin/bash
### BEGIN SCRIPT INFO
# Scriptname:           statusscrapper.sh
# Author:               Mohamed Abdelwahab
# Email:                mabdelwahab@dtad.de
# Last Changes:         17.07.2019
# Short-Description:    scrape external status pages and fill cachet via API
### END SCRIPT INFO


cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

startTime=$(date +%s)

if [[ ! -d logs ]]; then
    mkdir logs
fi

echo -e "||||||||||||||||||||||||||||||| Started ($(date -d "@$startTime")) ||||||||||||||||||||||||||||||||\n" >>logs/statusscrapper.log

/usr/local/bin/pipenv run python3 ./main.py >>logs/statusscrapper.log 2>>logs/error.log

if [[ $? -eq 0 ]]; then
    echo -e "||||||||||||||||||||||||||||||| Ended Normally ($(date +"%X") - Execution Time: $(bc <<< $(date +%s)-$startTime)) ||||||||||||||||||||||||||||||||\n" >>logs/statusscrapper.log
else
    echo -e "||||||||||||||||||||||||||||||| Ended Abnormally ($(date +"%X") - Execution Time: $(bc <<< $(date +%s)-$startTime)) ||||||||||||||||||||||||||||||||\n" >>logs/statusscrapper.log
fi
