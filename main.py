import os
import re
import subprocess
import whisper

def get_video_title(url):
    import yt_dlp
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'tiktok_video')


def sanitize_filename(name):
    # Remove invalid filename characters
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_tiktok_video(url, output_path='video.mp4'):
    # Download TikTok video using yt-dlp
    command = [
        'yt-dlp',
        '-o', output_path,
        url
    ]
    subprocess.run(command, check=True)
    return output_path

def extract_audio(video_path, audio_path='audio.mp3'):
    # Extract audio using ffmpeg
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vn',
        '-c:a', 'libmp3lame',
        '-b:a', '192k',
        audio_path,
        '-y'  # Overwrite output file if exists
    ]
    subprocess.run(command, check=True)
    return audio_path

def transcribe_audio(audio_path):
    # Transcribe audio using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    tiktok_url = input("Enter the TikTok video URL: ")

    print("Fetching video title...")
    video_title = get_video_title(tiktok_url)
    safe_title = sanitize_filename(video_title)
    video_file = f'{safe_title}.mp4'
    audio_file = f'{safe_title}.mp3'
    transcript_file = f'{safe_title}.txt'

    print("Downloading video...")
    download_tiktok_video(tiktok_url, video_file)

    print("Extracting audio...")
    extract_audio(video_file, audio_file)

    print("Transcribing audio...")
    transcript = transcribe_audio(audio_file)

    print("\n--- Transcript ---\n")
    print(transcript)

    # Save transcript to a file named after the video title
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    print(f"\nTranscript saved to {transcript_file}")
