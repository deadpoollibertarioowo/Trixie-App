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
    st.header("🔍 Módulo FAWN: Buscador Inteligente")
    
    personajes_dict = {"1": "Javier Milei", "2": "Axel Kaiser", "3": "Gloria Álvarez", "4": "Dannan", "5": "Jaime Dunn"}
    seleccion = st.multiselect("¿Qué personaje(s) quieres hoy?", list(personajes_dict.values()))
    
    # --- NUEVA SECCIÓN DE FECHAS POR MES Y AÑO ---
    st.subheader("Rango de Búsqueda")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, datetime.date.today().year + 1))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Desde:**")
        mes_inicio_n = st.selectbox("Mes inicio", meses, index=3) # Abril por defecto
        anio_inicio = st.selectbox("Año inicio", anios, index=anios.index(2020))
    
    with col2:
        st.write("**Hasta:**")
        mes_fin_n = st.selectbox("Mes fin", meses, index=datetime.date.today().month - 1)
        anio_fin = st.selectbox("Año fin", anios, index=len(anios)-1)

    if st.button("Generar Informe de Videos"):
        if seleccion:
            with st.spinner("Buscando videos largos..."):
                # Convertir selección de mes/año a fechas reales
                m_ini = meses.index(mes_inicio_n) + 1
                m_fin = meses.index(mes_fin_n) + 1
                
                # Primer día del mes de inicio
                fecha_inicio = datetime.date(anio_inicio, m_ini, 1)
                # Último día del mes de fin (calculado automáticamente)
                ultimo_dia = calendar.monthrange(anio_fin, m_fin)[1]
                fecha_fin = datetime.date(anio_fin, m_fin, ultimo_dia)
                
                query = " ".join([f'"{p}"' for p in seleccion])
                
                request = youtube.search().list(
                    q=query,
                    part="snippet",
                    type="video",
                    videoDuration="long",
                    publishedAfter=fecha_inicio.strftime('%Y-%m-%dT00:00:00Z'),
                    publishedBefore=fecha_fin.strftime('%Y-%m-%dT23:59:59Z'),
                    maxResults=10
                )
                response = request.execute()

                if response['items']:
                    st.success(f"Videos encontrados entre {mes_inicio_n} {anio_inicio} y {mes_fin_n} {anio_fin}:")
                    for item in response['items']:
                        titulo = item['snippet']['title']
                        canal = item['snippet']['channelTitle']
                        video_id = item['id']['videoId']
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        
                        with st.container():
                            st.markdown(f"### {titulo}")
                            st.write(f"📺 Canal: **{canal}** | [🎥 Ver en YouTube]({url})")
                            st.divider()
                else:
                    st.warning("No se encontraron videos largos en ese rango mensual.")
        else:
            st.warning("Selecciona al menos un personaje.")

# Módulos TEX, Futuro y Marky se mantienen igual debajo...
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    asunto = st.text_input("Asunto de la carta:")
    puntos = st.text_area("Detalles clave a incluir:")
    if st.button("Redactar Carta"):
        prompt = f"Redacta una carta formal sobre: {asunto}. Puntos clave: {puntos}"
        response = model.generate_content(prompt)
        st.write(response.text)

elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    pregunta = st.text_area("Plantea tu situación:")
    if st.button("Obtener Dictamen"):
        prompt = f"Actúa como un consejo de líderes (Trump, Musk). Analicen esto: {pregunta}"
        response = model.generate_content(prompt)
        st.markdown(response.text)

elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    fecha_m = st.date_input("Fecha de campaña:")
    if st.button("Generar Plan"):
        prompt = f"Estrategia de marketing para el {fecha_m}"
        response = model.generate_content(prompt)
        st.markdown(response.text)