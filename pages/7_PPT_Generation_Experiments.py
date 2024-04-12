from openai import OpenAI
import streamlit as st
import os
import openai
from dotenv import load_dotenv

import re
from pexelsapi.pexels import Pexels

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
api = os.environ['PEXELS_API_KEY']

st.set_page_config(
    page_title="Chatbot",
    page_icon="💬"
)

api = os.environ['PEXELS_API_KEY']

def parse_response_to_ppt_content(response):
    text = response

    # Splitting text into sections
    sections = re.split(r'_+\n?', text.strip())

    # List to store dictionaries
    result = []

    # Regular expressions to extract title, image, and details
    title_pattern = re.compile(r'Title:\s*(.*?)\s*Image:', re.IGNORECASE | re.DOTALL)
    image_pattern = re.compile(r'Image:\s*\[(.*?)\]\s*Details:', re.IGNORECASE | re.DOTALL)
    details_pattern = re.compile(r'Details:\s*(.*?)$', re.IGNORECASE | re.DOTALL)

    # Extracting information for each section
    for section in sections:
        # Extracting title, image, and details
        title_match = re.search(title_pattern, section)
        image_match = re.search(image_pattern, section)
        details_match = re.search(details_pattern, section)

        # Creating dictionary for the section
        if title_match and image_match and details_match:
            section_dict = {
                "Title": title_match.group(1).strip(),
                "Image": image_match.group(1).strip(),
                "Details": details_match.group(1).strip()
            }
            result.append(section_dict)

    return result


def response_parser_response_to_ppt_slides(response):
    pexel = Pexels(api)
    slide_list = parse_response_to_ppt_content(response)
    for i in range(len(slide_list)):
        title = slide_list[i]['Title']
        st.header(title)
        image = slide_list[i]['Image']
        st.write(image)
        search_photos = pexel.search_photos(query=image, orientation='', size='50x50', color='', locale='', page=1,
                                            per_page=1)
        st.image(search_photos['photos'][0]['src']['original'])
        details = slide_list[i]['Details']
        st.write(details)


st.title("🤖💻📑👔 AI Generated PPTs")
client = OpenAI()
prompt=""

with st.form("ppt_generation_prompt"):
    topic = st.text_area("Enter topic related to which you want to generate slide upon")
    number_of_slides=st.slider("Enter number of slides")
    submitted = st.form_submit_button("Generate PPT")

    if submitted:
        prompt = ("""Generate %s slide of content for PPT on %s. Follow below rules:RULE-1: Each slide must contain "Title:","Image: ","Details: " RULE-2: Each slide must be separated by "_________________________________"RULE-3: Don't add slide number RULE-4: generate content between 1000 and 2000 characters only HARD RULE : Follow all above rules""" % (number_of_slides, topic))
        print(prompt)

with st.spinner("Generating content..."):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
        # prompt_text
    ).choices[0].message.content
    print(response)
    response_parser_response_to_ppt_slides(response)
