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

st.title("💬 Chatbot")
# st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

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
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


"""
References:
- For multiple page sample code -  https://github.com/francescocarlucci/learn-langchain/blob/main/pages/1LLMs.py
- For multiple page example - https://learnlangchain.streamlit.app/Chains
- Chatbot session example on streamlit - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
- Multipage app guidance by streamlit - https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
"""