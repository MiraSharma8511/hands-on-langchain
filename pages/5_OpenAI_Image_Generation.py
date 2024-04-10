from dotenv import load_dotenv

import streamlit as st
import openai
import os
from openai import OpenAI

load_dotenv()
st.set_page_config(
    page_title="OpenAI Image Generation",
    page_icon="🤖")

with st.form("getopenAIkey"):
    openai.api_key= st.text_input('OPENAI_API_KEY')
    use_key= st.form_submit_button("🚀 Execute")
    # if use_key:
    #     openai.api_key = key


# openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()
with st.form("image_genaration"):
    prompt = st.text_input("Share your imaginations")
    prompt_execute = st.form_submit_button("Generate")
    if prompt_execute:
        response = client.images.generate(
          model="dall-e-2",
          prompt=prompt,
          size="256x256",
          quality="standard",
          n=2,
        )

        image_url = response.data[0].url
        st.image(image_url)