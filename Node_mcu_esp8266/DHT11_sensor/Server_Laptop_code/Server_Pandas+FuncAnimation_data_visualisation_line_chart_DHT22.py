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
import matplotlib
import pandas as pd
# to dynamically draw a plot
import matplotlib.animation as animationi
import logging              # for future references


# ---->>>>>>>>> Database parameters | Table creation  <<<<<<<<---------#
# Connection parameters
# because I am displaying the pgadmin table in the same laptop I am reading the values

dbhost = "localhost"
dbport = "5432"  # default port number for postgresql
db = "postgres"
dbuser = "postgres_username"
dbpassword = "Your_postgress_password"

count = 0


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
port = 0000      # Port number to listen on
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

print("Time Stamp:           " + "Humidity" + "  Temperature")

# If the funcanimation is to be used then the while loop have to disposed of


# specifying the details of the columns and the table from which we want to extract data, just a string but will be used in the next command
sql_connection = (
    "SELECT timestamp, temperature, humidity FROM DHT22_nodemcu_table")

# ---->>>>>>>>> Accessing data from the Postgresql database and create a dataframe <<<<<<<<---------
#
# here we are using pandas to read from an sql and the conn object to communicate with the database using psycopg2 library
# the .tail(10) will give us the last 10 rows, the latest readings. We are going to use those latest 10 entries to plot the graph, relevant and up-to-date.

df = pd.read_sql(sql_connection, conn).tail(10)

# to avoid unordered temperature values in the y-axis we make sure that temperature readings are in float data type; otherwise only latest temperature readings
# that are lower values will be on higher level in the y-axis (because matplotlib.pyplot will simply interpret them as strings unless mentioned as float)
temp = df['temperature'].astype(float)
humi = df['humidity'].astype(float)
tim = df['timestamp']
# df['timestamp'] = df['timestamp'].astype("string")  because it is being saved as varchar() it is a string, so no need to specify
width = 600
height = 800
# resizes figure as a whole, that's why it is plt.figure(). Indirectly, the plot also is resized maintaining its proportions

fig = plt.figure(figsize=(width, height))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.8)
ax1 = fig.add_subplot(111)
line, = ax1.plot(tim, temp, marker="o", color="red")

"""
        Try the approach specified in the line below (this is a food for thought):

        # just for testing try ax2= fig.add_subplot(112) we could display the humudity values in two plots in one window

"""

# jad java command line that generates source code after 90%. What does it do?

ax2 = ax1.twinx()
# here we will use set_xlim to reverse the orientation of ax2. We exploited the set_xlim function by reversing the minimum and maximum
# but we didn't specify and we just converted the
ax2.set_xlim(ax1.get_xlim()[::-1])
line2 = ax2.plot(tim, humi, marker="o", color="blue")[0]
plt.title("Temperature and Humidity vs timestamp")
ax1.set_xlabel(" Timestamp")
ax1.set_ylabel(" Temperature (°C)", fontdict={
    'fontsize': 20,  'fontstyle': 'oblique'}, color='red')
ax2.set_ylabel("Humidity (%)", fontdict={
    'fontsize': 20, 'fontstyle': 'oblique'}, color='blue')

# The two lines below, set_label() is just used to set the text what will be used as a legend for the subplots

line.set_label("Temperature")
line2.set_label("Humidity")

# creating legend in the plot for both subplots
ax1.legend([line, line2], [line.get_label(), line2.get_label()], loc=1)


def animation_attempt(frame):
    print("It has gone inside the animation_attempt")

    # Get the current local time
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # Receive data from the client
    data = client_socket.recv(1024)

    print(" checking if there is even a data/reading obtained")
    if not data:
        # No more data, connection closed by client
        # it was break before, but break can only be used in a loop in python so i substituted it with return because it will end the function
        print("Well there is nothing this season")
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

# ------------>>>>>>>>>>>>> Ploting the line chart using Matplotlib library <<<<<<<<<<<<-----------------------
    print("Now going to deal with database")
    # specifying the details of the columns and the table from which we want to extract data, just a string but will be used in the next command
    sql_connection2 = (
        "SELECT timestamp, temperature, humidity FROM DHT22_nodemcu_table")

    # ---->>>>>>>>> Accessing data from the Postgresql database and create a dataframe <<<<<<<<---------
    #
    # here we are using pandas to read from an sql and the conn object to communicate with the database using psycopg2 library
    # the .tail(10) will give us the last 10 rows, the latest readings. We are going to use those latest 10 entries to plot the graph, relevant and up-to-date.
    print("Obtaining dataframes")
    d = pd.read_sql(sql_connection2, conn).tail(10)

    # to avoid unordered temperature values in the y-axis we make sure that temperature readings are in float data type; otherwise only latest temperature readings
    # that are lower values will be on higher level in the y-axis (because matplotlib.pyplot will simply interpret them as strings unless mentioned as float)
    temp_array = d['temperature'].astype(float)
    humidity_array = d['humidity'].astype(float)
    time_array = d['timestamp']

   # updating the label on the x-axis
    line.set_xdata(time_array)
    line.set_ydata(temp_array)
    line2.set_ydata(humidity_array)

    # Insert the readings into the table
    cursor.execute(
        "INSERT INTO DHT22_nodemcu_table (TimeStamp, Temperature, Humidity) VALUES (%s, %s, %s);", (TimeStamp, Temperature, Humidity))
    conn.commit()

    return line, line2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
# by setting blit = True parameter we are optimizing our code, the compiler will compare the previous frame and current frame state
# and will only change the values that have been changed not the whole plot


anime = animationi.FuncAnimation(fig, animation_attempt, frames=100,
                                 interval=20, blit=True, repeat=True)   # remove blit = True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``


# Close connections and cleanup
def cleanup():
 # Close the connection
    client_socket.close()
# Close the cursor and database connection
    cursor.close()
    conn.close()
    server_socket.close()
    print("Server stopped.")


# Register the cleanup function to be called when the animation ends or is manually stopped


plt.show()
print("After vising plt.show() wow wow")
