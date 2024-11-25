import requests
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
stability_api = os.environ['STABILITY_API_KEY']

with st.form("get_image_input"):
    prompt = st.text_input("Enter prompt for image generation", value = "Golden gate of fortune")
    file_name = st.text_input("Enter file name to save file", value="golden-gate-fortune")
    submit = st.form_submit_button("Generate Image")
    if submit:
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "authorization": f"Bearer {stability_api}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": f"{prompt}",
                "output_format": "png",
            },
        )
        if response.status_code == 200:
            with open(f"./{file_name}.png", 'wb') as file:
                img = response.content
                file.write(img)
                st.image(img)
        else:
            raise Exception(str(response.json()))
