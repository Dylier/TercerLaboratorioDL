from CombinatoriaBinaria import crearCombinatoria
import metodoQuineMcCluskey as mc
import ExpresionLogica as ex

""" 
if __name__ == "__main__gh":
    incial = time.time()
    bits = 4
    variables = ['A', 'B']
    pruebas = {"Prueba 1":"(A*B)+(A-B)/A", "Prueba 2":"(A+B)*(A-B)/A", "Prueba 3":"(A*B)-(A-B)/A", "Prueba 4":"(A*B*A*B)/A"}
    
    for prueba in pruebas.keys():
        operacion = pruebas[prueba].split("/")
        print(operacion[0] + operacion[1])
        #df = valores_C_y_RearCombinatoria(denominador = operacion[0], divisor = operacion[1], toExcel = True, variables=variables, bits=bits)
        #encontrar_expresiones_logicas(df, variables, bits, prueba)

        # Identificar entradas y salidas
        #entradas = [col for col in df.columns if col.startswith("A_") or col.startswith("B_")]
        #salidas = [col for col in df.columns if col.startswith("C_") or col.startswith("R_")]
        # Llamar a la función
        #resultados = mapa.simplificar_todas_las_salidas(df, entradas, salidas)
        print("\nResultados finales:")
        #for salida, simplificacion in resultados.items():
        #    print(f"{salida}: {simplificacion}")
        print(prueba + ": Se ha demorado "+str(time.time()-incial))
        incial = time.time()
    
    
    # df = valores_C_y_RearCombinatoria(denominador = "(A+B)*(A-D)", divisor = 'A', toExcel = True, variables=variables, bits=bits)
    # encontrar_expresiones_logicas(df, variables, bits, "2")
    # print("Prueba 2: Se ha demorado "+str(time.time()-incial))
    # incial = time.time()
    # df = valores_C_y_RearCombinatoria(denominador = "(A*B)-(A-D)", divisor = 'A', toExcel = True, variables=variables, bits=bits)
    # encontrar_expresiones_logicas(df, variables, bits, "3")
    # print("Prueba 3: Se ha demorado "+str(time.time()-incial))
    # incial = time.time()
    # df = valores_C_y_RearCombinatoria(denominador = "(A*B*A*D)", divisor = 'A', toExcel = True, variables=variables, bits=bits)
    # encontrar_expresiones_logicas(df, variables, bits, "4")
    # print("Prueba 4: Se ha demorado "+str(time.time()-incial))
    # denominador = "((A*B)-(A+B))"
    # divisor = "A"
    # variables = ['A', 'B']
    # bits = 4
    # df = valores_C_y_RearCombinatoria(denominador = denominador, divisor = divisor, toExcel = False, variables=variables, bits=bits)
    # print(df)
    # encontrar_expresiones_logicas(df, variables, bits, 60) """

df = crearCombinatoria("(A*B)-(A+B)", "A", ['A', 'B'], 3, True, "Ejemplo")
lista_simplificada = mc.quine_mccluskey(df, ['A', 'B'], 3)
ex.quine_mccluskey_con_canonicas(df, ['A', 'B'], 3, "SIMPLIFICADO", lista_simplificada)
ex.encontrar_expresiones_logicas(df, ['A', 'B'], 3, "NO SIMPLIFICADO")
