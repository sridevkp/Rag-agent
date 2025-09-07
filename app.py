import streamlit as st
from pathlib import Path

from src.chat import get_llm
from src.ingest import add_file, create_index_from_file

st.title("RAG assistant")


# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "index" not in st.session_state:
    st.session_state.index = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()


# === File Upload Section ===
st.subheader("Resources")

col1, col2 = st.columns([2, 5])

with col1:
    uploaded = st.file_uploader(
        "Upload your docs and other resources"
    )
    if uploaded:
        file = uploaded
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"🔎 Indexing {file.name} and generating embeddings..."):
                if st.session_state.index is None:
                    st.session_state.index = create_index_from_file(file)
                else:
                    add_file(st.session_state.index, file)

            st.session_state.uploaded_files.append(file)
            st.session_state.processed_files.add(file.name) 

with col2:
    if st.session_state.uploaded_files:
        st.markdown("#### 📂 Your Resources")

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

if st.session_state.index is not None:
    llm = get_llm(st.session_state.index)

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input("How can I help you today?")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = llm(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
else:
    st.info("⬆️ Upload PDF/TXT files to create an index and start chatting.")

