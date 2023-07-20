


#include <max6675.h>
#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
//#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager​
#include <WiFiClient.h>
//#include <WiFiUdp.h>               //this library I think is to send the string that I want using the UDP protocol now there is no need because 
//WiFiClient.h is already setting up a TCP connection
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Wire.h>

#define refresh = 3; //this will determine how often temperature is read

//WiFiServer server(80);
// WiFi parameters to be configured
const char* ssid = "LAN_network"; // Write here your router's username
const char* password = "password"; // Write here your router's passward
const char* serverIP = "server_address";  //the IP address of the server  
int serverPort = 0000;  //  port number of the server


//what is the difference if we declare it as wifiserver or wificlient. I think if it is a server it is in either A or mode

// initialize the pins to be used as clock, chip select and data
int CLK = D3;
int CS = D2; 
int data = D4;

// Create a MAX6675 object, which is thermocouple
 MAX6675 thermocouple(CLK, CS, data);
 float temperature;   //to read temperature 

 WiFiClient client;  //always initialize an object of a library or a class to use it in the code

 
void setup() {
  //setting the baud rate of the MAX6675 so that the data can be correctly displayed in the serial monitor:
  WiFi.mode(WIFI_STA);
  Serial.begin(9600);
  Serial.print("Connecting to ");
  Serial.println(ssid);

  //Connecting the Node MCU esp8266 to the WiFi
  WiFi.begin(ssid, password);
  //while wifi not connected yet, print '.'
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  //print a new line, then print WiFi connected and the IP address
  Serial.println("");
  Serial.println("WiFi connected");
  // Print the IP address
  Serial.println(WiFi.localIP());


  // Connecting the esp8266 to the server which is the laptop
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
  }
  else {
    Serial.println("Connection failed");
  }
}

void loop() {
  
  if (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print("Oh no! something is wrong");
  }
  // Read the temperature from the sensor in degree celsius
  temperature = thermocouple.readCelsius();
  // print the temperature on the Serial Monitor.
  Serial.print("The temperature at this moment is: ");
  Serial.println(temperature);
  //1 second delay 
  //client.send("");
  delay(1000);
  //Serial.println("The local Ip of the Node MCU esp8266 is : ");
  //Serial.println(client.localIP());
  //Serial.println("The local port number of the Node MCU esp8266 is : ");
 // Serial.println(client.localPort());
  // Serial.println("Sending the temperature reading to the Laptop");

  String sending_data =  String(temperature)+"~" ;

  client.print(sending_data);
  delay(1000);
  Serial.println("Data sent to the laptop");
}

// void sendTemp(){
// }





