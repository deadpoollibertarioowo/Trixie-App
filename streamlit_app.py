import streamlit as st
import datetime
import calendar
import google.generativeai as genai
from googleapiclient.discovery import build

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TRIXIE", page_icon="⚡", layout="wide")

GEMINI_API_KEY = "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg"
YOUTUBE_API_KEY = "AIzaSyC690dfN-lRw-eQimwEwDd3J1cab8Gcofw"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

st.title("⚡ TRIXIE")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN: Buscador de Élite")
    
    # Filtros optimizados: Nombre exacto + términos opcionales para no bloquear resultados
    personajes_contexto = {
        "Javier Milei": '"Javier Milei" (libertario OR política)',
        "Axel Kaiser": '"Axel Kaiser" (liberalismo OR economía)',
        "Gloria Álvarez": '"Gloria Álvarez" (libertaria OR política)',
        "Dannan": '"Emmanuel Dannan" OR "Dannan"',
        "Jaime Dunn": '"Jaime Dunn" (economía OR Bolivia)'
    }
    
    seleccion = st.multiselect("¿Qué personaje(s) quieres hoy?", list(personajes_contexto.keys()))
    
    st.subheader("Rango Mensual")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, 2027))
    
    col1, col2 = st.columns(2)
    with col1:
        mes_ini = st.selectbox("Mes inicio", meses, index=0) # Enero
        anio_ini = st.selectbox("Año inicio", anios, index=anios.index(2026))
    with col2:
        mes_fin = st.selectbox("Mes fin", meses, index=0)
        anio_fin = st.selectbox("Año fin", anios, index=anios.index(2026))

    if st.button("Generar Informe de Videos"):
        if seleccion:
            with st.spinner("Buscando videos..."):
                m_i = meses.index(mes_ini) + 1
                m_f = meses.index(mes_fin) + 1
                fecha_inicio = datetime.date(anio_ini, m_i, 1)
                ultimo_dia = calendar.monthrange(anio_fin, m_f)[1]
                fecha_fin = datetime.date(anio_fin, m_f, ultimo_dia)
                
                # Query flexible
                query = " ".join([personajes_contexto[p] for p in seleccion])
                
                request = youtube.search().list(
                    q=query,
                    part="snippet",
                    type="video",
                    # Quitamos el filtro 'long' temporalmente para ver si es lo que bloquea
                    # o lo dejamos si solo quieres +20 min. 
                    videoDuration="any", 
                    publishedAfter=fecha_inicio.strftime('%Y-%m-%dT00:00:00Z'),
                    publishedBefore=fecha_fin.strftime('%Y-%m-%dT23:59:59Z'),
                    maxResults=15
                )
                response = request.execute()

                if response['items']:
                    st.success(f"He encontrado estos videos en {mes_ini} {anio_ini}:")
                    for item in response['items']:
                        # Filtro manual anti-shorts en el título/descripción
                        titulo = item['snippet']['title']
                        if "#shorts" in titulo.lower(): continue
                        
                        canal = item['snippet']['channelTitle']
                        video_id = item['id']['videoId']
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        
                        with st.container():
                            st.markdown(f"### {titulo}")
                            st.write(f"📺 Canal: **{canal}** | [🎥 Ver Video]({url})")
                            st.divider()
                else:
                    st.warning("No se encontraron videos. Prueba ampliando el rango o quitando términos.")
        else:
            st.warning("Selecciona un personaje.")

# (TEX, Futuro y Marky siguen debajo sin cambios)