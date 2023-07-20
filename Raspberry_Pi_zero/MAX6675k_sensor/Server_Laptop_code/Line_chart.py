"""

Unique Approach
--------------

  For this file, data visualisation with pandas, I will use a different approach to develop a plot for line chart
  instead of pushing the temperature, humidity readings received directly into a deque and adding the timestamp
  I will leave this and from the Postgresql database I will download a certain window of data into a csv file. 

  Then from the csv file I will extact the columsn and their values. Then I will plot the line chart using the values generated

  this approach is better as it employs the whole component sof IOT of this project. Moreover, there is no need for special operations. 
  No need to add readings to the list and then sort the list...

  This code's approach 

    Node MCU --->Laptop---> Postgresql --->laptop = DataFrame format ---> plot

  Previous approach

       Node MCU  ---> laptop ----> postgresql
                           \
                            \
                             \ deque()----> sortdeque() --> plot 

"""

# library for TCP connection/ here used to establish/setup connection with Node MCU
import socket
# to display the readings obtained in a datbase, links python code to PostgreSQL database
import psycopg2

# library to deal with time, more comprehensive than the other 'time' library in python
# this library has time properties and also data, month and year
import datetime
# used to sketch graphs and diagrams to visualize data
import matplotlib.pyplot as plt
# library for specialised datatype containers, used here to create deque data types
from collections import deque
#import time
# import threading           #potential idea to be used
import numpy as np         # for numerical manipulations
# pandas library is used for data analysis and manipulation, here we will use it to access Postgresql database
import pandas as pd

import logging  # log messages should be used instead of the prosaic method print(), for future purposes
#import matplotlib

####### ------||||||-------||||-----------||||---------||||------|||||-------||||------//////--------\\\\\\-------||||--------|||||--------|||||#####

# The sole purpose of this file is to make the code organized in modules so that changes could be made easily without affecting the control flow

# ***********************************************************************************************************************************************#

# a queue for temperature, initialised as zero because here we want it to be a size of 10
tempqueue = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# otherwise, it would be difficult to manage a deque using append,pop() to get the graph we want
# a queue for timestamp, initialised as zero because here we want it to be a size of 10
timqueue = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# ---------->>>>>>>>> Database Parameters & connection setup <<<<<<<<-------------------

dbhost = 'localhost'     # because I am hosting the pgadmin table in the same laptop I am reading the values, my host name is "localhost" in postgresql
dbport = '5432'                     # default port for PostgreSQL
db = 'postgres'                     # default database name is postgres
# default database user name is postgres
dbuser = 'postgresql_username'
# PostgreSQL password to be established with the database
dbpassword = 'your_postgresql_password'
# datetime library is more comprehensive in that it includes dates, months and even years and that's why it is used
current_t = datetime.datetime.now()
# instead of the time library

# Establishing a connection to the database
conn = psycopg2.connect(host=dbhost, port=dbport,
                        database=db, user=dbuser, password=dbpassword)


# Creating a cursor object so that we can interact with a database
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS MAX6675_Raspberrypi (
        id serial PRIMARY KEY,
        Timestamp VARCHAR(150),
        Temperature VARCHAR(100)
    );
""")


# ---------->>>>>>>>> TCP wifi connection parameters <<<<<<<<------------------------------

host = "0.0.0.0"  # Listen on all available network interfaces
port = 0000      # Port number to listen on

# Creating a socket object, specifying that the type of socket is IPv4, and TCP type by the second argument
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print("Server started. Listening on {}:{}".format(host, port))
# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Client connected: {}".format(client_address))


# {{{{{{{{{{{{{{{     All the functions used in this program lie in between the curly braces

# ------------>>>>>>>>>>>>> Ploting the line chart using Matplotlib library <<<<<<<<<<<<-----------------------

""" The purpose of the function below is to plot the temperture readings obtained from the sensor

   parameters: None

   Output: None

   Dependencies: read_table() function that reads entries from the postgresql database and returns a data_frame 
