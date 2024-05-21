from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import create_retrieval_chain
import streamlit as st

import openai
import os

load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
# openai.api_key = os.environ['OPENAI_API_KEY']
with st.form("getopenAIkey"):
    openai.api_key= st.text_input('OPENAI_API_KEY')
    use_key= st.form_submit_button("🚀 Execute")
    # if use_key:
    #     openai.api_key = key


model = ChatOpenAI(temperature=0.0)
link = st.text_input("Enter page link you want to search within")
loader = WebBaseLoader(link)
docs = loader.load()

embeddings = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context:<context>{context}</context> Question: {
    input}"""
)
document_chain = create_stuff_documents_chain(model, prompt)

# query_input = st.text_area()

document_chain.invoke({
    "input": "what is LCEL?",
    "context": docs
})

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "what is LCEL?"})
print(response["answer"])
st.write(response["answer"])
