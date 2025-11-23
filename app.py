import streamlit as st
import os
import sys

# --- DER VORSCHLAGHAMMER (Installation erzwingen) ---
try:
    import langchain
    import faiss
except ImportError:
    import subprocess
    # Wir zwingen den Server, das jetzt zu installieren
    subprocess.run([sys.executable, "-m", "pip", "install", "openai", "langchain", "langchain-community", "langchain-openai", "faiss-cpu", "pypdf", "tiktoken"])

# --- JETZT GEHT ES NORMAL WEITER ---
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# --- 1. CONFIG & DESIGN ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #FFD700 !important; }
    div.stButton > button:first-child { background-color: #FFD700; color: black; border: none; font-weight: bold; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border: 1px solid #444; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("# VANTORQ")
    st.markdown("### Industrial Intelligence")
    st.markdown("---")
    
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    if not api_key:
        st.warning("⚠️ Bitte API Key eingeben.")
        st.stop()
        
    os.environ["OPENAI_API_KEY"] = api_key
    
    uploaded_file = st.file_uploader("PDF hier hochladen", type="pdf")
    st.success("System: **ONLINE**")

# --- 3. MAIN APP ---
st.title("⚡ VANTORQ Diagnose-Center")

if uploaded_file is not None:
    with st.spinner('⚙️ System wird eingerichtet & Datei analysiert... (Das kann beim ersten Mal 1 Min dauern)'):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            loader = PyPDFLoader(tmp_path)
            pages = loader.load_and_split()
            
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(pages, embeddings)
            
            llm = ChatOpenAI(model_name="gpt-4", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            st.success(f"✅ Analyse fertig! {len(pages)} Seiten im Index.")
            
            query = st.text_input("🔧 Fehler beschreiben:")
            if query:
                response = qa_chain.run(query)
                st.info(response)

        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("👈 Bitte PDF hochladen.")
