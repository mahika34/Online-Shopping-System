import socket
import ssl
import threading
import csv
import pickle

TCP_SERVER_HOST = 'localhost'
TCP_SERVER_PORT = 12345#5555
CERTFILE = 'server.crt'
KEYFILE = 'server.key'

UDP_SERVER_HOST = 'localhost'
UDP_SERVER_PORT = 12000#5555
sum_value=0
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_SERVER_HOST, TCP_SERVER_PORT))
    server_socket.listen(1)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    print("TCP Server is listening for connections...")

    while True:
        connection, address = server_socket.accept()
        print("TCP Connection from:", address)
        connection = ssl_context.wrap_socket(connection, server_side=True)  
        message_to_client = "This is a test message from the server to the client! SSL established"
        connection.sendall(message_to_client.encode())
        connection.close()

def handle_client(server_socket):
    sum_value=0
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received data from {client_address}: {data.decode()}")
        i=0
        lst=[]
        if(i==0):
            lst.append(client_address[1])
        i=i+1
        if(client_address[1] in lst):
            message = data.decode("utf-8")

            if message == "1":
                data1, _ = server_socket.recvfrom(1024)
                message1 = data1.decode("utf-8")
                browse(client_address, message1, server_socket)
            elif message == "2":
                file = open("item3.csv", "r")
                sum2=0
                message2, _ = server_socket.recvfrom(1024)
                message2 = message2.decode("utf-8")
                message3, _ = server_socket.recvfrom(1024)
                message3 = message3.decode("utf-8")
                sum2+=purchase(file, message2, message3, client_address,  server_socket)
            elif message == "3":

                modified_message1 = pickle.dumps(receipt)
                server_socket.sendto(modified_message1, client_address)
                
            elif message == "4":
                break
            else:
                modified_message = "Wrong choice"
                server_socket.sendto(modified_message.encode("utf-8"), client_address)
        else:
            message = data.decode("utf-8")

            if message == "1":
                data1, _ = server_socket.recvfrom(1024)
                message1 = data1.decode("utf-8")
                browse(client_address, message1, server_socket)
            elif message == "2":
                sum1=0
                file = open("item3.csv", "r")
                message2, _ = server_socket.recvfrom(1024)
                message2 = message2.decode("utf-8")
                message3, _ = server_socket.recvfrom(1024)
                message3 = message3.decode("utf-8")
                sum1+=purchase(file, message2, message3, client_address,  server_socket)
            elif message == "3":
                modified_message1 = pickle.dumps(receipt)
                server_socket.sendto(modified_message1, client_address)
                # modified_message2 = str(sum_value).encode("utf-8")
                # server_socket.sendto(modified_message2, client_address)
            elif message == "4":
                break
            else:
                modified_message = "Wrong choice"
                server_socket.sendto(modified_message.encode("utf-8"), client_address)


def purchase(csvfile, message2, message3, client_address, server_socket):
    sum_value = 0
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)
    for row in rows:
        if row[0] == 'Sno':
            continue
        if int(message3) < int(row[2]):
            if row[0] == message2:
                for i in receipt:
                    if i[0] == message2:
                        i[2] = str(int(i[2]) + int(message3))
                        sum_value = sum_value+ (int(row[3]) * int(message3))
                        row[2] = str(int(row[2]) - int(message3))
                        modified_message = pickle.dumps(receipt)
                        server_socket.sendto(modified_message, client_address)
                        break
                else:
                    row[2] = str(int(row[2]) - int(message3))
                    sum_value= sum_value+ (int(row[3]) * int(message3))
                    lst = list((row[0], row[1], message3, row[3]))
                    receipt.append(lst)
                    modified_message = pickle.dumps(receipt)
                    server_socket.sendto(modified_message, client_address)
        else:
            modified_message = "Insufficient quantity!!"
            server_socket.sendto(modified_message.encode("utf-8"), client_address)
    with open("item3.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
    return sum_value

def browse(client_address, msg1, server_socket):
    try:
        with open("item3.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  
            for row in csvreader:
                if msg1 == "1" and 100 < int(row[0]) < 106:
                    modified_message = pickle.dumps(row)
                    server_socket.sendto(modified_message, client_address)
                elif msg1 == "2" and 200 < int(row[0]) < 206:
                    modified_message = pickle.dumps(row)
                    server_socket.sendto(modified_message, client_address)
                elif msg1 == "3" and 300 < int(row[0]) < 306:
                    modified_message = pickle.dumps(row)
                    server_socket.sendto(modified_message, client_address)
                elif msg1 == "4" and 400 < int(row[0]) < 406:
                    modified_message = pickle.dumps(row)
                    server_socket.sendto(modified_message, client_address)
                elif msg1 == "5" and 500 < int(row[0]) < 506:
                    modified_message = pickle.dumps(row)
                    server_socket.sendto(modified_message, client_address)
    except UnicodeDecodeError:
        print("Error")

receipt=[]
# Start TCP server thread
tcp_thread = threading.Thread(target=tcp_server)
tcp_thread.start()
s=0
# Start UDP server
server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket_udp.bind((UDP_SERVER_HOST, UDP_SERVER_PORT))
print("UDP Server is listening for connections...")

# Handle UDP client requests
thread = threading.Thread(target=handle_client, args=(server_socket_udp,))
thread.start()