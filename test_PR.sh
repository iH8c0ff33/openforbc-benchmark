
#/bin.bash

echo
echo "INSTALLING DEPENDENCIES"
pip install flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

echo
echo "RUNNING FLAKE8"
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

echo
echo "RUNNING PYTEST"
pytest

echo
echo "RUNNING BASH TESTS"
bash ./bin/test_*
