import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time

# --- 1. CONFIGURAZIONE E STILE ---
st.set_page_config(page_title="Rune Master Ultimate", page_icon="ᛟ", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .rune-card { background-color: #262730; border: 1px solid #4B4B4B; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-bottom: 20px; }
    .rune-symbol { font-size: 80px; color: #FFD700; font-weight: bold; text-shadow: 0 0 10px #FFD700; }
    .rune-symbol-rev { font-size: 80px; color: #A0A0A0; font-weight: bold; transform: rotate(180deg); display: inline-block; }
    .rune-title { font-size: 24px; font-weight: bold; color: #E0E0E0; margin-top: 10px; }
    .tag { background-color: #4B0082; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 5px; }
    .stButton>button { background-color: #4B0082; color: white; border-radius: 5px; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE POTENZIATO (Con Date Astrologiche e TAG) ---
# Le date sono approssimative basate sul calendario runico solare moderno
runes_db = [
    {"name": "Fehu", "symbol": "ᚠ", "tags": ["Soldi", "Lavoro", "Inizi"], "start": (6, 29), "end": (7, 13),
     "ipa": "ˈfehu", "sound_it": "Fe-hu", "sound_en": "Fay-who", 
     "meaning": "Abbondanza, Energia", "desc": "Nuovi inizi, ricchezza, energia creativa.", "desc_rev": "Perdita finanziaria, avidità."},
    
    {"name": "Uruz", "symbol": "ᚢ", "tags": ["Salute", "Forza", "Coraggio"], "start": (7, 14), "end": (7, 28),
     "ipa": "ˈuːruz", "sound_it": "U-ruz", "sound_en": "Oo-rooz", 
     "meaning": "Forza, Salute", "desc": "Forza fisica, salute, potenziale.", "desc_rev": "Debolezza, forza mal diretta."},
    
    {"name": "Thurisaz", "symbol": "ᚦ", "tags": ["Protezione", "Conflitto", "Difesa"], "start": (7, 29), "end": (8, 12),
     "ipa": "ˈθurisaz", "sound_it": "Thu-ri-saz", "sound_en": "Thoor-ee-sawz", 
     "meaning": "Protezione, Caos", "desc": "Forza reattiva, conflitto necessario.", "desc_rev": "Pericolo, indifeso."},
    
    {"name": "Ansuz", "symbol": "ᚨ", "tags": ["Comunicazione", "Studio", "Saggezza"], "start": (8, 13), "end": (8, 28),
     "ipa": "ˈansuz", "sound_it": "An-suz", "sound_en": "Awn-sooz", 
     "meaning": "Saggezza, Voce", "desc": "Messaggio divino, ispirazione, verità.", "desc_rev": "Incomprensione, inganno."},
    
    {"name": "Raidho", "symbol": "ᚱ", "tags": ["Viaggio", "Scelta", "Movimento"], "start": (8, 29), "end": (9, 12),
     "ipa": "ˈraiðo", "sound_it": "Rai-dho", "sound_en": "Rye-though", 
     "meaning": "Viaggio, Ritmo", "desc": "Viaggio fisico o interiore, evoluzione.", "desc_rev": "Crisi, stasi, ingiustizia."},
    
    {"name": "Kenaz", "symbol": "ᚲ", "tags": ["Creatività", "Amore", "Passione"], "start": (9, 13), "end": (9, 27),
     "ipa": "ˈkaʊnan", "sound_it": "Ke-naz", "sound_en": "Kane-awz", 
     "meaning": "Fuoco, Conoscenza", "desc": "Rivelazione, creatività, luce.", "desc_rev": "Malattia, ignoranza, fine."},
    
    {"name": "Gebo", "symbol": "ᚷ", "tags": ["Amore", "Relazioni", "Amicizia"], "start": (9, 28), "end": (10, 12),
     "ipa": "ˈgebo", "sound_it": "Ghe-bo", "sound_en": "Ghay-boh", 
     "meaning": "Dono, Scambio", "desc": "Generosità, partnership, unione.", "desc_rev": "Sempre positiva."},
    
    {"name": "Wunjo", "symbol": "ᚹ", "tags": ["Felicità", "Successo", "Desideri"], "start": (10, 13), "end": (10, 27),
     "ipa": "ˈwunjo", "sound_it": "Vun-yo", "sound_en": "Woon-yo", 
     "meaning": "Gioia, Armonia", "desc": "Felicità, successo, realizzazione.", "desc_rev": "Tristezza, ritardi."},
    
    {"name": "Hagalaz", "symbol": "ᚺ", "tags": ["Crisi", "Cambiamento", "Caos"], "start": (10, 28), "end": (11, 12),
     "ipa": "ˈhagalaz", "sound_it": "Ha-ga-laz", "sound_en": "Haw-gaw-lawz", 
     "meaning": "Distruzione", "desc": "Cambiamento incontrollato, crisi necessaria.", "desc_rev": "Forza inevitabile."},
    
    {"name": "Nauthiz", "symbol": "ᚾ", "tags": ["Bisogno", "Pazienza", "Ostacoli"], "start": (11, 13), "end": (11, 27),
     "ipa": "ˈnauθiz", "sound_it": "Nau-thiz", "sound_en": "Now-thiz", 
     "meaning": "Necessità", "desc": "Restrizioni, lezioni dure, resistenza.", "desc_rev": "Privazione estrema."},
    
    {"name": "Isa", "symbol": "ᛁ", "tags": ["Blocco", "Pausa", "Calma"], "start": (11, 28), "end": (12, 12),
     "ipa": "ˈiːsa", "sound_it": "I-sa", "sound_en": "Ee-saw", 
     "meaning": "Ghiaccio, Stasi", "desc": "Blocco, pausa, concentrazione.", "desc_rev": "Egoismo, cecità."},
    
    {"name": "Jera", "symbol": "ᛃ", "tags": ["Tempo", "Raccolto", "Pazienza"], "start": (12, 13), "end": (12, 27),
     "ipa": "ˈjeːra", "sound_it": "Je-ra", "sound_en": "Yair-ah", 
     "meaning": "Ciclo, Raccolto", "desc": "Risultati nel tempo, pace, ciclicità.", "desc_rev": "Ripetizione."},
    
    {"name": "Eihwaz", "symbol": "ᛇ", "tags": ["Magia", "Trasformazione", "Morte"], "start": (12, 28), "end": (1, 12),
     "ipa": "ˈeɪhwaz", "sound_it": "Ei-hvaz", "sound_en": "Eye-wawz", 
     "meaning": "Tasso, Difesa", "desc": "Resistenza, connessione tra mondi.", "desc_rev": "Confusione."},
    
    {"name": "Perthro", "symbol": "ᛈ", "tags": ["Destino", "Mistero", "Fortuna"], "start": (1, 13), "end": (1, 27),
     "ipa": "ˈperðro", "sound_it": "Per-dhro", "sound_en": "Per-throw", 
     "meaning": "Mistero, Sorte", "desc": "Segreti, occulto, fertilità.", "desc_rev": "Sfortuna, solitudine."},
    
    {"name": "Algiz", "symbol": "ᛉ", "tags": ["Protezione", "Spiritualità", "Istinto"], "start": (1, 28), "end": (2, 12),
     "ipa": "ˈalgiz", "sound_it": "Al-ghiz", "sound_en": "All-ghiz", 
     "meaning": "Protezione Alta", "desc": "Scudo, connessione divina.", "desc_rev": "Vulnerabilità."},
    
    {"name": "Sowilo", "symbol": "ᛊ", "tags": ["Vittoria", "Salute", "Energia"], "start": (2, 13), "end": (2, 26),
     "ipa": "ˈsoːwilo", "sound_it": "So-ui-lo", "sound_en": "So-ee-lo", 
     "meaning": "Sole, Successo", "desc": "Vittoria, onore, potere.", "desc_rev": "Arroganza."},
    
    {"name": "Tiwaz", "symbol": "ᛏ", "tags": ["Giustizia", "Vittoria", "Coraggio"], "start": (2, 27), "end": (3, 13),
     "ipa": "ˈtiːwaz", "sound_it": "Ti-uaz", "sound_en": "Tea-wawz", 
     "meaning": "Giustizia", "desc": "Onore, autorità, razionalità.", "desc_rev": "Ingiustizia, sconfitta."},
    
    {"name": "Berkana", "symbol": "ᛒ", "tags": ["Famiglia", "Crescita", "Donna"], "start": (3, 14), "end": (3, 29),
     "ipa": "ˈberkana", "sound_it": "Ber-ka-na", "sound_en": "Bear-kaw-nah", 
     "meaning": "Nascita", "desc": "Fertilità, guarigione, nuovi inizi.", "desc_rev": "Problemi familiari."},
    
    {"name": "Ehwaz", "symbol": "ᛖ", "tags": ["Movimento", "Squadra", "Viaggio"], "start": (3, 30), "end": (4, 13),
     "ipa": "ˈehwaz", "sound_it": "Eh-uaz", "sound_en": "Ay-wawz", 
     "meaning": "Cavallo", "desc": "Trasporto, lealtà, progresso.", "desc_rev": "Sfiducia, tradimento."},
    
    {"name": "Mannaz", "symbol": "ᛗ", "tags": ["Mente", "Società", "Amicizia"], "start": (4, 14), "end": (4, 28),
     "ipa": "ˈmanːaz", "sound_it": "Man-naz", "sound_en": "Man-awz", 
     "meaning": "Umanità", "desc": "Intelligenza, aiuto sociale.", "desc_rev": "Isolamento, nemico."},
    
    {"name": "Laguz", "symbol": "ᛚ", "tags": ["Emozioni", "Intuizione", "Sogni"], "start": (4, 29), "end": (5, 13),
     "ipa": "ˈlaguz", "sound_it": "La-guz", "sound_en": "Law-ghooz", 
     "meaning": "Acqua", "desc": "Flusso, sogni, inconscio.", "desc_rev": "Paura, confusione."},
    
    {"name": "Ingwaz", "symbol": "ᛜ", "tags": ["Pace", "Casa", "Conclusione"], "start": (5, 14), "end": (5, 28),
     "ipa": "ˈiŋwaz", "sound_it": "Ing-uaz", "sound_en": "Ing-wawz", 
     "meaning": "Gestazione", "desc": "Riposo, crescita interna, pace.", "desc_rev": "Sempre positiva."},
    
    {"name": "Othala", "symbol": "ᛟ", "tags": ["Soldi", "Famiglia", "Eredità"], "start": (5, 29), "end": (6, 13),
     "ipa": "ˈoːθala", "sound_it": "O-tha-la", "sound_en": "Oath-aw-law", 
     "meaning": "Patria", "desc": "Proprietà, radici, eredità.", "desc_rev": "Povertà, perdita."},
    
    {"name": "Dagaz", "symbol": "ᛞ", "tags": ["Svolta", "Luce", "Speranza"], "start": (6, 14), "end": (6, 28),
     "ipa": "ˈdagaz", "sound_it": "Da-gaz", "sound_en": "Daw-ghawz", 
     "meaning": "Risveglio", "desc": "Svolta, chiarezza, fine di un ciclo.", "desc_rev": "Cecità alla luce."}
]

# --- FUNZIONI DI SUPPORTO ---
def get_birth_rune(day, month):
    """Calcola la runa basata sulla data di nascita"""
    for r in runes_db:
        # Gestione date normali e cavallo d'anno (dicembre-gennaio)
        start_m, start_d = r['start']
        end_m, end_d = r['end']
        
        is_in_range = False
        if start_m == end_m:
            if start_m == month and start_d <= day <= end_d: is_in_range = True
        elif start_m < end_m:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d): is_in_range = True
        else: # Scavalla l'anno (Dic-Gen)
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d): is_in_range = True
            
        if is_in_range:
            return r
    return runes_db[0] # Fallback

def draw_rune_card(rune_data, is_reversed=False):
    symbol_class = "rune-symbol-rev" if is_reversed else "rune-symbol"
    meaning_text = rune_data['desc_rev'] if is_reversed else rune_data['desc']
    title_suffix = "(Rovesciata)" if is_reversed else ""
    
    tags_html = "".join([f"<span class='tag'>{t}</span>" for t in rune_data.get('tags', [])])
    
    html = f"""
    <div class="rune-card">
        <div class="{symbol_class}">{rune_data['symbol']}</div>
        <div class="rune-title">{rune_data['name']} {title_suffix}</div>
        <div style="margin:5px 0;">{tags_html}</div>
        <div style="color:#BBB; font-style:italic; margin-bottom:10px;">"{rune_data['meaning']}"</div>
        <hr style="border-color: #444;">
        <div style="text-align:justify; color:#DDD;">{meaning_text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- STATO E MENU ---
if 'journal' not in st.session_state: st.session_state.journal = [] 
if 'score' not in st.session_state: st.session_state.score = 0 
if 'game_rune' not in st.session_state: st.session_state.game_rune = None 

st.sidebar.title("ᛟ Navigazione")
menu = st.sidebar.radio("Percorso:", 
    ["1. Il Grimorio (Studio)", "2. La Palestra (Quiz)", "3. L'Oracolo (Divinazione)", 
     "4. Profilo Runico (Nascita)", "5. Il Diario (Statistiche)"])

# --- PAGINE ---

if menu == "1. Il Grimorio (Studio)":
    st.title("📖 Il Grimorio")
    st.write("Cerca per nome o per intento (es. 'Amore', 'Soldi').")
    search = st.text_input("Cerca...")
    
    for r in runes_db:
        # Ricerca potenziata: cerca anche nei TAG
        tags_str = " ".join(r['tags']).lower()
        if search.lower() in r['name'].lower() or search.lower() in r['meaning'].lower() or search.lower() in tags_str:
            with st.expander(f"{r['symbol']} {r['name']}"):
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"<div style='font-size:70px; text-align:center; color:#FFD700;'>{r['symbol']}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**Tag:** " + " ".join([f"`{t}`" for t in r['tags']]))
                    st.markdown(f"🔊 **{r['sound_it']}** (IPA: /{r['ipa']}/)")
                    st.write(f"_{r['desc']}_")

elif menu == "2. La Palestra (Quiz)":
    st.title("⚔️ La Palestra")
    st.caption(f"Punti: {st.session_state.score}")
    if st.session_state.game_rune is None:
        st.session_state.game_rune = random.choice(runes_db)
        options = [st.session_state.game_rune]
        while len(options) < 4:
            x = random.choice(runes_db)
            if x not in options: options.append(x)
        random.shuffle(options)
        st.session_state.game_options = options

    st.markdown(f"<div style='font-size:100px; text-align:center; color:#FFD700;'>{st.session_state.game_rune['symbol']}</div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.game_options):
        with cols[i % 2]:
            if st.button(f"{opt['name']}", key=f"btn_{i}"):
                if opt['name'] == st.session_state.game_rune['name']:
                    st.success("Corretto! +10"); st.session_state.score += 10; time.sleep(0.5); st.session_state.game_rune = None; st.rerun()
                else:
                    st.error(f"No, era {st.session_state.game_rune['name']}"); st.session_state.score -= 5

elif menu == "3. L'Oracolo (Divinazione)":
    st.title("🔮 L'Oracolo")
    spread = st.selectbox("Metodo", ["Runa Singola", "Le Tre Norne", "Croce Elementale"])
    if st.button("Consulta"):
        with st.spinner("..."): time.sleep(1)
        if spread == "Runa Singola":
            r = random.choice(runes_db); rev = random.choice([True, False])
            draw_rune_card(r, rev)
            st.session_state.last_read = {"type": spread, "runes": [r]}
        # (Ometto le altre stese per brevità, sono uguali a prima)
        elif spread == "Le Tre Norne":
             picks = random.sample(runes_db, 3)
             cols = st.columns(3)
             for i, col in enumerate(cols):
                 with col: draw_rune_card(picks[i], random.choice([True, False]))
             st.session_state.last_read = {"type": spread, "runes": picks}

    if 'last_read' in st.session_state:
        if st.button("Salva nel Diario"):
            st.session_state.journal.append({"Data": datetime.now().strftime("%d/%m"), "Rune": [x['name'] for x in st.session_state.last_read['runes']]})
            st.success("Salvato!")

### NOVITÀ: PROFILO RUNICO
elif menu == "4. Profilo Runico (Nascita)":
    st.title("🎂 La tua Runa di Nascita")
    st.write("Scopri quale Runa governava il cielo quando sei nato.")
    
    col1, col2 = st.columns(2)
    d = col1.number_input("Giorno", 1, 31, 1)
    m = col2.number_input("Mese", 1, 12, 1)
    
    if st.button("Calcola Runa"):
        birth_rune = get_birth_rune(d, m)
        st.markdown("### La tua guardiana è:")
        draw_rune_card(birth_rune)
        st.info("Questa runa rappresenta le tue qualità innate e le sfide che devi superare nella vita.")

### NOVITÀ: DIARIO CON STATISTICHE
elif menu == "5. Il Diario (Statistiche)":
    st.title("📜 Statistiche")
    if not st.session_state.journal:
        st.info("Nessuna lettura salvata.")
    else:
        # Analisi frequenza
        all_runes = []
        for entry in st.session_state.journal:
            all_runes.extend(entry['Rune'])
        
        counts = pd.Series(all_runes).value_counts()
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.write("### Frequenza Apparizioni")
            st.bar_chart(counts)
        with c2:
            st.write("### Storico")
            st.dataframe(st.session_state.journal)