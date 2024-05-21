from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import openai
import os
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']
os.environ["LANGCHAIN_TRACING_V2"] = "true"
langchain_key = os.environ["LANGCHAIN_API_KEY"]

# print(langchain_key)

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are great chatbot assistant."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
user_input = st.text_input("Enter your message here.. ")
st.write(user_input)

response = chain.invoke({"input": user_input})
st.write(response)
