// Código generado automaticamente
#include <Arduino.h>

// Declaracion de variables
bool A_0; // Entrada
bool A_1; // Entrada
bool A_2; // Entrada
bool B_0; // Entrada
bool B_1; // Entrada
bool B_2; // Entrada
bool SC; // Salida
bool SR; // Salida
bool I; // Salida
bool C_0; // Salida
bool C_1; // Salida
bool C_2; // Salida
bool R_0; // Salida
bool R_1; // Salida
bool R_2; // Salida

void setup() {
  Serial.begin(9600);
  Serial.println("Programa iniciado. Ingresa los valores para cada entrada (0 o 1).");
}

void loop() {
  // Leer entradas desde el monitor serial
  A_0 = obtenerValor("A_0");
  A_1 = obtenerValor("A_1");
  A_2 = obtenerValor("A_2");
  B_0 = obtenerValor("B_0");
  B_1 = obtenerValor("B_1");
  B_2 = obtenerValor("B_2");

  // Evaluar expresiones lógicas
  SC = (A_0 & B_1 & !B_0) | (A_0 & B_2 & !B_0) | (A_0 & A_1 & B_0 & !B_1) | (A_0 & A_1 & B_2 & !B_1) | (A_1 & B_2 & !B_0 & !B_1) | (A_0 & A_1 & A_2 & B_0 & !B_2) | (A_0 & A_1 & A_2 & B_1 & !B_2) | (A_0 & A_2 & B_0 & !B_1 & !B_2) | (A_1 & A_2 & B_1 & !B_0 & !B_2);
  SR = (A_0 & B_1 & !B_0) | (A_0 & B_2 & !B_0) | (A_0 & A_1 & B_0 & !B_1) | (A_0 & A_1 & B_2 & !B_1) | (A_1 & B_2 & !B_0 & !B_1) | (A_0 & A_1 & A_2 & B_0 & !B_2) | (A_0 & A_1 & A_2 & B_1 & !B_2) | (A_0 & A_2 & B_0 & !B_1 & !B_2) | (A_1 & A_2 & B_1 & !B_0 & !B_2);
  I = (A_0 & !B_0 & !B_1 & !B_2) | (A_1 & !B_0 & !B_1 & !B_2) | (A_2 & !B_0 & !B_1 & !B_2) | (B_0 & !A_0 & !A_1 & !A_2) | (B_1 & !A_0 & !A_1 & !A_2) | (B_2 & !A_0 & !A_1 & !A_2) | (!A_0 & !A_1 & !A_2 & !B_0) | (!A_0 & !A_1 & !A_2 & !B_1) | (!A_0 & !A_1 & !A_2 & !B_2) | (!A_0 & !B_0 & !B_1 & !B_2) | (!A_1 & !B_0 & !B_1 & !B_2) | (!A_2 & !B_0 & !B_1 & !B_2);
  C_0 = (A_0 & A_1 & A_2 & B_1 & !B_0) | (A_0 & A_1 & A_2 & B_2 & !B_0) | (A_1 & B_0 & B_1 & B_2 & !A_0) | (A_2 & B_0 & B_1 & B_2 & !A_0) | (A_0 & A_1 & B_1 & !B_0 & !B_2) | (A_0 & A_1 & B_2 & !B_0 & !B_1) | (A_0 & A_2 & B_2 & !B_0 & !B_1) | (A_1 & B_0 & B_1 & !A_0 & !A_2) | (A_2 & B_0 & B_1 & !A_0 & !A_1) | (A_2 & B_0 & B_2 & !A_0 & !A_1);
  C_1 = (A_1 & A_2 & B_2 & !B_1) | (A_2 & B_1 & B_2 & !A_1) | (A_0 & A_1 & A_2 & B_0 & !B_1) | (A_0 & B_0 & B_1 & B_2 & !A_1) | (A_0 & A_1 & B_0 & !B_1 & !B_2) | (A_0 & A_2 & B_1 & !A_1 & !B_0) | (A_0 & B_0 & B_1 & !A_1 & !A_2) | (A_1 & B_0 & B_2 & !A_0 & !B_1) | (A_0 & B_1 & !A_1 & !A_2 & !B_2) | (A_0 & B_1 & !A_1 & !B_0 & !B_2) | (A_1 & B_0 & !A_0 & !A_2 & !B_1) | (A_1 & B_0 & !A_2 & !B_1 & !B_2) | (A_0 & A_1 & B_1 & B_2 & !A_2 & !B_0) | (A_1 & A_2 & B_0 & B_1 & !A_0 & !B_2) | (A_0 & B_2 & !A_1 & !A_2 & !B_0 & !B_1) | (A_2 & B_0 & !A_0 & !A_1 & !B_1 & !B_2);
  C_2 = (A_0 & B_2 & !A_2) | (A_1 & B_2 & !A_2) | (A_2 & B_0 & !B_2) | (A_2 & B_1 & !B_2);
  R_0 = (A_0 & A_1 & A_2 & B_1 & !B_0) | (A_0 & A_1 & A_2 & B_2 & !B_0) | (A_1 & B_0 & B_1 & B_2 & !A_0) | (A_2 & B_0 & B_1 & B_2 & !A_0) | (A_0 & A_1 & B_1 & !B_0 & !B_2) | (A_0 & A_1 & B_2 & !B_0 & !B_1) | (A_0 & A_2 & B_2 & !B_0 & !B_1) | (A_1 & B_0 & B_1 & !A_0 & !A_2) | (A_2 & B_0 & B_1 & !A_0 & !A_1) | (A_2 & B_0 & B_2 & !A_0 & !A_1);
  R_1 = (A_1 & A_2 & B_2 & !B_1) | (A_2 & B_1 & B_2 & !A_1) | (A_0 & A_1 & A_2 & B_0 & !B_1) | (A_0 & B_0 & B_1 & B_2 & !A_1) | (A_0 & A_1 & B_0 & !B_1 & !B_2) | (A_0 & A_2 & B_1 & !A_1 & !B_0) | (A_0 & B_0 & B_1 & !A_1 & !A_2) | (A_1 & B_0 & B_2 & !A_0 & !B_1) | (A_0 & B_1 & !A_1 & !A_2 & !B_2) | (A_0 & B_1 & !A_1 & !B_0 & !B_2) | (A_1 & B_0 & !A_0 & !A_2 & !B_1) | (A_1 & B_0 & !A_2 & !B_1 & !B_2) | (A_0 & A_1 & B_1 & B_2 & !A_2 & !B_0) | (A_1 & A_2 & B_0 & B_1 & !A_0 & !B_2) | (A_0 & B_2 & !A_1 & !A_2 & !B_0 & !B_1) | (A_2 & B_0 & !A_0 & !A_1 & !B_1 & !B_2);
  R_2 = (A_0 & B_2 & !A_2) | (A_1 & B_2 & !A_2) | (A_2 & B_0 & !B_2) | (A_2 & B_1 & !B_2);

  // Imprimir resultados
  Serial.println("Resultados:");
  Serial.print("SC = "); Serial.println(SC);
  Serial.print("SR = "); Serial.println(SR);
  Serial.print("I = "); Serial.println(I);
  Serial.print("C_0 = "); Serial.println(C_0);
  Serial.print("C_1 = "); Serial.println(C_1);
  Serial.print("C_2 = "); Serial.println(C_2);
  Serial.print("R_0 = "); Serial.println(R_0);
  Serial.print("R_1 = "); Serial.println(R_1);
  Serial.print("R_2 = "); Serial.println(R_2);

  delay(5000);
}


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
