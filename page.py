import streamlit as st
import datetime

# Inicialización de variables en el estado de la sesión
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"
if 'ratings' not in st.session_state:
    st.session_state.ratings = []
if 'selected_professor' not in st.session_state:
    st.session_state.selected_professor = None
if 'professors' not in st.session_state:
    # Lista de profesores simulada
    st.session_state.professors = [
        {"id": 1, "nombre": "Dr. Juan Pérez", "departamento": "Ingeniería", "foto": "https://via.placeholder.com/150"},
        {"id": 2, "nombre": "Dra. María García", "departamento": "Matemáticas", "foto": "https://via.placeholder.com/150"},
        {"id": 3, "nombre": "Dr. Carlos López", "departamento": "Física", "foto": "https://via.placeholder.com/150"}
    ]

# Función para actualizar la navegación
def navigate(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

# Menú lateral de navegación
page = st.sidebar.radio("Navegación", ("Inicio", "Listado de Profesores", "Estadísticas", "Ayuda"))
st.session_state.page = page

# Página de Inicio
def inicio_page():
    st.title("Bienvenido a CalificaProf-UPV")
    st.write("Esta aplicación permite a los alumnos de la UPV calificar de forma anónima a sus profesores.")
    st.write("Utiliza el menú lateral para navegar por la aplicación.")

# Página de Listado de Profesores
def listado_profesores_page():
    st.title("Listado de Profesores")
    st.write("Selecciona un profesor para calificar:")
    for profesor in st.session_state.professors:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(profesor["foto"], width=100)
        with col2:
            st.subheader(profesor["nombre"])
            st.write("Departamento:", profesor["departamento"])
            if st.button("Calificar", key=f"calificar_{profesor['id']}"):
                st.session_state.selected_professor = profesor["id"]
                navigate("Detalle y Calificación")

# Página de Detalle y Calificación del Profesor
def detalle_calificacion_page():
    profesor_id = st.session_state.selected_professor
    profesor = next((p for p in st.session_state.professors if p["id"] == profesor_id), None)
    if profesor is None:
        st.error("Profesor no encontrado.")
        return

    st.title(f"Calificar a {profesor['nombre']}")
    st.image(profesor["foto"], width=150)
    st.write("Departamento:", profesor["departamento"])
    st.write("Por favor, califica a este profesor de 1 a 5 estrellas.")

    # Selección de calificación (1-5 estrellas)
    rating = st.radio("Calificación (estrellas):", [1, 2, 3, 4, 5])
    comentario = st.text_area("Comentario (opcional):")

    if st.button("Enviar Calificación"):
        rating_record = {
            "id_profesor": profesor["id"],
            "estrellas": rating,
            "comentario": comentario,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.ratings.append(rating_record)
        st.success("¡Calificación enviada exitosamente!")
        navigate("Listado de Profesores")

# Página de Estadísticas
def estadisticas_page():
    st.title("Estadísticas de Calificaciones")
    if not st.session_state.ratings:
        st.write("Aún no hay calificaciones.")
        return

    data = []
    for profesor in st.session_state.professors:
        ratings = [r["estrellas"] for r in st.session_state.ratings if r["id_profesor"] == profesor["id"]]
        if ratings:
            promedio = sum(ratings) / len(ratings)
            data.append({
                "Profesor": profesor["nombre"],
                "Departamento": profesor["departamento"],
                "Calificación Promedio": round(promedio, 2),
                "Número de Calificaciones": len(ratings)
            })
    if data:
        st.table(data)
    else:
        st.write("No hay calificaciones para mostrar estadísticas.")

# Página de Ayuda/Soporte
def ayuda_page():
    st.title("Ayuda / Soporte")
    st.write("Si tienes preguntas o necesitas asistencia, por favor contacta al administrador de la plataforma.")
    st.write("Correo de soporte: soporte@upv.es")

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
