import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

def generar_columnas_entrada(variables: List[str], bits_por_var: int) -> List[str]:
    """Genera la lista de nombres de columnas para las entradas binarias.
    
    Por ejemplo, si las variables son ['A', 'B'] y bits_por_var es 2, generará:
    ['A_0', 'A_1', 'B_0', 'B_1']
    
    Esto es útil para acceder a las columnas específicas del DataFrame que contienen
    los valores binarios de cada variable de entrada.
    
    parametros:
        variables: Lista con los nombres de las variables (ej: ['A', 'B', 'C'])
        bits_por_var: Cantidad de bits usados para representar cada variable
    
    Devuelve:
        Lista de strings con los nombres de las columnas generadas
    """
    columnas = []
    for var in variables:
        for bit in range(bits_por_var):
            columnas.append(f"{var}_{bit}")
    return columnas

def contar_unos_en_fila(fila: pd.Series, columnas_entrada: List[str]) -> int:
    """Cuenta la cantidad de unos (1s) en las columnas de entrada de una fila.
    
    Esta función es fundamental para el algoritmo de Quine-McCluskey ya que necesitamos
    agrupar los términos según la cantidad de unos que contienen. Por ejemplo:
    - Para la fila '0001' el resultado sería 1
    - Para la fila '1101' el resultado sería 3
    
    parametros:
        fila: Serie de pandas que representa una fila del DataFrame
        columnas_entrada: Lista de nombres de columnas que contienen los bits
    
    Devuelve:
        Número entero que representa la cantidad de unos en las columnas especificadas
    """
    return sum(fila[columnas_entrada])

def convertir_a_binario(fila: pd.Series, columnas_entrada: List[str]) -> str:
    """Convierte las columnas de entrada de una fila en una cadena binaria.
    
    Esta función toma los valores de las columnas de entrada y los concatena en
    una sola cadena. Por ejemplo, si tenemos las columnas ['A_0', 'A_1', 'B_0', 'B_1']
    con valores [1, 0, 1, 1], el resultado será '1011'.
    
    parametros:
        fila: Serie de pandas que representa una fila del DataFrame
        columnas_entrada: Lista de nombres de columnas que contienen los bits
    
    Devuelve:
        String que representa la concatenación de los bits de entrada
    """
    return ''.join(str(int(fila[col])) for col in columnas_entrada)

def encontrar_diferencia_un_bit(bin1: str, bin2: str) -> Tuple[bool, str]:
    """Analiza si dos cadenas binarias difieren en exactamente un bit.
    
    Esta es una función clave en el algoritmo de Quine-McCluskey. Determina si dos términos
    pueden combinarse. Por ejemplo:
    - '1101' y '1111' difieren en un bit (posición 2) -> returna (True, '11_1')
    - '1101' y '1001' difieren en un bit (posición 1) -> returna (True, '1_01')
    - '1101' y '1010' difieren en más de un bit -> returna (False, '')
    
    El guion bajo ('_') en el resultado indica la posición donde los términos difieren.
    
    parametros:
        bin1: Primera cadena binaria
        bin2: Segunda cadena binaria
    
    Devuelve:
        Tupla donde el primer elemento es True si difieren en un bit, y el segundo
        elemento es la cadena resultante con '_' en la posición de diferencia
    """
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
    """Identifica las columnas que representan salidas de interés en el DataFrame.
    
    Las salidas de interés son aquellas que cumplen con alguno de estos criterios:
    1. El nombre es exactamente "SC", "SR" o "I"
    2. El nombre contiene "C_" o "R_"
    
    Por ejemplo, para un DataFrame con columnas ['A_0', 'B_0', 'SC', 'C_1', 'R_0'],
    retornará ['SC', 'C_1', 'R_0'].
    
    parametros:
        df: DataFrame que contiene la tabla de verdad completa
    
    Devuelve:
        Lista de nombres de columnas que representan salidas de interés
    """
    salidas = []
    for col in df.columns:
        if col in ["SC", "SR", "I"] or "C_" in col or "R_" in col:
            salidas.append(col)
    return salidas

