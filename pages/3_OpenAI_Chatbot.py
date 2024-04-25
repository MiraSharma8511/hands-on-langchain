from openai import OpenAI
import streamlit as st
import os
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

openai_api_key = openai.api_key
st.set_page_config(
    page_title="Chatbot",
    page_icon="💬"
)
#
# with st.form("getopenAIkey"):
#     key= st.text_input('OPENAI_API_KEY')
#     use_key= st.form_submit_button("🚀 Execute")
#     if use_key:
#         openai.api_key = key


st.title("💬 GenAI Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": "Hi, How are you?"}, {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("❤").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("🎶").write(msg)
