from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import create_retrieval_chain

import streamlit as st
import openai
import os

load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_key = st.text_input('OPENAI_API_KEY')

st.set_page_config(
    page_title="LangChain RAG",
    page_icon="🤖"
)

model = ChatOpenAI(temperature=0.0)

# context = st.text_area("Enter context..")

st.subheader("Langchain RAG (Retrieval-Augmented Generation)")
with st.form("langchain_link"):
    link = st.text_input("Enter page link you want to search within")
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        loader = WebBaseLoader("https://python.langchain.com/docs/expression_language/get_started/")
        docs = loader.load()

        embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(documents, embeddings)

        # prompt = ChatPromptTemplate.from_template("""Answer the following question
        # Question: {input}""")

        prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
        <context>
        {context}
        </context>

        Question: {input}""")
        document_chain = create_stuff_documents_chain(model, prompt)
# with st.form("langchain_rag"):
        user_input = st.text_area("Enter your question here")
        execute = st.form_submit_button("🚀 Execute RAG")
        if execute:
            document_chain.invoke({
                "input": user_input,
                # "context": docs
                "context": [Document(page_content=docs)]
            })

            retriever = vector.as_retriever()
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            response = retrieval_chain.invoke({"input": user_input})
            # st.divider()
            st.write(response["answer"])

# prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
# <context>
# {context}
# </context>
#
# Question: {input}""")
