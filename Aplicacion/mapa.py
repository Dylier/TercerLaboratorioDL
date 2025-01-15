import pandas as pd

def simplificar_todas_las_salidas(df, entradas, salidas):
    """
    Simplifica cada columna de salidas aplicando un mapa de Karnaugh y muestra los pasos intermedios.
    :param df: DataFrame con datos de entradas y salidas.
    :param entradas: Lista de columnas de entradas.
    :param salidas: Lista de columnas de salidas.
    :return: Diccionario con las simplificaciones de cada salida.
    """
    resultados = {}

    def mostrar_pasos(pasos):
        """Muestra los pasos intermedios de forma ordenada."""
        for i, paso in enumerate(pasos, 1):
            print(f"\nPaso {i}:")
            print(paso)

    def generar_mapa_karnaugh(df, entradas, salida):
        """
        Genera y simplifica un mapa de Karnaugh para una salida específica con pasos intermedios.
        """
        pasos = []

        # Crear tabla de verdad
        df_verdad = df[entradas + [salida]].drop_duplicates().sort_values(by=entradas).reset_index(drop=True)
        pasos.append("Tabla de verdad creada:\n" + df_verdad.to_string(index=False))

        # Inicializar mapa de Karnaugh
        num_entradas = len(entradas)
        combinaciones = 2 ** num_entradas
        combinaciones_bin = [bin(i)[2:].zfill(num_entradas) for i in range(combinaciones)]
        mapa = {comb: None for comb in combinaciones_bin}

        # Llenar el mapa de Karnaugh
        for _, fila in df_verdad.iterrows():
            valores_entradas = ''.join(map(str, fila[entradas].astype(int)))
            mapa[valores_entradas] = fila[salida]
        pasos.append("Mapa de Karnaugh llenado:\n" + "\n".join(f"{k}: {v}" for k, v in mapa.items()))

        # Agrupaciones iniciales por número de unos
        implicantes = {key: val for key, val in mapa.items() if val == 1}
        grupos = {}
        for num_ones in range(num_entradas + 1):
            grupo_actual = [
                key for key in implicantes.keys() if key.count("1") == num_ones
            ]
            if grupo_actual:
                grupos[num_ones] = grupo_actual
        pasos.append("Agrupaciones iniciales por número de unos:\n" + "\n".join(f"{k}: {v}" for k, v in grupos.items()))

        # Simplificar términos
        resultado = implicantes.copy()
        for num_ones in range(num_entradas):
            if num_ones in grupos and num_ones + 1 in grupos:
                for a in grupos[num_ones]:
                    for b in grupos[num_ones + 1]:
                        # Comparar si solo difieren en un bit
                        diferencias = [
                            i for i in range(len(a)) if a[i] != b[i]
                        ]
                        if len(diferencias) == 1:
                            simplificado = list(a)
                            simplificado[diferencias[0]] = "-"
                            simplificado = "".join(simplificado)
                            resultado[simplificado] = 1

        pasos.append("Términos simplificados:\n" + "\n".join(f"{k}: {v}" for k, v in resultado.items() if v == 1))

        # Convertir el resultado simplificado a términos lógicos
        terminos = []
        for key, val in resultado.items():
            if val == 1:
                terminos.append("".join([
                    f"{entradas[i]}" if bit == "1" else f"¬{entradas[i]}" if bit == "0" else ""
                    for i, bit in enumerate(key)
                ]).strip())

        mostrar_pasos(pasos)
        return " + ".join(terminos) if terminos else "0"

    # Ciclar por cada salida
    for salida in salidas:
        print(f"\nSimplificando salida: {salida}")
        simplificacion = generar_mapa_karnaugh(df, entradas, salida)
        resultados[salida] = simplificacion
        print(f"Simplificación final para {salida}: {simplificacion}")

    return resultados


# # Cargar el DataFrame
# data = {
#     "A_1": [0, 0, 0, 0, 1, 1, 1, 1],
#     "A_2": [0, 0, 1, 1, 0, 0, 1, 1],
#     "B_1": [0, 1, 0, 1, 0, 1, 0, 1],
#     "B_4": [0, 0, 0, 0, 1, 1, 1, 1],
#     "SC": [0, 1, 1, 0, 1, 1, 0, 0],
#     "C_1": [0, 1, 0, 1, 1, 1, 0, 0],
#     "C_2": [1, 1, 1, 1, 0, 0, 0, 0],
#     "R_1": [0, 1, 0, 0, 1, 1, 0, 1],
#     "R_2": [1, 0, 1, 1, 0, 0, 1, 0]
# }

# df = pd.DataFrame(data)
# # Identificar entradas y salidas
# entradas = [col for col in df.columns if col.startswith("A_") or col.startswith("B_")]
# salidas = [col for col in df.columns if col.startswith("C_") or col.startswith("R_")]

# # Llamar a la función
# resultados = simplificar_todas_las_salidas(df, entradas, salidas)
# print("\nResultados finales:")
# for salida, simplificacion in resultados.items():
#     print(f"{salida}: {simplificacion}")
