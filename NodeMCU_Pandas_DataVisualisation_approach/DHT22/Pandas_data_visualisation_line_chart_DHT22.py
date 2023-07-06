# Mention what is included in this code:
# 1. How to use deques()
# 2. How to manipulate and control overview of a plot
# 3.
# 4.
# 5.
#
import socket  # library for TCP connection
import psycopg2  # to display the readings obtained in a datbase
import datetime  # library to get timestamp, provides in a year,month,date,hour,minute,second format
# a class of special containers of data types, and we will use deque, a queue which can be manipulated from both sides
# deques are special datatypes that posses the properties of queue data structures and list data types in python
from collections import deque
import numpy as np                     # for numberical manipulation
import matplotlib.pyplot as plt         # library to plot the line chart we want
import pandas as pd
import matplotlib            # for plotting, explore the difference of explicitly importing a library such as matplotlib.pyplot and the library generally as in this case
import logging              # for future references


# _______________________This part enclosed can be skipped, I just included it to make it more interactive________________________________

window_size = 10  # default sample size to be displayed
# asking user if they want to change the sample size from 10
choice = input(
    "Do you want to display temperature and humudity readings for more than 10 samples? y/n")

# if their choice is yes asks for the new sample size, else it continues
if choice == "y":
    window_size = input(
        "Please enter how many temperature readings do you want to display")
    window_size = int(window_size)
# _______________________________________________________________________________________________________________________________________________


# ---->>>>>>>>> Database parameters | Table creation  <<<<<<<<---------#
# Connection parameters
# because I am displaying the pgadmin table in the same laptop I am reading the values
dbhost = "your_host_name"
dbport = "database_port_being_used"
db = "database_name"
dbuser = "database_user_name"
dbpassword = "Your_database_password"


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

# ---->>>>>>>>> TCP wifi connection parameters<<<<<<<<---------

host = "0.0.0.0"  # Listen on all available network interfaces
port = 0000      # Port number to listen on/ should be changed to fit your PC free port number and must match the port in arduino IDE
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
    #timestamp_for_plot = current_time.strftime("%d - %H:%M:%S")
    Temperature = float(heat)
    Humidity = float(humud)

# ---->>>>>>>>> Accessing data from the Postgresql database and create a dataframe <<<<<<<<---------

    # specifying the details of the columns and the table from which we want to extract data, just a string but will be used in the next command
    sql_connection = (
        "SELECT timestamp, temperature, humidity FROM DHT22_nodemcu_table")

    # here we are using pandas to read from an sql and the conn object to communicate with the database using psycopg2 library
    # the .tail(10) will give us the last 10 rows, the latest readings. We are going to use those latest 10 entries to plot the graph, relevant and up-to-date.
    df = pd.read_sql(sql_connection, conn).tail(window_size)

    # to avoid unordered temperature values in the y-axis we make sure that temperature readings are in float data type; otherwise only latest temperature readings
    # that are lower values will be on higher level in the y-axis (because matplotlib.pyplot will simply interpret them as strings unless mentioned as float)
    df['temperature'] = df['temperature'].astype(float)
    df['humidity'] = df['humidity'].astype(float)
    # df['timestamp'] = df['timestamp'].astype("string")  because it is being saved as varchar() it is a string, so no need to specify


# ------------>>>>>>>>>>>>> Ploting the line chart using Matplotlib library <<<<<<<<<<<<-----------------------

    width = 800
    height = 800
    # resizes figure as a whole, that's why it is plt.figure(). Indirectly, the plot also is resized maintaining its proportions
    plt.ion()
    plt.figure(figsize=(width, height))

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.8)
    plt.plot(df['timestamp'], df['temperature'], marker=".", color="red")
    plt.xlabel(" Timestamp", fontdict={'fontsize': 20, 'fontstyle': 'oblique'})
    plt.ylabel(" Temperature (°C)", fontdict={
               'fontsize': 20,  'fontstyle': 'oblique'}, color='red')

    # Now ploting the humidity readings on the same plot but on a mirroring y-axis
    ax1 = plt.twinx()
    ax1.plot(df['timestamp'], df['humidity'], marker=".", color="blue")
    ax1.set_ylabel("Humidity (%)", fontdict={
        'fontsize': 20, 'fontstyle': 'oblique'}, color='blue')
    ax1.set_title(" Temperature, Humidity vs timestamp", fontdict={
        'fontsize': 22, 'fontstyle': 'italic'}, color="brown", pad=20)
    plt.xticks(rotation=45)

    plt.show()
    plt.pause(3.5)
    plt.close()

    # calling the function to update the queues and plot the line chart
    # update_plot(timestamp_for_plot, Temperature, Humidity,
    #           temp_que, timestamp_que, humidity_que)

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