"""


def plotting_function():

    # read_table() returns the latest 10 entries from the database and returns them as a dataframe that can be manipulated
    data_frame = read_table()
    # width and height of the figure to be displayed (which includes the plot)
    width = 800
    height = 800

    # this line resizes the whole figure in widthxheight pixels, indirectly also resizing the plot/graph
    plt.figure(figsize=(width, height))

    # the parameters below indicate how much should boundary value of the range of x or y, for instance if left = 0.1 indicates
    # the plot should range starting from 0.1 in the x-axis and the right = 0.9 indicates until 0.9 as the maximum reach
    # this range doesn't include the titles and axis labels so we should consider that. That's why the numbers aren't starting from 0 and going to 1
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.8)

    # providing the x-axis and y-axis values from the dataFrame. The values can be accessed by calling their column name.
    # dataFrames work similar to dictionary (because when the key is called the value associated with the key in a dictionary is provided)
    # only in this case the value is not just one value but a whole column
    try:
        plt.plot(data_frame['timestamp'],
                 data_frame['temperature'], marker="*")

        # labelling the x-axis, y-axis, title of the graph and ticks along the x-axis
        plt.title(" Temperature vs timestamp graph (10 second window)", fontdict={
            'fontsize': 18, 'fontstyle': 'italic'}, pad=10)
        plt.xlabel("Timestamp", color='red', fontdict={
            'fontsize': 18, 'fontstyle': 'italic'})
        plt.ylabel("Temperature reading", color='blue', fontdict={
            'fontsize': 18, 'fontstyle': 'italic'})
        plt.xticks(data_frame['timestamp'], rotation=45)
        # displaying the plot without any interruption for 9 seconds
        # this is an important parameter because it determines the gap that we desire between two readings
        # as its stands with plt.pause(4) a reading will be inserted into the database every 4 seconds
        plt.pause(4)
        plt.close()
    except:
        pass


# ------------>>>>>>>>>>>>> Accessing SQL data into dataFrame using Pandas  <<<<<<<<<<<<-----------------------
""" The purpose of this function is to read the latest 10 entries of the selected postgres table

   parameters: None
   Output: df --> a data frame type
   Dependency: None

"""


def read_table():
    # specifying the table I want to read and which columns from it
    sql_query = "SELECT timestamp, temperature FROM MAX6675_Raspberrypi"
    # Fetch data from the database using pandas
    df = pd.read_sql(sql_query, conn).tail(10)
    df['temperature'] = df['temperature'].astype(float)
    return df

# ------------>>>>>>>>>>>>> returns the time a data entry has been captured  <<<<<<<<<<<<-----------------------


def get_time_data_received():
   # Get the current local time
    current_time = datetime.datetime.now()
    time_string1 = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # Receive data from the client
    return time_string1

# ------------>>>>>>>>>>>>> Updates the database with the new entry received  <<<<<<<<<<<<-----------------------


def update_database(TimeStamp, Temperature):

    # we add the temperature value just received to the database with its timestamp. This will make sure that our database is being updated regularly
    cursor.execute(
        "INSERT INTO MAX6675_Raspberrypi (TimeStamp, Temperature) VALUES (%s, %s);", (TimeStamp, Temperature))
    conn.commit()


# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}


print("Time Stamp:           " + "Temperature reading")

while True:
    time_string = get_time_data_received()
    data = client_socket.recv(1024)
    if not data:
        # No more data, connection closed by client
        break
    # Process the received data as needed
    Temp = data.decode()   # give us string representation of the data it receives
    separator = ";"
    splitter = Temp.split(separator)
    # Send a response back to the client
    response = "Data received from the Node MCU esp8266"
    client_socket.sendall(response.encode())

    # Sample readings
    TimeStamp = time_string
    Temperature = splitter[0]
    print(TimeStamp + "       " + Temperature)

    plotting_function()
    update_database(TimeStamp, Temperature)


# ------------>>>>>>>>>>>>> Closing connections <<<<<<<<<<<<-----------------------
# Closing the connection
client_socket.close()
# Closing the cursor and database connection
cursor.close()
conn.close()
server_socket.close()
print("Server stopped.")
