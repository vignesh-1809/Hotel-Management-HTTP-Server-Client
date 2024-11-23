# Hotel Room Booking System using Socket Programming

## Overview
This project demonstrates a simple client-server-based **Hotel Room Booking System** implemented using **socket programming** in Python. It showcases how a server can handle multiple requests from a client, simulating a room booking and management system for a hotel.

The server manages the hotel room data in memory and processes client requests for room booking, availability, and checkout functionalities. The client communicates with the server using a command-line interface, sending requests for different operations.

---

## Features
- **View Room Types and Costs**: The client can view available room types (`single_bed`, `double_bed`, `suite`) along with their respective costs.
- **Book a Room**: The client can book an available room by providing their name and check-in date.
- **View All Room Details**: Displays all room information, including room number, type, current occupant, and check-in date.
- **Check Out**: The client can check out of a room by providing the room number and check-out date. The server calculates the total bill based on the room type and stay duration.
- **Socket-Based Communication**: Demonstrates the use of GET and POST-like requests in the client-server communication, showcasing fundamental concepts of networking.

---

## System Architecture
The project uses a **client-server model**:
- **Server**: Handles client requests, processes room information, and sends responses.
- **Client**: Sends requests to the server and displays responses.

The server maintains room information in a Python dictionary and updates it dynamically based on client operations.

---

## Tools and Technologies
- **Programming Language**: Python
- **Socket Programming**: Python's `socket` module for TCP-based communication
- **Data Storage**: In-memory dictionary for managing room data

---

## Usage Instructions

### Prerequisites
- Install Python 3.x on your system.
- Ensure the server and client scripts are in the same directory.

### Running the Project
1. **Start the Server**:
   Run the server script to start listening for client requests.
   ```bash
   python server.py
2. **Run the Client**:
   Start the client script to interact with the server.
   ```bash
   python client.py
