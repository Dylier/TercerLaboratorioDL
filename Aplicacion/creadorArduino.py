import os

def crear_archivo_arduino(nombre_carpeta, nombre_archivo, nombre_entradas, expresiones, bits):
    """
    Crea un archivo .ino con las expresiones logicas y entradas especificadas.
    """

    entradas = []
    for ent in nombre_entradas:
        for bit in range(bits):
            entradas.append(f"{ent}_{bit}")

    # Crear la carpeta si no existe
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    
    # Ruta del archivo
    ruta_archivo = os.path.join(nombre_carpeta, nombre_archivo + ".ino")
    
    # Generar el código Arduino
    codigo_arduino = generar_codigo_arduino(entradas, expresiones)
    
    # Guardar el archivo .ino
    with open(ruta_archivo, "w") as archivo:
        archivo.write(codigo_arduino)
    
    print(f"Archivo generado: {ruta_archivo}")


def generar_codigo_arduino(entradas, expresiones):
    """
    Genera el código Arduino para manejar entradas, evaluar expresiones y mostrar resultados.
    """
    # Encabezado del código Arduino
    codigo = "// Código generado automaticamente\n"
    codigo += "#include <Arduino.h>\n\n"
    
    # Definir entradas y salidas
    codigo += "// Declaracion de variables\n"
    for entrada in entradas:
        codigo += f"bool {entrada}; // Entrada\n"
    for salida in expresiones.keys():
        codigo += f"bool {salida}; // Salida\n"
    
    # Setup
    codigo += "\nvoid setup() {\n"
    codigo += "  Serial.begin(9600);\n"
    codigo += "  Serial.println(\"Programa iniciado. Ingresa los valores para cada entrada (0 o 1).\");\n"
    codigo += "}\n\n"
    
    # Loop principal
    codigo += "void loop() {\n"
    codigo += "  // Leer entradas desde el monitor serial\n"
    for entrada in entradas:
        codigo += f"  {entrada} = obtenerValor(\"{entrada}\");\n"
    
    # Evaluar las expresiones
    codigo += "\n  // Evaluar expresiones lógicas\n"
    for salida, expresion in expresiones.items():
        codigo += f"  {salida} = {expresion};\n"
    
    # Imprimir resultados
    codigo += "\n  // Imprimir resultados\n"
    codigo += "  Serial.println(\"Resultados:\");\n"
    for salida in expresiones.keys():
        codigo += f"  Serial.print(\"{salida} = \"); Serial.println({salida});\n"
    
    codigo += "\n  delay(5000);\n"
    codigo += "}\n\n"
    
    # Función auxiliar para obtener valores
    codigo += """
bool obtenerValor(String nombre) {
  while (true) {
    Serial.print(nombre + " = ");
    while (!Serial.available());
    char input = Serial.read();
    if (input == '0') return false;
    if (input == '1') return true;
    Serial.println("Entrada inválida. Por favor ingresa 0 o 1.");
  }
}
"""
    return codigo


# Ejemplo de uso
if __name__ == "__main__":
    # Entradas proporcionadas
    entradas = ["A_0", "A_1", "B_0", "B_1"]
    
    # Expresiones lógicas proporcionadas
    expresiones = {
        "SC": "0",
        "SR": "(A_0 && A_1 && B_0 && !B_1) || (A_0 && B_0 && B_1 && !A_1)",
        "I": "(B_0 && !A_0 && !A_1) || (B_1 && !A_0 && !A_1) || (!A_0 && !A_1 && !B_0) || (!A_0 && !A_1 && !B_1)",
        "C_0": "(A_1 && B_0 && B_1) || (A_1 && B_0 && !A_0) || (A_1 && B_1 && !A_0) || (A_0 && !B_0 && !B_1) || (A_1 && !A_0 && !B_0) || (A_1 && !A_0 && !B_1) || (A_1 && !B_0 && !B_1)",
        "R_0": "(A_0 && B_1 && !A_1) || (A_0 && B_1 && !B_0) || (A_0 && A_1 && B_0 && !B_1)"
    }
    
    # Crear el archivo .ino
    crear_archivo_arduino("ProyectoArduino", "ExpresionesLogicas", entradas, expresiones)
