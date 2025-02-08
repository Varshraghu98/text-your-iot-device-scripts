# IoT Communication Scripts

This project contains the scripts required to enable communication between the **Mosquitto.rsmb** broker running on the **EC2 instance**, sensors, and the **Telegram sensor data bot**.

## Scripts Overview

The two main scripts are:
- [`sendFromMQTTBrokerToTelegram.py`](sendFromMQTTBrokerToTelegram.py)
- [`sendToBrokerFromTelegram.py`](sendToBrokerFromTelegram.py)

## Configuration

To run these scripts locally, update the configurations in [`config.yaml`](config.yaml).

## Running the Scripts

### Running Locally

To start the scripts manually:
```bash
python3 sendToBrokerFromTelegram.py
```

Alternatively, you can execute the shell script:
```bash
./run_iot_scripts.sh
```

When executed locally, the scripts will connect to the MQTT broker running on the **EC2 instance**.

### Running on EC2 Instance

To run the scripts on the EC2 instance:
1. Ensure the **MQTT broker** is started on the EC2 instance.
2. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
3. Execute the shell script to start the Python scripts:
   ```bash
   ./run_iot_scripts.sh
   ```
   This will start the scripts that listen to the broker.

## Additional Notes
- Ensure that Python 3 and necessary dependencies are installed before running the scripts.
- The `config.yaml` file must be properly configured to ensure successful communication between the broker and Telegram bot.

For any issues, refer to the logs or reach out to the project maintainers.
