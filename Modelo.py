import streamlit as st
import pandas as pd
import time  # Para simular procesamiento

# ----- Configuración -----
st.title("📄 Extracción de Datos desde PDF")

# Subir múltiples archivos PDF
uploaded_files = st.file_uploader("📂 Selecciona uno o varios archivos PDF", type=["pdf"], accept_multiple_files=True)

# Lista para almacenar datos extraídos (simulados)
data_simulada = []

# Procesar archivos si se suben
if uploaded_files:
    with st.spinner("🔍 Procesando archivos..."):
        time.sleep(2)  # Simulación de carga

    for file in uploaded_files:
        # Simulación de extracción de datos
        datos_extraidos = {
            "Archivo": file.name,
            "Nombre": "Juan Pérez",
            "Profesión": "Ingeniero de Datos",
            "Años de Experiencia": 5,
            "Tecnologías": "Python, SQL, Spark",
            "Herramientas": "Airflow, Docker"
        }
        data_simulada.append(datos_extraidos)

    # Convertir a DataFrame para mostrar
    df = pd.DataFrame(data_simulada)
    st.subheader("📋 Datos Extraídos (Simulación)")
    st.dataframe(df)

    # Opción para descargar los datos simulados como CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV", data=csv, file_name="datos_extraidos.csv", mime="text/csv")
