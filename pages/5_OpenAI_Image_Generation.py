from dotenv import load_dotenv

import streamlit as st
import openai
import os
from openai import OpenAI

load_dotenv()
st.set_page_config(
    page_title="OpenAI Image Generation",
    page_icon="🤖")

st.header("Imagine-Write-Get Image | OpenAI Image Generation")
client = OpenAI()


# openai.api_key = os.environ['OPENAI_API_KEY']

def execute_image_api(user_prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=user_prompt,
        size="256x256",
        quality="standard",
        n=2,
    )
    image_url = response.data[0].url
    return image_url


with st.form("image_generation"):
    prompt = st.text_input("Share your imaginations")
    prompt_execute = st.form_submit_button("Generate")
    if prompt_execute:
        st.image(execute_image_api(prompt))
