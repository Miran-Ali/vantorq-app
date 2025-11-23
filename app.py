import streamlit as st
import os
import time

# --- CONFIG & PAGE SETUP ---
st.set_page_config(page_title="VANTORQ", page_icon="⚡", layout="wide")

# --- SESSION STATE (Das Kurzzeitgedächtnis) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    # Wir simulieren hier vergangene Chats für das Design
    st.session_state.chat_history = ["Fehlercode E-404", "Wartung Pumpe B", "Hydraulikplan Check"]
if "user_role" not in st.session_state:
    st.session_state.user_role = "Techniker" # Standard ist der Endnutzer

# --- DESIGN SYSTEM (Gemini Style CSS) ---
st.markdown("""
<style>
    /* Hauptfarbe Dunkel */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Sidebar Dunkel */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #222; }
    
    /* Chat Nachrichten Styling */
    .stChatMessage { background-color: transparent; border: none; }
    .stChatMessageUser { background-color: #1e1e1e; }
    
    /* Input Feld unten fixiert wie bei ChatGPT */
    .stTextInput input {
        background-color: #1e1e1e; color: white; border: 1px solid #333; border-radius: 20px; padding: 10px;
    }
    
    /* Buttons Gold/Gelb */
    div.stButton > button:first-child {
        background-color: #FFD700; color: black; border: none; border-radius: 8px; font-weight: bold;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Navigation & History) ---
with st.sidebar:
    st.title("⚡ VANTORQ")
    
    # Rollen-Wechsler (Nur für Demo-Zwecke sichtbar, später versteckt)
    st.caption("--- DEMO STEUERUNG ---")
    st.session_state.user_role = st.radio("Ansicht wählen:", ["Techniker", "Admin (Upload)"])
    
    if st.session_state.user_role == "Admin (Upload)":
        st.markdown("---")
        st.write("📂 **Wissensdatenbank füttern**")
        st.caption("Hier lädt die IT-Abteilung die Handbücher hoch.")
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key: os.environ["OPENAI_API_KEY"] = api_key
        uploaded_file = st.file_uploader("PDFs / Technische Zeichnungen", type="pdf", accept_multiple_files=True)
        if uploaded_file:
            st.success(f"{len(uploaded_file)} Dokumente indexiert und im Vektor-Speicher abgelegt.")
    
    st.markdown("---")
    
    # Neuer Chat Button
    if st.button("+ Neuer Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("### Verlauf")
    for chat in st.session_state.chat_history:
        st.button(f"💬 {chat}", key=chat, use_container_width=True) # Fake Buttons für History

    st.markdown("---")
    st.caption(f"User: Miran Ali\nStatus: Connected")

# --- HAUPTBEREICH ---

# 1. Top Bar (Modell Auswahl)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    # Modell-Wahl wie bei Gemini/ChatGPT
    mode = st.pills("Modus:", ["⚡ Flash (Schnell)", "🧠 Reasoning (Denker)", "🔍 Search"], selection_mode="single", default="⚡ Flash (Schnell)")

st.divider()

# 2. Chat Verlauf anzeigen
if not st.session_state.messages:
    # Willkommens-Screen wenn leer
    st.markdown("<h1 style='text-align: center; color: #444;'>Wie kann ich helfen?</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("🔧 **Fehlerdiagnose**\n\n'Kran X-500 hebt Last nicht an'")
    with c2:
        st.info("📖 **Wartung**\n\n'Wann muss der Ölfilter bei Modell B getauscht werden?'")

# Nachrichten rendern
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Input Area & Logic
prompt = st.chat_input("Frage an die Maschinendatenbank...")

if prompt:
    # User Nachricht speichern & anzeigen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # KI Antwort simulieren (Hier würde später die echte RAG-Logik greifen)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulation des "Denkens"
        if "Reasoning" in str(mode):
            with st.status("Analysiere Schaltpläne und Historie...", expanded=True):
                time.sleep(1)
                st.write("Prüfe Fehlerdatenbank...")
                time.sleep(1)
                st.write("Vergleiche mit Handbuch Seite 42-50...")
        
        # Die Antwort generieren (Hier nutzen wir noch Mock-Daten für das Design)
        # Sobald du den API Key eingibst und echte Logik willst, kopieren wir den alten RAG-Teil hier rein.
        full_response = f"Basierend auf den Handbüchern der letzten 20 Jahre deutet '{prompt}' auf folgendes Problem hin:\n\n"
        full_response += "**Mögliche Ursache:** Verschleiß am Dichtungsring B (Teilenummer: 99-X).\n\n"
        full_response += "**Empfohlene Maßnahme:**\n1. Druck ablassen.\n2. Ventil öffnen.\n3. Ring tauschen.\n\n*Quelle: Wartungshandbuch 2018, Seite 12.*"
        
        # Streaming Effekt (Buchstabe für Buchstabe)
        displayed_response = ""
        for chunk in full_response.split():
            displayed_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(displayed_response + "▌")
        
        message_placeholder.markdown(displayed_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 4. Tools Leiste (Fake für Design)
st.markdown("---")
t1, t2, t3, t4 = st.columns([1,1,1,10])
with t1: st.button("🎤", help="Spracheingabe")
with t2: st.button("📷", help="Foto hochladen")
with t3: st.button("📎", help="Datei anhängen")
