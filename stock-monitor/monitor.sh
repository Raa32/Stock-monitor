#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/alert.log"
PYTHON_SCRIPT="$SCRIPT_DIR/monitor.py"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] monitor.sh started" >> "$LOG_FILE"

if ! command -v python3 &> /dev/null; then
    echo "[$TIMESTAMP] ERROR: python3 not found" >> "$LOG_FILE"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "[$TIMESTAMP] ERROR: monitor.py not found at $PYTHON_SCRIPT" >> "$LOG_FILE"
    exit 1
fi

python3 "$PYTHON_SCRIPT"

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "[$TIMESTAMP] ERROR: monitor.py exited with code $EXIT_CODE" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] monitor.sh completed" >> "$LOG_FILE"
