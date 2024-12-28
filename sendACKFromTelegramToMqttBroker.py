import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "100.27.200.155"  # Replace with your EC2 instance IP or hostname
MQTT_PORT = 1884
MQTT_TOPIC = "sensor/data"  # Replace with the topic you want to publish to

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7804241350:AAHqGGrZzzU3jtx3GBsCwDIJ3siqpLJNh-k"  # Replace with your bot token

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

# Handler for incoming Telegram messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming Telegram messages and publishes them to MQTT."""
    message = update.message.text  # Extract message text
    logging.info(f"Received message from Telegram: {message}")

    # Publish to MQTT
    result = mqtt_client.publish(MQTT_TOPIC, message)
    status = result[0]

    if status == 0:
        logging.info(f"Sent message to MQTT topic {MQTT_TOPIC}: {message}")
    else:
        logging.error(f"Failed to send message to MQTT topic {MQTT_TOPIC}")

# Main function to set up the bot
async def main() -> None:
    # Create Application instance
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add a message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logging.info("Starting the bot...")
    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())