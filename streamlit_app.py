import streamlit as st
import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN DE IDENTIDAD ---
st.set_page_config(page_title="TRIXIE", page_icon="⚡", layout="centered")

# --- API KEYS INTEGRADAS ---
GEMINI_API_KEY = "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg"
YOUTUBE_API_KEY = "AIzaSyC690dfN-lRw-eQimwEwDd3J1cab8Gcofw"

# Configuración del motor de Inteligencia Artificial
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- DISEÑO DE LA INTERFAZ ---
st.title("⚡ TRIXIE")
st.sidebar.title("Menú de Gems")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

# ---------------------------------------------------------
# MÓDULO FAWN (Buscador Filtrado de Personajes)
# ---------------------------------------------------------
if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN")
    st.info("Búsqueda automática sin Shorts y con filtros de fecha.")
    
    personajes_dict = {
        "1": "Javier Milei",
        "2": "Axel Kaiser",
        "3": "Gloria Álvarez",
        "4": "Dannan",
        "5": "Jaime Dunn"
    }
    
    seleccion = st.multiselect("¿Qué personaje(s) quieres hoy?", list(personajes_dict.values()))
    
    col1, col2 = st.columns(2)
    with col1:
        inicio = st.date_input("Fecha inicial:", datetime.date(2020, 4, 1))
    with col2:
        fin = st.date_input("Fecha final:", datetime.date.today())
        
    if st.button("Ejecutar Búsqueda Automática"):
        if seleccion:
            # 1. Nombres entre comillas para búsqueda exacta
            query_nombres = " ".join([f'"{p}"' for p in seleccion])
            
            # 2. Formato de fechas para YouTube
            fecha_inicio = inicio.strftime('%Y-%m-%d')
            fecha_fin = fin.strftime('%Y-%m-%d