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
    st.header("🔍 Módulo FAWN: Filtro Liberalismo")
    
    # Tu lista numerada de personajes
    personajes_dict = {
        "1": "Javier Milei",
        "2": "Axel Kaiser",
        "3": "Gloria Álvarez",
        "4": "Emmanuel Dannan",
        "5": "Jaime Dunn"
    }
    
    seleccion = st.multiselect("Selecciona los personajes de hoy:", list(personajes_dict.values()))
    
    st.subheader("Rango de Búsqueda")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios = list(range(2015, 2027))
    
    col1, col2 = st.columns(2)
    with col1:
        mes_ini = st.selectbox("Mes inicio", meses, index=10) # Noviembre por defecto
        anio_ini = st.selectbox("Año inicio", anios, index=anios.index(2025))
    with col2:
        mes_fin = st.selectbox("Mes fin", meses, index=datetime.date.today().month - 1)
        anio_fin = st.selectbox("Año fin", anios, index=anios.index(datetime.date.today().year))

    if st.button("Generar Informe"):
        if seleccion:
            with st.spinner("Buscando bajo el filtro 'liberalismo'..."):
                # Fechas
                m_i = meses.index(mes_ini) + 1
                m_f = meses.index(mes_fin) + 1
                fecha_inicio = datetime.date(anio_ini, m_i, 1).strftime('%Y-%m-%dT00:00:00Z')
                ultimo_dia = calendar.monthrange(anio_fin, m_f)[1]
                fecha_fin = datetime.date(anio_fin, m_f, ultimo_dia).strftime('%Y-%m-%dT23:59:59Z')
                
                # Búsqueda individual por personaje + liberalismo para asegurar resultados
                resultados_totales = []
                for p in seleccion:
                    query = f'"{p}" liberalismo -shorts'
                    request = youtube.search().list(
                        q=query,
                        part="snippet",
                        type="video",
                        publishedAfter=fecha_inicio,
                        publishedBefore=fecha_fin,
                        maxResults=5
                    )
                    response = request.execute()
                    if 'items' in response:
                        resultados_totales.extend(response['items'])

                if resultados_totales:
                    st.success(f"Informe listo para {', '.join(seleccion)}")
                    # Evitar duplicados
                    vistos = set()
                    for item in resultados_totales:
                        v_id = item['id']['videoId']
                        if v_id not in vistos:
                            vistos.add(v_id)
                            st.markdown(f"### {item['snippet']['title']}")
                            st.write(f"📺 **Canal:** {item['snippet']['channelTitle']} | [🎥 Ver Video](https://www.youtube.com/watch?v={v_id})")
                            st.divider()
                else:
                    st.warning("No se encontraron videos recientes con el filtro 'liberalismo'.")
        else:
            st.warning("Selecciona un personaje de la lista.")

# Módulos TEX, Futuro y Marky...
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    asunto = st.text_input("Asunto:")
    puntos = st.text_area("Puntos:")
    if st.button("Redactar"):
        res = model.generate_content(f"Escribe una carta sobre {asunto}. {puntos}")
        st.write(res.text)
elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    p = st.text_area("Planteamiento:")
    if st.button("Consultar"):
        res = model.generate_content(f"Dictamen de Trump y Musk: {p}")
        st.markdown(res.text)
elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    f = st.date_input("Fecha:")
    if st.button("Estrategia"):
        res = model.generate_content(f"Plan de marketing para {f}")
        st.markdown(res.text)