import os
import openai
import streamlit as st
from fpdf import FPDF

# Configura tu API Key de OpenAI de forma segura
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    heridas_info = {
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
        preguntas = []
        respuestas = {}
        for sintoma in cls.sintomas_criticos:
            if sintoma not in descripcion_usuario.lower():
                respuesta = input(f"¿Presenta {sintoma}? (sí/no): ").strip().lower()
                while respuesta not in ["sí", "si", "no"]:
                    print("Por favor, responde con 'sí' o 'no'.")
                    respuesta = input(f"¿Presenta {sintoma}? (sí/no): ").strip().lower()
                respuestas[sintoma] = respuesta in ["sí", "si"]
        return respuestas

# ------------------- Módulo 4: Generador de Informe PDF -------------------
class GeneradorInformePDF:
    @staticmethod
    def crear_informe(diagnostico, primeros_auxilios, filename="informe_medico.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título del informe
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, txt="Informe Médico Inicial", ln=True, align='C')
        pdf.ln(10)

        # Sección de diagnóstico
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, txt="Diagnóstico Inicial:", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, diagnostico, border=1, align='L')
        pdf.ln(10)

        # Sección de primeros auxilios
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, txt="Recomendaciones de Primeros Auxilios:", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, primeros_auxilios, border=1, align='L')
        pdf.ln(10)

        # Pie de página
        pdf.set_font("Arial", size=10)
        pdf.set_y(-30)
        pdf.cell(0, 10, txt="Este informe es generado automáticamente y no sustituye una consulta médica profesional.", ln=True, align='C')

        # Guardar el archivo
        pdf.output(filename)
        print(f"✅ Informe generado: {filename}")

# ------------------- Streamlit UI -------------------

def main():
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

    # Paso 1: Verificar síntomas críticos
    if sintomas_usuario:
        preguntas_extra = GestorDeTriaje.sintomas_faltantes(sintomas_usuario)
        if preguntas_extra:
            st.write("Antes de continuar, responde a estas preguntas:")
            respuestas_actualizadas = {}
            for sintoma, presente in preguntas_extra.items():
                respuesta = st.radio(f"¿Presenta {sintoma}?", ("Sí", "No"), key=f"radio_{sintoma}")
                respuestas_actualizadas[sintoma] = respuesta == "Sí"

            if st.button("Responder y Continuar"):
                st.session_state["preguntas_extra"] = respuestas_actualizadas
                st.success("Respuestas registradas. Puedes continuar.")

        # Paso 2: Obtener diagnóstico
        diagnostico = DiagnosticoSintomasTool.obtener_diagnostico(sintomas_usuario)
        st.subheader("Diagnóstico Inicial:")
        st.write(diagnostico)

        # Paso 3: Obtener instrucciones de primeros auxilios
        instrucciones = PrimerosAuxiliosTool.obtener_instrucciones(tipo_herida)
        st.subheader(f"Instrucciones de Primeros Auxilios para {tipo_herida.capitalize()}:")
        st.write(instrucciones)

        # Paso 4: Generar PDF
        if st.button("Generar Informe PDF"):
            GeneradorInformePDF.crear_informe(diagnostico, instrucciones, filename="informe_medico.pdf")
            with open("informe_medico.pdf", "rb") as pdf_file:
                st.download_button(
                    label="Descargar Informe PDF",
                    data=pdf_file,
                    file_name="informe_medico.pdf",
                    mime="application/pdf"
                )
            st.success("Informe generado correctamente. Puedes descargarlo usando el botón de arriba.")

if __name__ == "__main__":
    main()
