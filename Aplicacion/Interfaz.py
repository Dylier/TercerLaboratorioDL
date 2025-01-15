import tkinter as tk
from tkinter import messagebox
from CombinatoriaBinaria import crearCombinatoria
import metodoQuineMcCluskey as mc
import ExpresionLogica as ex
import creadorArduino as ca

def procesar_expresion(expresion):
    partes = expresion.split('/')
    if len(partes) == 2:
        return partes[0].strip(), partes[1].strip()
    return expresion, "1"

def ejecutar_codigo():
    try:
        expresion = entry_expresion.get()
        denominador, divisor = procesar_expresion(expresion)
        variables = entry_variables.get().split(',')
        bits = int(entry_bits.get())
        exportar_excel = var_excel.get()
        nombre = entry_nombre.get()

        # Ejecutar las funciones con los parámetros ingresados
        print(expresion, denominador, variables, bits, exportar_excel, nombre)
        df = crearCombinatoria(denominador, divisor, variables, bits, exportar_excel, nombre)
        ex.encontrar_expresiones_logicas(df, variables, bits, f"{nombre}_no_simplificado", False)
        # exp_lgoicas = ex.encontrar_expresiones_logicas(df, variables, bits, f"{nombre}_simplificado", True)
        exp_lgoicas = ex.quine_mccluskey_con_canonicas(df, variables, bits, "SIMPLIFICADO", mc.quine_mccluskey(df, variables, bits))
        ca.crear_archivo_arduino(nombre, nombre, variables, exp_lgoicas, bits)
        messagebox.showinfo("Éxito", "Operación completada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz para Quine McCluskey")

# Crear widgets
label_expresion = tk.Label(root, text="Expresión (denominador/divisor):")
label_expresion.grid(row=0, column=0, padx=5, pady=5)
entry_expresion = tk.Entry(root, width=30)
entry_expresion.grid(row=0, column=1, padx=5, pady=5)

label_variables = tk.Label(root, text="Variables (separadas por coma):")
label_variables.grid(row=1, column=0, padx=5, pady=5)
entry_variables = tk.Entry(root, width=30)
entry_variables.grid(row=1, column=1, padx=5, pady=5)

label_bits = tk.Label(root, text="bits:")
label_bits.grid(row=2, column=0, padx=5, pady=5)
entry_bits = tk.Entry(root, width=30)
entry_bits.grid(row=2, column=1, padx=5, pady=5)

var_excel = tk.BooleanVar()
checkbox_excel = tk.Checkbutton(root, text="Exportar tabla de verdad", variable=var_excel)
checkbox_excel.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

label_nombre = tk.Label(root, text="Nombre del archivo:")
label_nombre.grid(row=4, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root, width=30)
entry_nombre.grid(row=4, column=1, padx=5, pady=5)

btn_ejecutar = tk.Button(root, text="Ejecutar", command=ejecutar_codigo)
btn_ejecutar.grid(row=5, column=0, columnspan=2, pady=10)

# Iniciar el loop principal
root.mainloop()
