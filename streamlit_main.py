import os
import re
import subprocess
import whisper
import streamlit as st
from chatbot import analyze_transcript

# Define your persona
persona = {
    "name": "Kevin Neo",
    "race": "Chinese",
    "nationality": "Singaporean",
    "Language": "Mandarin, English",
    "style": "friendly, informative, concise",
    "job": "Crypto Digital Marketing Manager for Saprolings Pte Ltd, a crypto consultancy and marketing firm that helps DeFi projects, previous worked with renowned projects such as Boba & Hasbulla",
    "interests": ["tech", "coding", "AI", "TikTok trends"],
    "catchphrases": ["Let's dive in!", "Here's a quick tip:", "Stay curious!"]
}

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

st.title("TikTok Video Transcriber & AI Persona Analyzer")

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

        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        st.success(f"Transcript saved to {transcript_file}")

        st.download_button(
            label="Download Transcript",
            data=transcript,
            file_name=transcript_file,
            mime='text/plain'
        )

        # AI Persona Analysis Button
        if st.button("Analyze Transcript as Kevin Neo"):
            with st.spinner("Analyzing transcript with AI persona..."):
                ai_summary = analyze_transcript(transcript, persona)
            st.subheader("AI-Generated Summary")
            st.write(ai_summary)
            st.download_button(
                label="Download AI Summary",
                data=ai_summary,
                file_name=f"{safe_title}_ai_summary.txt",
                mime='text/plain'
            )
    else:
        st.error("Please enter a valid TikTok URL.")
