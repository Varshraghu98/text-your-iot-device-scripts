# Import required libraries:
# - paho.mqtt.client for MQTT protocol handling
# - requests for sending HTTP requests
# - yaml for reading configuration files
# - json for handling JSON data
import paho.mqtt.client as mqtt
import requests
import yaml
import json

# Load configuration details (like MQTT broker info and Telegram bot credentials) from a YAML file
# This ensures flexibility by separating code from configuration data
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
# Replace placeholders with actual values from the loaded YAML configuration
TELEGRAM_BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]

# Set up the Telegram API endpoint using the bot token
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# Define MQTT broker details, including broker address, port, and topic to subscribe to
# These are also loaded from the YAML configuration file
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_TOPIC = 'sensor/data'
# Callback function triggered whenever a message is received on the subscribed topic
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')

    # Parse the JSON payload
    try:
        payload_data = json.loads(payload)
        temperature = payload_data.get("temperature")

        if temperature is not None:
            # Format temperature with degree Celsius symbol
            temperature_message = f"The recorded temperature is  {temperature}°C. 🌡"

            telegram_payload = {
                'chat_id': CHAT_ID,
                'text': f'{temperature_message}'
            }
            response = requests.post(url, json=telegram_payload)
            if response.status_code == 200:
                print('Message sent successfully!')
            else:
                print('Failed to send message:', response.text)
        else:
            print("Temperature not found in payload:", payload)

    except json.JSONDecodeError:
        print("Invalid JSON payload:", payload)


# Setup MQTT client and connect
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(MQTT_TOPIC)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
