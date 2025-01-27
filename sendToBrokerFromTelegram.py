import asyncio
import logging

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import paho.mqtt.client as mqtt
from transformers import pipeline

# Load configuration from YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# MQTT Configuration
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
TELEGRAM_BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]
# MQTT Configuration
#MQTT_BROKER = "localhost"  # Replace with your EC2 instance IP or hostname
#MQTT_PORT = 1884
MQTT_TOPIC = "telegram/data"  # Raeplace with the topic you want to publish to

# Telegram Bot Token
#TELEGRAM_BOT_TOKEN = "7804241350:AAHqGGrZzzU3jtx3GBsCwDIJ3siqpLJNh-k"  # Replace with your bot token


# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# MQTT Client Setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.error(f"Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Load a zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Command to send temperature
async def send_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Request for temperature received."
    logging.info(f"Received /tmp command from Telegram.")

    # Publish to MQTT
    result = mqtt_client.publish(MQTT_TOPIC, message)
    status = result[0]

    if status == 0:
        logging.info(f"Sent message to MQTT topic {MQTT_TOPIC}: {message}")
        await update.message.reply_text("Temperature request has been sent to IOT device.🌡")
    else:
        logging.error(f"Failed to send message to MQTT topic {MQTT_TOPIC}")
        await update.message.reply_text("Failed to send the temperature request. Please try again later.")

# Handles messages to check if they relate to temperature
async def handle_temperature_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles messages to check if they relate to temperature."""
    message = update.message.text

    # Define the candidate labels for zero-shot classification
    labels = ["temperature query", "general query"]

    # Perform zero-shot classification
    result = classifier(message, labels)
    logging.info(f"Classification result: {result}")

    # Ignore thanks or acknowledgment messages
    if any(keyword in message for keyword in ["thank", "thanks", "okay", "ok", "great", "cool"]):
        logging.info("Acknowledgment message received. No action required.")
        return

    # Check if the query is about temperature
    if result["labels"][0] == "temperature query":
        await send_temperature(update, context)
    else:
        await update.message.reply_text("I can only check the temperature. Please ask about the temperature. 😉")

# Main function to set up the bot
async def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_temperature_query))

    logging.info("Starting the bot...")
    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())