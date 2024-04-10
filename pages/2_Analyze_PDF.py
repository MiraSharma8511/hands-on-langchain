from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
import os
import openai

# def main():
load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
# openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(page_title="Ask your PDF")
st.header("Ask your PDF 💬")
openai.api_key = st.text_input('OPENAI_API_KEY')
openai_api_key = openai.api_key

# upload file
pdf = st.file_uploader("Upload your PDF", type="pdf")

# extract the text
if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    # FAISS.from_texts()

    # show user input
    st.divider()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi, How may I help you today?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_question = st.chat_input("Ask a question about your PDF")
    if user_question:
        docs = knowledge_base.similarity_search(user_question)

        llm = OpenAI()
        chain = load_qa_chain(llm)

        st.session_state.messages.append({"role": "user", "content": user_question})
        st.chat_message("user").write(user_question)
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # with st.chat_message("user"):
        #     st.write(user_question)
        #
        # with st.chat_message("😎"):
        #     response = chain.run(input_documents=docs, question=user_question)
        #     st.write(response)

        with get_openai_callback() as cb:
            print(cb)

    # else:
    #     st.write("Looks like some issue with PDF, Please check PDF")

#
# if __name__ == '__main__':
#     main()


"""
References:
- https://github.com/francescocarlucci/learn-langchain/blob/main/pages/1LLMs.py
- https://learnlangchain.streamlit.app/Chains
"""