import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Union
from concurrent.futures import ProcessPoolExecutor
import quine as mc
from sympy import symbols, Not, And, Or

def convertir_termino_a_expresion(termino: str, variables: List[str], bits_por_var: int) -> List[Union[symbols, Not]]:
    simbolos = []
    nombre_columnas = []
    
    for var in variables:
        for bit in range(bits_por_var):
            nombre_columnas.append(f"{var}_{bit}")
    
    for col, bit in zip(nombre_columnas, termino):
        if bit != '_':
            sym = symbols(col)
            simbolos.append(sym if bit == '1' else Not(sym))
            
    return simbolos

def generar_expresion_canonica(df_simplificado: pd.DataFrame, variables: List[str], bits_por_var: int) -> str:
    if df_simplificado.empty:
        return "0"
        
    terminos = []
    for _, fila in df_simplificado.iterrows():
        simbolos = convertir_termino_a_expresion(fila['binario'], variables, bits_por_var)
        if simbolos:
            terminos.append(And(*simbolos))
    
    if not terminos:
        return "0"
        
    return str(Or(*terminos))

def procesar_expresiones_canonicas(args: Tuple) -> Tuple[str, str]:
    df_simplificado, nombre_salida, variables, bits_por_var = args
    expresion = generar_expresion_canonica(df_simplificado, variables, bits_por_var)
    return nombre_salida, expresion

def quine_mccluskey_con_canonicas(df, variables, bits, nombre_archivo, resultados_qm):
    salidas = mc.identificar_salidas_interes(df)
    argumentos = [(df_result, salida, variables, bits) 
                 for df_result, salida in zip(resultados_qm, salidas)]
    
    expresiones_canonicas = {}
    with ProcessPoolExecutor() as executor:
        resultados = executor.map(procesar_expresiones_canonicas, argumentos)
        for salida, expresion in resultados:
            expresiones_canonicas[salida] = expresion
            print(f"Expresión lógica para {salida}: {expresion}")  # Imprimir la expresión lógica
    
    if nombre_archivo:
        with open(f"./Logico/{nombre_archivo}.txt", "w") as f:
            contenido = ""
            for salida, expr in expresiones_canonicas.items():
                contenido += f"{salida}={expr};\n"
            f.write(contenido)
    
    return expresiones_canonicas
