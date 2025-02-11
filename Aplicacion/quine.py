import pandas as pd
import numpy as np
from typing import List, Tuple, Union
from sympy import symbols, Not, And, Or


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

def convertir_termino_a_expresion(termino: str, variables: List[str], bits_por_var: int) -> List[Union[symbols, Not]]:
    simbolos = []
    nombre_columnas = [f"{var}_{bit}" for var in variables for bit in range(bits_por_var)]
    
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
    
    return str(Or(*terminos)) if terminos else "0"




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
    
    print("\nComparaciones entre terminos:")
    
    for i, fila1 in df.iterrows():
        for j, fila2 in df.iterrows():
            if i >= j:
                continue
                
            if abs(fila1['cant_unos'] - fila2['cant_unos']) > 1:
                continue
                
            combinable, combinado = encontrar_diferencia_un_bit(
                fila1['binario'], fila2['binario'])
            
            print(f"Comparando {fila1['binario']} ({fila1['minterms']}) con {fila2['binario']} ({fila2['minterms']})")
            
            if combinable:
                print(f" -> Se pueden agrupar: {fila1['binario']} y {fila2['binario']} -> {combinado}")
                usados.add(fila1['minterms'])
                usados.add(fila2['minterms'])
                nuevos_minterms = ','.join(sorted([fila1['minterms'], fila2['minterms']]))
                simplificados.append({
                    'minterms': nuevos_minterms,
                    'binario': combinado
                })
            else:
                print(" -> No se pueden agrupar")
    
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
        print(f"\nProcesando salida: {salida}")
        
        # Crear grupos iniciales
        df_actual = preparar_grupos_iniciales(df, salida, columnas_entrada)
        print("\nGrupos iniciales:")
        print(df_actual)
        
        iteracion = 1
        longitud_anterior = -1
        
        # Iterar hasta que no haya más simplificaciones posibles
        while len(df_actual) != longitud_anterior:
            longitud_anterior = len(df_actual)
            df_actual = simplificar_grupos(df_actual)
            
            if len(df_actual) > 0 and iteracion < 3:
                print(f"\nIteración {iteracion}:")
                print(df_actual)
                iteracion += 1
            else:
                break
        
        resultados_finales.append(df_actual)
        
    for resultado, salida in zip(resultados_finales, salidas):
        print(f"\n\nExpresiones logicas finales de {salida}\n\n")
        expresion_logica = generar_expresion_canonica(resultado, variables, bits_por_var)
        print(resultado)
        print(f"Expresion logica: {expresion_logica}")
    
    return resultados_finales