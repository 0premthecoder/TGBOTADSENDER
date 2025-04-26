import asyncio
from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Your Telegram Bot Token
TOKEN = "7789542725:AAHVWw90shiE231M4UefPrQXRrTsixETI-k"

# Temporary storage (for each user session)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 Welcome! Please send me your API ID.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {'step': 'api_id'}

    step = user_data[user_id]['step']

    if step == 'api_id':
        try:
            user_data[user_id]['api_id'] = int(text)
            user_data[user_id]['step'] = 'api_hash'
            await update.message.reply_text('✅ Got it. Now send me your API Hash.')
        except ValueError:
            await update.message.reply_text('⚠️ API ID must be a number. Please enter it again.')

    elif step == 'api_hash':
        user_data[user_id]['api_hash'] = text
        user_data[user_id]['step'] = 'phone_number'
        await update.message.reply_text('📞 Now send me your Phone Number (with country code).')

    elif step == 'phone_number':
        user_data[user_id]['phone_number'] = text
        user_data[user_id]['step'] = 'target_group'
        await update.message.reply_text('🎯 Please send me the Target Group ID (e.g., -100xxxxxxxxxx) or @username.')

    elif step == 'target_group':
        user_data[user_id]['target_group'] = text
        user_data[user_id]['step'] = 'message'
        await update.message.reply_text('✉️ Almost done! Now send me the Message you want to deliver.')

    elif step == 'message':
        user_data[user_id]['message'] = text
        await update.message.reply_text('🚀 Sending your message... Please wait.')

        # Actually send the message
        try:
            await send_message(user_data[user_id])
            await update.message.reply_text('✅ Message sent successfully!')
        except Exception as e:
            await update.message.reply_text(f'❌ Error: {str(e)}')

        # Clear session
        user_data.pop(user_id)

async def send_message(data):
    api_id = data['api_id']
    api_hash = data['api_hash']
    phone_number = data['phone_number']
    target_group = data['target_group']
    message = data['message']

    # Using dynamic session name to avoid conflicts
    session_name = f"session_{phone_number.replace('+', '')}"

    client = TelegramClient(session_name, api_id, api_hash)
    
    await client.start(phone_number)# 👇 Check and convert if needed
    if target_group.lstrip('-').isdigit():
        target_group = int(target_group)

    await client.send_message(target_group, message)
    await client.disconnect()

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running. Waiting for commands...")
    app.run_polling()

if __name__ == '__main__':
    main()
