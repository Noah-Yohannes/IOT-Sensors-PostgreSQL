

import socket  # library for TCP connection
import psycopg2  # to display the readings obtained in a datbase
import datetime


# TCP wifi connection parameters
host = "0.0.0.0"  # Listen on all available network interfaces
port = 0000     # Port number to listen on

# Database Parameters
# Connection parameters
# because I am displaying the pgadmin table in the same laptop I am reading the values
dbhost = "localhost"
dbport = "5432"  # default port number
db = "postgres"
dbuser = "postgresql_username"
dbpassword = "Your_postgresql_password"  # ezia kab zkone seb hibaya


# Establishing a connection to the database
conn = psycopg2.connect(host=dbhost, port=dbport,
                        database=db, user=dbuser, password=dbpassword)
# Create a cursor object
# the purpose of the cursor object is to select and do operations in the PostgreSQL.
cursor = conn.cursor()
# as its name indicates it allows you to select what you want to do and then we can execute anything we want

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DHT22_nodemcu_table (
        id serial PRIMARY KEY,
        Timestamp VARCHAR(150),
        Temperature VARCHAR(50),
        Humidity VARCHAR(50)
    );
""")

# Create a socket object
# specifying that the type of socket is IPv4, and TCP type by the second argument
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print("Server started. Listening on {}:{}".format(host, port))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Client connected: {}".format(client_address))

print("Time Stamp:           " + "Humudity" + "  Temperature")


while True:
    # Get the current local time
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # Receive data from the client
    data = client_socket.recv(1024)

    if not data:
        # No more data, connection closed by client
        break
    # Process the received data as needed
    temporary = data.decode()
    separator = ";"
    splitted = temporary.split(separator)
    heat = splitted[0]
    humud = splitted[1]

    print(time_string+"           "+heat + "    " + humud)

    # Send a response back to the client
    response = "Data received from the Node MCU esp8266"
    client_socket.sendall(response.encode())

    # Sample readings
    TimeStamp = time_string
    Temperature = heat
    Humidity = humud

    # Insert the readings into the table
    cursor.execute(
        "INSERT INTO DHT22_nodemcu_table (TimeStamp, Temperature, Humidity) VALUES (%s, %s, %s);", (TimeStamp, Temperature, Humidity))
    conn.commit()


# Close the connection
client_socket.close()
# Close the cursor and database connection
cursor.close()
conn.close()
server_socket.close()
print("Server stopped.")
