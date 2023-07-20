
# a library to configure and read temperature and humidity values from the DHt11 sensor
import Adafruit_DHT
# a library that helps to establish a TCP connection within the existing
import socket

# Specify the pin to read readings from the DHT11
# This pin 15 is according to the CanaKit in the raspberrypi board I received
# so the number used here should be the literal beside the GPIO, for this case it was GPIO15
pin = 15

# ----------- <<< Establishing Wi-Fi connection, specifically TCP connection >>>--------------------------

# assigning server ip address and port numbers to variables
server_ip_address = 'server_address'
server_port_number = 0000

# establishing a socket object with the following specifications:
#      socket.AF_INET --> specifies IPV4 address family
#      socket.SOCK_STREAM --> specifies TCP connection, socket.SOCK_DGRAM would be used for UDP
client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# since the connect method takes only one argument we have to provide the address and port number as a tuple
client_connection.connect((server_ip_address, server_port_number))

# The purpose of this while loop is to continually read temperature and humidity values and send it to the sever
while True:
    # reading values by specifying the DHT sensor type as DHT11 and pin in the read_retry(11,pin) method
    humidity, temperature = Adafruit_DHT.read_retry(11, pin)

    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature: .2f} °C')
        print(f'Humidity: {humidity: .2f} %')
        data_to_be_sent = str(temperature)+";"+str(humidity)+";"
        data_to_be_sent = bytes(data_to_be_sent, 'utf-8')
        client_connection.sendall(data_to_be_sent)
    else:
        print('Failed to get reading from the sensor. ')

# if out of the loop we close the connection
client_connection.close()
