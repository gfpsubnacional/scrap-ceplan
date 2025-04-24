import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from scraper import scrape_ceplan  # Importa tu función de scraping

def ejecutar_scraping():
    # Obtén los parámetros de la interfaz
    gobierno_regional = entrada_gobierno.get()
    categoria_presupuestal = entrada_categoria.get()

    try:
        # Ejecutar el scraping con los parámetros proporcionados
        resultado = scrape_ceplan(gobierno_regional, categoria_presupuestal)

        # Si se obtiene un resultado válido, convertirlo a CSV
        if resultado is not None:
            guardar_como_csv(resultado)
        else:
            messagebox.showerror("Error", "No se pudieron obtener resultados del scraping.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar el scraping: {str(e)}")

def guardar_como_csv(result):
    # Convertir el resultado en un DataFrame
    df = pd.DataFrame(result)
    
    # Pedir al usuario que seleccione una ubicación para guardar el archivo CSV
    archivo_guardado = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        initialfile="resultados_scraping.csv"  # Nombre predeterminado del archivo
    )
    
    if archivo_guardado:
        # Guardar el DataFrame como un archivo CSV en la ubicación elegida
        try:
            df.to_csv(archivo_guardado, index=False)
            messagebox.showinfo("Éxito", f"El archivo CSV ha sido guardado en: {archivo_guardado}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo CSV: {str(e)}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Scraping")
ventana.geometry("500x300")
ventana.config(bg="#f0f0f0")

# Etiquetas y campos de entrada
etiqueta_gobierno = ttk.Label(ventana, text="Gobierno Regional:", font=("Arial", 12))
etiqueta_gobierno.pack(pady=10)
entrada_gobierno = ttk.Entry(ventana, font=("Arial", 12), width=40)
entrada_gobierno.pack(pady=5)

etiqueta_categoria = ttk.Label(ventana, text="Categoría Presupuestal:", font=("Arial", 12))
etiqueta_categoria.pack(pady=10)
entrada_categoria = ttk.Entry(ventana, font=("Arial", 12), width=40)
entrada_categoria.pack(pady=5)

# Botón para ejecutar el scraping
boton_scrapear = ttk.Button(ventana, text="Ejecutar Scraping", command=ejecutar_scraping, width=20)
boton_scrapear.pack(pady=20)

# Iniciar la interfaz
ventana.mainloop()
