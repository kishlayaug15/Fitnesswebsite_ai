import streamlit as st
from langchain.llms import Ollama
import ollama_handler

ollama_response = ollama_handler.initialize_ollama()

def display_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
