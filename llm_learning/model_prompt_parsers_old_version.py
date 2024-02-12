from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import streamlit as st
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
llm_model = "gpt-3.5-turbo"


def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message.content


st.header("Model-Prompt-Parser")
tab1, tab2, = st.tabs(["Prompt", "Output Parser"])

with tab1:
    st.subheader("Prompt")
    customer_email = st.text_area('Enter customer email')
    style = st.text_area('Enter style')
    # st.button("Submit Email")
    prompt = f"""Translate the text \
    that is delimited by triple backticks
    into a style that is {style}.
    text: ```{customer_email}```
"""
    st.write(get_completion(prompt))


def execute_output_parser():
    product_schema = ResponseSchema(name="product",
                                    description="Was the item purchased?\
                             Answer name of the product")
    product_qty = ResponseSchema(name="product_qty",
                                 description="how many item(s) purchased?\
                             extract total number of qty bought\
                             Answer total number of the product(s) purchased")
    product_brand_schema = ResponseSchema(name="product_brand",
                                          description="What is the brand of the item purchased?\
                             Answer name of the product brand")

    gift_schema = ResponseSchema(name="gift",
                                 description="Was the item purchased\
                             as a gift for someone else? \
                             Answer True if yes,\
                             False if not\
                             Unknown if unknown.")
    delivery_days_schema = ResponseSchema(name="delivery_days",
                                          description="How many days\
                                      did it take for the product\
                                      to arrive? If this \
                                      information is not found,\
                                      output -1.")
    price_value_schema = ResponseSchema(name="price_value",
                                        description="Extract any\
                                    sentences about the value or \
                                    price, and output them as a \
                                    comma separated Python list.")
    sentiment_schema = ResponseSchema(name="sentiment",
                                      description="what the reviewer feels about the product purchased?\
                                               Answer classifying it as Positive, Negative, Mixed, Unknown")

    response_schemas = [gift_schema,
                        product_schema,
                        product_brand_schema,
                        product_qty,
                        delivery_days_schema,
                        price_value_schema,
                        sentiment_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    review_template_2 = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product\
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

text: {text}

{format_instructions}
"""

    prompt = ChatPromptTemplate.from_template(template=review_template_2)

    messages = prompt.format_messages(text=customer_review, format_instructions=format_instructions)

    response = chat(messages)

    output_dict = output_parser.parse(response.content)
    st.write(output_dict)


with tab2:
    st.header("OUTPUT PARSER")
    customer_review = st.text_area("Enter customer review")
    st.button("Submit Review", on_click=execute_output_parser)
    chat = ChatOpenAI(temperature=0.0, model=llm_model)
