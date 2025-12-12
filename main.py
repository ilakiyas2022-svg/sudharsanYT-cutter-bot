from pyrogram import Client, filters
import os
import subprocess
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client(
    "yt_cut_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def download_video(url):
    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.mp4"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "video.mp4"


def cut_video(input_file, start, end, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ss", start,
        "-to", end,
        "-c", "copy",
        output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@app.on_message(filters.command("cut"))
async def cut_handler(client, message):
    try:
        parts = message.text.split()

        if len(parts) != 4:
            await message.reply("❗ Format:\n/cut <youtube_link> <start> <end>\nExample:\n/cut https://youtu.be/abc 10:24 12:35")
            return

        url = parts[1]
        start = parts[2]
        end = parts[3]

        await message.reply("⏳ Downloading video...")

        video = download_video(url)

        await message.reply("✂️ Cutting the video...")

        output = "cut_video.mp4"
        cut_video(video, start, end, output)

        await message.reply("🎬 Sending your video...")
        await message.reply_video(output)

        os.remove(video)
        os.remove(output)

    except Exception as e:
        await message.reply(f"❌ Error: {e}")


app.run()
