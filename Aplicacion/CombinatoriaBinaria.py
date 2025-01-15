import pandas as pd
import math, time
import itertools 

def crearCombinatoria(denominador, divisor, nombre_entradas, bits, toExcel, nombre_archivo):
    '''Inicialmente se crean 3 variables necesarias para el programa:

    - combinaciones_binarias: Esta contendra todas las combinaciones binarias posibles de realizar
    con una cantidad n de entradas y m de bits, por ejemplo, si se ingresan 2 entradas de 5 bits,
    se creara una lista con 2^5 elementos, algo como [0000000001, 0000000010 ... 1111111111], de modo
    que al agarrar las primeras 5 columnas de cada elemento representara una variable, en 0000000001,
    00000 corresponde a la primera variable, y 00001 corresponde a la segunda variable.
    
    - tabla_de_verdad: Literalmente es la tabla de verdad, la idea es que la tabla de verdad se llene
    en 2 pasos, el primero corresponde a rellenarla con los valores base 10 y binarios de las variables,
    A, B ... Z, y A_0, A_1 ... Z_M, tambien con los valores de SC, C, SR, R e I, aqui entra el segundo 
    paso, donde se rellenaran nuevas columnas que representaran los bits binarios de C y R, de modo que
    la tabla de verdad quede completa.
    
    - valores_entradas: Valor entradas es un arreglo que se actualizara al mismo tiempo que se calcula la 
    tabla de verdad, contiene los valores correspondientes de cada entrada, por ejemplo A = 2, B = 1, C = 2
    D = 5 ... Z = X, al calcular cada fila de la tabla de verdad, valores_entradas se actualizara, y la
    tabla de verdad hara de nuevo los calculos con los nuevos valores.'''

    combinaciones_binarias = list(itertools.product([0, 1], repeat=len(nombre_entradas)*bits))
    tabla_de_verdad = pd.DataFrame(columns=[*nombre_entradas, *[f"{nombre_entrada}_{bit}" for nombre_entrada in nombre_entradas for bit in range(bits)], 'SC', 'C', 'SR', 'R', 'I'])
    valores_entradas = {}

    '''Preparacion de denominador y divisor, haciendo uso del diccionario de valores_entradas 
    podran saber que valor tienen las entradas en cada momento, para para esto es necesario
    reescribir al denominador y al divisor para que llamen al diccionario.'''
    
    for entrada in nombre_entradas:
        denominador = denominador.replace(entrada, f"valores_entradas['{entrada}']")
        divisor = divisor.replace(entrada, f"valores_entradas['{entrada}']")
        
    '''PRIMER PASO
    El primer paso consiste en calcular cada fila de la tabla de verdad para rellenarla con los valores base 10 
    y binarios de las variables, A, B ... Z, y A_0, A_1 ... Z_M, tambien con los valores de SC, C, SR, R e I.'''

    for combinacion_binaria in combinaciones_binarias:    
        '''Se crea un arreglo que contendra el valor de las entradas binarias, como 00,01 .. 11, estos valores
        binarios se pasan a base 10 y se le asignan a la variable correspondiente en el diccionario valores_entradas.'''  
        valor_entrada_binaria = [''.join(map(str, combinacion_binaria[i:i+bits])) for i in range(0, len(combinacion_binaria), bits)]
        for valor_binario, nombre_entrada in zip(valor_entrada_binaria, nombre_entradas):
            valores_entradas[nombre_entrada] = int(valor_binario, 2)

        '''Evalua las salidas C, R, SC, SR e I con la funcion eval y condicionales, si el divisor es 0, el resultado
        sera invalido automaticamente (I sera 1).'''
        if eval(divisor) != 0: 
            resultado_denominador = eval(str(denominador))
            resultado_divisor = eval(str(divisor))
            C = abs(resultado_denominador) // resultado_divisor
            R = abs(resultado_denominador) % resultado_divisor
            SC = 1 if resultado_denominador > 0 and C > 0 else 0
            SR = 1 if resultado_denominador / resultado_divisor > 0 and R > 0 else 0
            I = 0
        else:
            C, R, SC, SR, I = 0, 0, 0, 0, 1
        '''Se añaden a la tabla de verdad las entradas base 10 (A, B ... C), las entradas binarias 
        (A_0, A_1 ... C_N) y sus salidas correspondientes en base 10 (SC, C, SR, R, I).'''
        tabla_de_verdad.loc[len(tabla_de_verdad)] = ([*list(valores_entradas.values()),*combinacion_binaria, SC, C, SR, R, I])
    '''SEGUNDO PASO
    Se calcula la cantidad minimos de bits para representar binariamente a C y R y se añaden nuevas 
    columnas y filas a la tabla de verdad, correspondientes a los bits de C y R (C_0, C_1 ... R_N).'''
    try:
        bits_minimos_C = math.floor(math.log2(tabla_de_verdad["C"].max())) + 1
    except:
        bits_minimos_C = 1
    try:
        bits_minimos_R = math.floor(math.log2(tabla_de_verdad["R"].max())) + 1
    except:
        bits_minimos_R = 1
    for bits_C in range(bits_minimos_C): tabla_de_verdad[f"C_{bits_C}"] = None
    for bits_R in range(bits_minimos_R): tabla_de_verdad[f"R_{bits_R}"] = None
    '''Se rellena la tabla de verdad, especificamente las columnas añadidas para los bits de C y R.'''
    for n, fila in tabla_de_verdad.iterrows():
        C_bits = [(fila['C'] >> i) & 1 for i in range(bits_minimos_C)]
        R_bits = [(fila['R'] >> i) & 1 for i in range(bits_minimos_R)]
        for indice in range(len(C_bits)):
            tabla_de_verdad.at[n, f'C_{indice}'] = C_bits[-indice-1]
        for indice in range(len(R_bits)):
            tabla_de_verdad.at[n, f'R_{indice}'] = R_bits[-indice-1]
    '''Finalmente, ya se tiene la tabla de verdad completa, para mayor comodidad al analisis se da
    la opcion de exportar a un archivo Excel, y si el archivo ya existe y esta abierto lo guardara 
    con un nombre podria decirse aleatorio.'''
    if toExcel:
        try:
            tabla_de_verdad.to_excel(f"./Resultados Excel/{nombre_archivo}.xlsx", index=False, sheet_name="Tabla de verdad")
        except:
            try:
                tabla_de_verdad.to_excel(f"./Resultados Excel/{time.time()}.xlsx", index=False, sheet_name="Tabla de verdad")
            except:
                tabla_de_verdad.to_excel(f"./{nombre_archivo}.xlsx", index=True, sheet_name="Tabla de verdad")
    '''Devuelve la tabla de verdad como DataFrame para posterior uso.'''
    return tabla_de_verdad