"""
Simple ChatGPT Bot for Streamlit
A minimal implementation of a chatbot using OpenAI API and Streamlit
"""

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"

# Page configuration
st.set_page_config(
    page_title="Simple ChatGPT Bot",
    page_icon="💬",
    layout="centered"
)
'''
def get_dataframe():
    df = pd.DataFrame(
        {
            "A": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "B": [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
            "C": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
        }
    )
    return df

'''
# Title
st.title("💬 Simple ChatGPT Bot")
st.caption("A simple chatbot powered by OpenAI GPT-4")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to talk about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        # Create streaming response
        stream = openai_client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )

        # Display streaming response
        response = st.write_stream(stream)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with options
with st.sidebar:
    st.header("Settings")

    # Model selection
    model_option = st.selectbox(
        "Choose Model",
        ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        index=0
    )
    st.session_state.openai_model = model_option

    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    # Chat statistics
    st.divider()
    st.subheader("Chat Statistics")
    st.write(f"**Messages:** {len(st.session_state.messages)}")
    st.write(f"**Model:** {st.session_state.openai_model}")

    # Instructions
    st.divider()
    st.subheader("How to Use")
    st.markdown("""
    1. Type your message in the chat input
    2. Press Enter to send
    3. The AI will respond in real-time
    4. Use the sidebar to change settings
    """)
