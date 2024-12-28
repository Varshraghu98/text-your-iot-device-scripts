import paho.mqtt.client as mqtt
import logging
import socket

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# MQTT-SN Broker (RSMB) details
MQTT_SN_BROKER = '54.234.116.159'  # Address of the MQTT-SN broker
MQTT_SN_PORT = 1883  # UDP port for MQTT-SN (default for RSMB)
MQTT_SN_TOPIC = 'sensor/datasn'

# MQTT Broker (Destination) details
MQTT_BROKER = '54.234.116.159'
MQTT_PORT = 1884
MQTT_TOPIC = 'sensor/data'

# Initialize MQTT client
mqtt_client = mqtt.Client()

# Setup UDP socket for MQTT-SN communication
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', MQTT_SN_PORT))

# Callback when a message is received from UDP (MQTT-SN)
def on_mqtt_sn_message(data, addr):
    logging.info(f"Received message from MQTT-SN: {data}")

    # Extract payload and forward to MQTT Broker
    payload = data.decode('utf-8')
    result = mqtt_client.publish(MQTT_TOPIC, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        logging.info(f"Message forwarded to MQTT Broker on topic {MQTT_TOPIC}: {payload}")
    else:
        logging.error(f"Failed to forward message to MQTT Broker on topic {MQTT_TOPIC}")

# Listen for incoming MQTT-SN messages
def listen_udp():
    logging.info("Listening for MQTT-SN messages...")
    while True:
        data, addr = udp_socket.recvfrom(1024)
        on_mqtt_sn_message(data, addr)

# Callback when connected to the MQTT Broker
def on_connect_mqtt(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully.")
    else:
        logging.error(f"Failed to connect to MQTT Broker, return code {rc}")

# Setup MQTT Client (Destination)
mqtt_client.on_connect = on_connect_mqtt
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT loops
mqtt_client.loop_start()

try:
    listen_udp()
except KeyboardInterrupt:
    logging.info("Stopping MQTT-SN listener...")
    udp_socket.close()
