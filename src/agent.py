import os
import streamlit as st
from fpdf import FPDF
import sqlite3
from datetime import datetime

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ------------------- Configuración API Key -------------------
# (usa variables de entorno para mayor seguridad)
os.environ["OPENAI_API_KEY"] = "tu_api_key_aqui"

# ------------------- Módulo 1: Diagnóstico de Síntomas -------------------
class DiagnosticoSintomasTool:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

        self.prompt_template = PromptTemplate(
            input_variables=["sintomas"],
            template="""
Eres un asistente médico virtual basado en literatura científica. 
Eres un médico de cabecera que ayuda a los pacientes a entender sus síntomas y brindar recomendaciones lo más precisas posibles. 
Analiza los siguientes síntomas reportados: {sintomas}

- Da posibles enfermedades asociadas.
- Clasifica la urgencia (baja, media, alta).
- Recomienda acción inmediata o cuidado en casa.
            """,
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def obtener_diagnostico(self, sintomas_usuario: str) -> str:
        return self.chain.run(sintomas=sintomas_usuario)

# ------------------- Módulo 2: Primeros Auxilios -------------------
class PrimerosAuxiliosTool:
    heridas_info = { 
        "corte": "Lavar con agua y jabón, presionar para detener el sangrado y cubrir con vendaje limpio.",
        "quemadura": "Enfriar con agua fría durante 10-20 minutos. No aplicar cremas sin indicación médica.",
        "fractura": "Inmovilizar la zona afectada y buscar atención médica inmediata.",
        # ... resto de heridas
    }

    @classmethod
    def obtener_instrucciones(cls, tipo_herida: str) -> str:
        return cls.heridas_info.get(tipo_herida.lower(), "No se encontraron instrucciones para este tipo de herida.")

# ------------------- Módulo 3: Gestor de Triaje -------------------
class GestorDeTriaje:
    sintomas_criticos = ["dolor en el pecho", "dificultad para respirar", "pérdida de conciencia"]

    @classmethod
    def sintomas_faltantes(cls, descripcion_usuario: str):
        preguntas = {}
        for sintoma in cls.sintomas_criticos:
            if sintoma not in descripcion_usuario.lower():
                preguntas[sintoma] = None
        return preguntas

# ------------------- Módulo 4: Generador de Informe PDF -------------------
class GeneradorInformePDF:
    @staticmethod
    def crear_informe(diagnostico, primeros_auxilios, filename="informe_medico.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(0, 0, 210, 297, 'F')

        # Encabezado
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 8, "Clínica Sanea - Informe Médico", ln=True)

        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Fecha: {fecha_actual}", ln=True)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "1. Diagnóstico Inicial", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, diagnostico)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "2. Primeros Auxilios", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, primeros_auxilios)

        pdf.set_font("Arial", "I", 9)
        pdf.cell(0, 7, "Este informe no sustituye atención médica profesional", ln=True, align='C')

        pdf.output(filename)
        return filename

# ------------------- Configuración DB -------------------
def configurar_base_datos():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/datos_medico_virtual.db"))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sintomas TEXT,
            tipo_herida TEXT,
            diagnostico TEXT,
            instrucciones TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def guardar_datos(sintomas, tipo_herida, diagnostico, instrucciones):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/datos_medico_virtual.db"))
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultas (sintomas, tipo_herida, diagnostico, instrucciones)
            VALUES (?, ?, ?, ?)
        """, (sintomas, tipo_herida, diagnostico, instrucciones))
        conn.commit()
    finally:
        conn.close()

# ------------------- Streamlit UI -------------------
def main():
    configurar_base_datos()

    st.title("Asistente Médico Virtual")

    sintomas_usuario = st.text_area("Describe tus síntomas:", "")
    tipo_herida = st.selectbox("Selecciona el tipo de herida:", ["corte", "quemadura", "fractura", "torcedura"])

    if st.button("Obtener Diagnóstico"):
        if sintomas_usuario:
            diagnostico_tool = DiagnosticoSintomasTool()
            diagnostico = diagnostico_tool.obtener_diagnostico(sintomas_usuario)

            instrucciones = PrimerosAuxiliosTool.obtener_instrucciones(tipo_herida)

            st.subheader("Diagnóstico Inicial:")
            st.write(diagnostico)
            st.subheader(f"Instrucciones de Primeros Auxilios para {tipo_herida.capitalize()}:")
            st.write(instrucciones)

            guardar_datos(sintomas_usuario, tipo_herida, diagnostico, instrucciones)

            if st.button("Generar Informe PDF"):
                pdf_path = "../data/informe_medico.pdf"
                GeneradorInformePDF.crear_informe(diagnostico, instrucciones, filename=pdf_path)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Descargar Informe PDF", pdf_file, file_name="informe_medico.pdf")

if __name__ == "__main__":
    main()
