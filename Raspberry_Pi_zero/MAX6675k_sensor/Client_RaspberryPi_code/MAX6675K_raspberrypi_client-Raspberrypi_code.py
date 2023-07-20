

""" This program is for reading temperature readings from the MAx6675k sensor in the raspberry pi zero W/WH and sending 
the reading through Wi-Fi to the server/laptop """

import spidev
import time
import sys  # this is just imported for testing purpose
import socket

# Set the SPI bus and device (0, 0) for SPI-0 bus and CE0 device
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# Set the wifi connection parameters
server_ip_address = 'Server_address'
server_port_number = 0000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip_address, server_port_number))


def read_temperature():
    # The MAX6675K requires a dummy byte to read the temperature
    dummy = 0x00
    raw = spi.xfer2([dummy, dummy])
    # Extract the temperature value from the received data
    temp = ((raw[0] << 8 | raw[1]) >> 3) * 0.25

    return temp


try:
    while True:
        temperature = read_temperature()
        print(f"Temperature: {temperature} °C")
        s = str(temperature) + ";"
        b = bytes(s, 'utf-8')
        client_socket.sendall(b)
        time.sleep(1)

except KeyboardInterrupt:
    # Press Ctrl+C to exit the loop and close the SPI device
    spi.close()
    client_socket.close()
