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
# Usamos el nombre del modelo estándar para evitar el error 404
model = genai.GenerativeModel('gemini-1.5-flash')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

st.title("⚡ TRIXIE")
gem_choice = st.sidebar.radio("Selecciona un Módulo:", ["FAWN", "TEX", "Futuro", "Marky"])

# ---------------------------------------------------------
# MÓDULO FAWN (Buscador Liberalismo)
# ---------------------------------------------------------
if gem_choice == "FAWN":
    st.header("🔍 Módulo FAWN")
    personajes_dict = {"1": "Javier Milei", "2": "Axel Kaiser", "3": "Gloria Álvarez", "4": "Emmanuel Dannan", "5": "Jaime Dunn"}
    seleccion = st.multiselect("Personajes:", list(personajes_dict.values()))
    
    st.subheader("Rango de Búsqueda")
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
            with st.spinner("Buscando videos..."):
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
# MÓDULO TEX (Redacción Única)
# ---------------------------------------------------------
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    st.info("Escribe lo que necesitas y TRIXIE redactará la carta completa.")
    
    # Campo único de referencia
    referencia = st.text_area("Referencia de la carta:", placeholder="Ej: Solicito vacaciones para el mes de marzo...", height=150)
    
    if st.button("Redactar Carta"):
        if referencia:
            with st.spinner("Generando redacción formal..."):
                try:
                    # Prompt que le pide a la IA que deduzca el asunto y el cuerpo sola
                    prompt_tex = f"Redacta una carta formal completa basada en la siguiente referencia: '{referencia}'. Incluye lugar (La Paz, Bolivia), fecha actual, un saludo profesional, el cuerpo de la carta bien estructurado y una despedida formal. Deja espacios en corchetes [ ] para datos personales faltantes."
                    
                    response = model.generate_content(prompt_tex)
                    st.markdown("---")
                    st.markdown("### 📄 Carta Redactada:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error de conexión: {e}. Intenta recargar la página.")
        else:
            st.warning("Escribe una referencia primero.")

# ---------------------------------------------------------
# OTROS MÓDULOS
# ---------------------------------------------------------
elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    p = st.text_area("Planteamiento para el consejo:")
    if st.button("Consultar"):
        res = model.generate_content(f"Dictamen de Donald Trump y Elon Musk sobre: {p}")
        st.markdown(res.text)

elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    f = st.date_input("Fecha para planear:")
    if st.button("Estrategia"):
        res = model.generate_content(f"Propón una estrategia de marketing creativa para el día {f}")
        st.markdown(res.text)