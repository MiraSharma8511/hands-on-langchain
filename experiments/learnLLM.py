import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import openai

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

chain.invoke({"topic": "ice cream"})

prompt_value = prompt.invoke({"topic": "ice cream"})
print(prompt_value)

ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])
print(prompt_value.to_messages())
print(prompt_value.to_string())

message = model.invoke(prompt_value)
print(message)

print(output_parser.invoke(message))

