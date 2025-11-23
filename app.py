import streamlit as st
import os
import subprocess
import sys
import tempfile

# --- NOTFALL-FIX (DER HAMMER) ---
# Dieser Block prüft, ob die KI-Module da sind. Wenn nicht, installiert er sie mit Gewalt.
try:
    import langchain
    import langchain_community
    import langchain_openai
    import faiss
    import pypdf
except ImportError:
    st.warning("⚙️ System-Update: Installiere KI-Module... Bitte warten (ca. 45 Sekunden)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain", "langchain-community", "langchain-openai", "openai", "faiss-cpu", "pypdf", "tiktoken"])
    st.experimental_rerun()

# --- AB HIER STARTET DIE EIGENTLICHE APP ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# --- 1. DESIGN & CONFIG ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #FFD700 !important; }
    div.stButton > button:first-child { background-color: #FFD700; color: black; border: none; font-weight: bold; }
    div.stButton > button:first-child:hover { background-color: #E6C200; color: black; }
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
    
    st.markdown("---")
    uploaded_file = st.file_uploader("PDF hier hochladen", type="pdf")
    st.markdown("---")
    st.info("System Status: **ONLINE**")

# --- 3. HAUPTBEREICH ---
st.title("⚡ VANTORQ Diagnose-Center")
st.markdown("KI-gestützte Analyse für Instandhaltung & Support.")

if uploaded_file is not None:
    with st.spinner('⚙️ VANTORQ analysiert Dokumente...'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load_and_split()
            
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(pages, embeddings)
            
            llm = ChatOpenAI(model_name="gpt-4", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            st.success(f"✅ Analyse abgeschlossen! {len(pages)} Seiten indexiert.")
            st.markdown("---")

            query = st.text_input("🔧 Beschreiben Sie den Fehler oder das Bauteil:")
            
            if query:
                with st.spinner('🔍 Suche Lösung im Archiv...'):
                    response = qa_chain.run(query)
                    st.markdown("### 💡 Lösungsvorschlag:")
                    st.success(response)

        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("👈 Bitte laden Sie zuerst ein Handbuch in der Sidebar hoch.")
