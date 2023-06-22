#include <DHT.h>
// #define data 2
#define DHTTYPE DHT22
const int data = 2;
DHT dht(data, DHTTYPE);

//wifi related imports
#include <ESP8266WiFi.h>    //main and extensive library that controls wifi connectivity of the esp8266
#include <WiFiClient.h>    //to set the NodeMCU_esp8266 as a client sending data

// WiFi parameters to be configured
const char* ssid = "Galaxy M31"; // Write here your router's username
const char* password = "87654321"; // Write here your router's passward
const char* serverIP = "192.168.107.137";  //the IP address of the server
int serverPort = 5095;  //  port number of the server

WiFiClient client;       //declare a client object to be used in all client side manipulations concerning wifi


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);   // very important not setting this made the serial monitor display unreadable text because the received bit were read in an incorrect way
  dht.begin();
  pinMode(data, INPUT);

  WiFi.mode(WIFI_STA); //setting WiFi mode as station, to be sure. This makes sure that the NodeMCU sends dat and not just act as a router
  WiFi.begin(ssid,password);    //the device will start to connect to WiFi

   //the loop below is for aesthetic purpose and can be removed
   //it displays '.' when trying to connect to WiFi
   //while wifi not connected yet, print '.'
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  //printing new line, then print WiFi connected message and the IP address
  Serial.println("");
  Serial.println("WiFi connected");
  // Print the IP address
  Serial.println(WiFi.localIP());

  //the above block purpose is for the programmer to see if the connection is successful
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
  }
  else {
    Serial.println("Connection failed");
  }
}

void loop() {
  // put your main code here, to run repeatedly:

    //humudity and temperature
  float humidity = dht.readHumidity();            //read humudity levels from the DHT11 sensor
  float temperature = dht.readTemperature();       //read humudity levels from the DHT11 sensor

  //temperature = (5*(temperature -32))/9;


  Serial.print("The temperature of the surrounding is: ");
  Serial.print(temperature);
  Serial.println("°C");
  delay(1000);
  Serial.println(" ");
  Serial.print("The humudity of the surrounding is: ");
  Serial.print(humidity);
  Serial.println(" % ");
  delay(1000);

  //Now we want to send temperature and humidity readings to a remote device or our laptop
  //but the client.print takes only one argument so we combine the two values
  String data_to_be_sent = String(temperature) +";" + String(humidity); //the purpose of the ";" is so that the values could be separated on the receiver's side
  client.print(data_to_be_sent);            //just as we print to the serial monitor using serial.print
                                            //when sending message through WiFi as a client we use client.print()
    
}
