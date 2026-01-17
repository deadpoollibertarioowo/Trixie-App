import streamlit as st
import datetime
import calendar
import google.generativeai as genai
from googleapiclient.discovery import build

# --- CONFIGURACIÓN DE IDENTIDAD ---
st.set_page_config(page_title="TRIXIE", page_icon="⚡", layout="wide")

# --- API KEYS ---
GEMINI_API_KEY = "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg"
YOUTUBE_API_KEY = "AIzaSyC690dfN-lRw-eQimwEwDd3J1cab8Gcofw"

# CONFIGURACIÓN DEL MOTOR IA (Corregido para evitar Error 404)
genai.configure(api_key=GEMINI_API_KEY)
# Usamos el nombre de modelo más estable para la API v1beta
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Conexión a YouTube
try:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
except:
    st.error("Error en la llave de YouTube.")

st.title("⚡ TRIXIE")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

# ---------------------------------------------------------
# MÓDULO FAWN
# ---------------------------------------------------------
if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN")
    personajes = ["Javier Milei", "Axel Kaiser", "Gloria Álvarez", "Emmanuel Dannan", "Jaime Dunn"]
    seleccion = st.multiselect("Personajes:", personajes)
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, 2027))
    col1, col2 = st.columns(2)
    with col1:
        mes_ini = st.selectbox("Desde:", meses, index=0)
        anio_ini = st.selectbox("Año inicio", anios, index=anios.index(2026))
    with col2:
        mes_fin = st.selectbox("Hasta:", meses, index=datetime.date.today().month - 1)
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

# ---------------------------------------------------------
# MÓDULO TEX (Corregido y Simplificado)
# ---------------------------------------------------------
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    referencia = st.text_area("¿Qué debe decir la carta?", placeholder="Escribe tu referencia aquí...", height=200)
    
    if st.button("Redactar Carta"):
        if referencia:
            with st.spinner("Redactando..."):
                try:
                    p_tex = f"Redacta una carta formal completa basada en: '{referencia}'. Lugar: La Paz, Bolivia. Incluye fecha actual, saludo, cuerpo y despedida profesional."
                    response = model.generate_content(p_tex)
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error de conexión con la IA: {e}")

# ---------------------------------------------------------
# MÓDULO FUTURO (Corregido)
# ---------------------------------------------------------
elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    p = st.text_area("Plantea tu situación:")
    if st.button("Consultar Consejo"):
        if p:
            with st.spinner("Consultando a Trump y Musk..."):
                try:
                    response = model.generate_content(f"Actúa como Donald Trump y Elon Musk. Den un dictamen sobre: {p}")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

# ---------------------------------------------------------
# MÓDULO MARKY (Corregido)
# ---------------------------------------------------------
elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    f = st.date_input("Fecha para el plan:")
    if st.button("Generar Estrategia"):
        with st.spinner("Planeando..."):
            try:
                response = model.generate_content(f"Propón una estrategia de marketing creativa para el {f}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error de conexión: {e}")