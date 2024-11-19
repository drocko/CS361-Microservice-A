import zmq

try:
    from googlesearch import search
except ImportError:
    print(">>> No module named 'google' found")


def server_main():
    """Main function to handle ZeroMQ server and book search microservice."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://0.0.0.0:5555")

    print(">>> Server running, waiting for client requests...")

    while True:
        request = socket.recv()  # Receive book title as string
        book_title = request.decode()
        print(f">>> Received request from the client: '{book_title}'...")

        if len(request) == 0:
            empty_request = ">>> Search Failed: Request Empty"
            print(f">>> Request empty")
            socket.send_string(empty_request)
            continue
        if book_title.upper() == "QSERVER":
            # Warning: this will completely shut down server
            socket.send_string('Closing server application')
            context.destroy()
            break


        # Perform Google Search
        results = perform_google_search(book_title)
        print(f">>> Searching Google...")

        result, status = find_amazon_link(results)
        print(f">>> Processing Amazon link...")

        # Prepare response
        if status:
            print(f">>> Success: {result}")
        else:
            print(f">>> Failed: {result}")

        response = result

        # Send response back to the client
        socket.send_string(response)
        continue

        # Destroy and exit
    context.destroy()


def perform_google_search(query: str) -> list[str]:
    """Perform a Google search and return a list of URLs."""
    search_query = f"{query} book"
    all_results = []

    try:
        for result in search(search_query, tld="co.in", num=10, stop=10, pause=2):
            all_results.append(str(result))
    except Exception as e:  # Error response for debugging
        print(f"Error during Google Search: {e}")

    return all_results


def find_amazon_link(results: list[str]) -> (str, bool):
    """Check the search results for an Amazon link."""
    status = False
    failed_response = "No Amazon link found"

    for result in results:
        if 'amazon' in result:
            status = True
            return result, status

    return failed_response, status


if __name__ == "__main__":
    server_main()

