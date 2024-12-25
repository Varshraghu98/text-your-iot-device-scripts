import requests

# Replace with your actual bot token and chat ID
BOT_TOKEN = '7804241350:AAHqGGrZzzU3jtx3GBsCwDIJ3siqpLJNh-k'
CHAT_ID = '8190888160'

# Telegram API URL
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# Message payload
payload = {
    'chat_id': CHAT_ID,
    'text': 'Hello from AWS EC2!'
}

# Send request
response = requests.post(url, json=payload)

if response.status_code == 200:
    print('Message sent successfully!')
else:
    print('Failed to send message:', response.text)
