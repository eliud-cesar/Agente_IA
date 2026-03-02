import os
import google.generativeai as genai

class Agent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        # Definimos las herramientas (Tools)
        # Gemini usa los "docstrings" para entender qué hace cada función

        # FUNCON DE LISTAR LOS ARCHIVOS
        def list_files_in_dir(directory: str = "."):
            """Lista los archivos que existen en un directorio dado."""
            print(f"  ⚙️ Herramienta llamada: list_files_in_dir ({directory})")
            try:
                return {"files": os.listdir(directory)}
            except Exception as e:
                return {"error": str(e)}

        # FUNCION DE LEER EL CONTENIDO DE UN ARCHIVO
        def read_file(path: str):
            """Lee el contenido de un archivo en una ruta especificada."""
            print(f"  ⚙️ Herramienta llamada: read_file ({path})")
            try:
                with open(path, encoding="utf-8") as f:
                    return {"content": f.read()}
            except Exception as e:
                return {"error": f"Error al leer el archivo {path}"}

        # FUNCION PARA REEMPLAZAR EL NOMBRE DEL ARCHIVO Y/O CREAR
        def edit_file(path: str, new_text: str, prev_text: str = None):
            """Edita un archivo reemplazando prev_text por new_text. Crea el archivo si no existe."""
            print(f"  ⚙️ Herramienta llamada: edit_file ({path})")
            try:
                existed = os.path.exists(path)
                if existed and prev_text:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if prev_text not in content:
                        return {"error": f"Texto no encontrado en {path}"}
                    content = content.replace(prev_text, new_text)
                else:
                    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
                    content = new_text
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                return {"status": f"Archivo {path} {'editado' if existed and prev_text else 'creado'} exitosamente"}
            except Exception as e:
                return {"error": str(e)}

        # Configuramos el modelo con las herramientas
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            tools=[list_files_in_dir, read_file, edit_file],
            system_instruction="Eres un asistente útil que habla español y eres muy conciso con tus respuestas."
        )
        
        # Gemini maneja el historial automáticamente si usamos start_chat
        # enable_automatic_function_calling=True hace todo el bucle de 'process_response' por ti
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def ask(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text