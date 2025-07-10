import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

def analyze_transcript(transcript, persona, video_desc, ai_goal):
    prompt = f"""
You are {persona['name']}, a {persona['race']} {persona['nationality']} who speaks {persona['Language']}.
Your job: {persona['job']}
Your style: {persona['style']}
Your interests: {', '.join(persona['interests'])}
Use catchphrases like: {', '.join(persona['catchphrases'])}

Original video description: {video_desc}
Desired outcome: {ai_goal}

Given the transcript below, write a new TikTok script that matches the desired outcome. Transform the content as needed, and ensure it is distinct from the original.

Transcript:
{transcript}
"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()
