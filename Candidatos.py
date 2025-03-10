import streamlit as st
import pandas as pd

# ----- Configuración -----
st.title("📋 Lista de Candidatos")
excel_file = "database/resultados_RRHH.xlsx"  # Ruta del archivo Excel

# ----- Cargar datos -----
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    st.error("❌ No se encontró el archivo Excel")
    st.stop()

# ----- Búsqueda avanzada con st.columns() -----
st.subheader("🔍 Filtrar Candidatos")
col1, col2, col3, col4 = st.columns(4)  # Organizar filtros en 4 columnas

with col1:
    profesion = st.text_input("👔 Profesión")  # Ejemplo: "Desarrollador"

with col2:
    exp_años = st.text_input("📅 Años de Experiencia")  # Búsqueda libre

with col3:
    tecnologias = st.text_input("💻 Tecnologías")  # Búsqueda libre

with col4:
    herramientas = st.text_input("🛠️ Herramientas")  # Búsqueda libre

# Aplicar filtros dinámicos
df_filtrado = df.copy()

if profesion:
    df_filtrado = df_filtrado[df_filtrado["Profesión"].str.contains(profesion, case=False, na=False)]

if exp_años:
    df_filtrado = df_filtrado[df_filtrado["Años de Experiencia"].astype(str).str.contains(exp_años, na=False)]

if tecnologias:
    df_filtrado = df_filtrado[df_filtrado["Tecnologías"].str.contains(tecnologias, case=False, na=False)]

if herramientas:
    df_filtrado = df_filtrado[df_filtrado["Herramientas"].str.contains(herramientas, case=False, na=False)]

# ----- Mostrar y permitir edición del DataFrame -----
st.subheader("📋 Resultados de búsqueda")
edited_df = st.data_editor(
    df_filtrado,
    num_rows="dynamic",  # Permite agregar o eliminar filas
    key="data_editor"
)

# ----- Guardar cambios -----
if st.button("💾 Guardar cambios en el Excel"):
    edited_df.to_excel(excel_file, index=False)
    st.toast("✅ Cambios guardados correctamente")


