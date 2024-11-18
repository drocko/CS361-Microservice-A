import zmq


def client_main():
    context = zmq.Context()
    print(">>> Client attempting to connect to server...")
    socket = context.socket(zmq.REQ)
    server_ip = "192.168.123.132"  # Replace with actual IP
    socket.connect(f"tcp://{server_ip}:5555")

    while True:
        input_string = input("Enter a book to lookup? ")
        if input_string.upper() == "Q":
            print(f">>> Exiting Program...")
            context.destroy()
            break
        else:
            print(f">>> Sending request...")
            socket.send_string(input_string)
            message = socket.recv()
            print(f">>> Server sent back: {message.decode()}")


if __name__ == '__main__':
    client_main()
