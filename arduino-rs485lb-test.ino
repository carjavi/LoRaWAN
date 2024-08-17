
/*
  * Arduino Modbus RS485/UART slave for Dragino RS485-BL
  * Created by Carlos Briceño (2024) 
  * https://github.com/smarmengol/Modbus-Master-Slave-for-Arduino
 */

// Uncomment these lines to use Software Serial for RS-485 communication (oooooooooooooooojjjjoooooooooooo)    <---------------------------
//#define SWSERIAL_RX 6  //Digital pin used for software serial rx
//#define SWSERIAL_TX 7  //Digital pin used for software serial tx

#define SLAVE_ID 0x01  //Modbus slave address 8bit
uint16_t modbus_array[] = {0,0,0,0,0,0}; //Initialization for Modbus Holding registers:  2 registros en 0 cada uno.
#define RS485_DERE 4  //Digital pin connected to DE & RE pin of RS-485 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

//Many thanks to smarmengol: https://github.com/smarmengol/Modbus-Master-Slave-for-Arduino
#include "src/Modbus-Master-Slave-for-Arduino-master/ModbusRtu.h"



const uint16_t int_min_value = -32768;  //signed 16 bit integer ranges from -32768 to 32767


#ifdef SWSERIAL_RX
#include <SoftwareSerial.h>
SoftwareSerial myserial(SWSERIAL_RX, SWSERIAL_TX);
//Modbus slave ID, RS-485 module comunication on Software Serial, and Arduino digital pin connected to both DE & RE pins of RS-485
Modbus slave(SLAVE_ID,myserial,RS485_DERE);
#else
//Modbus slave ID, RS-485 module comunication on Hardware Serial, and Arduino digital pin connected to both DE & RE pins of RS-485
// OJOOOOO RS485_DERE podria ser 0 probar
Modbus slave(SLAVE_ID,Serial,RS485_DERE);
#endif

//slave This is the name of the object being created from the Modbus class you can use it to manage communication with the Modbus master, including responding to read/write requests.
//(SLAVE_ID, Serial, RS485_DERE):
// The Serial object represents the default serial port on the Arduino, used for communication with the RS-485 transceiver.
// the RS485_DERE This is the digital pin connected to both the DE (Driver Enable) and RE (Receiver Enable) pins of the RS-485 transceiver module.

void setup()
{
  Serial.begin(9600);
  Serial.println("Arduino Modbus Slave");
  delay(5000);

  
  Serial.begin(9600);  //Init serial at 9600 baud
  #ifdef SWSERIAL_RX
  myserial.begin(9600);
  #endif
  uint16_t num5 = 4567;
  slave.start();
}



void loop()
{
  //Read commands from master
  // If a request is received, the slave decodes it and determines if the request is to read from or write to the holding registers.
  slave.poll(modbus_array,sizeof(modbus_array)/sizeof(modbus_array[0]));

  //sizeof(modbus_array)/sizeof(modbus_array[0]) This expression calculates the number of elements in the modbus_array.
  //required by the poll method to know how many registers it can read from or write to.

  int num1 = 187;
  int num2 = 100;
  int num3 = 49;
  int num4 = 8;
  uint16_t num5 = 4567;
  uint16_t num6 = 123;

  uint16_t valor1 = num1-int_min_value; //Manually converting from int to uint. To get back the actual value you should just subtract 32768 (and divide by 100)
  uint16_t valor2 = num2-int_min_value;
  uint16_t valor3 = num3-int_min_value;
  uint16_t valor4 = num4-int_min_value;

  //Grabamos data en los registros del array 
  modbus_array[0] = valor1; // el array debe ser uint16_t y no un int o float. si valor tiene decimales se debe * 100 para quitar decimales y luego / 100 para mostrar el valor original
  modbus_array[1] = valor2;
  modbus_array[2] = valor3;
  modbus_array[3] = valor4;
  modbus_array[4] = num5;
  modbus_array[5] = num6;

  // solo para DEBUG, no puede enviar texto al terminal serial porque modifica el payload
  //muestra el valor del registro 1 en uint
  //Serial.print("Register 1 (uint): "); 
  //Serial.println(modbus_array[0]); //

  // muestra el registro1 como entero
  //int num = (modbus_array[0]+int_min_value); //Convert from uint to int
  //Serial.print("Register 1 (int): ");
  //Serial.println(num);  // deberia mostrar 123

  delay(200);

}
