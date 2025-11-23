import streamlit as st
import time
import datetime

# -----------------------------------------------------------------------------
# 1. SYSTEM CONFIGURATION & STRICT PALETTE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VANTORQ | Enterprise Engine",
    page_icon="▪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PROFI-CSS: Überschreibt alle Streamlit-Standards für einen "Clean Code" Look
st.markdown("""
<style>
    /* --- STRICT MONOCHROME PALETTE --- */
    :root {
        --bg-core: #09090b;       /* Fast Schwarz (Zinc 950) */
        --bg-card: #18181b;       /* Dunkelgrau (Zinc 900) */
        --bg-hover: #27272a;      /* Hover Grau (Zinc 800) */
        --border: #3f3f46;        /* Rahmen (Zinc 700) */
        --text-primary: #f4f4f5;  /* Fast Weiß */
        --text-secondary: #a1a1aa;/* Muted Grau */
        --accent: #2563EB;        /* Professional Blue (nur für Highlights) */
    }

    /* Reset Streamlit Defaults */
    .stApp { background-color: var(--bg-core); color: var(--text-primary); font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { 
        background-color: #000000; 
        border-right: 1px solid var(--border);
    }
    
    /* Input Felder: Clean & Minimal */
    .stTextInput input, .stTextArea textarea {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important; /* Kantiger, professioneller */
        padding: 12px !important;
    }
    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* Buttons: Einheitlich und professionell */
    div.stButton > button {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: var(--bg-hover);
        border-color: var(--text-secondary);
    }
    div.stButton > button:active {
        background-color: var(--accent);
        color: white;
        border-color: var(--accent);
    }

    /* --- CHAT NACHRICHTEN DESIGN --- */
    .msg-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-bottom: 80px;
    }
    
    .msg-row {
        display: flex;
        width: 100%;
    }
    
    .msg-user {
        justify-content: flex-end;
    }
    
    .msg-ai {
        justify-content: flex-start;
    }
    
    .msg-bubble {
        max-width: 80%;
        padding: 16px 20px;
        border-radius: 4px; /* Industrieller Look */
        font-size: 15px;
        line-height: 1.6;
        position: relative;
    }
    
    .bubble-user {
        background-color: var(--bg-hover); /* Dunkelgrau */
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-left: 2px solid var(--text-secondary);
    }
    
    .bubble-ai {
        background-color: #000; /* Schwarz für maximalen Kontrast */
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-left: 2px solid var(--accent); /* Der einzige Farbklecks */
    }

    .meta-tag {
        font-size: 11px;
        color: var(--accent);
        margin-top: 10px;
        font-family: 'Courier New', monospace; /* Code-Optik für Daten */
        opacity: 0.8;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Hide Bloat */
    header, footer, .stDeployButton { visibility: hidden; }
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# 3. UI LAYOUT
# -----------------------------------------------------------------------------

# --- SIDEBAR (Navigation) ---
with st.sidebar:
    st.markdown("<h3 style='margin-bottom:0; padding-bottom:0;'>▪️ VANTORQ</h3>", unsafe_allow_html=True)
    st.caption("SYSTEM STATUS: ONLINE")
    
    st.markdown("---")
    
    # Minimalistische Status-Anzeige
    st.markdown("**MANDANT**")
    st.code("DE-MB-8291") # Sieht technischer aus als Text
    
    st.markdown("**DATABASE**")
    st.markdown("""
    <div style="display:flex; justify-content:space-between; font-size:13px; color:#666; margin-bottom:4px;">
        <span>PDF Index</span>
        <span style="color:#fff;">12,401</span>
    </div>
    <div style="background:#222; height:4px; width:100%; border-radius:2px;">
        <div style="background:#2563EB; height:4px; width:98%; border-radius:2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Controls (Funktional & Clean)
    mode = st.selectbox("Modus", ["Live Diagnose", "Admin Konsole"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Neuer Prozess"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN AREA ---

# Leerer Zustand (Empty State) - Clean Typography
if not st.session_state.messages:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:60vh; text-align:center;">
        <h1 style="color: #333; font-size: 40px; margin-bottom: 10px;">VANTORQ</h1>
        <p style="color: #666; max-width: 500px;">
            Industrielle KI-Diagnose für Wartung & Betrieb.<br>
            Verbunden mit Archivserver (1995-2024).
        </p>
    </div>
    """, unsafe_allow_html=True)

# Nachrichten rendern
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row msg-user">
            <div class="msg-bubble bubble-user">
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row msg-ai">
            <div class="msg-bubble bubble-ai">
                {msg["content"]}
                <div class="meta-tag">
                    <span>⚡</span> {msg["source"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input Area - Unten fixiert
st.markdown("---")
c1, c2 = st.columns([8, 1])

with c1:
    prompt = st.chat_input("Befehl eingeben oder Fehlercode scannen...")

if prompt:
    # 1. User Input speichern
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# KI Antwort Logik
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        time.sleep(0.8) # Kurze professionelle Verzögerung
        
        # Simulierte Antwort-Logik
        user_text = st.session_state.messages[-1]["content"].lower()
        
        if "admin" in str(mode).lower():
             # Admin View Simulation
            response = "Upload-Protokoll aktiv. Bitte ziehen Sie Dateien in den markierten Bereich."
            src = "System: Ingest-Mode"
        else:
            # Techniker View Simulation
            if "fehler" in user_text or "code" in user_text:
                response = """
                **Fehleridentifikation: Positiv.**<br><br>
                Der Code korreliert mit einem Spannungsabfall im Steuermodul K.
                Dies tritt laut Historie häufig nach langen Stillstandzeiten auf.<br><br>
                **Maßnahme:** Modul K4 resetten und Sicherung F1 prüfen.
                """
                src = "SRC: Handbuch S.42 | Log: 2023-11"
            elif "hydraulik" in user_text:
                response = """
                **Drucksystem Analyse**<br><br>
                Sollwerte weichen um 15% ab. Verdacht auf Leckage im Rücklauf.<br>
                Bitte Dichtungsring 4B visuell prüfen.
                """
                src = "SRC: Schaltplan Hyd-04"
            else:
                response = f"Eintrag '{user_text}' in 4 Dokumenten gefunden. Analysiere Kontext..."
                src = "SRC: Vektor-DB Index"

        st.session_state.messages.append({"role": "ai", "content": response, "source": src})
        st.rerun()
