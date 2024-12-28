import socket
import logging
import time
import struct

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# MQTT-SN Broker (RSMB) details
MQTT_SN_BROKER = '100.27.200.155'
MQTT_SN_PORT = 1883  # Default UDP port for MQTT-SN

# MQTT-SN Client settings
CLIENT_ID = 'sensor-client'
MQTT_SN_TOPIC = 'sensor/data'
TOPIC_ID = 1  # Use a predefined topic ID for simplicity
MESSAGE_ID = 1

# UDP socket setup
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(5)

# Helper function to send MQTT-SN packet
def send_packet(packet):
    udp_socket.sendto(packet, (MQTT_SN_BROKER, MQTT_SN_PORT))
    logging.info(f"Sent packet: {packet}")

# Increment message ID to avoid collisions
def increment_message_id():
    global MESSAGE_ID
    MESSAGE_ID += 1
    if MESSAGE_ID > 65535:
        MESSAGE_ID = 1

# Encode MQTT-SN CONNECT message
def connect():
    logging.info("Sending CONNECT message...")
    protocol_id = 0x01  # Protocol ID for MQTT-SN
    keep_alive = 0x0A  # Keep alive (10 seconds)
    client_id = CLIENT_ID.encode('utf-8')
    length = 6 + len(client_id)

    # Correct packet formation to include client_id properly
    packet = struct.pack("!BBH", length, 0x04, protocol_id) + struct.pack("!H", keep_alive) + client_id
    send_packet(packet)

# Encode MQTT-SN REGISTER message
def register_topic():
    logging.info("Sending REGISTER message...")
    topic_name = MQTT_SN_TOPIC.encode('utf-8')
    length = 6 + len(topic_name)

    # Proper struct packing for REGISTER
    packet = struct.pack("!BBHH", length, 0x0A, 0x0000, MESSAGE_ID) + topic_name
    send_packet(packet)

# Encode MQTT-SN PUBLISH message
def publish_message(payload):
    global MESSAGE_ID
    logging.info(f"Publishing message: {payload}")
    payload_bytes = payload.encode('utf-8')
    length = 7 + len(payload_bytes)
    flags = 0x00  # QoS 0, Predefined topic ID

    # Correct struct packing for PUBLISH message
    packet = struct.pack("!BBHBH", length, 0x0C, flags, TOPIC_ID, MESSAGE_ID) + payload_bytes
    send_packet(packet)

    increment_message_id()  # Increment message ID after sending

# Receive response from the broker
def receive_response():
    try:
        data, addr = udp_socket.recvfrom(1024)
        logging.info(f"Received response: {data}")
    except socket.timeout:
        logging.warning("No response from broker.")

if __name__ == "__main__":
    connect()
    receive_response()

    register_topic()
    receive_response()

    # Periodic message publishing
    try:
        while True:
            publish_message("Hello from MQTT-SN client")
            receive_response()
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Stopping MQTT-SN client...")
        udp_socket.close()