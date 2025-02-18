import streamlit as st
import datetime
import time

# Configuración de la página y estilos
st.set_page_config(page_title="CalificaProf-UPV", layout="wide")

# CSS personalizado para un diseño más moderno
st.markdown("""
<style>
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #FF2B2B;
    }
    .profesor-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .prof-name {
        color: #1E1E1E;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .prof-dept {
        color: #666;
        font-size: 0.9rem;
    }
    .search-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        color: #1E1E1E;
    }
    .rating-modal {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .rating-stars {
        font-size: 2rem;
        margin: 1rem 0;
    }
    .professor-rating {
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .welcome-container {
        text-align: center;
        padding: 2rem;
    }
    .welcome-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
    }
    .feature-button {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .feature-button:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .back-btn-container {
        text-align: right;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }
    .back-btn-container .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        min-width: 150px;
        transition: background-color 0.3s;
    }
    .back-btn-container .stButton > button:hover {
        background-color: #FF2B2B;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de variables en el estado de la sesión
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"

# Calificaciones inventadas: para todos los profesores, excepto para id 8 (lumbreras), que tendrá 10 calificaciones de 1 estrella.
if 'ratings' not in st.session_state:
    st.session_state.ratings = [
        # Profesor id 1
        {"id_profesor": 1, "estrellas": 5, "comentario": "Excelente, muy claro.", "fecha": "2024-02-01 14:30:00"},
        {"id_profesor": 1, "estrellas": 4, "comentario": "Buen profesor, explica bien.", "fecha": "2024-02-03 09:15:00"},
        {"id_profesor": 1, "estrellas": 5, "comentario": "Inspirador y atento.", "fecha": "2024-02-05 16:45:00"},
        # Profesor id 2
        {"id_profesor": 2, "estrellas": 4, "comentario": "Explica bien, pero se apresura.", "fecha": "2024-02-02 10:00:00"},
        {"id_profesor": 2, "estrellas": 3, "comentario": "Podría mejorar su metodología.", "fecha": "2024-02-04 11:20:00"},
        # Profesor id 3
        {"id_profesor": 3, "estrellas": 5, "comentario": "Muy didáctico y organizado.", "fecha": "2024-02-01 08:45:00"},
        {"id_profesor": 3, "estrellas": 4, "comentario": "Bueno, pero a veces confuso.", "fecha": "2024-02-03 13:00:00"},
        {"id_profesor": 3, "estrellas": 4, "comentario": "Cumple con sus clases.", "fecha": "2024-02-06 15:30:00"},
        # Profesor id 4
        {"id_profesor": 4, "estrellas": 3, "comentario": "No es muy claro en sus explicaciones.", "fecha": "2024-02-02 14:00:00"},
        {"id_profesor": 4, "estrellas": 4, "comentario": "Tiene esfuerzo, pero requiere mejorar.", "fecha": "2024-02-05 16:00:00"},
        # Profesor id 5
        {"id_profesor": 5, "estrellas": 5, "comentario": "Excelente manejo de la materia.", "fecha": "2024-02-03 11:30:00"},
        {"id_profesor": 5, "estrellas": 4, "comentario": "Muy profesional.", "fecha": "2024-02-04 12:15:00"},
        # Profesor id 6
        {"id_profesor": 6, "estrellas": 4, "comentario": "Interesante, pero a veces monótono.", "fecha": "2024-02-01 15:00:00"},
        {"id_profesor": 6, "estrellas": 3, "comentario": "La materia es complicada.", "fecha": "2024-02-03 17:20:00"},
        # Profesor id 7
        {"id_profesor": 7, "estrellas": 5, "comentario": "Inspirador y dedicado.", "fecha": "2024-02-02 09:45:00"},
        {"id_profesor": 7, "estrellas": 5, "comentario": "Muy claro en sus exposiciones.", "fecha": "2024-02-04 10:30:00"},
        # Profesor id 8: 10 calificaciones de 1 estrella
        {"id_profesor": 8, "estrellas": 1, "comentario": "Suena Bien", "fecha": "2024-02-01 08:00:00"},
        {"id_profesor": 8, "estrellas": 1, "comentario": "Puentesito 😋👏", "fecha": "2024-02-02 08:00:00"},
        {"id_profesor": 8, "estrellas": 1, "comentario": "El Grupo Hardcore", "fecha": "2024-02-03 08:00:00"},
    ]

# Sustituir la lista de profesores actual por la nueva con imágenes de mayor resolución
if 'professors' not in st.session_state:
    st.session_state.professors = [
        {"id": 1, "nombre": "Dr. Héctor Hugo Avilés Arriaga", "departamento": "Ingeniería", "foto": "https://picsum.photos/500?random=1"},
        {"id": 2, "nombre": "Dr. Marco Aurelio Nuño Maganda", "departamento": "Matemáticas", "foto": "https://picsum.photos/500?random=2"},
        {"id": 3, "nombre": "Dr. Jorge Arturo Hernández Almazán", "departamento": "Física", "foto": "https://picsum.photos/500?random=3"},
        {"id": 4, "nombre": "Dr. Rubén Machucho Cadena", "departamento": "Química", "foto": "https://picsum.photos/500?random=4"},
        {"id": 5, "nombre": "Dr. Said Polanco Martagón", "departamento": "Biología", "foto": "https://picsum.photos/500?random=5"},
        {"id": 6, "nombre": "M.I. Eréndira Gutiérrez Meza", "departamento": "Historia", "foto": "https://picsum.photos/500?random=6"},
        {"id": 7, "nombre": "M.I. Arturo Guadalupe Mascorro Cienfuegos", "departamento": "Literatura", "foto": "https://picsum.photos/500?random=7"},
        {"id": 8, "nombre": "M.I. Juan Diego Lumbreras Vega", "departamento": "Lenguas", "foto": "https://picsum.photos/500?random=8"}
    ]

if 'selected_professor' not in st.session_state:
    st.session_state.selected_professor = None
    
if 'rating_modal' not in st.session_state:
    st.session_state.rating_modal = False
if 'current_rating' not in st.session_state:
    st.session_state.current_rating = 0

# Función para actualizar la navegación
def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()  # Cambiar experimental_rerun() por rerun()

# Menú lateral de navegación: inicializar la radio con el valor actual
with st.sidebar:
    page_options = ("Inicio", "Listado de Profesores", "Estadísticas", "Ayuda")
    default_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
    nav_page = st.radio("Navegación", page_options, index=default_index, key="nav_radio")
st.session_state.page = nav_page

# Página de Inicio
def inicio_page():
    # Contenedor de bienvenida
    st.markdown("<div class='welcome-container'>", unsafe_allow_html=True)
    
    # Título y subtítulo
    st.title("Bienvenido a CalificaProf-UPV")
    st.write("Tu opinión es importante para mejorar la calidad educativa")
    
    # Imagen de bienvenida
    st.image("https://picsum.photos/800/400?random=welcome", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-button'>
            <div class='feature-icon'>📚</div>
            <h3>Listado de Profesores</h3>
            <p>Explora y califica a tus profesores</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Profesores", key="btn_profesores"):
            st.session_state.page = "Listado de Profesores"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='feature-button'>
            <div class='feature-icon'>📊</div>
            <h3>Estadísticas</h3>
            <p>Consulta las calificaciones y comentarios</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Estadísticas", key="btn_estadisticas"):
            st.session_state.page = "Estadísticas"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='feature-button'>
            <div class='feature-icon'>❓</div>
            <h3>Ayuda</h3>
            <p>Obtén asistencia y soporte</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Ayuda", key="btn_ayuda"):
            st.session_state.page = "Ayuda"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Nueva función para mostrar el botón de regreso en la parte inferior de la página
def back_to_home():
    st.markdown("<div class='back-btn-container'>", unsafe_allow_html=True)
    if st.button("← Regresar a Inicio", key="back_home"):
        st.session_state.page = "Inicio"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Página de Listado de Profesores
def mostrar_modal_calificacion(profesor):
    st.markdown("<div class='rating-modal'>", unsafe_allow_html=True)
    st.subheader(f"Calificar a {profesor['nombre']}")
    st.markdown(f"<p class='prof-dept'>{profesor['departamento']}</p>", unsafe_allow_html=True)
    
    # Sistema de calificación con estrellas
    col1, col2 = st.columns([2, 1])
    with col1:
        rating = st.select_slider(
            "Calificación",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: "⭐" * x
        )
    
    comentario = st.text_area("Comentario (opcional):", key=f"comentario_{profesor['id']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Enviar", key=f"enviar_{profesor['id']}"):
            rating_record = {
                "id_profesor": profesor["id"],
                "estrellas": rating,
                "comentario": comentario,
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.ratings.append(rating_record)
            st.success("¡Calificación enviada exitosamente!")
            time.sleep(1)
            st.session_state.rating_modal = False
            st.rerun()
    with col3:
        if st.button("Cancelar", key=f"cancelar_{profesor['id']}"):
            st.session_state.rating_modal = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def listado_profesores_page():
    st.markdown("<h1 class='main-title'>Listado de Profesores</h1>", unsafe_allow_html=True)
    
    # Barra de búsqueda
    with st.container():
        st.markdown("<div class='search-container'>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 Buscar profesor...", "")
        st.markdown("</div>", unsafe_allow_html=True)

    # Filtrar profesores según la búsqueda
    profesores_filtrados = [
        p for p in st.session_state.professors
        if search_query.lower() in p["nombre"].lower() or 
           search_query.lower() in p["departamento"].lower()
    ] if search_query else st.session_state.professors

    # Mostrar profesores en un grid moderno
    cols = st.columns(3)
    for idx, profesor in enumerate(profesores_filtrados):
        # Calcular calificación promedio del profesor
        ratings_prof = [r["estrellas"] for r in st.session_state.ratings if r["id_profesor"] == profesor["id"]]
        promedio = sum(ratings_prof) / len(ratings_prof) if ratings_prof else 0
        
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='profesor-card'>
                <img src='{profesor["foto"]}' style='width:100%; border-radius:5px; margin-bottom:1rem;'>
                <div class='prof-name'>{profesor["nombre"]}</div>
                <div class='prof-dept'>{profesor["departamento"]}</div>
                <div class='professor-rating'>
                    {'⭐' * round(promedio) if promedio > 0 else 'Sin calificaciones'}
                    <br>
                    <small>{len(ratings_prof)} calificaciones</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Calificar", key=f"calificar_{profesor['id']}"):
                st.session_state.selected_professor = profesor["id"]
                st.session_state.rating_modal = True

        # Mostrar modal si corresponde a este profesor
        if (st.session_state.rating_modal and 
            st.session_state.selected_professor == profesor["id"]):
            mostrar_modal_calificacion(profesor)
    
    # Al final agregar el botón de regreso
    back_to_home()

# Página de Detalle y Calificación del Profesor
def detalle_calificacion_page():
    profesor_id = st.session_state.selected_professor
    profesor = next((p for p in st.session_state.professors if p["id"] == profesor_id), None)
    if profesor is None:
        st.error("Profesor no encontrado.")
        return

    st.markdown(f"<h1 class='main-title'>Calificar a {profesor['nombre']}</h1>", unsafe_allow_html=True)
    
    # Obtener calificaciones previas del profesor
    ratings_profesor = [r for r in st.session_state.ratings if r["id_profesor"] == profesor_id]
    promedio = sum(r["estrellas"] for r in ratings_profesor) / len(ratings_profesor) if ratings_profesor else 0
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(profesor["foto"], width=300)
        if ratings_profesor:
            st.markdown(f"### Calificación actual: {'⭐' * round(promedio)} ({round(promedio, 2)})")
            st.markdown(f"### Total de calificaciones: {len(ratings_profesor)}")
    
    with col2:
        st.markdown(f"<div class='prof-dept' style='font-size:1.2rem;'>{profesor['departamento']}</div>", unsafe_allow_html=True)
        rating = st.select_slider(
            "Calificación",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x
        )
        comentario = st.text_area("Comentario (opcional):", height=150)

        if st.button("Enviar Calificación", key="submit_rating"):
            rating_record = {
                "id_profesor": profesor["id"],
                "estrellas": rating,
                "comentario": comentario,
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.ratings.append(rating_record)
            st.success("¡Calificación enviada exitosamente!")
            time.sleep(1)  # Pequeña pausa para mostrar el mensaje
            navigate("Listado de Profesores")
    
    back_to_home()

# Página de Estadísticas
def estadisticas_page():
    st.markdown("<h1 class='main-title'>Estadísticas de Calificaciones</h1>", unsafe_allow_html=True)
    
    if not st.session_state.ratings:
        st.write("Aún no hay calificaciones.")
        return

    # Tabla de estadísticas
    data = []
    for profesor in st.session_state.professors:
        ratings = [r for r in st.session_state.ratings if r["id_profesor"] == profesor["id"]]
        if ratings:
            promedio = sum(r["estrellas"] for r in ratings) / len(ratings)
            data.append({
                "Profesor": profesor["nombre"],
                "Departamento": profesor["departamento"],
                "Calificación Promedio": f"{'⭐' * round(promedio)} ({round(promedio, 2)})",
                "Número de Calificaciones": len(ratings)
            })
    
    if data:
        st.table(data)

        # Mostrar comentarios recientes
        st.markdown("### Comentarios Recientes")
        for profesor in st.session_state.professors:
            comentarios = [r for r in st.session_state.ratings 
                         if r["id_profesor"] == profesor["id"] and r["comentario"]]
            if comentarios:
                st.markdown(f"#### {profesor['nombre']}")
                for com in sorted(comentarios, key=lambda x: x["fecha"], reverse=True)[:3]:
                    st.markdown(f"""
                    <div style="padding: 1rem; background-color: white; border-radius: 5px; margin-bottom: 0.5rem;">
                        <div style="color: #666; font-size: 0.8rem;">{com['fecha']}</div>
                        <div>{'⭐' * com['estrellas']}</div>
                        <div style="margin-top: 0.5rem;">{com['comentario']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.write("No hay calificaciones para mostrar estadísticas.")
    
    back_to_home()

# Página de Ayuda/Soporte
def ayuda_page():
    st.title("Ayuda / Soporte")
    st.write("Si tienes preguntas o necesitas asistencia, por favor contacta al administrador de la plataforma.")
    st.write("Correo de soporte: soporte@upv.edu.mx")
    
    back_to_home()

# Renderizar la página correspondiente
if st.session_state.page == "Inicio":
    inicio_page()
elif st.session_state.page == "Listado de Profesores":
    listado_profesores_page()
elif st.session_state.page == "Detalle y Calificación":
    detalle_calificacion_page()
elif st.session_state.page == "Estadísticas":
    estadisticas_page()
elif st.session_state.page == "Ayuda":
    ayuda_page()

