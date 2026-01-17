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

# Configuración de servicios
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

st.title("⚡ TRIXIE")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN: Buscador de Élite")
    st.info("Filtros de identidad activados para evitar homónimos.")
    
    # Diccionario de búsqueda optimizada (Nombres + Contexto Profesional)
    personajes_contexto = {
        "Javier Milei": '"Javier Milei" política argentina libertario',
        "Axel Kaiser": '"Axel Kaiser" liberalismo economía Chile',
        "Gloria Álvarez": '"Gloria Álvarez" libertaria política Guatemala',
        "Dannan": '"Emmanuel Dannan" oficial política',
        "Jaime Dunn": '"Jaime Dunn" economía finanzas Bolivia'
    }
    
    seleccion = st.multiselect("¿Qué personaje(s) quieres hoy?", list(personajes_contexto.keys()))
    
    st.subheader("Rango Mensual")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, datetime.date.today().year + 1))
    
    col1, col2 = st.columns(2)
    with col1:
        mes_ini = st.selectbox("Mes inicio", meses, index=3) # Abril por defecto
        anio_ini = st.selectbox("Año inicio", anios, index=anios.index(2020))
    with col2:
        mes_fin = st.selectbox("Mes fin", meses, index=datetime.date.today().month - 1)
        anio_fin = st.selectbox("Año fin", anios, index=len(anios)-1)

    if st.button("Generar Informe de Videos"):
        if seleccion:
            with st.spinner("Realizando búsqueda quirúrgica en YouTube..."):
                # Cálculo de fechas
                m_i = meses.index(mes_ini) + 1
                m_f = meses.index(mes_fin) + 1
                fecha_inicio = datetime.date(anio_ini, m_i, 1)
                ultimo_dia = calendar.monthrange(anio_fin, m_f)[1]
                fecha_fin = datetime.date(anio_fin, m_f, ultimo_dia)
                
                # Construcción de la query con contexto
                query = " ".join([personajes_contexto[p] for p in seleccion])
                
                request = youtube.search().list(
                    q=query,
                    part="snippet",
                    type="video",
                    videoDuration="long", # Solo videos de +20 min (Adiós Shorts)
                    publishedAfter=fecha_inicio.strftime('%Y-%m-%dT00:00:00Z'),
                    publishedBefore=fecha_fin.strftime('%Y-%m-%dT23:59:59Z'),
                    maxResults=10
                )
                response = request.execute()

                if response['items']:
                    st.success(f"Resultados encontrados para: {', '.join(seleccion)}")
                    for item in response['items']:
                        titulo = item['snippet']['title']
                        canal = item['snippet']['channelTitle']
                        video_id = item['id']['videoId']
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        
                        with st.container():
                            st.markdown(f"### {titulo}")
                            st.write(f"📺 Canal: **{canal}**")
                            st.markdown(f"[🎥 Ver Video en YouTube]({url})")
                            st.divider()
                else:
                    st.warning("No se encontraron videos largos con estos filtros específicos.")
        else:
            st.warning("Por favor, selecciona al menos un personaje.")

# --- MÓDULOS RESTANTES ---
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    asunto = st.text_input("Asunto:")
    puntos = st.text_area("Detalles:")
    if st.button("Redactar"):
        res = model.generate_content(f"Redacta una carta formal: {asunto}. {puntos}")
        st.write(res.text)

elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    p = st.text_area("Plantea tu caso:")
    if st.button("Consultar"):
        res = model.generate_content(f"Dictamen de Trump y Musk sobre: {p}")
        st.markdown(res.text)

elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    f = st.date_input("Fecha:")
    if st.button("Estrategia"):
        res = model.generate_content(f"Estrategia de marketing para: {f}")
        st.markdown(res.text)