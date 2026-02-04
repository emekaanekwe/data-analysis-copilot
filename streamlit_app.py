import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ROW_HIGHT = 100
TEXTBOX_HIGHT = 100

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

'''
Function to generate a sample dataframe
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
# Simple chatbot response generation
def generate_chatbot_response(openai_client, session_state, user_input):
    """Generate a simple chatbot response using OpenAI API"""

    # Generate streaming response
    stream = openai_client.chat.completions.create(
        model=session_state["openai_model"],
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant for data analysis. You can answer questions, provide guidance, and have conversations with users."
            }
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in session_state.messages
        ],
        stream=True
    )

    # Stream the response
    response = st.write_stream(stream)
    return response



'''
# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = get_dataframe()


################################################
##### Below are all the code to do with UI #####
################################################

# Set page config
#st.set_page_config(page_title="Simple Data Analysis Chatbot", layout="wide")

# Title
#st.title("💬 Simple Data Analysis Chatbot")

# Create two columns layout
col1, col2 = st.columns(2)

# Left column: Chatbot
with col1:
    st.subheader("Chat with AI Assistant")

    # Display chat history
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container.chat_message("user"):
            st.markdown(user_input)

        # Generate and display assistant response
        with chat_container.chat_message("assistant"):
            response = generate_chatbot_response(
                openai_client, st.session_state, user_input
            )

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Right column: Data Editor
with col2:
    st.subheader("Your Dataset")

    # Display editable dataframe
    edited_df = st.data_editor(
        st.session_state.df,
        key="editable_table",
        num_rows="dynamic",
        use_container_width=True,
        height=500
    )

    # Update dataframe
    st.session_state.df = edited_df

    # Show basic stats
    if st.checkbox("Show dataset info"):
        st.write(f"**Shape:** {st.session_state.df.shape}")
        st.write(f"**Columns:** {', '.join(st.session_state.df.columns)}")
'''