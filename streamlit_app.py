import streamlit as st
import datetime
import calendar
import google.generativeai as genai
from googleapiclient.discovery import build

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TRIXIE", page_icon="⚡", layout="wide")

GEMINI_API_KEY = "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg"
YOUTUBE_API_KEY = "AIzaSyC690dfN-lRw-eQimwEwDd3J1cab8Gcofw"

# Configuración mejorada para evitar errores de "NotFound"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

st.title("⚡ TRIXIE")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

# --- MÓDULO FAWN (Buscador Liberalismo) ---
if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN")
    personajes_dict = {"1": "Javier Milei", "2": "Axel Kaiser", "3": "Gloria Álvarez", "4": "Emmanuel Dannan", "5": "Jaime Dunn"}
    seleccion = st.multiselect("Personajes:", list(personajes_dict.values()))
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, 2027))
    col1, col2 = st.columns(2)
    with col1:
        mes_ini = st.selectbox("Mes inicio", meses, index=0)
        anio_ini = st.selectbox("Año inicio", anios, index=anios.index(2026))
    with col2:
        mes_fin = st.selectbox("Mes fin", meses, index=datetime.date.today().month - 1)
        anio_fin = st.selectbox("Año fin", anios, index=anios.index(2026))

    if st.button("Generar Informe"):
        if seleccion:
            with st.spinner("Buscando..."):
                m_i, m_f = meses.index(mes_ini) + 1, meses.index(mes_fin) + 1
                f_i = datetime.date(anio_ini, m_i, 1).strftime('%Y-%m-%dT00:00:00Z')
                f_f = datetime.date(anio_fin, m_f, calendar.monthrange(anio_fin, m_f)[1]).strftime('%Y-%m-%dT23:59:59Z')
                
                vistos = set()
                for p in seleccion:
                    query = f'"{p}" liberalismo -shorts'
                    res = youtube.search().list(q=query, part="snippet", type="video", publishedAfter=f_i, publishedBefore=f_f, maxResults=5).execute()
                    for item in res.get('items', []):
                        v_id = item['id']['videoId']
                        if v_id not in vistos:
                            vistos.add(v_id)
                            st.markdown(f"### {item['snippet']['title']}")
                            st.write(f"📺 **Canal:** {item['snippet']['channelTitle']} | [🎥 Ver Video](https://www.youtube.com/watch?v={v_id})")
                            st.divider()

# --- MÓDULO TEX (Redacción Simplificada) ---
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX: Redactor de Cartas")
    st.info("Escribe una referencia de lo que necesitas y TRIXIE redactará la carta formal completa.")
    
    # Un solo campo de texto para todo
    instruccion = st.text_area("¿Qué debe decir la carta? (Ej: requerimiento de material para farmacia)", height=200)
    
    if st.button("Redactar Carta"):
        if instruccion:
            with st.spinner("Redactando con estilo formal..."):
                try:
                    # Prompt optimizado para que la IA entienda el contexto sola
                    prompt_final = f"Actúa como un experto en redacción formal y administrativa. Basado en esta referencia: '{instruccion}', redacta una carta formal completa, con lugar, fecha (usa la de hoy), saludo, cuerpo detallado y despedida profesional. Si faltan datos como nombres de personas, deja los espacios en blanco entre corchetes [ ]."
                    
                    response = model.generate_content(prompt_final)
                    st.markdown("---")
                    st.markdown("### 📄 Resultado de la Redacción:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Hubo un problema con la conexión a Gemini. Verifica tu API Key. Error: {e}")
        else:
            st.warning("Por favor, escribe al menos una breve referencia de lo que necesitas.")

# --- MÓDULOS FUTURO Y MARKY ---
elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    p = st.text_area("Planteamiento:")
    if st.button("Consultar"):
        res = model.generate_content(f"Dictamen de Trump y Musk sobre: {p}")
        st.markdown(res.text)

elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    f = st.date_input("Fecha:")
    if st.button("Estrategia"):
        res = model.generate_content(f"Plan de marketing para {f}")
        st.markdown(res.text)