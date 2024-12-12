#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
cd "$(dirname "$0")"
echo "Starting test execution..."

# Run pytest 
pytest_output=$(pytest test.py --disable-warnings --tb=short)
pytest_exit_code=$?

# Calculate score based on passed and failed tests
total_tests=$(echo "$pytest_output" | grep -oP 'collected \K[0-9]+')
passed_tests=$(echo "$pytest_output" | grep -oP '\b[0-9]+ passed\b' | grep -oP '[0-9]+')
failed_tests=$((total_tests - passed_tests))

# Each test  20 marks Display the score
marks_per_test=20
total_marks=$((total_tests * marks_per_test))
score=$((passed_tests * marks_per_test))
if [ "$pytest_exit_code" -eq 0 ]; then
    echo "All tests passed successfully."
else
    echo "Some tests failed."
fi
echo "Test Score: $score out of $total_marks"
exit $pytest_exit_code
