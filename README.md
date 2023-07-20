# IOT-Sensors-PostgreSQL

- An IOT system for two devices: the Node_mcu_esp8266 and the Raspberry_Pi_zero_W/WH. For each device, the DHT11 and the MAX6675K sensors were used.
- Humidity values were obtained from the DHT11 sensor, and temperature values were obtained from the MAX6675K sensor and the DHT11 sensor.
- The readings obtained were sent to a server (laptop in this case) through shared wifi (mobile hotspot).
- Once the data was received in the server it is put in a **PostgreSQL** database.
- The data is also displayed in line charts and scatter plots using the *Matplotlib* library using different approaches.


## **Hierarchy**
        -             Node_mcu_esp8266                                     Raspberry_Pi_Zero_W/WH
                      /             \                                          /         \
                     /               \                                        /           \
                DHT11              MAX6675K                               DHT11          MAX6675K
              /      \               /     \                              /    \          /       \
           Client   Server       Client   Server                    Client    Server     Client   Server
     (Arduino_IDE)  (laptop) (Arduino_IDE)   (laptop)              (Python)   (laptop)  (Python)  (laptop)


## **Dependencies & Libraries**

- Node_mcu_esp8266:
         - Client's code (in Arduino IDE): = 'WiFiClient.h', 'ESP8266WiFi.h', 'DHT.h', 'max6675.h', 'ESP8266WebServer.h' 
         - Server's code (Laptop) = 'socket', 'psycopg2','datetime', 'collections', 'numpy', 'matplotlib', 'pandas', 'logging'
- Raspberry_Pi_Zero_W/WH:
          - Client's code (Python): 'spidev', 'time', 'sys', 'socket'
          - Server's code (Laptop): 'socket', 'psycopg2','datetime', 'collections', 'numpy', 'matplotlib', 'pandas', 'logging'

  ## Author
   - Noah Yohannes
   - GitHub: [Noah-Yohannes](https://github.com/Noah-Yohannes)
   - Email: NoahYohannesWoldegiorgish@gmail.com 
  


