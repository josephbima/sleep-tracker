# -*- coding: utf-8 -*-
"""
This Python script receives incoming unlabelled accelerometer data through 
the server and uses your trained classifier to predict its class label.

"""

import socket
import sys
import json
import threading
import numpy as np
import pickle
from features import extract_features # make sure features.py is in the same directory
from util import reorient, reset_vars
from datetime import datetime
import time
from prettytable import PrettyTable


# TODO: Replace the string with your user ID
user_id = "team-jj"
# TODO: list the class labels that you collected data for in the order of label_index (defined in collect-labelled-data.py)
class_names = ["vigil", "sleeping"] #...

send_socket = None

hourly_array = []
all_time_array = []

activity_detection_table = PrettyTable()
activity_detection_table_columns = ['Activity','Timestamp']

# Loading the classifier that you saved to disk previously
with open('classifier.pickle', 'rb') as f:
    classifier = pickle.load(f)
    
if classifier == None:
    print("Classifier is null; make sure you have trained it!")
    sys.exit()

    
def onActivityDetected(activity):
    """
    Notifies the user of the current activity
    """
    global hourly_array, all_time_array, activity_detection_table

    time = datetime.now()

    act = { "activity":activity, "time": str(time) }

    hourly_array.append(act)

    # print("Pushed ")
    # print(act)

    data = []

    # if it has been an hour, count how many sleep and vigil activities detected
    HOUR_PERIOD =  12
    QUARTER_HOUR_PERIOD = 3

    # Change to HOUR_PERIOD to use hour periods analysis, using 15 minute periods for testing purpouses only
    if(len(hourly_array) == QUARTER_HOUR_PERIOD):

        sleep_count = 0
        vigil_count = 0

        for e in hourly_array:
            if e["activity"] == "sleeping":
                sleep_count = sleep_count + 1
            else:
                vigil_count = vigil_count + 1
            
            data.append(e)
        
        # print("Sleep count detected: %s \n Vigil count detected: %s", (sleep_count,vigil_count))
        
        hourly_array = []

        sleep_percentage = sleep_count/(sleep_count+vigil_count)

        sleep_percentage_str = "{:.2%}".format(sleep_percentage)

        sleeping_description = ''

        threshold = 0.10

        if sleep_percentage > 0.75-threshold:
            sleeping_description = "Sleeping with minimal movement"
        elif sleep_percentage > 0.55-threshold and sleep_percentage < 0.75 - threshold:
            sleeping_description = "Sleeping with a lot of movements"
        elif sleep_percentage > 0.40 - threshold and sleep_percentage <  0.55 - threshold:
            sleeping_description = "A lot of movement, possibly not asleep or only partially"
        elif sleep_percentage < 0.4 - threshold:
            sleeping_description = "A lot of movement, most likely not asleep"
        

        sleep_analysis = {"sleep_count": sleep_count, "vigil_count": vigil_count, "sleep_percentage": sleep_percentage_str, "sleep_description": sleeping_description, "sleep_data": data}

        # print("Pushing to all_time", sleep_analysis)

        all_time_array.append(sleep_analysis)
    

    activity_detection_table.add_row([activity,time.strftime('%H:%M:%S, %A - %d %M %Y')])
    print(activity_detection_table)

    # print("Detected activity: " + activity + " Time: " + str(time))

def predict(window):
    """
    Given a window of accelerometer data, predict the activity label. 
    """
    
    # TODO: extract features over the window of data
    feature_names, feature_vector = extract_features(window)
    
    # TODO: use classifier.predict(feature_vector) to predict the class label.
    # Make sure your feature vector is passed in the expected format
    class_label = int((classifier.predict(feature_vector.reshape(1,-1)))[0])

    # TODO: get the name of your predicted activity from 'class_names' using the returned label.
    # pass the activity name to onActivityDetected()
    class_name = class_names[class_label]

    onActivityDetected(class_name)
    
    # return
    

#################   Server Connection Code  ####################

'''
    This socket is used to receive data from the data collection server
'''

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.connect(("none.cs.umass.edu", 8888))
# ensures that after 1 second, a keyboard interrupt will close
receive_socket.settimeout(1.0)

msg_request_id = "ID"
msg_authenticate = "ID,{}\n"
msg_acknowledge_id = "ACK"

def create_send_socket():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect(("none.cs.umass.edu", 9999))
    print("Authenticating user for receiving data...")
    sys.stdout.flush()
    authenticate(send_socket)
    return send_socket

def send_message(tag, data):
    """
    Notifies the client.
    
    For example, to send reps back to the phone, call `send_message('REP', timestamp)`
    when your algorithm detects a repetition.
		
		Make sure you first create a send socket with `send_socket = create_send_socket()`
		in the main program.
    """
    global send_socket
    json_msg = ''
    json_msg = json.dumps({'user_id' : user_id, 'sensor_type' : 'SENSOR_SERVER_MESSAGE', 'message' : tag, 'data': data}) + '\n'
    json_msg = json_msg.encode('utf-8')
    send_socket.send(json_msg)

