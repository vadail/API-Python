EXIT_STATUS=0

function check_command {
    "$@"
    local STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "error with $1 ($STATUS)" >&2
        EXIT_STATUS=$STATUS
    fi
}

echo -e "Run All Test"

echo -e "\n============================================================ Cyclomatic Complexity Test =========================================================== \n"
chmod +x tests/complexity/test.sh
check_command tests/complexity/test.sh

echo -e "\n==================================================================== Unit Test ==================================================================== \n"
check_command pipenv run pytest tests/unit -v

echo -e "\n=============================================================== Code Coverage Test ================================================================ \n"
chmod +x tests/coverage/test.sh
check_command tests/coverage/test.sh

echo -e "\n================================================================ Code Quality Test ================================================================ \n"
chmod +x tests/quality/test.sh
check_command tests/quality/test.sh

echo -e "\n=================================================================  Security Test ================================================================== \n"
chmod +x tests/security/test.sh
check_command tests/security/test.sh

exit $EXIT_STATUS