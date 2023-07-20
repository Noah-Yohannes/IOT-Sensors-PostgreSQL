
# library for TCP connection/ here used to establish/setup connection with Node MCU
import socket
# to display the readings obtained in a datbase, links python code to PostgreSQL database
import psycopg2
import datetime
# used to sketch graphs and diagrams to visualize data
import matplotlib.pyplot as plt
# library for specialised datatype containers, used here to create deque data types
from collections import deque
import time
# import threading           #potential idea to be used
import numpy as np         # for numerical manipulations


####### ------||||||-------||||-----------||||---------||||------|||||-------||||------//////--------\\\\\\-------||||--------|||||--------|||||#####
# organise map of the functions and parts used, lean and clean code (to be filled later)

# also mentioned involved concepts overall the code: Threading, matplotlib,_ _ _ (to be filled later)

# ************************************************************************This requires a new mindset**************************************************#

# a queue for temperature, initialised as zero because here we want it to be a size of 10
tempqueue = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# otherwise, it would be difficult to manage a deque using append,pop() to get the graph we want
# a queue for timestamp, initialised as zero because here we want it to be a size of 10
timqueue = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

count = 0           # is to count how many of the queue entries have been updated/visited
x_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# the purpose of this function is to update the list containing temperature and timestamp values
def update_plot(Te, Ts, temperat, timest):
    # declaring count as global so that it could be used in this function as well
    global count
    #print("count is ")
    # print(count)
    #print("The value of count is")

    # this visualisation will present a graph with a line graph of 10 time stamps in the x-axis, and their corresponding temperature readings in the y-axis

    # The if-block below's purpose is to replace the values previously initialized values as 0 by the reading we first receive we do this for the first 10 samples
    # then as the count exceeds 10 we will compute the modulus and in consequently we are the oldest timestamp and its corresponding temperature reading will be
    # substituted with new value we have received. For instance, when count = 14 we will be replacing the 4th sample (mod(14,10))
    if (count <= 9):
        Te[count] = temperat  # substituting the temperature
        Ts[count] = timest  # substituting the timestamp
        count = count + 1
    else:
        # if already all the 10 elements have been updated from zero to real value
        # we update them using the modulus of count by replacing the earliest timestamp
        modulus = np.mod(count, 10)

        # Te.popleft()               this line caused the program to terminate after only displaying 10 samples because it didn't match the, in other words it had less elements than the sorted numpy array
        Te[modulus] = temperat  # substituting the temperature
        Ts[modulus] = timest  # substituting the timestamp
        count = count + 1            # still count should increase

    # print(Te)  for debugging purpose
    # print(Ts)  for debugging purpose

# ---->>>>>>>>>  Sorting the temperature and timestamp deques and preserving their correspondence   <<<<<<<<---------

# Even though we have replaced the earliest timestamp the X-axis values are still out of order and values were overlapping
# some even going back in time, also temperatures were overlapping, so before plotting the values the two deques(lists) must be sorted without loosing their correspondence

  # The code below does just that
    # argsotrt returns an array of indexes when the values are storted, sorted_indices
    sorted_indices = np.argsort(Ts)
    # to be noted that in this case we are sorting in terms of their timestamp it could be other factor for other instance

    # Sort Ts and rearrange Te accordingly using the sorted indices
    # np.array(Ts) converts the array Ts into a numpy array, easier for manipulation. Then sortes it in the order of the indexes of sorted_indices
    Ts_sorted = np.array(Ts)[sorted_indices]
    # this part preserves the correspondence between the timestamp and temperature values because they are being sorted
    # in the same order
    Te_sorted = np.array(Te)[sorted_indices]

# ---->>>>>>>>>>>>>>>>>>>>>>>>>>>>  Plotting the Line Chart   <<<<<<<<<<<<<----------------------------------------------

    plt.ion()           # this is the key that makes a plot interactive. As a result the compiler proceeds executing after executing the plt.show() line below
    # otherwise no other instruction below it is executed unless a user everytime manually closes the plot window. This is because plt.show() is a blocking
    # function, it stops the program from executing any other instruction.

    # we can get the size of the screen using this line
    screen_width, screen_height = plt.gcf().canvas.get_width_height()
    # gcf() is used to get a referrence to the current figure and we can manipulate it as required
    width = 800                  # accordingly, we can change the width and height of the window
    height = 800
    # this determines the size of the figure as a whole by the dimensions of width and height
    plt.figure(figsize=(width, height))
    # adjusts the margins of the graph
    plt.subplots_adjust(left=0.3, right=0.9, bottom=0.3, top=0.7)
    # this creates a 'figure' by default, the first argument is for x-axis, second for y-axis and the '*' as point indicator
    plt.plot(Ts_sorted, Te_sorted, marker='*')
    # title of the line chart
    plt.title('Temperature reading line chart')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature reading')
    # as its name indicates puts ticks, marker, sign in the x_values positions specified above at an angle 45 degrees
    plt.xticks(x_values, rotation=45)
    plt.show()  # when the figure, plot  is manifested/displayed


# ---->>>>>>>>>>>>>>>>>>>>>>>>>>>>  Plotting the Line Chart   <<<<<<<<<<<<<----------------------------------------------

    # The code below is to make the popping up rate of the plot convenient: it should quickly show normally but when the modulus is 9, that is when the 10 samples
    # window is almost filled the user should be able to see it for a little bit longer time this way the data could be visualised better
    rateOfRefresh = np.mod(count, 10)
    if (rateOfRefresh == 9):
        plt.pause(8)
    else:
        plt.pause(1)
    plt.close()
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ----------->>>>>>>>>>>>>>>>> Database parameters | Establishing connection | Creating a table <<<<<<<<<<<<<<<---------------------

dbhost = "localhost"  # because I am hosting the pgadmin table in the same laptop I am reading the values, my host name is "localhost" in postgresql
dbport = "5432"                     # default port for PostgreSQL
db = "postgres"                     # default database name is postgres
# default database user name is postgres
dbuser = "postgresql_username"
# PostgreSQL password to be established with the database
dbpassword = "Your_postgresql_password"
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
    CREATE TABLE IF NOT EXISTS MAX6675 (
        id serial PRIMARY KEY,
        Timestamp VARCHAR(150),
        Temperature VARCHAR(50)
    );
""")

# ---->>>>>>>>> TCP wifi connection parameters<<<<<<<<---------

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
print("Time Stamp:           " + "Temperature reading")
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
    Temp = data.decode()   # the problem lies here in that it combines
    separator = "~"
    splitter = Temp.split(separator)

    # Send a response back to the client
    response = "Data received from the Node MCU esp8266"
    client_socket.sendall(response.encode())

    # Sample readings
    TimeStamp = time_string
    stampDisplay = current_time.strftime("%d-%H:%M:%S")
    Temperature = splitter[0]
    print(TimeStamp + "       " + Temperature)


# calling update_plot to add this temperature reading to the list and plot it
    update_plot(tempqueue, timqueue, Temperature, stampDisplay)

    # adding the entry to the database
    cursor.execute(
        "INSERT INTO MAX6675 (TimeStamp, Temperature) VALUES (%s, %s);", (TimeStamp, Temperature))
    conn.commit()


# Closing the connection
client_socket.close()
# Closing the cursor and database connection
cursor.close()
conn.close()
server_socket.close()
print("Server stopped.")
