import os
import asyncio  
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
from datetime import datetime

TOKEN = "7783482159:AAG7lYAtwwmikbnHqWvDHcZM6J342nG1LCE"

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    merged_file_path = f"{file_path}.mp4"
    
    return merged_file_path

async def start(update, context):
    await update.message.reply_text("Send me a video link to download.")

async def download(update, context):
    url = update.message.text
    await update.message.reply_text("Downloading video...")

    try:
        file_path = await download_video(url)

        while not os.path.exists(file_path):
            await asyncio.sleep(1)

        await update.message.reply_text("Uploading video...")
        with open(file_path, "rb") as video_file:
            await update.message.reply_video(video=video_file)
        
        await update.message.reply_text("Video uploaded successfully!")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    application.run_polling()

if __name__ == "__main__":
    main()
