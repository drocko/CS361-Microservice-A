import zmq

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def server_main():
    """Main function to handle ZeroMQ server and book search microservice."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Server is running... waiting for client requests.")

    while True:
        request = socket.recv()  # Receive book title as string
        book_title = request.decode()
        print(f"Received request from the client: {book_title}")

        # Perform Google Search
        results = perform_google_search(book_title)
        print(f"Searching Google for: {book_title}")

        result, status = find_amazon_link(results)
        print(f"Processing an Amazon link for: {book_title}")

        # Prepare response
        if status:
            print(f"Success! Found Amazon link")
            print(f"Preparing successful search response")
        else:
            print(f"Fail :( Can't find Amazon link")
            print(f"Preparing failed search response")

        response = result

        # Send response back to the client
        socket.send(response)


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


def test():
    book_test = "The Catcher in the Rye"
    results_test = perform_google_search(book_test)
    result_test, status_test = find_amazon_link(results_test)
    print(result_test)


if __name__ == "__main__":
    server_main()
    test()

