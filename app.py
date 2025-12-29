import os
import shutil
import pandas as pd
from datetime import datetime

# 📁 Rutas
carpeta_origen = 'A_PROCESAR'
carpeta_destino = 'PROCESADOS'
archivo_excel = 'BASE_DE_DATOS.xlsx'

# 🧾 Lista para nuevos datos
nuevos_datos = []
txt_encontrado = False  # 🏁 Bandera para detectar archivos .txt

# 🔍 Recorre todos los archivos .txt
for nombre_archivo in os.listdir(carpeta_origen):
    if nombre_archivo.endswith('.txt'):
        txt_encontrado = True
        ruta_completa = os.path.join(carpeta_origen, nombre_archivo)

        # 📖 Lee el contenido del archivo
        with open(ruta_completa, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        # ➕ Agrega a la lista
        nuevos_datos.append({'Archivo': nombre_archivo, 'Contenido': contenido})

        # 🕒 Genera timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # ✏️ Renombra y mueve el archivo
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nuevo_nombre = f'{timestamp}_{nombre_base}.txt'
        nueva_ruta = os.path.join(carpeta_destino, nuevo_nombre)
        shutil.move(ruta_completa, nueva_ruta)

# 📊 Si hubo archivos, actualiza el Excel
if txt_encontrado:
    if os.path.exists(archivo_excel):
        df_existente = pd.read_excel(archivo_excel)
        df_nuevo = pd.DataFrame(nuevos_datos)
        df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_actualizado = pd.DataFrame(nuevos_datos)

    # 💾 Guarda el Excel actualizado
    df_actualizado.to_excel(archivo_excel, index=False)
    print("✅ Datos agregados y archivos renombrados con fecha.")
else:
    print("⚠️ No existe archivo .txt en la carpeta.")
