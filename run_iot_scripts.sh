#!/bin/bash

# Navigate to the folder containing the scripts
cd ./text-your-iot-device-scripts || {
    echo "Directory /text-your-iot-device-scripts not found!"
    exit 1
}

# Define Python scripts
SCRIPT_1="sendFromMQTTBrokerToTelegram.py"
SCRIPT_2="sendToBrokerFromTelegram.py"

# Check if the scripts exist
if [[ ! -f $SCRIPT_1 ]]; then
    echo "Error: $SCRIPT_1 not found!"
    exit 1
fi

if [[ ! -f $SCRIPT_2 ]]; then
    echo "Error: $SCRIPT_2 not found!"
    exit 1
fi

# Run the scripts in the background
echo "Starting $SCRIPT_1..."
nohup python3 $SCRIPT_1 > script1.log 2>&1 &

echo "Starting $SCRIPT_2..."
nohup python3 $SCRIPT_2 > script2.log 2>&1 &

# Display running processes
echo "Both scripts are now running in the background. 🎉"
echo "Logs are being written to script1.log and script2.log."
ps aux | grep -E "$SCRIPT_1|$SCRIPT_2" | grep -v grep