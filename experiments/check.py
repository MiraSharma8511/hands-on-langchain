import os
import streamlit as st
import openai

from dotenv import load_dotenv
from langchain_core.language_models import LLM

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# import streamlit as st
from langchain.llms import OpenAI  # Replace with your preferred LLM
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from streamlit_chat import message

# import os

# Set your OpenAI API key (if using OpenAI)
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Create chat history memory
chat_history_memory = ConversationBufferMemory(max_turns=20)

llm = OpenAI(temperature=0.7)
# Define a function to handle chatbot interactions
def chat_with_llm(user_input):
    prompt = PromptTemplate(
        input_variables=["user_input", "chat_history"],
        output_variables=["response"],
        template="Chat with LLM:\n{chat_history}\nUser: {user_input}\nLLM: {response}",
    )

    memory = chat_history_memory
    memory.chat_memory.add_message(user_input)
    response = llm(prompt, memory=memory)

    return response["response"]


# Set up Streamlit layout and chat components
st.set_page_config(page_title="LLM Chat with History", layout="wide")

chat_messages = st.empty()
user_input = st.text_input("Enter your message:", key="user_input")

if user_input:
    response = chat_with_llm(user_input)
    message(response, is_user=False, key="response")
    chat_messages.empty()  # Clear previous messages
    for message in chat_history_memory.get_messages():
        message(message.payload, is_user=message.actor == "Human")

# print(api_key)

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = [
#         {"role": "system", "content": "You are a helpful assistant."}
#     ]
#
#
# def generate_response(prompt):
#     st.session_state['messages'].append({"role": "user", "content": prompt})
#     openai_model = "gpt-3.5-turbo"
#     completion = openai.ChatCompletion.create(
#         model=openai_model,
#         messages=st.session_state['messages']
#     )
#     response = completion.choices[0].message.content
#     st.session_state['messages'].append({"role": "assistant", "content": response})
#
#
# from streamlit_chat import message
#
# if st.session_state['generated']:
#     with response_container:
#         for i in range(len(st.session_state['generated'])):
#             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["generated"][i], key=str(i))

#
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"
#
# st.title("Miraalfasa")
# openai.api_key = st.secrets[api_key]
#
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         # Simulate stream of response with milliseconds delay
#         for response in openai.ChatCompletion.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             #will provide lively writing
#             stream=True,
#         ):
#             # get content in response
#             full_response += response.choices[0].delta.get("content", "")
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#
#
# st.session_state.messages.append({"role": "assistant", "content": full_response})
#
# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Display assitant message in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         # Simulate stream of response with milliseconds delay
#         for response in openai.ChatCompletion.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             #will provide lively writing
#             stream=True,
#         ):
#             #get content in response
#             full_response += response.choices[0].delta.get("content", "")
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
