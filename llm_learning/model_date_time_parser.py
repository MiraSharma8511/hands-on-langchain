from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.output_parsers import DatetimeOutputParser
from langchain.prompts import PromptTemplate
import streamlit as st
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def convert_datetime_to_utc_date(iso_datetime_str):
    """
  Converts a string ISO datetime to UTC date format DD-MM-YYYY.

  Args:
    iso_datetime_str: The string ISO datetime to convert.

  Returns:
    The UTC date in DD-MM-YYYY format.
  """

    # Parse the ISO datetime string
    datetime_obj = datetime.fromisoformat(iso_datetime_str)

    # Convert to UTC and format as DD-MM-YYYY
    utc_date_str = datetime_obj.strftime("%d-%m-%Y")

    return utc_date_str


st.header("DATETIME_OUTPUT_PARSER")
model = ChatOpenAI()
output_parser = DatetimeOutputParser()

template = """Answer the users question: {question}

        {format_instructions}"""
# output_parser.set_format()
prompt = PromptTemplate.from_template(template,
                                      partial_variables={"format_instructions": output_parser.get_format_instructions()}
                                      )
PromptTemplate(input_variables=['question'], partial_variables={'format_instructions': "Write a datetime string that "
                                                                                       "matches the following "
                                                                                       "pattern:%Y-%m-%dT%H:%M:%S.%fZ"
                                                                                       "\nReturn ONLY this string, "
                                                                                       "no other words!"},
               template='Answer the users question:\n\n{question}\n\n{format_instructions}')

chain = prompt | model
chain = prompt | model | output_parser
question = st.text_input("Enter your question here...")
output = chain.invoke({"question": question})
# print(type(str(output)))
# print(convert_datetime_to_utc_date(str(output)))
st.write((output))
# st.write(convert_datetime_to_utc_date(str(output)))
