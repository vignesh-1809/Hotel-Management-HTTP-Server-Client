import socket

def create_request(method, path, data=None):
    """Create an HTTP request string"""
    if method == "GET":
        return f"{method} {path} HTTP/1.1\r\n\r\n"
    elif method == "POST":
        return f"{method} {path} HTTP/1.1\r\nContent-Length: {len(data)}\r\n\r\n{data}"
    return ""

def send_request(request):
    """Send HTTP request to the server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8080))
    client.send(request.encode())
    response = client.recv(1024).decode('utf-8')
    print(f"Server Response:\n{response}")
    client.close()

def main():
    while True:
        print("\nHotel Management Client")
        print("1. Check available rooms")
        print("2. Book a room")
        print("3. Checkout room")
        print("4. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            request = create_request("GET", "/availability")
            send_request(request)

        elif choice == "2":
            print("\nChoose Room Type:")
            print("1. Single Bed - $100")
            print("2. Double Bed - $150")
            print("3. Suite - $200")
            room_choice = input("Enter your choice: ").strip()
            
            if room_choice == "1":
                room_type = "single_bed"
                cost = 100
            elif room_choice == "2":
                room_type = "double_bed"
                cost = 150
            elif room_choice == "3":
                room_type = "suite"
                cost = 200
            else:
                print("Invalid choice, try again.")
                continue
            
            # Displaying room type and cost for the user
            print(f"\nSelected Room Type: {room_type.capitalize()} - Cost: ${cost}")
            
            # Collecting customer name and check-in date
            customer_name = input("Enter customer name: ").strip()
            checkin_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
            
            # Sending data to the server without cost included
            data = f"{customer_name},{room_type},{checkin_date}"
            request = create_request("POST", "/book", data)
            send_request(request)

        elif choice == "3":
            room_number = input("Enter room number to checkout: ").strip()
            checkout_date = input("Enter checkout date (YYYY-MM-DD): ").strip()
            data = f"{room_number},{checkout_date}"
            request = create_request("POST", "/checkout", data)
            send_request(request)

        elif choice == "4":
            print("Exiting client.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
