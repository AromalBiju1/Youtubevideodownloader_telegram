import os
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
from datetime import datetime
import browser_cookie3 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def download_video(url, quality):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_file_name = f"downloaded_video_{timestamp}"
    file_path = os.path.join(os.getcwd(), base_file_name)

    ydl_opts = {
        'outtmpl': file_path,
        'format': quality,
        'retries': 3,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'cookies': browser_cookie3.chrome(), 
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
    quality = 'bestvideo+bestaudio/best'

    if context.args:
        if 'quality' in context.args:
            quality = context.args[context.args.index('quality') + 1] if len(context.args) > context.args.index('quality') + 1 else 'bestvideo+bestaudio/best'

    await update.message.reply_text(f"Downloading video in {quality} quality...")

    try:
        file_path = await download_video(url, quality)

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

