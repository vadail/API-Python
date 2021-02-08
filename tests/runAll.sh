
echo -e "Run All Test"

echo -e "\n============================================================ Cyclomatic Complexity Test =========================================================== \n"
chmod +x tests/complexity/test.sh
tests/complexity/test.sh

echo -e "\n==================================================================== Unit Test ==================================================================== \n"
chmod +x tests/unit -v
pytest tests/unit -v

echo -e "\n=============================================================== Code Coverage Test ================================================================ \n"
chmod +x tests/coverage/test.sh
tests/coverage/test.sh

echo -e "\n================================================================ Code Quality Test ================================================================ \n"
chmod +x tests/quality/test.sh
tests/quality/test.sh

echo -e "\n=================================================================  Security Test ================================================================== \n"
chmod +x tests/security/test.sh
tests/security/test.sh
