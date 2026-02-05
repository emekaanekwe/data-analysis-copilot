import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
print("API Key exists:", bool(os.getenv("API_KEY")))  # Note: "API_KEY" not "API KEY"
print("API Key length:", len(os.getenv("API_KEY", "")))

# If using .env file, make sure it's loaded
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
#openai_client = OpenAI(api_key="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")
open_router_client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"

if "df" not in st.session_state:
    # Create sample dataframe
    st.session_state.df = pd.DataFrame({
        "A": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "B": [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
        "C": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
    })

# Open Router Setup


# Generate response
def generate_data_analysis_response(user_input):
    

    # Convert dataframe to string for context
    df_info = f"""
    Dataset Info:
    - Shape: {st.session_state.df.shape}
    - Columns: {', '.join(st.session_state.df.columns.tolist())}

    First 5 rows:
    {st.session_state.df.head().to_string()}

    Basic statistics:
    {st.session_state.df.describe().to_string()}
    """

    # Create streaming response with data context
completion = open_router_client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  model="openai/gpt-5.2",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)
'''
    stream = open_router_client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful data analysis assistant. You have access to the user's dataset.

{df_info}

Help users understand their data, answer questions about it, and provide insights.
When users ask about the data, refer to the specific values and statistics shown above.
Keep responses clear and concise."""
            }
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True
    )

    return st.write_stream(stream)
'''

################################################
##### UI Layout #####
################################################

# Page configuration
st.set_page_config(
    page_title="Simple Data Analysis Agent",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Simple Data Analysis Agent")
st.caption("Powered by OpenAI GPT-4")

# Create two columns
col1, col2 = st.columns(2)

# Left column: Chatbot
with col1:
    st.subheader("💬 Chat with AI")

    # Display chat history
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("Ask about your data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response with data context
        with chat_container.chat_message("assistant"):
            response = generate_data_analysis_response(user_input)

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Right column: Data Editor
with col2:
    st.subheader("📋 Your Dataset")

    # Display editable dataframe
    edited_df = st.data_editor(
        st.session_state.df,
        key="editable_table",
        num_rows="dynamic",
        use_container_width=True,
        height=400
    )

    # Update dataframe
    st.session_state.df = edited_df

    # Show dataset info
    st.divider()
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Rows", st.session_state.df.shape[0])
    with col_b:
        st.metric("Columns", st.session_state.df.shape[1])
    with col_c:
        st.metric("Total Cells", st.session_state.df.shape[0] * st.session_state.df.shape[1])

    # Quick stats toggle that shows counts, mean, std, min
    if st.checkbox("Show detailed statistics"):
        st.dataframe(st.session_state.df.describe(), use_container_width=True)

# Sidebar with options
with st.sidebar:
    st.header("⚙️ Settings")

    # Model selection
    model_option = st.selectbox(
        "AI Model",
        ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        index=0
    )
    st.session_state.openai_model = model_option

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Reset data button
    if st.button("🔄 Reset Dataset", use_container_width=True):
        st.session_state.df = pd.DataFrame({
            "A": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "B": [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
            "C": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
        })
        st.rerun()

    st.divider()

    # Upload CSV
    st.subheader("📤 Upload Data")
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success("✅ CSV loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading CSV: {e}")


