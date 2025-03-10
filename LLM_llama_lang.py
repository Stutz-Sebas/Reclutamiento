import fitz  # PyMuPDF para leer PDFs
import pandas as pd
from transformers import pipeline  # Para cargar el modelo local de Hugging Face
import re  # Para extraer datos con expresiones regulares

# ==============================
# 📌 Cargar el modelo local de Mistral desde Hugging Face
# ==============================
MODEL_PATH = "./mistral-7b-instruct"  # Ajusta la ruta a donde guardaste el modelo
print("🚀 Cargando modelo local de Mistral...")
mistral_pipeline = pipeline(
    "text-generation",
    model=MODEL_PATH,
    device=0,  # -1 para CPU, 0 para GPU si tienes una disponible

)
print("✅ Modelo cargado correctamente.")

# ==============================
# 📌 Función para extraer texto de PDFs
# ==============================
def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF."""
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error al leer PDF {pdf_path}: {e}")
        return ""

# ==============================
# 📌 Función para procesar el texto con el modelo local
# ==============================
def extract_info_with_local_model(text):
    """Procesa el texto con el modelo Mistral local para extraer información clave."""
    if not text:
        return "❌ Error: Texto vacío."

    prompt = f"""
    Extrae la siguiente información del texto del CV y organízala claramente en este formato exacto:

    - Nombre completo: [nombre]
    - Profesión, especialidad o cargo: [profesión]
    - Años de experiencia: [años]
    - Tecnologías que usa la persona: [tecnologías]
    - Herramientas que usa la persona: [herramientas]
    - Ciudad de residencia: [ciudad]

    Si no encuentras alguna información, usa "No especificado".

    **Texto del CV:**  
    {text[:2000]}  # Limitamos a 2000 caracteres para optimizar

    **Respuesta:**  
    """

    try:
        # Generar respuesta con el pipeline de transformers
        response = mistral_pipeline(prompt, max_length=2500, truncation=True)[0]["generated_text"]
        # Eliminar el prompt del inicio de la respuesta
        response = response[len(prompt):].strip()
        return response
    except Exception as e:
        print(f"❌ Error al procesar texto con el modelo: {e}")
        return "❌ Error al procesar el CV."

# ==============================
# 📌 Función para organizar la respuesta en columnas
# ==============================
def parse_response(response_text):
    """Convierte la respuesta del modelo en un diccionario estructurado."""
    try:
        parsed_data = {
            "Nombre Completo": re.search(r"Nombre completo:\s*(.*)", response_text).group(1).strip(),
            "Profesión": re.search(r"Profesión.*?:\s*(.*)", response_text).group(1).strip(),
            "Años de Experiencia": re.search(r"Años de experiencia:\s*(.*)", response_text).group(1).strip(),
            "Tecnologías": re.search(r"Tecnologías.*?:\s*(.*)", response_text).group(1).strip(),
            "Herramientas": re.search(r"Herramientas.*?:\s*(.*)", response_text).group(1).strip(),
            "Ciudad de Residencia": re.search(r"Ciudad de residencia:\s*(.*)", response_text).group(1).strip(),
        }
        return parsed_data
    except AttributeError:
        return {
            "Nombre Completo": "Error al procesar",
            "Profesión": "Error al procesar",
            "Años de Experiencia": "Error al procesar",
            "Tecnologías": "Error al procesar",
            "Herramientas": "Error al procesar",
            "Ciudad de Residencia": "Error al procesar",
        }

# ==============================
# 📌 Ruta de PDFs
# ==============================
pdf_files = [
    "./cvs/cv1.pdf",
    "./cvs/cv2.pdf",
    "./cvs/cv3.pdf",
    "./cvs/cv4.pdf",
    "./cvs/cv5.pdf"
]

# ==============================
# 📌 Procesar los PDFs y almacenar los resultados
# ==============================
data = []
for pdf in pdf_files:
    try:
        text = extract_text_from_pdf(pdf)[:2000]  # Limitar texto a 2000 caracteres
        raw_response = extract_info_with_local_model(text)  # Obtener respuesta en lenguaje natural
        structured_response = parse_response(raw_response)  # Convertir en diccionario estructurado
        print(f"\n📢 Respuesta generada para {pdf}:\n{structured_response}\n")  # Debug
        data.append(structured_response)
    except Exception as e:
        print(f"❌ Error procesando {pdf}: {e}")
        data.append({
            "Nombre Completo": "Error",
            "Profesión": "Error",
            "Años de Experiencia": "Error",
            "Tecnologías": "Error",
            "Herramientas": "Error",
            "Ciudad de Residencia": "Error"
        })

# ==============================
# 📌 Crear DataFrame con los resultados
# ==============================
df = pd.DataFrame(data, columns=["Nombre Completo", "Profesión", "Años de Experiencia", "Tecnologías", "Herramientas", "Ciudad de Residencia"])

# ==============================
# 📌 Mostrar DataFrame con los datos extraídos
# ==============================
print("\n✅ Resultados extraídos:\n")
print(df)


# ==============================
# 📌 Exportar los datos a un excel y ubicarlo en una posición especifica con acceso a RRHH
# ==============================
# Continuara....