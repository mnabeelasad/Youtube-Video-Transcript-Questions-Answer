import streamlit as st
from app import process_transcript_and_query

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI with chat-like interface
st.title("YouTube Transcript Q&A")

# Custom CSS for chat-like styling
st.markdown("""
    <style>
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f3e5f5;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 10px 5px 50%;
        max-width: 45%;
        word-wrap: break-word;
    }
    .bot-message {
        background-color: #e6e6e6;
        color: black;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 10px 5px 5px;
        max-width: 45%;
        word-wrap: break-word;
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #007bff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Chat message display area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input form for video ID and question
with st.form(key="chat_form"):
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    video_id = st.text_input("YouTube Video ID", value="J2VnJOw5Cd0", key="video_id")
    query = st.text_input("Ask a question about the video", value="", key="query")
    submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Process form submission
if submit_button and video_id and query:
    # Add user message to chat history
    user_message = f"Video ID: {video_id}\nQuestion: {query}"
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.spinner("Processing transcript and generating answer..."):
        try:
            # Call backend function to process transcript and query
            response = process_transcript_and_query(video_id, query)
            # Add bot response to chat history
            st.session_state.messages.append({"role": "bot", "content": response})
            # Rerun to update the chat display
            st.rerun()
        except Exception as e:
            st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})
            st.rerun()