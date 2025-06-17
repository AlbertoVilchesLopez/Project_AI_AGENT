# test_clave.py
import os
from dotenv import load_dotenv

print("--- INICIANDO TEST DE CLAVE API ---")

# Construir la ruta al archivo .env (subiendo un nivel desde 'src')
try:
    ruta_script = os.path.abspath(__file__)
    directorio_src = os.path.dirname(ruta_script)
    directorio_proyecto = os.path.dirname(directorio_src)
    ruta_env = os.path.join(directorio_proyecto, '.env')

    print(f"Ruta del script de prueba: {ruta_script}")
    print(f"Buscando archivo .env en: {ruta_env}")

    if os.path.exists(ruta_env):
        print("\nRESULTADO: ¡Archivo .env encontrado!")
        load_dotenv(dotenv_path=ruta_env)
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            print("RESULTADO: ¡Clave API cargada exitosamente!")
            # Por seguridad, solo mostramos los primeros y últimos caracteres
            print(f"La clave empieza con '{api_key[:4]}' y termina con '{api_key[-4:]}'.")
        else:
            print("RESULTADO: ERROR. Se encontró el archivo .env, pero no contiene la variable 'OPENAI_API_KEY' o está vacía.")
    else:
        print("\nRESULTADO: ERROR. No se encontró el archivo .env en la ruta esperada.")

except Exception as e:
    print(f"Ocurrió un error inesperado durante el test: {e}")

print("\n--- FIN DEL TEST ---")