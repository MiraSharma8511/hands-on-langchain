from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

import streamlit as st
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(
    page_title="LangChain Parsers",
    page_icon="🤖"
)
# with st.form("getopenAIkey"):
#     key= st.text_input('OPENAI_API_KEY')
#     use_key= st.form_submit_button("🚀 Execute")
#     if use_key:
#         openai.api_key = key

st.header(" Structure Output Parser")
with st.form("basic_chain"):
    customer_review = st.text_area("Enter customer review")
    execute = st.form_submit_button("🚀 Execute")
    if execute:
        with st.spinner('Processing your request...'):

            model = ChatOpenAI(temperature=0.0)

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
            
                customer review: {customer review}
            
                {format_instructions}
                """

            prompt = PromptTemplate(
                template=review_template_2,
                input_variables=["customer review"],
                partial_variables={"format_instructions": format_instructions},
            )

            chain = prompt | model | output_parser

            output = chain.invoke({"customer review": customer_review})

            st.write(output)