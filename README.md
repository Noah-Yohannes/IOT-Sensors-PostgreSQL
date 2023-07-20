# IOT-Sensors-PostgreSQL

- An IOT system for two devices: the Node_mcu_esp8266 and the Raspberry_Pi_zero_W/WH. For each device, the DHT11 and the MAX6675K sensors were used.
- Humidity values were obtained from the DHT11 sensor, and temperature values were obtained from the MAX6675K sensor and the DHT11 sensor.
- The readings obtained were sent to a server (laptop in this case) through shared wifi (mobile hotspot).
- Once the data was received in the server it is put in a PostgreSQL database.
- The data is also displayed in line charts and scatter plots using the *matplotlib* library using different approaches. 

