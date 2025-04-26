from telethon import TelegramClient

# Your API ID and Hash from Telegram's Developer Portal
api_id = 24363261
api_hash = 'e713babdb456b6606e1d968c91d96148'

# Your phone number (including country code)
phone_number = '+12174095604'

# The target group ID or username (you can get the group ID by adding the bot to the group)
target_group = -1002613074606  # e.g., 'mygroup' or '-100xxxxxxxxxx' for private groups

# The message you want to send
message = "working...!"

# Create the client
client = TelegramClient('session_name', api_id, api_hash)

async def send_message():
    # Connect to Telegram
    await client.start(phone_number)

    # Send the message to the group
    await client.send_message(target_group, message)
    print(f"Message sent to group {target_group}!")

    # Disconnect after sending the message
    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(send_message())
