import socket
import threading
from datetime import datetime

# Room types and costs
ROOM_TYPES = {
    "single_bed": {"prefix": 100, "cost": 50},
    "double_bed": {"prefix": 200, "cost": 100},
    "suite": {"prefix": 300, "cost": 200}
}
ROOMS_PER_TYPE = 10

# Initialize rooms and bookings data
rooms = {
    room_type: [{"room_number": prefix + i + 1, "customer_name": None, "checkin_date": None}
                for i in range(ROOMS_PER_TYPE)]
    for room_type, data in ROOM_TYPES.items()
    for prefix in [data["prefix"]]
}

def is_valid_date(date_text):
    """Helper function to validate the date format and value."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def handle_client(client_socket):
    """Handle the client request and perform the necessary operations"""
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        # Split request into lines and determine the method (GET or POST)
        lines = request.split("\r\n")
        method, path, _ = lines[0].split(" ")
        
        print(f"Request Method: {method}")

        if method == "GET":
            if path == "/availability":
                check_availability(client_socket)
        elif method == "POST":
            if path == "/book":
                book_room(client_socket, lines)
            elif path == "/checkout":
                checkout(client_socket, lines)
        else:
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nInvalid request".encode())
    
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nServer error".encode())
    
    finally:
        client_socket.close()

def check_availability(client_socket):
    """Check room availability"""
    availability = {
        room_type: sum(1 for room in rooms_list if room["customer_name"] is None)
        for room_type, rooms_list in rooms.items()
    }
    response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + str(availability)
    client_socket.sendall(response.encode())

def book_room(client_socket, lines):
    """Book a room"""
    data = lines[-1].strip()
    try:
        customer_name, room_type, checkin_date = data.split(",")
        if room_type not in rooms:
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nInvalid room type".encode())
            return

        if not is_valid_date(checkin_date):
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nInvalid check-in date".encode())
            return

        available_room = next((room for room in rooms[room_type] if room["customer_name"] is None), None)
        if not available_room:
            client_socket.sendall(f"HTTP/1.1 400 Bad Request\r\n\r\nNo {room_type} rooms available".encode())
            return

        # Update room details for the booking
        available_room["customer_name"] = customer_name
        available_room["checkin_date"] = checkin_date
        response = f"HTTP/1.1 200 OK\r\n\r\nRoom {available_room['room_number']} booked successfully!"
        client_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error booking room: {e}")
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nError booking room".encode())

def checkout(client_socket, lines):
    """Checkout the room"""
    try:
        data = lines[-1].strip()
        room_number, checkout_date = data.split(",")
        room_number = int(room_number)

        if not is_valid_date(checkout_date):
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nInvalid checkout date".encode())
            return

        for room_type, rooms_list in rooms.items():
            room = next((room for room in rooms_list if room["room_number"] == room_number), None)
            if room and room["customer_name"] is not None:
                checkin_date = room["checkin_date"]
                
                # Convert dates to datetime objects
                checkin_date_obj = datetime.strptime(checkin_date, "%Y-%m-%d")
                checkout_date_obj = datetime.strptime(checkout_date, "%Y-%m-%d")

                # Ensure checkout date is after check-in date
                if checkout_date_obj <= checkin_date_obj:
                    client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nCheckout date must be after check-in date".encode())
                    return
                
                days_stayed = (checkout_date_obj - checkin_date_obj).days
                room_cost = ROOM_TYPES[room_type]["cost"]
                total_bill = days_stayed * room_cost

                # Clear room booking details
                room["customer_name"] = None
                room["checkin_date"] = None

                response = f"HTTP/1.1 200 OK\r\n\r\nDays stayed: {days_stayed}, Total bill: ${total_bill}"
                client_socket.sendall(response.encode())
                return

        client_socket.sendall("HTTP/1.1 404 Not Found\r\n\r\nRoom not found".encode())

    except Exception as e:
        print(f"Error during checkout: {e}")
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nError during checkout".encode())

def start_server():
    """Start the server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(5)
    print("Server is listening on port 8080")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
