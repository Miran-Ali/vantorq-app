import streamlit as st
import time
import random
import datetime

# -----------------------------------------------------------------------------
# 1. KONFIGURATION & DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VANTORQ AI | Enterprise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Das "ChatGPT / Enterprise Dark Mode" CSS
st.markdown("""
<style>
    /* --- FARBPALETTE --- */
    :root {
        --bg-color: #0E1117;
        --sidebar-bg: #000000;
        --text-color: #E0E0E0;
        --accent-color: #FFD700; /* VANTORQ Gold */
        --user-msg-bg: #2B2D31;
        --ai-msg-bg: #1A1C24;
    }

    /* Grundlayout */
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
    section[data-testid="stSidebar"] { background-color: var(--sidebar-bg); border-right: 1px solid #222; }

    /* --- CHAT NACHRICHTEN --- */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 100px;
    }
    
    .message-box {
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        line-height: 1.6;
        font-size: 15px;
        animation: fadeIn 0.4s ease;
    }
    
    .user-msg {
        background-color: var(--user-msg-bg);
        border-left: 3px solid #555;
    }
    
    .ai-msg {
        background-color: var(--ai-msg-bg);
        border-left: 3px solid var(--accent-color);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* --- QUELLEN ANZEIGE (RAG Feature) --- */
    .source-tag {
        font-size: 11px;
        background: #333;
        color: #bbb;
        padding: 4px 8px;
        border-radius: 4px;
        margin-top: 8px;
        display: inline-block;
        border: 1px solid #444;
    }

    /* --- INPUT FELD --- */
    .stTextInput input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 24px !important;
        padding: 12px 20px !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* Header entfernen */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE (Das Gedächtnis der App)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "role" not in st.session_state:
    st.session_state.role = "Techniker" # Standard-Ansicht
if "processing" not in st.session_state:
    st.session_state.processing = False

# -----------------------------------------------------------------------------
# 3. SIDEBAR (Navigation & Status)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ VANTORQ")
    st.caption("Industrial Intelligence Engine v2.4")
    
    st.markdown("---")
    
    # KUNDEN-SIMULATION
    st.markdown("### 🏢 Mandant")
    st.info("**Deutsche Maschinenbau GmbH**\n\nStandort: Hamburg Werk 2")
    
    st.markdown("### 🧠 Wissens-Datenbank")
    col1, col2 = st.columns([1,4])
    with col1: st.write("✅")
    with col2: st.caption("2.4 TB Historische Daten")
    
    col1, col2 = st.columns([1,4])
    with col1: st.write("✅")
    with col2: st.caption("12.400 PDF Handbücher")
    
    col1, col2 = st.columns([1,4])
    with col1: st.write("✅")
    with col2: st.caption("ERP-Live-Verbindung")
    
    st.markdown("---")
    
    # ROLLEN-WECHSEL (Geheim für dich für die Demo)
    st.markdown("### 🔧 Systemsteuerung")
    mode_selection = st.radio("Ansicht wählen:", ["Techniker (App)", "Admin (Data Ingest)"])
    st.session_state.role = mode_selection
    
    if st.button("🗑️ Chat leeren", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# 4. HAUPTBEREICH - LOGIK
# -----------------------------------------------------------------------------

# --- ANSICHT A: ADMIN / DATA INGEST (Zum Angeben beim Kunden) ---
if st.session_state.role == "Admin (Data Ingest)":
    st.title("📂 Data Ingestion Hub")
    st.markdown("Hier werden die physischen und digitalen Daten des Unternehmens in die KI eingespeist.")
    
    st.warning("⚠️ Zugriff nur für IT-Administratoren")
    
    c1, c2 = st.columns(2)
    with c1:
        st.file_uploader("Handbücher / PDFs hochladen", accept_multiple_files=True)
    with c2:
        st.text_area("Handschriftliche Notizen (OCR Text)", height=150, placeholder="Paste OCR text here...")
    
    st.markdown("### Vektor-Datenbank Status")
    st.progress(100, text="Indexierung abgeschlossen. System bereit für Abfragen.")
    
    st.markdown("---")
    st.write("Verbundene Systeme:")
    st.code("SAP S/4HANA [Connected]\nOracle Database [Connected]\nSharePoint Legacy [Connected]")

# --- ANSICHT B: TECHNIKER / CHAT (Das Produkt) ---
else:
    # Header Bereich
    c1, c2 = st.columns([6, 1])
    with c1:
        # Modell Auswahl (Fake aber cool)
        st.markdown("**Modell:** `VANTORQ Industrial Pro (Fine-Tuned)`")
    with c2:
        st.write("🟢 Online")

    st.markdown("<br>", unsafe_allow_html=True)

    # WILLKOMMENS-SCREEN (Wenn Chat leer)
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 50px;">
            <h1>Wie kann ich helfen?</h1>
            <p>Ich habe Zugriff auf alle Wartungsprotokolle seit 1995.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Druckabfall Hydraulik", use_container_width=True):
                st.session_state.input_buffer = "Druckabfall Hydraulik Pumpe B"
        with col2:
            if st.button("Fehlercode E-404", use_container_width=True):
                st.session_state.input_buffer = "Was bedeutet Fehlercode E-404?"
        with col3:
            if st.button("Wartungsplan Fräse", use_container_width=True):
                st.session_state.input_buffer = "Zeige Wartungsplan für CNC Fräse 2"

    # CHAT HISTORY ANZEIGEN
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="message-box user-msg">👤 <b>Techniker:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            # KI Nachricht mit HTML Parsing für Fettschrift etc.
            st.markdown(f"""
            <div class="message-box ai-msg">
                🤖 <b>VANTORQ AI:</b><br>{msg["content"]}
                <br>
                <div class="source-tag">📚 {msg["source"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # INPUT FELD (unten verankert)
    user_input = st.chat_input("Beschreibe das Problem, mache ein Foto oder nenne einen Code...")

    # --- KI LOGIK (SIMULATION) ---
    if user_input:
        # 1. User Nachricht sofort anzeigen
        st.session_state.messages.append({"role": "user", "content": user_input, "source": ""})
        st.rerun()

    # Wenn eine neue User-Nachricht da ist, aber noch keine Antwort
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        
        with st.spinner("Analysiere 2.4 TB Firmendaten..."):
            time.sleep(1.5) # Denkpause für Realismus
            
            # --- INTELLIGENTE SIMULATION ---
            # Hier simulieren wir, dass er "echte" Dokumente findet
            
            txt = user_input.lower()
            response_text = ""
            source_text = ""
            
            if "hydraulik" in txt or "druck" in txt:
                response_text = """
                **Diagnose: Kritischer Druckabfall im Hauptkreis.**
                
                Basierend auf den Log-Dateien der letzten 48h und dem Handbuch "Serie-X":
                Das Problem liegt höchstwahrscheinlich am **Überdruckventil (Teil #8892)** oder einer Leckage an **Schlauch B4**.
                
                **Handlungsempfehlung:**
                1. Not-Aus betätigen.
                2. Ventil auf Korrosion prüfen (siehe Bild 4.2 im Handbuch).
                3. Falls undicht: Ersatzteil #8892 aus Lagerreihe 4 holen.
                """
                source_text = "Quelle: Wartungshandbuch Kap. 4, S. 12 & Logfile_2024.txt"
                
            elif "fehler" in txt or "code" in txt:
                response_text = """
                **Fehlercode Identifiziert.**
                
                Dieser Code deutet auf eine **Unterspannung im Steuermodul** hin. 
                Dies trat historisch bereits 14-mal auf, meistens montags nach dem Kaltstart.
                
                **Lösung:**
                Setzen Sie das Modul C zurück (Reset-Knopf 5 Sekunden halten). Prüfen Sie anschließend die Sicherung F12.
                """
                source_text = "Quelle: Fehlerdatenbank Export 2023 (CSV)"
                
            elif "wartung" in txt:
                response_text = """
                **Wartungsplan Status: Überfällig.**
                
                Die letzte Wartung für dieses Gerät war am 12.05.2023.
                Gemäß Vorschrift (ISO 9001) müssen folgende Teile getauscht werden:
                
                * Ölfilter (Typ X)
                * Keilriemen
                * Dichtungsringe Satz 4
                """
                source_text = "Quelle: SAP Wartungsplaner & ISO Dokumentation"
                
            else:
                response_text = """
                Ich habe in den Dokumenten nach diesem Begriff gesucht.
                
                Es gibt **4 relevante Einträge** in den Handschriftlichen Notizen von Hr. Müller (2019).
                Es scheint sich um ein Problem mit der **Zufuhreinheit** zu handeln. Bitte prüfen Sie, ob die Lichtschranke sauber ist.
                """
                source_text = "Quelle: Notizen_Werkstatt_Scan_04.pdf"

            # Nachricht speichern
            st.session_state.messages.append({"role": "ai", "content": response_text, "source": source_text})
            st.rerun()

    # --- FAKE TOOLS (Nur für Optik) ---
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1,1,1,10])
    with col1: st.button("📷", help="Fotoanalyse starten (Demo)")
    with col2: st.button("🎤", help="Sprachnotiz (Demo)")
    with col3: st.button("📞", help="Support anrufen")
