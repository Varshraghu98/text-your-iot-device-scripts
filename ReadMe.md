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

Setup Ubuntu based EC2 instance on AWS, provide the required UDP and TCP, ICMP (For pinging the EC2) connections in the security groups . 
While setting up the EC2 Instance IPv6 needs to be enabled on EC2 instance 
Refer this page to setup IPv6 address while launching the EC2 
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-ipv6-addresses.html

To run the scripts on the EC2 instance:
1. Ensure the **MQTT broker** is started on the EC2 instance.
2. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
3. Execute the shell script to start the Python scripts:
   ```bash
   chmod +x run_iot_scripts.sh  //Give executable permissions to execute the script
   ./run_iot_scripts.sh
   ```
   This will start the scripts that listen to the broker.
4. The logs generated by the scripts can be found in : 
```bash
   tail -f /home/ubuntu/text-your-iot-device-scripts/script2.log
   tail -f /home/ubuntu/text-your-iot-device-scripts/script1.log
   ```


## Additional Notes
- Ensure that Python 3 and necessary dependencies are installed before running the scripts.
- Install the required dependencies specified in the requirements.txt file using the pip install command,  
Note: To install dependencies via pip on ubuntu OS we might have to 
pip install --break-system-packages package_name
- The `config.yaml` file must be properly configured to ensure successful communication between the broker and Telegram bot.

For any issues, refer to the logs or reach out to the project maintainers.