def preparar_grupos_iniciales(df: pd.DataFrame, columna_salida: str, 
                            columnas_entrada: List[str]) -> pd.DataFrame:
    """Prepara los grupos iniciales para aplicar el método de Quine-McCluskey.
    
    Esta función realiza varios pasos importantes:
    1. Filtra el DataFrame para mantener solo las filas donde la salida es 1
    2. Agrega una columna con los índices originales (minterms)
    3. Cuenta los unos en cada término
    4. Convierte las entradas a formato binario
    5. Ordena los términos por cantidad de unos
    
    Por ejemplo, si tenemos la tabla:
    A_0 A_1 B_0 B_1 SC
     0   1   1   0  1
     1   1   0   0  1
     0   0   1   1  0
    
    El resultado será (para SC=1):
    minterms  binario  cant_unos
    1         0110    2
    2         1100    2
    
    parametros:
        df: DataFrame con la tabla de verdad
        columna_salida: Nombre de la columna de salida a procesar
        columnas_entrada: Lista de columnas que contienen los bits de entrada
    
    Devuelve:
        DataFrame preparado y ordenado para el proceso de simplificación
    """
    # Filtrar por salida = 1
    filtrado = df[df[columna_salida] == 1].copy()
    
    # Agregar columnas necesarias
    filtrado['minterms'] = filtrado.index.astype(str)
    filtrado['cant_unos'] = filtrado.apply(
        lambda row: contar_unos_en_fila(row, columnas_entrada), axis=1)
    filtrado['binario'] = filtrado.apply(
        lambda row: convertir_a_binario(row, columnas_entrada), axis=1)
    
    return filtrado.sort_values('cant_unos')

def simplificar_grupos(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza una iteración de simplificación en el método de Quine-McCluskey.
    
    Esta función es el corazón del algoritmo. Busca pares de términos que 
    difieran en exactamente un bit y los combina. Por ejemplo:
    
    Entrada:
    minterms  binario  cant_unos
    1         0110    2
    2         1110    3
    
    Salida:
    minterms  binario    cant_unos
    1,2       _110      2
    
    El proceso:
    1. Compara términos adyacentes (que difieran en máximo 1 en cant_unos)
    2. Si difieren en un bit, los combina y marca ambos como usados
    3. Mantiene los términos que no se pudieron combinar
    4. Elimina duplicados
    
    parametros:
        df: DataFrame con los términos actuales
    
    Devuelve:
        Nuevo DataFrame con los términos simplificados
    """
    if len(df) <= 1:
        return pd.DataFrame(columns=['minterms', 'binario'])
        
    simplificados = []
    usados = set()
    
    # Comparar cada par de términos
    for i, fila1 in df.iterrows():
        for j, fila2 in df.iterrows():
            if i >= j:
                continue
                
            if abs(fila1['cant_unos'] - fila2['cant_unos']) > 1:
                continue
                
            combinable, combinado = encontrar_diferencia_un_bit(
                fila1['binario'], fila2['binario'])
            
            if combinable:
                usados.add(fila1['minterms'])
                usados.add(fila2['minterms'])
                nuevos_minterms = ','.join(sorted([fila1['minterms'], fila2['minterms']]))
                simplificados.append({
                    'minterms': nuevos_minterms,
                    'binario': combinado
                })
    
    # Agregar términos no utilizados
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
    """Implementa el método completo de Quine-McCluskey para todas las salidas.
    
    Esta función coordina todo el proceso del algoritmo:
    1. Identifica las salidas a procesar
    2. Para cada salida:
       - Prepara los grupos iniciales
       - Realiza iteraciones de simplificación hasta que no haya cambios
       - Guarda el resultado final
    
    Por ejemplo, para una tabla de verdad con salidas SC y SR:
    - Procesa SC y encuentra sus términos minimizados
    - Procesa SR y encuentra sus términos minimizados
    - Retorna una lista con ambos resultados
    
    parametros:
        df: DataFrame con la tabla de verdad
        variables: Lista de nombres de variables
        bits_por_var: Cantidad de bits por variable
    
    Devuelve:
        Lista de DataFrames, cada uno contiene los términos minimizados
        para una salida específica
    """
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
    
    return resultados_finales