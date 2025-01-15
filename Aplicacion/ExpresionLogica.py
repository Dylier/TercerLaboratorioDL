import metodoQuineMcCluskey as mc
from concurrent.futures import ProcessPoolExecutor
from sympy import symbols, Not, And, Or

def calcular_expresion_logica(args):
    df, salida, entradas, simplificado = args
    filtro = df[df[salida] == 1]
    simbolos_variables = {variable: symbols(variable) for variable in entradas}
    
    expresiones = []
    for _, fila in filtro.iterrows():
        expresion = [
            simbolos_variables[variable] if fila[variable] == 1 else Not(simbolos_variables[variable])
            for variable in entradas
        ]
        expresiones.append(And(*expresion))
    if simplificado:
        expr_final = Or(*expresiones).simplify()
    else: 
        expr_final = Or(*expresiones)
    return salida, expr_final

def encontrar_expresiones_logicas(df, variables, bits, nombre, simplificado):
    entradas = [f"{var}_{bit}" for var in variables for bit in range(bits)]
    salidas = list(df.columns.values)[len(entradas)+2:]
    salidas.remove('C') if "C_1" in salidas else None
    salidas.remove('R') if "R_1" in salidas else None
    
    expresiones_logicas = {}
    
    with ProcessPoolExecutor() as executor:
        # Preparamos las tuplas con los argumentos para enviar al map
        argumentos = [(df, salida, entradas, simplificado) for salida in salidas]
        
        # Ejecutamos calcular_expresion_logica en paralelo
        resultados = executor.map(calcular_expresion_logica, argumentos)
        
        for salida, expr_final in resultados:
            expresiones_logicas[salida] = expr_final
    try:
        with open(f"./Logico/{nombre}.txt", "w") as f:
            t = ""
            for salida in salidas:
                t += f"{salida}={expresiones_logicas[salida]};\n"
            f.write(t)
    except:
         with open(f"./{nombre}.txt", "w") as f:
            t = ""
            for salida in salidas:
                t += f"{salida}={expresiones_logicas[salida]};\n"
            f.write(t)
    
    return expresiones_logicas

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Union
from concurrent.futures import ProcessPoolExecutor
from sympy import symbols, Not, And, Or

# [Mantener todas las funciones anteriores sin cambios hasta quine_mccluskey()]

def convertir_termino_a_expresion(termino: str, variables: List[str], 
                                bits_por_var: int) -> List[Union[symbols, Not]]:
    """Convierte un término binario en una expresión lógica.
    
    Por ejemplo, para el término '101_' con variables ['A', 'B'] y 2 bits:
    - Crea símbolos A_1, A_2, B_1, B_2
    - Convierte '1' en el símbolo directo
    - Convierte '0' en la negación del símbolo
    - Ignora '_' (no incluye ese término)
    
    Args:
        termino: String binario con posibles guiones bajos
        variables: Lista de nombres de variables
        bits_por_var: Cantidad de bits por variable
    
    Returns:
        Lista de expresiones simbólicas (símbolos o negaciones)
    """
    simbolos = []
    nombre_columnas = []
    
    # Generar nombres de columnas
    for var in variables:
        for bit in range(bits_por_var):
            nombre_columnas.append(f"{var}_{bit}")
    
    # Crear símbolos para cada bit
    for col, bit in zip(nombre_columnas, termino):
        if bit != '_':
            sym = symbols(col)
            simbolos.append(sym if bit == '1' else Not(sym))
            
    return simbolos

def generar_expresion_canonica(df_simplificado: pd.DataFrame, 
                             variables: List[str], 
                             bits_por_var: int) -> str:
    """Genera la expresión canónica a partir de un DataFrame simplificado.
    
    Toma cada término del DataFrame y lo convierte en una expresión lógica.
    Por ejemplo, si tenemos:
    minterms  binario
    1,2       _110
    4         1001
    
    Generará: (A_1 & B_0 & B_1) | (A_0 & !A_1 & !B_0 & B_1)
    
    Args:
        df_simplificado: DataFrame con términos minimizados
        variables: Lista de nombres de variables
        bits_por_var: Cantidad de bits por variable
    
    Returns:
        Expresión lógica simplificada como string
    """
    if df_simplificado.empty:
        return "0"  # Retorna 0 lógico si no hay términos
        
    terminos = []
    for _, fila in df_simplificado.iterrows():
        simbolos = convertir_termino_a_expresion(
            fila['binario'], variables, bits_por_var)
        if simbolos:
            terminos.append(And(*simbolos))
    
    if not terminos:
        return "0"
        
    return str(Or(*terminos))

def procesar_expresiones_canonicas(args: Tuple) -> Tuple[str, str]:
    """Procesa un DataFrame simplificado para generar su expresión canónica.
    
    Esta función está diseñada para ser usada con ProcessPoolExecutor.
    
    Args:
        args: Tupla con (df_simplificado, nombre_salida, variables, bits_por_var)
    
    Returns:
        Tupla (nombre_salida, expresión_canónica)
    """
    df_simplificado, nombre_salida, variables, bits_por_var = args
    expresion = generar_expresion_canonica(df_simplificado, variables, bits_por_var)
    return nombre_salida, expresion

def quine_mccluskey_con_canonicas(df, variables, bits, nombre_archivo, resultados_qm):
    """Versión extendida que incluye la generación de expresiones canónicas.
    
    Esta función realiza el proceso completo:
    1. Ejecuta el algoritmo de Quine-McCluskey
    2. Convierte los resultados en expresiones canónicas
    3. Opcionalmente guarda las expresiones en un archivo
    
    Args:
        df: DataFrame con la tabla de verdad
        variables: Lista de nombres de variables
        bits_por_var: Cantidad de bits por variable
        nombre_archivo: Nombre del archivo para guardar resultados (opcional)
    
    Returns:
        Diccionario con las expresiones canónicas por cada salida
    """    
    #encontrar_expresiones_logicas(df, variables, bits, "SIMPLIFICADO", True)
    salidas = mc.identificar_salidas_interes(df)
    argumentos = [(df_result, salida, variables, bits) 
                 for df_result, salida in zip(resultados_qm, salidas)]
    
    expresiones_canonicas = {}
    with ProcessPoolExecutor() as executor:
        resultados = executor.map(procesar_expresiones_canonicas, argumentos)
        for salida, expresion in resultados:
            expresiones_canonicas[salida] = expresion
    
    # Guardar en archivo si se especificó nombre
    if nombre_archivo:
        with open(f"./Logico/{nombre_archivo}.txt", "w") as f:
            contenido = ""
            for salida, expr in expresiones_canonicas.items():
                contenido += f"{salida}={expr};\n"
            f.write(contenido)
    return expresiones_canonicas