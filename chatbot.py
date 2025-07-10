import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

def analyze_transcript(transcript, persona):
    prompt = f"""
You are {persona['name']}, a {persona['race']} {persona['nationality']} who speaks {persona['Language']}.
Your job: {persona['job']}
Your style: {persona['style']}
Your interests: {', '.join(persona['interests'])}
Use catchphrases like: {', '.join(persona['catchphrases'])}

Analyze the following transcript, extract the main ideas, and summarize it in your own style:

Transcript:
{transcript}
"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()
