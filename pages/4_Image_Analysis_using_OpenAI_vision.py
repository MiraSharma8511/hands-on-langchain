import os

import openai
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()
st.header("OpenAI Vison GPT-4-Turbo")

with st.form("imageurl"):
    imageURL = st.text_input("Enter the image URL here")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.image(imageURL)
        response = client.chat.completions.create(
          model="gpt-4-turbo",
          messages=[
            {
              "role": "user",
              "content": [
                {"type": "text",
                 "text": "What’s in this image?, What is the image about?, summary of image"},
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

        # audio_response = client.audio.speech.create(
        #     model="tts-1",
        #     voice="alloy",
        #     input=image_summary
        # )
        # st.audio(audio_response.content)

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



# from pathlib import Path
# from openai import OpenAI
#
# client = OpenAI()

# response.stream_to_file(speech_file_path)
# speech_file_path = Path(__file__).parent / "speech.mp3"

