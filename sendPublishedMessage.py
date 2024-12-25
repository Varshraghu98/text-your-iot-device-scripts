import paho.mqtt.client as mqtt
import requests

# Replace with your actual bot token and chat ID
BOT_TOKEN = '7804241350:AAHqGGrZzzU3jtx3GBsCwDIJ3siqpLJNh-k'
CHAT_ID = '8190888160'

# Telegram API URL
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# MQTT Broker details
MQTT_BROKER = 'localhost'
MQTT_PORT = 1884
MQTT_TOPIC = 'sensor/data'

# Callback when message is received from MQTT broker
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
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
