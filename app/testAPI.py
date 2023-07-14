import requests
from pprint import pprint

def query_fast_api(query: str):
    # Define the URL to your FastAPI server.
    base_url = "http://localhost:5566/query"

    # Construct the URL with the provided query.
    url = f"{base_url}?query={query}"

    # Send a POST request to the FastAPI application.
    response = requests.post(url)

    # Ensure the request was successful.
    response.raise_for_status()

    # Parse the JSON response.
    data = response.json()['response']

    return data

if __name__ == "__main__":
    # Enter a loop for multiple queries
    while True:
        # Prompt for a query from the user
        print(f"\n!#############################################")
        query = input(f"\nPlease enter your query (or 'q' to exit):\n")
        print(f"\n####\n")

        # If the user types 'quit', exit the loop
        if query.lower() == "q":
            break

        # Otherwise, send the query to the FastAPI application and print the response
        response = query_fast_api(query)
        print(f"*#############################################\n{response}")
