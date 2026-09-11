import streamlit as st
from uuid import uuid4

from supervisor_agent import build_supervisor_agent


st.set_page_config(
    page_title="Multi-Agent AI",
    page_icon="🤖"
)

st.title("Multi-Agent AI")
st.write("YouTube Video Analysis & Fact Checking")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("New conversation"):
    st.session_state.session_id = str(uuid4())
    st.session_state.messages = []
    st.rerun()


supervisor = build_supervisor_agent()


query = st.text_input("Enter your YouTube video URL")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.button("Analyze"):

    if query:
        with st.status("Analyzing video...", expanded=True) as status:
            response = supervisor.run(
                query,
                session_id=st.session_state.session_id,
            )
            st.session_state.messages.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": response.content},
            ])
            status.update(label="Analysis complete", state="complete")
        st.rerun()

follow_up = st.chat_input(
    "Ask a follow-up question about this video"
)

if follow_up:
    st.session_state.messages.append({"role": "user", "content": follow_up})
    with st.status("Remembering the video context...", expanded=True) as status:
        response = supervisor.run(
            follow_up,
            session_id=st.session_state.session_id,
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": response.content}
        )
        status.update(label="Answer ready", state="complete")
    st.rerun()