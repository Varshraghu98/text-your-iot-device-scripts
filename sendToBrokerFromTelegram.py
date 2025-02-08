# Import required libraries:
# - asyncio: for handling asynchronous execution
# - logging: for logging system messages and debugging
# - yaml: for loading configuration from an external YAML file
# - telegram: for handling Telegram API interactions
# - paho.mqtt.client: for MQTT communication with IoT devices
# - transformers: for machine learning-based natural language processing
import asyncio
import logging
import yaml
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import paho.mqtt.client as mqtt
from transformers import pipeline
import nest_asyncio

# Load configuration from YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Extract MQTT and Telegram configuration settings from the YAML file
# These values are used for MQTT communication and Telegram bot interactions
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
TELEGRAM_BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]

# Define the MQTT topic to be used for communication
# Ensure this topic matches the one used by the IoT device
MQTT_TOPIC = "telegram/data"


# Configure logging for debugging and monitoring bot activity
# This logs important events such as received messages and errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the MQTT client for communication with the broker
mqtt_client = mqtt.Client()

# Callback function triggered when the client successfully connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")   # Successful connection
    else:
        logging.error(f"Failed to connect, return code {rc}")  # Failed Connection

# Assign the on_connect callback function to the MQTT client
mqtt_client.on_connect = on_connect

# Connect the MQTT client to the broker using the specified address and port
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
# Start the MQTT network loop in a non-blocking manner
# This ensures the script continues running while maintaining the MQTT connection
mqtt_client.loop_start()

# Load a zero-shot classification pipeline using a pre-trained model
# This model helps classify user queries to determine if they are temperature-related
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Command handler function for sending temperature request via MQTT
async def send_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Request for temperature received."
    logging.info(f"Received /tmp command from Telegram.")

    # Publish the temperature request message to the MQTT topic
    result = mqtt_client.publish(MQTT_TOPIC, message)
    status = result[0]  # Extract the status of the publish attempt

    # Check if the message was successfully published
    if status == 0:
        logging.info(f"Sent message to MQTT topic {MQTT_TOPIC}: {message}")
        await update.message.reply_text("Temperature request has been sent to IOT device.🌡")
    else:
        logging.error(f"Failed to send message to MQTT topic {MQTT_TOPIC}")
        await update.message.reply_text("Failed to send the temperature request. Please try again later.")

# Message handler function to analyze user queries and determine if they relate to temperature
async def handle_temperature_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles messages to check if they relate to temperature."""
    message = update.message.text

    # Define the candidate labels for zero-shot classification
    labels = ["temperature query", "general query"]

    # Perform zero-shot classification
    result = classifier(message, labels)
    logging.info(f"Classification result: {result}")

    # Ignore generic acknowledgment messages to avoid unnecessary responses
    if any(keyword in message for keyword in ["thank", "thanks", "okay", "ok", "great", "cool"]):
        logging.info("Acknowledgment message received. No action required.")
        return

    # Check if the query is about temperature
    if result["labels"][0] == "temperature query":
        await send_temperature(update, context)
    else:
        await update.message.reply_text("I can only check the temperature. Please ask about the temperature. 😉")

# Main function to set up and start the Telegram bot
async def main() -> None:
    # Initialize the Telegram bot application with the provided bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_temperature_query))

    logging.info("Starting the bot...")
    # Start polling to receive updates from Telegram
    await application.run_polling()

# Entry point for the script execution
if __name__ == "__main__":
    # apply nest_asyncio to prevent event loop conflicts in some environments
    nest_asyncio.apply()
    # Run the main function asynchronously to start the bot
    asyncio.run(main())