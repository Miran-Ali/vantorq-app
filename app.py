import streamlit as st
import os
import tempfile

# --- CONFIG ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

# --- MODERNE IMPORTS (angepasst für neueste Versionen) ---
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
except ImportError:
    # Falls der Server noch lädt, zeigen wir das an statt abzustürzen
    st.warning("System lädt Module... Bitte Seite neu laden (F5) in 30 Sekunden.")
    st.stop()

# --- DESIGN ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #FFD700 !important; }
    div.stButton > button:first-child { background-color: #FFD700; color: black; border: none; font-weight: bold; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border: 1px solid #444; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ VANTORQ")
    st.caption("Industrial Intelligence")
    
    api_key = st.text_input("OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("Bitte Key eingeben.")
        st.stop()
        
    os.environ["OPENAI_API_KEY"] = api_key
    
    uploaded_file = st.file_uploader("PDF hochladen", type="pdf")

# --- MAIN ---
st.title("Diagnose-Center")

if uploaded_file:
    with st.spinner("Analysiere..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            pages = loader.load_and_split()
            
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(pages, embeddings)
            
            llm = ChatOpenAI(model_name="gpt-4", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            st.success(f"Bereit! {len(pages)} Seiten indexiert.")
            
            query = st.text_input("Frage:")
            if query:
                res = qa_chain.run(query)
                st.info(res)
                
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte PDF in der Sidebar hochladen.")
