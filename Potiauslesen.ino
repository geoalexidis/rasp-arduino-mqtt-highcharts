// reads analog value from potentiometer

int LED1 = 11;
int LED2 = 10;
int LED3 = 9;


int poti = 0;
int x;
void setup()
{

  Serial.begin(9600);
  analogReference(DEFAULT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

}

void loop()
{
  int potiwert = analogRead(poti);
  x = map(potiwert, 0, 1023, 300, 1000); // Rechnet den Wert 0-1023 um  in Werte zwischen 300 und 1000
  Serial.println(x);

  if (x < 500)
  {
    digitalWrite(LED3, HIGH);
    digitalWrite(LED2, LOW);
    digitalWrite(LED1, LOW);
  }
  else if (x >= 800)
  {
    digitalWrite(LED2, LOW);
    digitalWrite(LED1, HIGH);
    digitalWrite(LED3, LOW);
  }
  else
  {
    digitalWrite(LED2, HIGH);
//    digitalWrite(LED3, LOW);
//    digitalWrite(LED1, LOW);
  }

  delay(1000);
}
