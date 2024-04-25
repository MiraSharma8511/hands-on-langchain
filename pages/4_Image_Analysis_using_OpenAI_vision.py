import os

import openai
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
st.set_page_config(page_title="Video Analysis")
st.header("Image Analysis | Chat with image")

client = OpenAI()

with st.form("imageurl"):
    imageURL = st.text_input("Enter the image URL here")
    ask_question = st.text_area("ask your question")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if imageURL != "" or imageURL is not None:
            st.image(imageURL)
        with st.spinner("Doing Image Analysis"):
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": ask_question
                             },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": imageURL,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )

        st.header("Image Summary")
        image_summary = response.choices[0].message.content
        st.write(image_summary)

        with st.spinner('Generating audio...'):
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=image_summary
            )
            response.write_to_file("summary_output.mp3")

        st.header("Listen the image summary audio")

        with open("summary_output.mp3", "rb") as audio_file:
            st.audio(audio_file, format='audio/mp3')
