import streamlit as st
from pathlib import Path
from src.chat import llm
from src.ingest import add_pdf


# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

class File:
    name = "file nam is too large to fill the the the "

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

st.title("Chat Bot Template")

# === File Upload Section ===
st.subheader("Resources")

col1, col2 = st.columns([2, 5])

with col1:
    uploaded = st.file_uploader(
        "Upload your docs and other resources"
    )
    if uploaded:
        f = uploaded# for f in uploaded:
        if f.name not in [uf.name for uf in st.session_state.uploaded_files]:
            add_pdf(f)
            st.session_state.uploaded_files.append(f)

with col2:
    if st.session_state.uploaded_files:
        st.markdown("#### 📂 Uploaded Files")
        size = 4
        file_cols = st.columns(max(4, len(st.session_state.uploaded_files[:size])))

        for i, f in enumerate(st.session_state.uploaded_files[:size]):
            with file_cols[i]:
                ext = Path(f.name).suffix.lower()
                icon = "📄" if ext != ".pdf" else "📕"
                st.markdown(
                    f"""
                    <div style="
                        border:1px solid #ddd;
                        border-radius:10px;
                        padding:15px;
                        text-align:center;
                        height:100%;
                        box-shadow:0px 2px 6px rgba(0,0,0,0.1);
                        display:flex;
                        flex-direction:column;
                        justify-content:center;
                        ">
                        <div style="font-size:40px;">{icon}</div>
                        <div style="margin-top:8px;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;width:100%">
                            {f.name}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# === Chat Section ===
st.subheader("Chat")

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input("How can I help you today?")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = llm(prompt)
    st.chat_message('agent').markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
