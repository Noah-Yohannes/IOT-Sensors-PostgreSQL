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


# creating the three deques that are to be displayed in the y-axis
# temperature readings list, initialised as size 10 with zero values as a placeholder for the
temp_que = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
timestamp_que = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # timestamp reading list
humidity_que = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # humidity reading lists
# this is to calculate the historical mean of the temperature reading
temperature_mean_que = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# this is to calculate the historical mean of the humidity reading
humidity_mean_que = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

count = 0  # counter that increments everytime a reading is received from the Node MCU esp 8266
# potential values to be put in the calibrated positions of the x-axis
x_tick_marker_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# A function that plots line chart of temperature and humidity readings with their respective timestamps.
def update_plot(time_stamp, heat_level, humidity, temp_que, timestamp_que, humidity_que):
    """
      Purpose: to plot temperature & humidity vs timestamp readings

      parameters: time_stamp (where temperature & humidity was received ) - type String
                  heat_level (a single temperature reading value) - type float
                  humidity (a single humidity reading value) - type float
                  temp_que (a deque storing previous 10 temperature readings) - type deque [int]
                  humidity_que (a deque storing previous 10 humidyty readings) - type deque[int]
                  timestamp_que (a deque storing previous 10 time stamps where readings were captured) - type deque [String]

      Return: No value to be returned from this function

      Major operations: 1. placing heat_level, humidity, and time_stamp in temp_que, humidity_que, timestamp_que.
                        2. Order the deques chronologically, based on timestamp. 
                        3. plotting the figure with its axes

    """

    global count  # declaring count as global so that we could use it inside

# 1.
    # the if-else block below purpose is to replace the placeholder (zero values) of the deque lists by the readings obtained
    # the two blocks are separated conditioned by the count to preserve the widow of 10 sample readings that we want to be displayed
    # when the line chart appears
    if (count <= 9):
        temp_que[count] = heat_level
        timestamp_que[count] = time_stamp
        humidity_que[count] = humidity
        count += 1
    else:
        modulus = np.mod(count, 10)
        temp_que[modulus] = heat_level
        timestamp_que[modulus] = time_stamp
        humidity_que[modulus] = humidity
        count += 1

    # So far, we have only substituted the oldest value. The points have to be dispalyed in a chronological order
    # so we need to sort the points interms of their timestamp
    print("To begin with the magnitude of count is : ")
    print(count)
    print("Unosrted temp_que is :")
    print(temp_que)

# 2 this stores the indices of timestamp_que when the values in it are sorted
    sorted_indices2 = np.argsort(timestamp_que)
    # using those indices we sort the timestamp_que
    sorted_timestamp_que = np.array(timestamp_que)[sorted_indices2]
    # using those indices we sort the temp_que
    sorted_temp_que = np.array(temp_que)[sorted_indices2]
    # using those indices we sort the humidity_que
    sorted_humidity_que = np.array(humidity_que)[sorted_indices2]
    print("After sorting the temp_que: ")
    print(sorted_temp_que)


# -------> Another approach is instead of replacing the cound index value we could replace the the first, that is the oldest entry from all the three
 #  ------->deques and then shift the list by one unit to the left and add these measurements at the end, then order . reconsider these alternatives


# -----------------------Plotting the Line chart ----------------------

    # plt.ion() is extremely important if we want our plot to be interactive
    # for instance, for the program to wait and close the window that appears after plt.show() without any human intervention
    #otherwise, it is impossible
    plt.ion()
    # gcf() is used to get a referrence to the current figure and we can manipulate it as required
    screen_width, screen_height = plt.gcf().canvas.get_width_height()
    width = 800                  # accordingly, we can change the width and height of the window
    height = 900

    # this determines the size of the figure as a whole by the dimensions of width and height
    plt.figure(figsize=(width, height))

    # subplots_adjust us the ability to manipulate the outlook of the plot and margins
    # this sets the starting position and ending position of both axes relative to the size of the figure
    # subplots_adjust treats the plot separately from the whole figure window that appears, consequently any change is of the plot relative to the figure

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.7)

    plt.plot(sorted_timestamp_que, sorted_temp_que, color="red", marker="*")

    plt.xlabel('Timestamp (Day - Hour:Minute:Second) of data',
               color="brown", fontdict={'fontsize': 20, 'fontstyle': 'italic'})
    plt.ylabel('Temperature (°C) ', color='red', fontdict={
        'fontsize': 20, 'fontstyle': 'italic'})
    # this allows us to plot another axis on the opposite of the y-axis while sharing the same x-axis with the plt.plot, just like a twin
    ax1 = plt.twinx()
    # we label this new twin, ax1 and all its entries except the x-axis which is named by the original plot which in our case is plt.plot()
    # all the rest main manipulations on the plot are done on the original plot, which is plt.plot()
    ax1.plot(sorted_timestamp_que, sorted_humidity_que,
             color="blue", marker="*", zorder=0)
    # a label text's outlook can be edited, the font size, color, type could be altered as below
    ax1.set_ylabel('Humidity ( % ) ', color='blue', fontdict={
        'fontsize': 20, 'fontstyle': 'italic'})

    # below we can set the title of the whole plot from the twin's side because it belongs to both ; however we can not
    # label the x-axis from the twin's object because when the twin is created it is created with an x-axis of its own that is invisible and hence
    # any change we make using ax1.xlabel() is being made on an invisible x-axis

    ax1.set_title("Temperature and Humidity readings of a DHT22 sensor",
                  color="black", fontdict={'fontsize': 25, 'fontstyle': "oblique"}, pad=20)

    # the first argument should be the values and positions we want to be ticked or marked
    plt.xticks(x_tick_marker_values, rotation=45, fontsize=29)
    #plt.yticks(y_tick_marker_values, rotation=0, fontsize=29)
    # another alternative to set the labels of a line chart is below

    # Adding a legend
    plt.legend()
    plt.show()
    plt.pause(2.5)
    plt.close()
# ------------------------ Plotting ends here ----------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ---->>>>>>>>> Database parameters | Table creation  <<<<<<<<---------#
# Connection parameters
# because I am displaying the pgadmin table in the same laptop I am reading the values
# localhost because I am working on my laptop as the server destination of the database
dbhost = "localhost"
dbport = "5432"     # default port number
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
    timestamp_for_plot = current_time.strftime("%d - %H:%M:%S")
    Temperature = float(heat)
    Humidity = float(humud)

    # calling the function to update the queues and plot the line chart
    update_plot(timestamp_for_plot, Temperature, Humidity,
                temp_que, timestamp_que, humidity_que)

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
