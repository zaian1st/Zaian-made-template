#!/bin/bash
set -e  
cd "$(dirname "$0")"
if pytest test.py; then
    echo "TEST STATUS: All Tests Passed Successfully"
    echo "Validation complete. The data pipeline has been successfully tested and is operational."
else
    echo "TEST STATUS: Errors Detected During Testing"
    exit 1
fi
