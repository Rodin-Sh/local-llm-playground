import ollama
from ollama import ChatResponse
import streamlit as st

messages = [
    {"role": "system", "content": "You are a personal therapist. Your responses are very concise and conversational."},
]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "conversation" not in st.session_state:
    st.session_state.conversation = ''''''

with st.sidebar:
    chatbot_name = st.text_input("Chatbot Name", value="MARCUS")

    st.download_button(
        label="Export Conversation",
        data=st.session_state.conversation,
        file_name="conversation.txt",
        mime="text/plain"
    )
    

st.title(chatbot_name)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": prompt})
    st.session_state.conversation += f"YOU: {prompt}\n"
    st.chat_message("user").write(prompt)

    response = ollama.chat(model='llama3.2', messages=messages)
    msg = response.message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    messages.append({"role": "assistant", "content": msg})
    st.session_state.conversation += f"{chatbot_name}: {msg}\n"
    st.chat_message("assistant").write(msg)