import os
import re
import subprocess
import whisper
import streamlit as st

def get_video_title(url):
    import yt_dlp
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'tiktok_video')

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_tiktok_video(url, output_path='video.mp4'):
    command = [
        'yt-dlp',
        '-o', output_path,
        url
    ]
    subprocess.run(command, check=True)
    return output_path

def extract_audio(video_path, audio_path='audio.mp3'):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vn',
        '-c:a', 'libmp3lame',
        '-b:a', '192k',
        audio_path,
        '-y'
    ]
    subprocess.run(command, check=True)
    return audio_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

st.title("TikTok Video Transcriber")

tiktok_url = st.text_input("Enter the TikTok video URL:")

if st.button("Transcribe"):
    if tiktok_url:
        with st.spinner("Fetching video title..."):
            video_title = get_video_title(tiktok_url)
            safe_title = sanitize_filename(video_title)
            video_file = f'{safe_title}.mp4'
            audio_file = f'{safe_title}.mp3'
            transcript_file = f'{safe_title}.txt'

        with st.spinner("Downloading video..."):
            download_tiktok_video(tiktok_url, video_file)

        with st.spinner("Extracting audio..."):
            extract_audio(video_file, audio_file)

        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(audio_file)

        st.subheader("Transcript")
        st.write(transcript)

        # Save transcript to a file
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        st.success(f"Transcript saved to {transcript_file}")

        # Download button for transcript
        st.download_button(
            label="Download Transcript",
            data=transcript,
            file_name=transcript_file,
            mime='text/plain'
        )
    else:
        st.error("Please enter a valid TikTok URL.")
