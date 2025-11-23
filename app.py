import streamlit as st
import os
import tempfile

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

# Imports (Ganz normal, ohne Tricks)
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
except ImportError:
    st.error("⚠️ System-Fehler: Die KI-Module wurden nicht geladen. Bitte unten rechts auf 'Manage app' -> 'Reboot app' klicken.")
    st.stop()

# --- 2. CSS DESIGN (Industrial Dark) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #FFD700 !important; }
    div.stButton > button:first-child { background-color: #FFD700; color: black; border: none; font-weight: bold; }
    div.stButton > button:first-child:hover { background-color: #E6C200; color: black; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border: 1px solid #444; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
    .stSpinner > div { border-color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("# VANTORQ")
    st.markdown("### Industrial Intelligence")
    st.markdown("---")
    
    # API Key sicher abfragen
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    if not api_key:
        st.warning("⚠️ Bitte API Key eingeben.")
        st.stop()
        
    os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    uploaded_file = st.file_uploader("PDF hier hochladen", type="pdf")
    st.markdown("---")
    st.success("System Status: **ONLINE**")

# --- 4. HAUPTBEREICH ---
st.title("⚡ VANTORQ Diagnose-Center")
st.markdown("KI-gestützte Analyse für Instandhaltung & Support.")

if uploaded_file is not None:
    with st.spinner('⚙️ VANTORQ analysiert Dokumente (Vektorisierung)...'):
        try:
            # Temporäre Datei speichern
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # A. PDF Laden
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load_and_split()
            
            # B. Gehirn bauen
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(pages, embeddings)
            
            # C. Suche einrichten
            llm = ChatOpenAI(model_name="gpt-4", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            st.success(f"✅ Analyse abgeschlossen! {len(pages)} Seiten im Index.")
            st.markdown("---")

            # D. Chat
            query = st.text_input("🔧 Fehler oder Frage beschreiben:")
            
            if query:
                with st.spinner('🔍 Suche Lösung im Archiv...'):
                    response = qa_chain.run(query)
                    st.markdown("### 💡 Lösung:")
                    st.info(response)

        except Exception as e:
            st.error(f"Ein technischer Fehler ist aufgetreten: {e}")
else:
    st.info("👈 Bitte laden Sie zuerst ein Handbuch in der Sidebar hoch.")
