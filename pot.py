import os
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def download_video(url):  
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_file_name = f"downloaded_video_{timestamp}"
    file_path = os.path.join(os.getcwd(), base_file_name)

    ydl_opts = {
        'outtmpl': file_path,
        'format': 'bestvideo+bestaudio/best',
        'retries': 3,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'cookies': 'https://raw.githubusercontent.com/AromalBiju1/Youtubevideodownloader_telegram/refs/heads/main/cookies.txt'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

    merged_file_path = f"{file_path}.mp4"
    return merged_file_path

async def start(update, context):
    await update.message.reply_text("Send me a video link to download.")

async def download(update, context):
    url = update.message.text
    await update.message.reply_text("Downloading video...")

    try:
        file_path = await download_video(url)

        if file_path and os.path.exists(file_path):
            await update.message.reply_text("Uploading video...")
            with open(file_path, "rb") as video_file:
                await update.message.reply_video(video=video_file)

            await update.message.reply_text("Video uploaded successfully!")
        else:
            await update.message.reply_text("Failed to download the video.")

    except Exception as e:
        logger.error(f"Error in download handler: {e}")
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    application.run_polling()

if __name__ == "__main__":
    main()
