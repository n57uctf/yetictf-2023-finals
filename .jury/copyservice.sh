#!/bin/bash

rm -rf checkers && mkdir checkers

while read -r line; do
    service=$(echo $line | awk -F',' '{print $1}')
    pyfile="../$service/checker/checker.py"
    reqfile="../$service/checker/requirements.txt"
    if [[ ! -f $pyfile || ! -f $reqfile ]]; then
        continue
    fi
    if [[ -f $pyfile ]]; then
        cp $pyfile checkers/$service.py
    fi
    if [[ -f $reqfile ]]; then
        cp $reqfile checkers/$service-requirements.txt
    fi
    for x in ../$service/checker/*; do
        if [[ $(basename $x) != "checker.py" && $(basename $x) != "requirements.txt"  ]]; then
            cp -r $x checkers/$(basename $x)
        fi
    done
done < txt/services.csv

sort -u checkers/*-requirements.txt | grep -v requests >> checkers/all-requirements.txt
echo "requests" >> checkers/all-requirements.txt
