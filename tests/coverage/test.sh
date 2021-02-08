#!/bin/bash

testFile="todos/models/todoDAO.py"
input="tests/coverage/coverage.txt"
minCoverage=80

pipenv run coverage run --include=$testFile -m pytest tests/unit -v
pipenv run coverage report | tee $input

while IFS= read -r line
do

    if [[ $line == $testFile* ]]; then
        
        tokens=( ${line//%/} )
        coverage=$((${tokens[3]}))
        
        echo "Coverage: $coverage"
        
        if [[ $coverage -ge $minCoverage ]]; then
            echo "Coverage success"
            exit 0
        else
            echo "Coverage less than the minimun ($minCoverage)"
            exit 1
        fi
        
    fi
  
done < "$input"