import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import time as t

def guardar_en_archivo(texto: str, nombre_archivo: str = "resultado_1.txt"):
    with open(nombre_archivo, "a") as archivo:
        archivo.write(texto + "\n")

def generar_columnas_entrada(variables: List[str], bits_por_var: int) -> List[str]:
    columnas = []
    for var in variables:
        for bit in range(bits_por_var):
            columnas.append(f"{var}_{bit}")
    return columnas

def contar_unos_en_fila(fila: pd.Series, columnas_entrada: List[str]) -> int:
    return sum(fila[columnas_entrada])

def convertir_a_binario(fila: pd.Series, columnas_entrada: List[str]) -> str:
    return ''.join(str(int(fila[col])) for col in columnas_entrada)

def encontrar_diferencia_un_bit(bin1: str, bin2: str) -> Tuple[bool, str]:
    if len(bin1) != len(bin2):
        return False, ''
        
    diferencias = 0
    resultado = ''
    
    for i, (b1, b2) in enumerate(zip(bin1, bin2)):
        if b1 != b2:
            diferencias += 1
            resultado += '_'
        else:
            resultado += b1
            
        if diferencias > 1:
            return False, ''
            
    return diferencias == 1, resultado

def identificar_salidas_interes(df: pd.DataFrame) -> List[str]:
    salidas = []
    for col in df.columns:
        if col in ["SC", "SR", "I"] or "C_" in col or "R_" in col:
            salidas.append(col)
    return salidas

def preparar_grupos_iniciales(df: pd.DataFrame, columna_salida: str, 
                            columnas_entrada: List[str]) -> pd.DataFrame:
    filtrado = df[df[columna_salida] == 1].copy()
    
    filtrado['minterms'] = filtrado.index.astype(str)
    filtrado['cant_unos'] = filtrado.apply(
        lambda row: contar_unos_en_fila(row, columnas_entrada), axis=1)
    filtrado['binario'] = filtrado.apply(
        lambda row: convertir_a_binario(row, columnas_entrada), axis=1)
    
    return filtrado.sort_values('cant_unos')

def simplificar_grupos(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) <= 1:
        return pd.DataFrame(columns=['minterms', 'binario'])
        
    simplificados = []
    usados = set()
    
    guardar_en_archivo("\nComparaciones entre términos:")
    
    for i, fila1 in df.iterrows():
        for j, fila2 in df.iterrows():
            if i >= j:
                continue
                
            if abs(fila1['cant_unos'] - fila2['cant_unos']) > 1:
                continue
                
            combinable, combinado = encontrar_diferencia_un_bit(
                fila1['binario'], fila2['binario'])
            
            guardar_en_archivo(f"Comparando {fila1['binario']} ({fila1['minterms']}) con {fila2['binario']} ({fila2['minterms']})")
            
            if combinable:
                guardar_en_archivo(f" -> Se pueden agrupar: {fila1['binario']} y {fila2['binario']} -> {combinado}")
                usados.add(fila1['minterms'])
                usados.add(fila2['minterms'])
                nuevos_minterms = ','.join(sorted([fila1['minterms'], fila2['minterms']]))
                simplificados.append({
                    'minterms': nuevos_minterms,
                    'binario': combinado
                })
            else:
                guardar_en_archivo(" -> No se pueden agrupar")
    
    for _, fila in df.iterrows():
        if fila['minterms'] not in usados:
            simplificados.append({
                'minterms': fila['minterms'],
                'binario': fila['binario']
            })
    
    if not simplificados:
        return pd.DataFrame(columns=['minterms', 'binario'])
        
    resultado = pd.DataFrame(simplificados).drop_duplicates()
    if 'cant_unos' not in resultado.columns:
        resultado['cant_unos'] = resultado['binario'].apply(lambda x: x.count('1'))
        
    return resultado.sort_values('cant_unos')

def quine_mccluskey(df: pd.DataFrame, variables: List[str], 
                    bits_por_var: int) -> List[pd.DataFrame]:
    columnas_entrada = generar_columnas_entrada(variables, bits_por_var)
    salidas = identificar_salidas_interes(df)
    resultados_finales = []
    
    for salida in salidas:
        guardar_en_archivo(f"\nProcesando salida: {salida}")
        
        df_actual = preparar_grupos_iniciales(df, salida, columnas_entrada)
        guardar_en_archivo("\nGrupos iniciales:")
        guardar_en_archivo(str(df_actual))
        
        iteracion = 1
        longitud_anterior = -1
        
        while len(df_actual) != longitud_anterior:
            longitud_anterior = len(df_actual)
            df_actual = simplificar_grupos(df_actual)
            
            if len(df_actual) > 0:
                guardar_en_archivo(f"\nIteración {iteracion}:")
                guardar_en_archivo(str(df_actual))
                iteracion += 1
            else:
                break
        
        resultados_finales.append(df_actual)
    return resultados_finales
