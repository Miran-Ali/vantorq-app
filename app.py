import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# --- 1. DESIGN & CONFIG ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

# Custom CSS für den Industrial Dark Look (Schwarz/Gold)
st.markdown("""
<style>
    /* Hintergrund & Text */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Überschriften Gold */
    h1, h2, h3 { color: #FFD700 !important; }
    
    /* Buttons Gold */
    div.stButton > button:first-child {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 4px;
    }
    div.stButton > button:first-child:hover {
        background-color: #E6C200;
        color: black;
    }
    
    /* Inputs Dunkel */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border: 1px solid #444;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (Eingaben) ---
with st.sidebar:
    st.markdown("# VANTORQ")
    st.markdown("### Industrial Intelligence")
    st.markdown("---")
    
    # API Key Input (Sicherheits-Check)
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    if not api_key:
        st.warning("⚠️ Bitte API Key eingeben.")
        st.stop()
        
    os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    st.write("📂 **Dokumente (Wissensbasis)**")
    uploaded_file = st.file_uploader("PDF hier hochladen", type="pdf")
    
    st.markdown("---")
    st.info("System Status: **ONLINE**")

# --- 3. HAUPTBEREICH (Logic) ---

st.title("⚡ VANTORQ Diagnose-Center")
st.markdown("KI-gestützte Analyse für Instandhaltung & Support.")

if uploaded_file is not None:
    # Spinner zeigt an, dass er arbeitet
    with st.spinner('⚙️ VANTORQ analysiert Dokumente und baut Index auf...'):
        
        # Temporäre Datei speichern (Trick für Streamlit)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # A. PDF lesen
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load_and_split()

            # B. Gehirn bauen (Embeddings & Vektor-Store)
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(pages, embeddings)

            # C. Die Suchmaschine (Chain)
            llm = ChatOpenAI(model_name="gpt-4", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            st.success(f"✅ Analyse abgeschlossen! {len(pages)} Seiten wurden indexiert.")
            st.markdown("---")

            # D. Chat Interface
            query = st.text_input("🔧 Beschreiben Sie den Fehler oder das Bauteil:")
            
            if query:
                with st.spinner('🔍 Suche Lösung im Archiv...'):
                    response = qa_chain.run(query)
                    
                    st.markdown("### 💡 Lösungsvorschlag:")
                    st.success(response)
                    
                    with st.expander("Technische Details anzeigen"):
                        st.write("Modell: GPT-4 Industrial")
                        st.write(f"Kontext-Basis: {uploaded_file.name}")

        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

else:
    # Leerer Zustand (Startbildschirm)
    st.info("👈 Bitte laden Sie zuerst ein Handbuch oder Wartungsprotokoll in der Sidebar hoch.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🛡️ Secure")
        st.caption("Lokale Verarbeitung im RAM")
    with col2:
        st.markdown("### ⚡ Fast")
        st.caption("Echtzeit-Retrieval")
    with col3:
        st.markdown("### ⚓ Maritime")
        st.caption("Optimiert für Hafentechnik")
