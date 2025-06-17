import os
import openai
import streamlit as st
from fpdf import FPDF
import sqlite3
from datetime import datetime

# Obtenemos la API Key de OpenAI de forma segura
openai.api_key = "tu_api_key_aqui"  # Reemplaza con tu clave de API de OpenAI
# ------------------- Módulo 1: Diagnóstico de Síntomas -------------------
class DiagnosticoSintomasTool:
    @staticmethod
    def obtener_diagnostico(sintomas_usuario):
        prompt = f"""
Eres un asistente médico virtual basado en literatura científica. 
Eres un médico de cabecera que ayuda a los pacientes a entender sus síntomas y brindar recomendaciones lo más precisas posibles. 
Analiza los siguientes síntomas reportados: {sintomas_usuario}

- Da posibles enfermedades asociadas.
- Clasifica la urgencia (baja, media, alta).
- Recomienda acción inmediata o cuidado en casa.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un médico virtual experto en triaje inicial."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response['choices'][0]['message']['content']

# ------------------- Módulo 2: Primeros Auxilios -------------------
class PrimerosAuxiliosTool:
    heridas_info = { #podría gestionarse mediante una BBDD.
        "corte": "Lavar con agua y jabón, presionar para detener el sangrado y cubrir con vendaje limpio.",
        "quemadura": "Enfriar con agua fría durante 10-20 minutos. No aplicar cremas sin indicación médica.",
        "fractura": "Inmovilizar la zona afectada y buscar atención médica inmediata.",
        "torcedura": "Aplicar hielo envuelto en tela durante 15-20 minutos. Elevar la extremidad.",
        "raspon": "Lavar con agua y jabón, aplicar antiséptico y cubrir con una gasa limpia si es necesario.",
        "ampolla": "No reventar. Cubrir con un apósito limpio y seco para proteger la zona.",
        "picadura": "Lavar con agua y jabón, aplicar hielo para reducir la hinchazón y usar crema antihistamínica si es necesario.",
        "mordedura": "Lavar con agua y jabón, aplicar presión si hay sangrado y buscar atención médica si es grave.",
        "hemorragia": "Aplicar presión directa con un paño limpio, elevar la zona afectada y buscar atención médica inmediata.",
        "esguince": "Descansar, aplicar hielo, comprimir con una venda elástica y elevar la extremidad.",
        "quemadura química": "Enjuagar con abundante agua durante al menos 20 minutos y buscar atención médica.",
        "quemadura eléctrica": "Apagar la fuente de electricidad si es seguro, no tocar a la persona directamente y buscar atención médica inmediata.",
        "desgarro muscular": "Aplicar hielo, descansar la zona afectada y evitar movimientos bruscos.",
        "herida punzante": "Lavar con agua y jabón, cubrir con un apósito limpio y buscar atención médica si es profunda.",
        "luxación": "Inmovilizar la articulación en la posición encontrada y buscar atención médica inmediata.",
        "herida infectada": "Lavar con agua y jabón, aplicar antiséptico y buscar atención médica si hay signos de infección.",
        "herida por objeto extraño": "No retirar el objeto, inmovilizar la zona y buscar atención médica inmediata.",
        "herida en la cabeza": "Aplicar presión suave si hay sangrado, mantener a la persona despierta y buscar atención médica.",
        "herida en el ojo": "No frotar ni aplicar presión, enjuagar con agua limpia si es posible y buscar atención médica inmediata.",
        "herida en zonas íntimas": "Lavar con agua tibia y jabón suave, evitar fricción o presión en la zona y buscar atención médica si hay dolor o sangrado.",
        "herida en el abdomen": "Cubrir con un paño limpio y húmedo, evitar presionar y buscar atención médica inmediata.",
        "herida en el pecho": "Aplicar presión suave si hay sangrado, evitar movimientos bruscos y buscar atención médica inmediata.",
        "herida en la espalda": "Limpiar con agua y jabón, cubrir con un apósito limpio y buscar atención médica si es profunda.",
        "herida en las extremidades": "Lavar con agua y jabón, aplicar presión si hay sangrado y cubrir con un vendaje limpio.",
        "herida en las manos": "Lavar con agua y jabón, aplicar antiséptico y cubrir con un apósito limpio.",
        "herida en los pies": "Lavar con agua y jabón, aplicar antiséptico y cubrir con un apósito limpio para evitar infecciones.",
        "herida en el cuello": "Aplicar presión suave si hay sangrado, evitar movimientos bruscos y buscar atención médica inmediata.",
        "herida en la cara": "Lavar con agua y jabón, aplicar antiséptico y cubrir con un apósito limpio si es necesario.",
        "herida en los genitales": "Lavar con agua tibia y jabón suave, evitar fricción o presión en la zona y buscar atención médica si hay dolor, sangrado o inflamación."
    }

    @classmethod
    def obtener_instrucciones(cls, tipo_herida):
        return cls.heridas_info.get(tipo_herida.lower(), "No se encontraron instrucciones para este tipo de herida.")

# ------------------- Módulo 3: Gestor de Triaje -------------------
class GestorDeTriaje:
    sintomas_criticos = ["dolor en el pecho", "dificultad para respirar", "pérdida de conciencia"]

    @classmethod
    def sintomas_faltantes(cls, descripcion_usuario):
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
        # Fondo blanco profesional
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(0, 0, 210, 297, 'F')

        # Encabezado con logo y datos de la clínica
        pdf.image("../images/sanea_logo.jpg", x=10, y=10, w=28)
        pdf.set_xy(45, 12)
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 8, "Clínica Sanea - Informe Médico", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.ln(8)
        pdf.set_draw_color(0, 51, 102)
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

        # Datos del informe
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(40, 8, "Fecha del informe:", 0, 0)
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, fecha_actual, ln=True)
        pdf.ln(2)

        # Sección de diagnóstico
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "1. Diagnóstico Inicial", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(33, 37, 41)
        pdf.multi_cell(0, 8, diagnostico, border=0, align='L')
        pdf.ln(4)

        # Sección de primeros auxilios
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "2. Recomendaciones de Primeros Auxilios", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(33, 37, 41)
        pdf.multi_cell(0, 8, primeros_auxilios, border=0, align='L')
        pdf.ln(4)

        # Recomendaciones generales
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 9, "3. Observaciones Importantes", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(100, 0, 0)
        pdf.multi_cell(0, 7, "Este informe es orientativo y no sustituye la valoración presencial de un profesional sanitario. "
                      "En caso de empeoramiento, síntomas graves o dudas, acuda a su centro médico o llame al 112.", border=0)
        pdf.ln(2)

        # Pie de página profesional
        pdf.set_y(-25)
        pdf.set_font("Arial", "I", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 7, "Informe generado automáticamente por Asistente Médico Virtual | Clínica Sanea", ln=True, align='C')
        pdf.cell(0, 5, "Confidencial - Uso exclusivo del paciente", ln=True, align='C')

        # Guardar el archivo
        pdf.output(filename)
        print(f"✅ Informe generado: {filename}")

# ------------------- Streamlit UI -------------------

# Configuración de la base de datos
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
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        if conn:
            conn.close()

def main():
    # Configurar base de datos
    configurar_base_datos()

    # Estilo de la página
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E3F2FD; /* Azul pastel */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Portada inicial
    if "inicio" not in st.session_state:
        st.session_state["inicio"] = False

    if not st.session_state["inicio"]:
        st.title("Bienvenido al Asistente Médico Virtual")
        st.image("../images/virtual-doctor-online-hospital-online-consultation-doctor-on-smartphone-diagnosis-patient-health-problem-medical-service-and-healthcare-innovation-technology-concept-vector.jpeg", use_container_width=True)  # Imagen ficticia, reemplazar con una real
        if st.button("Comenzar"):
            st.session_state["inicio"] = True
        return

    # Título principal
    st.title("Asistente Médico Virtual")

    # Ingreso de síntomas
    sintomas_usuario = st.text_area("Describe tus síntomas:", "")
    tipo_herida = st.selectbox("Selecciona el tipo de herida:", ["corte", "quemadura", "fractura", "torcedura", "raspon", "ampolla", "picadura", "mordedura", "hemorragia", "esguince", "quemadura química", "quemadura eléctrica", "desgarro muscular", "herida punzante", "luxación", "herida infectada", "herida por objeto extraño", "herida en la cabeza", "herida en el ojo", "herida en zonas íntimas", "herida en el abdomen", "herida en el pecho", "herida en la espalda", "herida en las extremidades", "herida en las manos", "herida en los pies", "herida en el cuello", "herida en la cara", "herida en los genitales"])

    if st.button("Continuar"):
        if not sintomas_usuario:
            st.warning("Por favor, describe tus síntomas antes de continuar.")
        else:
            st.session_state["sintomas_usuario"] = sintomas_usuario
            st.session_state["tipo_herida"] = tipo_herida
            st.session_state["continuar"] = True

    # Botón para reiniciar consulta
    if st.button("Reiniciar Consulta"):
        st.session_state.clear()
        st.experimental_rerun()

    preguntas_extra = GestorDeTriaje.sintomas_faltantes(sintomas_usuario)
    if preguntas_extra:
        st.write("Antes de continuar, responde a estas preguntas:")
        respuestas_actualizadas = {}
        for sintoma, _ in preguntas_extra.items():
            respuesta = st.radio(f"¿Presenta {sintoma}?", ("Sí", "No"), key=f"radio_{sintoma}")
            respuestas_actualizadas[sintoma] = respuesta == "Sí"

        if st.button("Responder y Continuar"):
            st.session_state["preguntas_extra"] = respuestas_actualizadas
            st.success("Respuestas registradas. Puedes continuar.")

    # Paso 2: Obtener diagnóstico
    diagnostico = DiagnosticoSintomasTool.obtener_diagnostico(sintomas_usuario)
    st.subheader("Diagnóstico Inicial:")
    st.write(diagnostico)

    # Mostrar contacto de emergencias si es urgente
    if "alta" in diagnostico.lower():
        st.error("Esta situación puede ser una emergencia. Por favor, contacta al 112 inmediatamente.")
    else:
        st.info("Si necesitas ayuda adicional, puedes contactar al 112.")

    # Paso 3: Obtener instrucciones de primeros auxilios
    instrucciones = PrimerosAuxiliosTool.obtener_instrucciones(tipo_herida)
    st.subheader(f"Instrucciones de Primeros Auxilios para {tipo_herida.capitalize()}:")
    st.write(instrucciones)

    # Guardar datos en la base de datos
    guardar_datos(sintomas_usuario, tipo_herida, diagnostico, instrucciones)

    # Mostrar contacto de emergencias después de las instrucciones
    st.info("Recuerda que puedes contactar al 112 en caso de necesitar asistencia médica urgente.")

    # Paso 4: Generar PDF 
    if st.button("Generar Informe PDF"):
        pdf_path = "../data/informe_medico.pdf"
        GeneradorInformePDF.crear_informe(diagnostico, instrucciones, filename=pdf_path)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Descargar Informe PDF",
                data=pdf_file,
                file_name="informe_medico.pdf",
                mime="application/pdf"
            )
        st.success("Informe generado correctamente. Puedes descargarlo usando el botón de arriba.")

    # Opción para realizar otra consulta
    if st.button("Realizar Otra Consulta"):
        st.session_state.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()