# Supermarket Management System

## Technologies Used
- **SSL Certification**: Ensures secure communication between client and server.
- **Client-Server Connection**: Facilitates interaction between the user and the server.
- **CSV Files**: Used for data storage and retrieval.

## Description
This project establishes a secure connection between a client and server using SSL encryption. Users on the client side can browse, search, and purchase items from the server-side database. The system ensures data integrity and security through encrypted communication.

## Installation and Usage Guide

### Clone the Repository
```
git clone https://github.com/mahika34/CN-project-4th-sem.git
cd CN-project-4th-sem
```

### Start the Server
Run the following command to initiate both TCP/SSL and UDP servers:
```
python server.py
```
You should see messages indicating that the servers are listening for connections.

### Start the Client
Open a new terminal or command prompt and execute:
```
python client.py
```

### Authentication
Upon running the client, enter valid login credentials:
- **Username:** root, **Password:** root
- **Username:** root1, **Password:** root1

### Interaction
Once authenticated, you can:
- View available items.
- Search for specific products.
- Purchase items securely through the system.

### Generating a Self-Signed SSL Certificate
To set up SSL encryption, generate a self-signed SSL certificate using OpenSSL. Follow this guide:
[Generate SSL Certificate](https://www.youtube.com/watch?v=c-LEHJy5g8Y)

