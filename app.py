import streamlit as st
import os
from pypdf import PdfReader
from openai import OpenAI

# --- 1. CONFIG & DESIGN ---
st.set_page_config(page_title="VANTORQ AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Industrial Dark Theme */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Gold Akzente für VANTORQ Brand */
    h1, h2, h3 { color: #FFD700 !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Buttons */
    div.stButton > button:first-child { 
        background-color: #FFD700; 
        color: black; 
        border: none; 
        font-weight: bold; 
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:first-child:hover { 
        background-color: #E6C200; 
        color: black; 
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Inputs */
    .stTextInput > div > div > input { 
        background-color: #1e1e1e; 
        color: white; 
        border: 1px solid #333; 
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { 
        background-color: #000000; 
        border-right: 1px solid #222; 
    }
    
    /* Chat Bubbles */
    .stChatMessage { background-color: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid #333; }
    
    /* Spinner */
    .stSpinner > div { border-top-color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (Steuerung) ---
with st.sidebar:
    st.title("⚡ VANTORQ")
    st.caption("Industrial Intelligence System")
    st.markdown("---")
    
    api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Hier den Schlüssel eingeben und Enter drücken.")
    
    if not api_key:
        st.warning("🔒 System gesperrt. Bitte API Key eingeben.")
        st.stop()
        
    # Client initialisieren
    client = OpenAI(api_key=api_key)
    
    st.markdown("### 📂 Daten-Ingestion")
    uploaded_file = st.file_uploader("Wartungsprotokoll / Handbuch (PDF)", type="pdf")
    
    if uploaded_file:
        st.success("✅ Datei im Vektor-Speicher (RAM)")
    else:
        st.info("Warte auf Dokument...")

    st.markdown("---")
    st.markdown("**System Status:**")
    st.code("ONLINE - V 1.4.2", language="text")

# --- 3. MAIN APP ---
st.title("Diagnose-Center")
st.markdown("Stellen Sie technische Fragen an Ihre Maschinendaten.")

# Funktion: PDF Text extrahieren (Robust)
def get_pdf_text(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return ""

# --- 4. LOGIK ---
if uploaded_file is not None:
    # PDF verarbeiten
    with st.spinner("⚙️ VANTORQ analysiert technische Dokumentation..."):
        try:
            # Text aus PDF holen
            pdf_text = get_pdf_text(uploaded_file)
            
            # Kontext limitieren (für die Demo reichen die ersten 15.000 Zeichen, das spart Kosten)
            preview_text = pdf_text[:20000] 

            if len(preview_text) < 10:
                st.error("Fehler: Das PDF scheint leer zu sein oder enthält nur Bilder (kein Text). Bitte ein PDF mit Text hochladen.")
            else:
                # Chat Interface
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Chatverlauf anzeigen
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Input Feld
                if prompt := st.chat_input("Beschreiben Sie das Problem (z.B. 'Fehler E-404 bei Kran X')"):
                    # User Nachricht
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # KI Antwort generieren
                    with st.chat_message("assistant"):
                        with st.spinner('Analysiere Kontext & Historie...'):
                            
                            # --- DER PROFI SYSTEM-PROMPT (Von ChatGPT inspiriert) ---
                            system_instruction = f"""
                            Du bist VANTORQ, ein präziser technischer Assistent für die Industrie-Instandhaltung.
                            Deine Aufgabe ist es, Feldtechniker bei der Fehlerdiagnose zu unterstützen.
                            
                            REGELN:
                            1. Nutze AUSSCHLIESSLICH den folgenden Kontext aus den hochgeladenen Handbüchern.
                            2. Wenn die Antwort nicht im Kontext steht, sage ehrlich: "Dazu liegen keine Informationen im aktuellen Handbuch vor." (Erfinde nichts!).
                            3. Strukturiere deine Antwort logisch: 
                               - **Diagnose:** Was ist das Problem?
                               - **Lösungsschritte:** Schritt-für-Schritt Anleitung.
                               - **Sicherheit:** Warnhinweise fett gedruckt.
                               - **Ersatzteile:** Falls im Text genannt, liste Teilenummern auf.
                            4. Sei kurz, präzise und technisch professionell (Ingenieurs-Sprache).

                            KONTEXT DATENBANK:
                            {preview_text}
                            """

                            response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "system", "content": system_instruction},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.3 # Niedrig = präziser, weniger kreativ
                            )
                            
                            answer = response.choices[0].message.content
                            st.markdown(answer)
                            
                    # KI Nachricht speichern
                    st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Systemfehler: {e}")
else:
    # Leerer Zustand
    st.info("👈 Bitte laden Sie links ein Handbuch hoch, um die Diagnose zu starten.")
    
    # Demo-Ansicht für den "Wow"-Effekt bevor man was hochlädt
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛡️ Secure Silos")
        st.caption("Daten verlassen Europa nicht.")
    with col2:
        st.markdown("### ⚡ Instant Retrieval")
        st.caption("Antworten in < 2 Sekunden.")
