#!/bin/bash

src="todos/"
report="tests/quality/report.txt"
result="tests/quality/result.txt"
maxError=0
maxWarning=0
maxAlert=0

pipenv run flake8 $src | tee $report

echo "Code Quality Test:">$result
            
error_found=0
warning_found=0
alert_found=0

file=""

while IFS= read -r line
do

    tokens=( ${line// / } )
    
    error=${tokens[1]}
    
    error_type=${error:0:1}
    
    case $error_type in

        W)
            ((warning_found++))
        ;;
    
        E)
            ((error_found++))
        ;;
    
        *)
            ((alert_found++))
        ;;
    esac
    
done < "$report"

echo "  Warnings found: $warning_found">>$result
echo "  Errors found: $error_found">>$result
echo "  Alerts found: $alert_found">>$result

if (( warning_found > maxWarning )) || 
   (( error_found > maxError )) || 
   (( alert_found > maxAlert )) ; then
    echo 'Code Quality test failed'
    echo "Code Quality test failed">>$result
    echo "  Max Warning allowed: $maxWarning">>$result
    echo "  Max Error allowed: $maxError">>$result
    echo "  Max Alerts allowed: $maxAlert">>$result
    echo "Check more information about in $report">>$result
    exit 1
else
    echo 'Code Quality test passed'
    echo "Code Quality test passed">>$result
    echo "Check more information about in $report">>$result
    exit 0
fi
