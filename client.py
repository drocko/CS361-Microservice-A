import zmq


def client_main():
    context = zmq.Context()
    print(">>> Client attempting to connect to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        input_string = input("Enter a book to lookup? (Enter Q to quit): ")
        if input_string.upper() == "Q":
            print(f">>> Exiting Program...")
            context.destroy()
            break
        elif input_string.upper() == "QSERVER":
            print(f">>> Exiting Program...")
            socket.send_string("QSERVER")
            context.destroy()
            break
        else:
            print(f">>> Sending request...")
            socket.send_string(input_string)
            message = socket.recv()
            print(f">>> Server sent back: {message.decode()}")


if __name__ == '__main__':
    client_main()
