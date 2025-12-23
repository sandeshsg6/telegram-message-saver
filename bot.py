import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Get bot token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Directory to save messages
SAVE_DIR = "saved_messages"
os.makedirs(SAVE_DIR, exist_ok=True)

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Save text
    if message.text:
        with open(os.path.join(SAVE_DIR, f"{message.message_id}.txt"), "w", encoding="utf-8") as f:
            f.write(message.text)
        await message.reply_text("Text saved!")

    # Save photos (including albums)
    elif message.photo:
        for idx, photo in enumerate(message.photo):
            file = await photo.get_file()
            file_path = os.path.join(SAVE_DIR, f"{message.message_id}_{idx}.jpg")
            await file.download_to_drive(file_path)
        await message.reply_text("Photo(s) saved!")

    # Save videos
    elif message.video:
        file = await message.video.get_file()
        await file.download_to_drive(os.path.join(SAVE_DIR, f"{message.message_id}.mp4"))
        await message.reply_text("Video saved!")

    # Save audio
    elif message.audio:
        file = await message.audio.get_file()
        await file.download_to_drive(os.path.join(SAVE_DIR, message.audio.file_name))
        await message.reply_text("Audio saved!")

    # Save voice messages
    elif message.voice:
        file = await message.voice.get_file()
        await file.download_to_drive(os.path.join(SAVE_DIR, f"{message.message_id}.ogg"))
        await message.reply_text("Voice message saved!")

    # Save documents
    elif message.document:
        file = await message.document.get_file()
        await file.download_to_drive(os.path.join(SAVE_DIR, message.document.file_name))
        await message.reply_text("Document saved!")

app = ApplicationBuilder().token(TOKEN).build()

# Handle any forwarded message
app.add_handler(MessageHandler(filters.ALL & filters.FORWARDED, save_message))

print("Bot started...")
app.run_polling()
