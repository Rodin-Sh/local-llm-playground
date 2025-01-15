import os
import yaml
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Loading Python tools
load_dotenv()

# Create a new Python exception for authentication
class AuthenticationError(Exception):
    pass

# All variables
api_key = os.getenv("API_KEY")
PW = os.getenv("PW")
prompt = os.getenv("PROMPT")
messages = [{"role": "system", "content": prompt}]

# HuggingFace client
client = InferenceClient(api_key=api_key)

# Streamlit Sidebar UI customization
with st.sidebar:
    chatbot_name = st.text_input("Chatbot Name", value="MARCUS")
    password = st.text_input("Password", type="password")

# Check if "messages" exist in Streamlit session_state.
# If not, create one.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Same as "messages" but for "conversation"
# This will later be used for exporting a .txt file of the conversation.
if "conversation" not in st.session_state:
    st.session_state.conversation = ''''''

# Streamlit title
st.title(chatbot_name)

# Continuously updating and presenting the new messages with Streamlit chat_message
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# If a new message is entered
if prompt := st.chat_input():

    # Update the session_state with the new message
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": prompt})

    # Add the new message to the .txt file with correct formatting
    st.session_state.conversation += f"YOU: {prompt}\n"
    st.session_state.conversation += "\n"
    st.chat_message("user").write(prompt)

    try:
        # Authentication logic
        if password != PW:
            raise AuthenticationError("Invalid credentials.")

        # Get AI response from HuggingFace
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3", 
            messages=messages, 
            max_tokens=500
        )
        msg = completion.choices[0].message.content
        
        # Update session_state and .txt file with new AI message
        st.session_state.messages.append({"role": "assistant", "content": msg})
        messages.append({"role": "assistant", "content": msg})
        st.session_state.conversation += f"{chatbot_name}: {msg}\n"
        st.session_state.conversation += "\n"
        st.chat_message("assistant").write(msg)

    except AuthenticationError as e:
        # Error message presented if there is authentication error
        st.write(e)

# On the side-bar, you can download a .txt file of the entire conversation
with st.sidebar:
    st.download_button(
        label="Export Conversation",
        data=st.session_state.conversation,
        file_name="conversation.txt",
        mime="text/plain"
    )