import streamlit as st
import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN DE IDENTIDAD ---
st.set_page_config(page_title="TRIXIE", page_icon="⚡", layout="centered")

# --- ESPACIO PARA TUS LLAVES (API KEYS) ---
# REEMPLAZA EL TEXTO ENTRE COMILLAS CON TUS LLAVES REALES
GEMINI_API_KEY = "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg"
YOUTUBE_API_KEY = "AIzaSyC690dfN-lRw-eQimwEwDd3J1cab8Gcofw"

# Configuración del motor de Inteligencia Artificial
if GEMINI_API_KEY != "AIzaSyDFCa4XKoGZ5ak8ldFqhA3dQT4eDwC0-Bg":
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
    st.info("Búsqueda automática sin Shorts.")
    
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
        
    iif st.button("Ejecutar Búsqueda Automática"):
        if seleccion:
            # Creamos la consulta con los personajes
            query_personajes = " ".join([f'"{p}"' for p in seleccion])
            
            # Construimos los comandos de búsqueda para YouTube
            filtros = f"after:{inicio} before:{fin} -shorts"
            full_query = f"{query_personajes} {filtros}"
            
            # El enlace final con el filtro de videos largos activado
            search_url = f"https://www.youtube.com/results?search_query={full_query.replace(' ', '+')}&sp=EgIYAw%253D%253D"
            
            st.success(f"Búsqueda lista para: {', '.join(seleccion)}")
            st.markdown(f"### [👉 Haz clic aquí para ver los resultados filtrados]({search_url})")
        else:
            st.warning("Por favor selecciona al menos un personaje.")

# ---------------------------------------------------------
# MÓDULO TEX (Redacción de Cartas)
# ---------------------------------------------------------
elif gem_choice == "TEX":
    st.header("📝 Módulo TEX")
    asunto = st.text_input("Asunto de la carta:")
    puntos = st.text_area("Detalles clave a incluir:")
    
    if st.button("Redactar Carta"):
        prompt = f"Actúa como un experto en comunicación corporativa. Redacta una carta formal sobre: {asunto}. Puntos clave: {puntos}"
        with st.spinner("Redactando..."):
            response = model.generate_content(prompt)
            st.markdown("### Resultado:")
            st.write(response.text)

# ---------------------------------------------------------
# MÓDULO FUTURO (Consejo Empresarial)
# ---------------------------------------------------------
elif gem_choice == "Futuro":
    st.header("🏢 Módulo FUTURO")
    st.write("Consulta al consejo de líderes (Trump, Musk, etc.)")
    pregunta = st.text_area("Plantea tu situación o problema:")
    
    if st.button("Obtener Dictamen"):
        prompt = f"Actúa como un consejo de líderes incluyendo a Donald Trump y Elon Musk. Analicen esto: {pregunta}"
        with st.spinner("El consejo debate..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)

# ---------------------------------------------------------
# MÓDULO MARKY (Marketing Estratégico)
# ---------------------------------------------------------
elif gem_choice == "Marky":
    st.header("📅 Módulo MARKY")
    fecha_m = st.date_input("Fecha para la campaña:")
    
    if st.button("Generar Plan"):
        prompt = f"Dime qué se celebra el {fecha_m} y propón una estrategia de marketing creativa."
        with st.spinner("Pensando..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)