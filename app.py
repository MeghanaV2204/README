import os

import streamlit as st

from agent import generate_response


st.set_page_config(page_title="Groq Assistant", page_icon="💬", layout="centered")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background: #f7f8f5; }
    [data-testid="stSidebar"] { background: #edf1eb; }
    [data-testid="stChatMessage"] { border: 1px solid #e0e5df; border-radius: 8px; }
    .block-container { max-width: 820px; padding-top: 2.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Groq Assistant")
st.caption("Chat powered by openai/gpt-oss-20b")

with st.sidebar:
    st.subheader("Connection")
    api_key = st.text_input(
        "Groq API key",
        value=os.environ.get("GROQ_API_KEY", ""),
        type="password",
        help="Your key is used for this session only. You can also set GROQ_API_KEY in your environment.",
    )
    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if not api_key:
    st.info("Add your Groq API key in the sidebar to start chatting.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question", disabled=not api_key)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = generate_response(st.session_state.messages, api_key)
            except Exception as error:
                st.error(f"Request failed: {error}")
            else:
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})