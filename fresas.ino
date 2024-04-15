const int enablePin = 9;   // Pin de habilitación del puente H
const int in1Pin = 8;      // Entrada 1 del puente H
const int in2Pin = 7;      // Entrada 2 del puente H

void setup() {
  pinMode(enablePin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);

  // Inicialmente, apagamos la bomba
  digitalWrite(enablePin, LOW);
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, LOW);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char estado = Serial.read();
    if (estado == '1') {
      // Encender la bomba
      digitalWrite(enablePin, HIGH);
      digitalWrite(in1Pin, HIGH);
      digitalWrite(in2Pin, LOW);
    } else if (estado == '0') {
      // Apagar la bomba
      digitalWrite(enablePin, LOW);
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, LOW);
    }
  }
}
