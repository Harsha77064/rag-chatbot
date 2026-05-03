# -*- coding: utf-8 -*-
import streamlit as st
from dotenv import load_dotenv
import os
import tempfile
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="RAG Document Q&A", page_icon="🤖", layout="wide")
st.title("🤖 RAG Document Q&A Chatbot")
st.markdown("Upload a PDF and ask questions about it!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and not st.session_state.pdf_processed:
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
            st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
            st.session_state.pdf_processed = True
            os.unlink(tmp_path)
        st.success("Processed " + str(len(chunks)) + " chunks from " + str(len(documents)) + " pages!")

    if st.session_state.pdf_processed:
        if st.button("Upload New PDF"):
            st.session_state.vectorstore = None
            st.session_state.chat_history = []
            st.session_state.pdf_processed = False
            st.rerun()

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            st.write(message.content)

if prompt := st.chat_input("Ask a question about your document..."):
    if not st.session_state.pdf_processed:
        st.warning("Please upload a PDF first!")
    else:
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
                docs = retriever.invoke(prompt)
                context = "\n\n".join([doc.page_content for doc in docs])

                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

                history_text = ""
                for msg in st.session_state.chat_history[:-1]:
                    if isinstance(msg, HumanMessage):
                        history_text += "Human: " + msg.content + "\n"
                    else:
                        history_text += "Assistant: " + msg.content + "\n"

                full_prompt = "You are a helpful assistant that answers questions based on the provided document context.\n\nContext from document:\n" + context + "\n\nPrevious conversation:\n" + history_text + "\n\nQuestion: " + prompt + "\n\nAnswer based on the context above. If the answer is not in the context, say so clearly."

                response = llm.invoke(full_prompt)
                answer = response.content
                st.write(answer)

                with st.expander("Sources"):
                    for i, doc in enumerate(docs[:3]):
                        page = doc.metadata.get("page", "?")
                        st.markdown("Page " + str(int(page)+1) + ": " + doc.page_content[:200] + "...")

        st.session_state.chat_history.append(AIMessage(content=answer))
