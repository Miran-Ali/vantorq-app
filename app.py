import streamlit as st
import os
from pypdf import PdfReader
from openai import OpenAI

# --- 1. CONFIG & DESIGN ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #FFD700 !important; }
    div.stButton > button:first-child { background-color: #FFD700; color: black; border: none; font-weight: bold; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border: 1px solid #444; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
    /* Spinner Farbe */
    .stSpinner > div { border-top-color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("⚡ VANTORQ")
    st.caption("Industrial Intelligence (Direct-Mode)")
    
    api_key = st.text_input("OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("Bitte Key eingeben.")
        st.stop()
        
    # Client initialisieren
    client = OpenAI(api_key=api_key)
    
    uploaded_file = st.file_uploader("PDF hochladen", type="pdf")
    st.success("System Status: **ONLINE**")

# --- 3. MAIN APP ---
st.title("Diagnose-Center")

# Funktion: PDF Text extrahieren
def get_pdf_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

if uploaded_file is not None:
    # PDF verarbeiten
    with st.spinner("Lese Dokument..."):
        try:
            # Text aus PDF holen
            pdf_text = get_pdf_text(uploaded_file)
            
            # Wir kürzen den Text für die Demo, falls er zu lang ist (Token Limit sparen)
            # Für Handbücher reicht das meistens
            preview_text = pdf_text[:15000] 

            st.success(f"✅ Dokument geladen! ({len(pdf_text)} Zeichen erkannt)")
            st.markdown("---")

            # Chat Interface
            query = st.text_input("🔧 Fehler oder Frage beschreiben:")
            
            if query:
                with st.spinner('Analysiere mit GPT-4...'):
                    # Direkte Anfrage an OpenAI (Ohne Langchain)
                    prompt = f"""
                    Du bist VANTORQ, eine industrielle KI für Instandhaltung.
                    Nutze NUR den folgenden Kontext aus dem Handbuch, um die Frage zu beantworten.
                    Wenn die Antwort nicht im Text steht, sag das.
                    
                    KONTEXT HANDBUCH:
                    {preview_text}
                    
                    FRAGE DES TECHNIKERS:
                    {query}
                    
                    ANTWORT (Präzise und technisch):
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Du bist ein technischer Assistent."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    answer = response.choices[0].message.content
                    st.markdown("### 💡 Lösung:")
                    st.info(answer)

        except Exception as e:
            st.error(f"Fehler beim Lesen: {e}")
else:
    st.info("👈 Bitte laden Sie zuerst ein Handbuch in der Sidebar hoch.")
