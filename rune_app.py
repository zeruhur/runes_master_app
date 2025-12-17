import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time

# --- 1. CONFIGURAZIONE E STILE VISIVO (DARK THEME) ---
st.set_page_config(page_title="Rune Master", page_icon="ᛟ", layout="wide")

# CSS Personalizzato per atmosfera mistica
st.markdown("""
    <style>
    /* Sfondo scuro e testo chiaro */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Stile delle carte delle Rune */
    .rune-card {
        background-color: #262730;
        border: 1px solid #4B4B4B;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .rune-symbol {
        font-size: 80px;
        color: #FFD700; /* Oro */
        font-weight: bold;
        text-shadow: 0 0 10px #FFD700;
    }
    .rune-symbol-rev {
        font-size: 80px;
        color: #A0A0A0; /* Grigio spento per rovescio */
        font-weight: bold;
        transform: rotate(180deg);
        display: inline-block;
    }
    .rune-title {
        font-size: 24px;
        font-weight: bold;
        color: #E0E0E0;
        margin-top: 10px;
    }
    /* Bottone personalizzato */
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE COMPLETO ---
runes_db = [
    {"name": "Fehu", "symbol": "ᚠ", "ipa": "ˈfehu", "sound_it": "Fe-hu (h aspirata)", "sound_en": "Fay-who", 
     "meaning": "Abbondanza, Energia", "desc": "Nuovi inizi, ricchezza guadagnata, energia creativa.", "desc_rev": "Perdita finanziaria, avidità, blocco creativo."},
    
    {"name": "Uruz", "symbol": "ᚢ", "ipa": "ˈuːruz", "sound_it": "U-ruz", "sound_en": "Oo-rooz", 
     "meaning": "Forza, Salute", "desc": "Forza fisica, velocità, salute, potenziale indomito.", "desc_rev": "Debolezza, forza mal diretta, violenza, malattia."},
    
    {"name": "Thurisaz", "symbol": "ᚦ", "ipa": "ˈθurisaz", "sound_it": "Thu-ri-saz ('th' come in 'think')", "sound_en": "Thoor-ee-sawz", 
     "meaning": "Protezione, Spina", "desc": "Forza reattiva, conflitto necessario, catarsi.", "desc_rev": "Pericolo, indifeso, tradimento, decisioni affrettate."},
    
    {"name": "Ansuz", "symbol": "ᚨ", "ipa": "ˈansuz", "sound_it": "An-suz", "sound_en": "Awn-sooz", 
     "meaning": "Saggezza, Comunicazione", "desc": "Messaggio divino, ispirazione, verità, consiglio.", "desc_rev": "Incomprensione, inganno, manipolazione, noia."},
    
    {"name": "Raidho", "symbol": "ᚱ", "ipa": "ˈraiðo", "sound_it": "Rai-dho ('dh' come in 'the')", "sound_en": "Rye-though", 
     "meaning": "Viaggio, Ritmo", "desc": "Viaggio fisico o interiore, evoluzione, ordine.", "desc_rev": "Crisi, stasi, ingiustizia, viaggio interrotto."},
    
    {"name": "Kenaz", "symbol": "ᚲ", "ipa": "ˈkaʊnan", "sound_it": "Ke-naz ('c' dura)", "sound_en": "Kane-awz", 
     "meaning": "Fuoco, Conoscenza", "desc": "Rivelazione, creatività, luce tecnica, trasformazione.", "desc_rev": "Malattia, ignoranza, mancanza di creatività, rottura."},
    
    {"name": "Gebo", "symbol": "ᚷ", "ipa": "ˈgebo", "sound_it": "Ghe-bo ('g' dura come 'gatto')", "sound_en": "Ghay-boh", 
     "meaning": "Dono, Scambio", "desc": "Generosità, partnership, equilibrio, unione.", "desc_rev": "Gebo non ha rovescio. Significa sempre connessione."},
    
    {"name": "Wunjo", "symbol": "ᚹ", "ipa": "ˈwunjo", "sound_it": "Vun-yo ('j' come 'ieri')", "sound_en": "Woon-yo", 
     "meaning": "Gioia, Armonia", "desc": "Felicità, successo, realizzazione, cameratismo.", "desc_rev": "Tristezza, alienazione, delirio, ritardi."},
    
    {"name": "Hagalaz", "symbol": "ᚺ", "ipa": "ˈhagalaz", "sound_it": "Ha-ga-laz (h aspirata, g dura)", "sound_en": "Haw-gaw-lawz", 
     "meaning": "Grandine, Distruzione", "desc": "Cambiamento incontrollato, crisi naturale, purificazione.", "desc_rev": "Non ha rovescio. È una forza inevitabile."},
    
    {"name": "Nauthiz", "symbol": "ᚾ", "ipa": "ˈnauθiz", "sound_it": "Nau-thiz ('th' come in 'think')", "sound_en": "Now-thiz", 
     "meaning": "Necessità, Resistenza", "desc": "Restrizioni, lezioni dure, pazienza, bisogno.", "desc_rev": "Non ha rovescio standard (o indica estrema privazione)."},
    
    {"name": "Isa", "symbol": "ᛁ", "ipa": "ˈiːsa", "sound_it": "I-sa", "sound_en": "Ee-saw", 
     "meaning": "Ghiaccio, Stasi", "desc": "Blocco, pausa, concentrazione, conservazione.", "desc_rev": "Non ha rovescio. Indica egoismo o cecità."},
    
    {"name": "Jera", "symbol": "ᛃ", "ipa": "ˈjeːra", "sound_it": "Je-ra ('j' come 'ieri')", "sound_en": "Yair-ah", 
     "meaning": "Ciclo, Raccolto", "desc": "Risultati nel tempo, pace, pazienza, ciclicità.", "desc_rev": "Non ha rovescio. Indica ripetizione."},
    
    {"name": "Eihwaz", "symbol": "ᛇ", "ipa": "ˈeɪhwaz", "sound_it": "Ei-hvaz (h aspirata)", "sound_en": "Eye-wawz", 
     "meaning": "Tasso, Difesa", "desc": "Resistenza, affidabilità, connessione tra mondi, morte/rinascita.", "desc_rev": "Non ha rovescio."},
    
    {"name": "Perthro", "symbol": "ᛈ", "ipa": "ˈperðro", "sound_it": "Per-dhro ('dh' come 'the')", "sound_en": "Per-throw", 
     "meaning": "Mistero, Sorte", "desc": "Segreti, occulto, fertilità, incertezza evolutiva.", "desc_rev": "Dipendenza, stagnazione, solitudine, sfortuna."},
    
    {"name": "Algiz", "symbol": "ᛉ", "ipa": "ˈalgiz", "sound_it": "Al-ghiz (g dura)", "sound_en": "All-ghiz", 
     "meaning": "Protezione, Istinto", "desc": "Scudo, connessione divina, seguire l'istinto.", "desc_rev": "Vulnerabilità, pericolo nascosto, tabù infranto."},
    
    {"name": "Sowilo", "symbol": "ᛊ", "ipa": "ˈsoːwilo", "sound_it": "So-ui-lo", "sound_en": "So-ee-lo", 
     "meaning": "Sole, Successo", "desc": "Vittoria, salute, onore, potere elementare.", "desc_rev": "Non ha rovescio. Attenzione all'arroganza."},
    
    {"name": "Tiwaz", "symbol": "ᛏ", "ipa": "ˈtiːwaz", "sound_it": "Ti-uaz", "sound_en": "Tea-wawz", 
     "meaning": "Giustizia, Sacrificio", "desc": "Onore, giustizia, autorità, razionalità, ordine.", "desc_rev": "Ingiustizia, squilibrio, conflitto, sconfitta."},
    
    {"name": "Berkana", "symbol": "ᛒ", "ipa": "ˈberkana", "sound_it": "Ber-ka-na", "sound_en": "Bear-kaw-nah", 
     "meaning": "Nascita, Crescita", "desc": "Fertilità, guarigione, nuovi inizi, famiglia.", "desc_rev": "Problemi familiari, ansia, sterilità di idee."},
    
    {"name": "Ehwaz", "symbol": "ᛖ", "ipa": "ˈehwaz", "sound_it": "Eh-uaz (h aspirata)", "sound_en": "Ay-wawz", 
     "meaning": "Cavallo, Movimento", "desc": "Trasporto, lealtà, lavoro di squadra, progresso.", "desc_rev": "Irrequietezza, sfiducia, disarmonia, tradimento."},
    
    {"name": "Mannaz", "symbol": "ᛗ", "ipa": "ˈmanːaz", "sound_it": "Man-naz", "sound_en": "Man-awz", 
     "meaning": "Umanità, Sè", "desc": "L'individuo, intelligenza, struttura sociale, aiuto.", "desc_rev": "Isolamento, manipolazione, nemico interno."},
    
    {"name": "Laguz", "symbol": "ᛚ", "ipa": "ˈlaguz", "sound_it": "La-guz (g dura)", "sound_en": "Law-ghooz", 
     "meaning": "Acqua, Emozioni", "desc": "Flusso, sogni, intuizione, l'inconscio.", "desc_rev": "Confusione, paura, ossessione, illogicità."},
    
    {"name": "Ingwaz", "symbol": "ᛜ", "ipa": "ˈiŋwaz", "sound_it": "Ing-uaz", "sound_en": "Ing-wawz", 
     "meaning": "Gestazione, Potenziale", "desc": "Riposo, crescita interna, pace, amore familiare.", "desc_rev": "Non ha rovescio."},
    
    {"name": "Othala", "symbol": "ᛟ", "ipa": "ˈoːθala", "sound_it": "O-tha-la ('th' come 'think')", "sound_en": "Oath-aw-law", 
     "meaning": "Patria, Eredità", "desc": "Proprietà, radici, eredità spirituale, sicurezza.", "desc_rev": "Mancanza di dimora, povertà, pregiudizio."},
    
    {"name": "Dagaz", "symbol": "ᛞ", "ipa": "ˈdagaz", "sound_it": "Da-gaz (g dura)", "sound_en": "Daw-ghawz", 
     "meaning": "Giorno, Risveglio", "desc": "Svolta, chiarezza, fine di un ciclo, speranza.", "desc_rev": "Non ha rovescio. Cecità alla luce."}
]

# --- 3. GESTIONE STATO ---
if 'journal' not in st.session_state:
    st.session_state.journal = [] 
if 'score' not in st.session_state:
    st.session_state.score = 0 
if 'game_rune' not in st.session_state:
    st.session_state.game_rune = None 

# --- FUNZIONI UTILI ---
def draw_rune_card(rune_data, is_reversed=False):
    """Renderizza visivamente una carta runica"""
    symbol_class = "rune-symbol-rev" if is_reversed else "rune-symbol"
    meaning_text = rune_data['desc_rev'] if is_reversed else rune_data['desc']
    title_suffix = "(Rovesciata)" if is_reversed else ""
    
    html = f"""
    <div class="rune-card">
        <div class="{symbol_class}">{rune_data['symbol']}</div>
        <div class="rune-title">{rune_data['name']} {title_suffix}</div>
        <div style="color:#BBB; font-style:italic; margin-bottom:10px;">"{rune_data['meaning']}"</div>
        <hr style="border-color: #444;">
        <div style="text-align:justify; color:#DDD;">{meaning_text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def save_reading(spread_type, runes_list, notes):
    """Salva la lettura nel diario"""
    entry = {
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Tipo Stesa": spread_type,
        "Rune": ", ".join([r['name'] for r in runes_list]),
        "Note": notes
    }
    st.session_state.journal.append(entry)

# --- MENU PRINCIPALE ---
st.sidebar.title("ᛟ Navigazione")
menu = st.sidebar.radio("Scegli il percorso:", 
    ["1. Il Grimorio (Studio)", 
     "2. La Palestra (Quiz)", 
     "3. L'Oracolo (Divinazione)", 
     "4. Il Diario (Memorie)"])

# --- PAGINA 1: IL GRIMORIO ---
if menu == "1. Il Grimorio (Studio)":
    st.title("📖 Il Grimorio Runico")
    st.markdown("Studia la forma, il suono corretto e il significato.")
    
    col_search, col_filter = st.columns([3, 1])
    search = col_search.text_input("Cerca runa...")
    
    for r in runes_db:
        if search.lower() in r['name'].lower() or search.lower() in r['meaning'].lower():
            with st.expander(f"{r['symbol']} {r['name']} - {r['meaning']}"):
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"<div style='font-size:70px; text-align:center; color:#FFD700;'>{r['symbol']}</div>", unsafe_allow_html=True)
                with c2:
                    # Blocco Pronuncia
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 10px; border-radius: 5px; border-left: 3px solid #FFD700;">
                        <strong>🔊 Pronuncia IT:</strong> {r['sound_it']}<br>
                        <span style="color: #AAA; font-size: 0.9em;">IPA: /{r['ipa']}/  •  Anglicizzata: {r['sound_en']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.write(f"**Dritta:** {r['desc']}")
                    st.write(f"**Rovesciata:** {r['desc_rev']}")

# --- PAGINA 2: LA PALESTRA (GAMIFICATION) ---
elif menu == "2. La Palestra (Quiz)":
    st.title("⚔️ La Palestra di Odino")
    st.write(f"**Punteggio attuale:** {st.session_state.score} punti")
    
    if st.session_state.game_rune is None:
        st.session_state.game_rune = random.choice(runes_db)
        options = [st.session_state.game_rune]
        while len(options) < 4:
            r = random.choice(runes_db)
            if r not in options:
                options.append(r)
        random.shuffle(options)
        st.session_state.game_options = options

    st.markdown("### Qual è il significato di questa Runa?")
    st.markdown(f"<div style='font-size:100px; text-align:center; color:#FFD700; margin: 20px 0;'>{st.session_state.game_rune['symbol']}</div>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.game_options):
        with cols[i % 2]:
            if st.button(f"{opt['name']} ({opt['meaning']})", key=f"btn_{i}"):
                if opt['name'] == st.session_state.game_rune['name']:
                    st.success("✅ Corretto! +10 Punti")
                    st.session_state.score += 10
                    time.sleep(1)
                    st.session_state.game_rune = None 
                    st.rerun()
                else:
                    st.error(f"❌ Sbagliato! Era {st.session_state.game_rune['name']}")
                    st.session_state.score -= 5

# --- PAGINA 3: L'ORACOLO (DIVINAZIONE AVANZATA) ---
elif menu == "3. L'Oracolo (Divinazione)":
    st.title("🔮 L'Oracolo Avanzato")
    
    spread = st.selectbox("Metodo di lettura", 
                          ["Runa Singola (Consiglio)", 
                           "Le Tre Norne (Tempo)", 
                           "Croce Elementale (5 Rune)"])
    
    if st.button("Consultare le Rune"):
        with st.spinner("Sussurrando all'antico pozzo..."):
            time.sleep(1)
        
        if spread == "Runa Singola (Consiglio)":
            rune = random.choice(runes_db)
            rev = random.choice([True, False])
            draw_rune_card(rune, rev)
            st.session_state.last_reading = {"type": spread, "runes": [rune]}
            
        elif spread == "Le Tre Norne (Tempo)":
            picks = random.sample(runes_db, 3)
            titles = ["URD (Passato)", "VERDANDI (Presente)", "SKULD (Futuro)"]
            cols = st.columns(3)
            saved_runes = []
            for i, col in enumerate(cols):
                with col:
                    st.subheader(titles[i])
                    rev = random.choice([True, False])
                    draw_rune_card(picks[i], rev)
                    saved_runes.append(picks[i])
            st.session_state.last_reading = {"type": spread, "runes": saved_runes}
            
        elif spread == "Croce Elementale (5 Rune)":
            picks = random.sample(runes_db, 5)
            titles = ["1. Spirito", "2. Aria (Mente)", "3. Fuoco (Azione)", "4. Acqua (Emozioni)", "5. Terra (Materia)"]
            
            st.subheader("1. Spirito (Il nocciolo della questione)")
            rev = random.choice([True, False])
            draw_rune_card(picks[0], rev)
            
            c1, c2 = st.columns(2)
            with c1:
                st.caption(titles[1])
                draw_rune_card(picks[1], random.choice([True, False]))
                st.caption(titles[3])
                draw_rune_card(picks[3], random.choice([True, False]))
            with c2:
                st.caption(titles[2])
                draw_rune_card(picks[2], random.choice([True, False]))
                st.caption(titles[4])
                draw_rune_card(picks[4], random.choice([True, False]))
            
            st.session_state.last_reading = {"type": spread, "runes": picks}

    if 'last_reading' in st.session_state:
        st.markdown("---")
        with st.expander("📝 Salva questa lettura nel Diario"):
            notes = st.text_area("Scrivi le tue impressioni o la domanda posta:")
            if st.button("Salva nel Diario"):
                save_reading(st.session_state.last_reading['type'], st.session_state.last_reading['runes'], notes)
                st.success("Lettura salvata con successo!")

# --- PAGINA 4: IL DIARIO ---
elif menu == "4. Il Diario (Memorie)":
    st.title("📜 Il Tuo Diario Runico")
    
    if not st.session_state.journal:
        st.info("Il diario è vuoto. Vai dall'Oracolo per fare la prima lettura.")
    else:
        df = pd.DataFrame(st.session_state.journal)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Scarica Diario come CSV",
            data=csv,
            file_name='diario_rune.csv',
            mime='text/csv',
        )

# Footer
st.markdown("<br><br><div style='text-align:center; color:grey;'>App sviluppata con Streamlit</div>", unsafe_allow_html=True)