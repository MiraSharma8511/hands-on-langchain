from openai import OpenAI
import streamlit as st
import os
import openai
from dotenv import load_dotenv
from response_parser_to_PPT import response_parser

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
openai_api_key = openai.api_key
api = os.environ['PEXELS_API_KEY']

st.set_page_config(
    page_title="Chatbot",
    page_icon="💬"
)

response = ""

st.title("🤖💻📑👔 AI Generated PPTs")
client = OpenAI()
with st.form("ppt_generation_prompt"):
    Topic = st.text_area("Enter topic related to which you want to generate slide upon")

# prompt = """
# Generate 5 slide of content for PPT on IT Operating Model. Follow below rules:
# RULE-1: Each slide must contain "Title:","Image: ","Details: "
# RULE-2: Each slide must be separated by "_________________________________\n"
# RULE-3: Don't add slide number
# RULE-4: generate content between 1000 and 2000 characters only
# HARD RULE : Follow all above rules
# """
    submitted = st.form_submit_button("Generate PPT")
    if submitted:
        # response = client.chat.completions.create(
        #   model="gpt-3.5-turbo",
        #   prompt=prompt_text,
        #   max_tokens=500
        # ).choices[0].text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt_text}]
            # prompt_text
        ).choices[0].message.content

        response_parser(response)