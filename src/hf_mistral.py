from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key=api_key
)

messages = [
    {"role": "system", "content": "You are a personal therapist. Your responses are very concise and conversational."},
]

with st.sidebar:
    chatbot_name = st.text_input("Chatbot Name", value="MARCUS")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "conversation" not in st.session_state:
    st.session_state.conversation = ''''''

st.title(chatbot_name)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": prompt})
    st.session_state.conversation += f"YOU: {prompt}\n"
    st.session_state.conversation += "\n"
    st.chat_message("user").write(prompt)

    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3", 
        messages=messages, 
        max_tokens=500
    )
    msg = completion.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    messages.append({"role": "assistant", "content": msg})
    st.session_state.conversation += f"{chatbot_name}: {msg}\n"
    st.session_state.conversation += "\n"
    st.chat_message("assistant").write(msg)

with st.sidebar:
    st.download_button(
        label="Export Conversation",
        data=st.session_state.conversation,
        file_name="conversation.txt",
        mime="text/plain"
    )