def authenticate(sock):
    """
    Authenticates the user by performing a handshake with the data collection server.
    
    If it fails, it will raise an appropriate exception.
    """
    message = sock.recv(256).strip().decode('ascii')
    if (message == msg_request_id):
        print("Received authentication request from the server. Sending authentication credentials...")
        sys.stdout.flush()
    else:
        print("Authentication failed!")
        raise Exception("Expected message {} from server, received {}".format(msg_request_id, message))
    sock.send(msg_authenticate.format(user_id).encode('utf-8'))

    try:
        message = sock.recv(256).strip().decode('ascii')
    except:
        print("Authentication failed!")
        raise Exception("Wait timed out. Failed to receive authentication response from server.")
        
    if (message.startswith(msg_acknowledge_id)):
        ack_id = message.split(",")[1]
    else:
        print("Authentication failed!")
        raise Exception("Expected message with prefix '{}' from server, received {}".format(msg_acknowledge_id, message))
    
    if (ack_id == user_id):
        print("Authentication successful.")
        sys.stdout.flush()
    else:
        print("Authentication failed!")
        raise Exception("Authentication failed : Expected user ID '{}' from server, received '{}'".format(user_id, ack_id))


try:

    

    print("Authenticating user for receiving data...")
    sys.stdout.flush()
    authenticate(receive_socket)
    
    print("Successfully connected to the server! Waiting for incoming data...")

    sys.stdout.flush()

    global time_activated

    time_activated = datetime.now()


    print("Time activated: ", time_activated.strftime('%H:%M:%S, %A - %d, %m %Y'))
        
    previous_json = ''
    
    sensor_data = []
    offset = 1
    mins = 5
    window_size = 25 * 60 * offset * mins # 5 minutes assuming 25 Hz sampling rate
    step_size = window_size # no overlap

    index = 0 # to keep track of how many samples we have buffered so far
    reset_vars() # resets orientation variables
        
    while True:
        try:
            message = receive_socket.recv(1024).strip().decode('ascii')
            # print("Message")
            # print(message)
            json_strings = message.split("\n")

            json_strings[0] = previous_json + json_strings[0]


            # print("************************************ json_strings *************************************")
            # print(json_strings)
            # print("************************************************************************************** \n")



            for json_string in json_strings:
                try:
                    data = json.loads(json_string)
                except:
                    previous_json = json_string
                    continue
                previous_json = '' # reset if all were successful
                sensor_type = data['sensor_type']
                if (sensor_type == u"SENSOR_ACCEL"):
                    t=data['data']['t']
                    x=data['data']['x']
                    y=data['data']['y']
                    z=data['data']['z']
                    
                    sensor_data.append(reorient(x,y,z))
                    index+=1
                    # make sure we have exactly window_size data points :
                    while len(sensor_data) > window_size:
                        sensor_data.pop(0)
                
                    if (index >= step_size and len(sensor_data) == window_size):
                        t = threading.Thread(target=predict, args=(np.asarray(sensor_data[:]),))
                        t.start()
                        index = 0
                
            sys.stdout.flush()
        except KeyboardInterrupt: 
            # occurs when the user presses Ctrl-C

            # Get the end time and print activity length
            end_time = datetime.now()

            length = end_time - time_activated

            length_str = str(length).split('.', 2)[0]
            
            print('\n Activity Length: ',length_str)

            # Print table
            all_time_output = PrettyTable()

            column_names = ['Period','Sleep Count', 'Vigil Count', 'Sleep Percentage','Description']

            keys = ["sleep_count","vigil_count","sleep_percentage","sleep_description"]

            all_time_output.add_column(column_names[0],list(range(1, len(all_time_array)+1)))

            for x in range(1,len(column_names)):
                data = []
                key = ""
                key = keys[x-1]
                for d in all_time_array:
                    data.append(d[key])
                all_time_output.add_column(column_names[x],data)

            if(len(all_time_array) == 0):
                print("Not enough data collected yet")

            print(all_time_output)


            send_socket = create_send_socket()

            send_message('STEP', 'Hey! > ')

            print("User Interrupt. Quitting...")
            break
        except Exception as e:
            # ignore exceptions, such as parsing the json
            # if a connection timeout occurs, also ignore and try again. Use Ctrl-C to stop
            # but make sure the error is displayed so we know what's going on
            if (str(e) != "timed out"):  # ignore timeout exceptions completely       
                print(e)
            pass
except KeyboardInterrupt: 
    # occurs when the user presses Ctrl-C

    send_socket = create_send_socket()

    send_message('STEP', 'Hey!')

    print("User Interrupt. Qutting...")
finally:
    print('closing socket for receiving data')
    receive_socket.shutdown(socket.SHUT_RDWR)
    receive_socket.close()