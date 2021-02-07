#!/bin/bash

src="todos/"
report="tests/security/report.txt"
result="tests/security/result.txt"
maxIssues=$SECURITY_MAX_ISSUES

pipenv shell
bandit -r $src | tee $report

echo "Security Test:">$result

issues=0

while IFS= read -r line
do

    if [[ $line == *Issue:* ]]; then
        
        ((issues++))
        
        echo $line
        echo $line>>$result

    fi
  
done < "$report"

if (( issues > maxIssues )) ; then
    echo 'Security test failed'
    echo "Security test failed">>$result
    echo "  Max issues allowed: $maxIssues">>$result
    echo "Check more information about in $report">>$result
    exit 1
else
    echo 'Security test passed'
    echo "Security test passed">>$result
    echo "Check more information about in $report">>$result
    exit 0
fi