from telethon import TelegramClient
import asyncio
import time

# Telegram credentials
api_id = 24363261
api_hash = 'e713babdb456b6606e1d968c91d96148'
phone_number = '+12174095604'

# Target group and message
target_group = -1002613074606
message = "Last Check!"

client = TelegramClient('session_name', api_id, api_hash)

async def send_message_periodically(initial_delay, repeat_interval):
    await client.start(phone_number)

    # Initial wait
    print(f"⏳ Waiting for {initial_delay} seconds before sending first message...")
    await asyncio.sleep(initial_delay)

    while True:
        await client.send_message(target_group, message)
        print(f"✅ Message sent to group {target_group} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Wait for next interval
        print(f"⏳ Waiting {repeat_interval} seconds before sending next message...")
        await asyncio.sleep(repeat_interval)

async def main():
    try:
        # Take custom timing inputs from user
        initial_delay = 5
        repeat_interval = int(input("🔁 Enter Repeat Interval between messages (in min): "))*60

        await send_message_periodically(initial_delay, repeat_interval)
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
