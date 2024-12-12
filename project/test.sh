#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Navigate to the directory containing the script
cd "$(dirname "$0")"

echo "Starting test execution..."

# Run tests using pytest
if pytest test.py --disable-warnings; then
    echo "TEST STATUS: All tests passed successfully."
    echo "Validation complete. The data pipeline has been successfully tested and is operational."
else
    echo "TEST STATUS: Errors detected during testing."
    exit 1
fi
