# Import the required modules

import socket
import cv2
import pickle
#import numpy as np
import struct ## new

HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(0)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        if not data:
            cv2.destroyAllWindows()
            conn,addr=s.accept()
            continue
    # receive image row data form client socket
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print (payload_size, packed_msg_size, msg_size)
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    # unpack image using pickle
    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imwrite("PiCamera.jpg",frame)
    
    #cv2.imshow('server',frame)
    #video = frame
    #Picture(video_box, image = frame, width = 250, height = 250)
    cv2.waitKey(1)