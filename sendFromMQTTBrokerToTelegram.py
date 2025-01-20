import paho.mqtt.client as mqtt
import requests
import yaml

# Load configuration from YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]

# Telegram API URL
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# MQTT Broker details
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_TOPIC = 'sensor/data'

# Callback when message is received from MQTT broker
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    # Check for keywords to filter
    if "Hi" in payload or "Thanks" in payload:
        print(f"Filtered out message: {payload}")
        return  # Skip sending this message to Telegram

    telegram_payload = {
        'chat_id': CHAT_ID,
        'text': f'MQTT Message: {payload}'
    }
    response = requests.post(url, json=telegram_payload)
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message:', response.text)

# Setup MQTT client and connect
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(MQTT_TOPIC)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
