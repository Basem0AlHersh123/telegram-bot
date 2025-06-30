import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Get values from environment variables
YOUR_TELEGRAM_ID = int(os.getenv("YOUR_TELEGRAM_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    caption = f"📩 From: {user.full_name}"
    if user.username:
        caption += f" (@{user.username})"
    caption += f"\nUser ID: {user.id}"

    try:
        if message.text:
            await context.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=f"{caption}\n\n{message.text}")
        elif message.photo:
            photo_file_id = message.photo[-1].file_id
            await context.bot.send_photo(chat_id=YOUR_TELEGRAM_ID, photo=photo_file_id, caption=caption)
        elif message.document:
            doc_file_id = message.document.file_id
            await context.bot.send_document(chat_id=YOUR_TELEGRAM_ID, document=doc_file_id, caption=caption)
        elif message.audio:
            audio_file_id = message.audio.file_id
            await context.bot.send_audio(chat_id=YOUR_TELEGRAM_ID, audio=audio_file_id, caption=caption)
        elif message.video:
            video_file_id = message.video.file_id
            await context.bot.send_video(chat_id=YOUR_TELEGRAM_ID, video=video_file_id, caption=caption)
        elif message.voice:
            voice_file_id = message.voice.file_id
            await context.bot.send_voice(chat_id=YOUR_TELEGRAM_ID, voice=voice_file_id, caption=caption)
        elif message.sticker:
            sticker_file_id = message.sticker.file_id
            await context.bot.send_sticker(chat_id=YOUR_TELEGRAM_ID, sticker=sticker_file_id)
            await context.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=caption)
    except Exception as e:
        print(f"Error forwarding message: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(~filters.COMMAND, forward_message))

print("✅ Bot is running...")
app.run_polling()