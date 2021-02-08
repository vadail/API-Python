#!/bin/bash

src="todos/"
report="tests/complexity/report.txt"
result="tests/complexity/result.txt"
minCC="B"

pipenv run radon cc $src | tee $report

echo "Cyclomatic Complexity Test:">$result

error_found=false
file=""
    
while IFS= read -r line
do
    
    if [[ $line == $src* ]]; then
        
        file=$line
    
    else
        
        complexity=${line: -1}
        
        if [[ $complexity > $minCC ]]; then
            
            error_found=true
            tokens=( ${line// / } )
            
            echo "Min CC $minCC. Error of cyclomatic complexity $complexity in ${tokens[2]} of module $file."
            echo "Min CC $minCC. Error of cyclomatic complexity $complexity in ${tokens[2]} of module $file">>$result
        fi
        
    fi
  
done < "$report"

if [ "$error_found" = true ] ; then
    echo ' '
    echo 'Cyclomatic Complexity test failed'
    echo "Cyclomatic Complexity test failed">>$result
    exit 1
else
    echo ' '
    echo 'Cyclomatic Complexity test passed'
    echo "Cyclomatic Complexity test passed">>$result
    exit 0
fi