#include <LiquidCrystal_I2C.h>

#include <LiquidCrystal_I2C.h>

// include the library code:
#include <Q2HX711.h>              //Downlaod from here: https://electronoobs.com/eng_arduino_hx711.php
//LCD config
#include <Wire.h> 
// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to

const byte hx711_data_pin = 3;    //Data pin from HX711
const byte hx711_clock_pin = 2;   //Clock pin from HX711

int msg;
Q2HX711 hx711(hx711_data_pin, hx711_clock_pin); // prep hx711
LiquidCrystal_I2C lcd(0x27, 20, 4);
String PuertaDisp="";
// int peso=243;
String mensaje="";

//Variables
/////////Change here with your calibrated mass////////////
float y1 = 200.0; // calibrated mass to be added
//////////////////////////////////////////////////////////

long x1 = 0L;
long x0 = 0L;
float avg_size = 10.0; // amount of averages for each mass measurement
float tara = 0;
//////////////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);
  
  PCICR |= (1 << PCIE0);              //enable PCMSK0 scan                                                 
  PCMSK0 |= (1 << PCINT0);            //Set pin D8 trigger an interrupt on state change.
  PCMSK0 |= (1 << PCINT3);            //Set pin D10 trigger an interrupt on state change.   
  lcd.init();
  lcd.backlight();
  delay(1000);                        // allow load cell and hx711 to settle

  
  // tare procedure
  for (int ii=0;ii<int(avg_size);ii++){
    delay(10);
    x0+=hx711.read();
  }
  x0/=long(avg_size);
  //Serial.println("Add Calibrated Mass");

  // calibration procedure (mass should be added equal to y1)
  int ii = 1;
  while(true){
    if (hx711.read()<x0+10000)
    {
      //do nothing...
    } 
    else 
    {
      ii++;
      delay(2000);
      for (int jj=0;jj<int(avg_size);jj++){
        x1+=hx711.read();
      }
      x1/=long(avg_size);
      break;
    }
  }
  //Serial.println("Calibration Complete");
  // set up the LCD's number of columns and rows:


  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Bienvenido!");
  delay(500);
  lcd.clear();

}

void loop() {
  long reading = 0;
  for (int jj=0;jj<int(avg_size);jj++)
  {
    reading+=hx711.read();
  }
  reading/=long(avg_size);
  
  // calculating mass based on calibration and linear fit
  float ratio_1 = (float) (reading-x0);
  float ratio_2 = (float) (x1-x0);
  float ratio = ratio_1/ratio_2;
  float mass = y1*ratio;
  
  Serial.println(String(mass - tara));

  delay(10000);

  if (Serial.available()) {
    if (msg != '\n' && msg != '\r'){  
      msg = Serial.read();
      // Serial.print("Puerta ingresada: ");
      Serial.println(msg);
      }
  }
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  //Serial.println(peso);
  
  delay(200);
  lcd.clear();
  lcd.setCursor(0, 0);
  mensaje = "Ir a puerta:";
  lcd.print(mensaje);
  lcd.setCursor(0, 1);
  if (msg > 100 && msg < 107) {
    msg = msg - 100;
  }
  
  lcd.print(msg);
  // limpiar el buffer
  if (Serial.available()) {
    Serial.read();
  }
  delay(200);
}