from datetime import datetime, timedelta
import re
from typing import List, Optional
import os
from dotenv import load_dotenv
import requests
import json
import pprint

BASE_URL = "http://192.168.1.101:8123"

def get_headers():
    """
    Retrieves headers for the API request.

    :return: A dictionary containing API request headers.
    """
    return {
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}",
        "Content-Type": "application/json",
    }

def make_request(method: str, endpoint: str, data: dict = None) -> dict:
    """
    Makes a request to the specified endpoint with the provided method and data.

    :param method: The HTTP method. Allowed methods are 'GET' and 'POST'.
    :param endpoint: The API endpoint.
    :param data: The data to be sent with the request. Default is None.
    :return: The response from the server as a dictionary.
    """
    # Print the parameters
    # print(f"\n#make_request#")
    # print(f"Method: {method}")
    # print(f"Endpoint: {endpoint}")
    # print(f"Data: {data}")
    headers = get_headers()

    url = f"{BASE_URL}{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise NotImplementedError("Only GET and POST methods are implemented.")
    
    # Check status code and handle exceptions
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Received status code {response.status_code}")
    #print("make_request response:")
    #pprint.pprint(response.json())
    #print("response end\n")
    return response.json()
    
def get_filtered_services(domains: Optional[List[str]] = None) -> str:
    """
    Gets services from the "/api/services" endpoint using the make_request function,
    filters them based on a list of domains,
    and returns a string of the filtered services, each on a new line.

    :param domains: A list of domains to filter the services. Default is None, which returns all services.
    :return: A string of the filtered services, each on a new line.
    """
    # Get all services from the "/api/services" endpoint
    services = make_request("GET", "/api/services")
    
    if domains:
        filtered_services = [f"[Domain: {service['domain']}][Services: {', '.join(service['services'].keys())}]" for service in services for domain in domains if service['domain'] == domain]
    else:
        filtered_services = [f"[Domain: {service['domain']}][Services: {', '.join(service['services'].keys())}]" for service in services]

    return '\n'.join(filtered_services)

def get_filtered_entity_states_service(patterns: Optional[List[str]] = None) -> str:
    """
    Gets entities and their states from the "/api/config" endpoint using the make_request function,
    filters them based on a list of regex patterns,
    and returns a string of the filtered entities and a unique list of the domains.
    This is handy to find the name and state of an entity to allow you to use it in a POST request later.

    :param patterns: A list of regex patterns to filter the entities. Default is None, which returns all entities.
    :return: A string of the filtered entities and a unique list of the domains.
    """
    # Get all entities from the "/api/states" endpoint
    states = make_request("GET", "/api/states")

    # print(f"\n#get_filtered_entity_states_service#\nsearch patterns: \n{patterns}")

    ls = ["entity_id, name, state"]
    domains = set()

    for e in states:
        entity_id = e['entity_id'].lower()
        domain = entity_id.split('.')[0]
        friendly_name = e['attributes'].get('friendly_name', '').lower()
        state = e['state']

        if patterns is not None:
            # Check if any of the patterns matches the entity_id or friendly_name
            if any(re.search(pattern, entity_id) or re.search(pattern, friendly_name) for pattern in patterns):
                ls.append(f"{entity_id},{friendly_name},{state}")
                domains.add(domain)
        else:
            ls.append(f"{entity_id},{friendly_name},{state}")
            domains.add(domain)

    if len(ls) == 1:
        entities = "No entities matched the provided patterns."
    else:
        entities = '\n'.join(ls)

    services = get_filtered_services(domains)
    result = f"%%%Returned entities:%%%\n{entities}\n%%%Returned <domains> and <services>%%%\n{services}"
    # print(result)
    return result

def get_entity_history(entity_ids: List[str], start_time: datetime, end_time: datetime) -> dict:
    """
    Get the history of one or more entities.

    :param entity_ids: A list of entity ids.
    :param start_time: The start time for the period.
    :param end_time: The end time for the period.
    :return: The response from the server as a dictionary.
    """
    # Convert entity_ids from list to comma-separated string
    entity_ids_str = ','.join(entity_ids)
    
    # Convert start_time and end_time from datetime objects to strings
    start_time_str = start_time#.isoformat()
    end_time_str = end_time#.isoformat()

    # Create data dictionary for API request
    data = {
        "filter_entity_id": entity_ids_str,
        "minimal_response": "",
        "no_attributes": "",
        "end_time": end_time_str
    }

    # Define API endpoint
    endpoint = f"/api/history/period/{start_time_str}"

    # Make API request
    response=make_request("GET", endpoint, data)
    
    simplified_response = []
    for sensor_data in response:
        sensor_dict = {"entity_id": sensor_data[0]['entity_id']}
        data_points = []
        for data_point in sensor_data:
            last_changed = data_point['last_changed']
            state = data_point['state']
            
            # Reduce the precision of the timestamp
            simplified_time = last_changed.split('.')[0]
            
            data_points.append({simplified_time: state})
        sensor_dict["data_points"] = data_points
        simplified_response.append(sensor_dict)
    # print(f"\n#get_entity_history#\n")
    # pprint.pprint(simplified_response)
    return simplified_response

 
# This block is executed only when the module is run directly
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Fetch status from the server
    response = make_request("GET", "/api/")
    pprint.pprint(response)
    
    # Fetch config from the server
    # response = make_request("GET", "/api/config")
    # pprint.pprint(response)
    
    # Fetch history from the server
    # response = make_request("GET", "/api/history/period/")
    # pprint.pprint(response)

    # timestamp = "2023-07-10T13:05:00+01:00"
    # call the function

    # Fetch history from the server
    # response = make_request("GET", "/api/history/period/2022-07-01T00:00:00+00:00")
    # pprint.pprint(response)
    
    # endpoint = "/api/history/period/2023-07-01T00:00:00+00:00"
    # method = "GET"
    # response = make_request(method, endpoint)

    
    # Fetch states from the server
    # response = make_request("GET", "/api/states")
    # # Define the keywords
    # regex_filter = ['living[_]?room']
    # # Filter the response
    # filtered_response = filter_response(response, regex_filter)
    # print(f"\nfiltered entity list\n{filtered_response}")
    
    
    # filtered_response = filter_response(response)
    # print(f"\nfull entity list\n{filtered_response}")
    
    # filtered_entities_domains_states = get_filtered_entity_states_service(['living[_]?room'])
    # print(filtered_entities_domains_states)
    
    # # Turn on the living room lamp
    # data_light_on = {"state": "on"}
    # response = make_request("POST", "/api/states/light.living_room_switch_2", data_light_on)
    # pprint.pprint(response)

    # # Turn off the living room lamp
    # data_light_off = {"state": "off"}
    # response = make_request("POST", "/api/states/light.living_room_switch_2", data_light_off)
    # pprint.pprint(response)
    
    # Get all services for 'light' and 'switch' domains
    #services = get_filtered_services(['light', 'switch'])
    # services = get_filtered_services(['automation'])
    # print(services)
    # print("S#################################")    
    # services = get_filtered_services()
    # print(services)
    
    response = get_entity_history(["sensor.temp_sensor_1_temperature_1","sensor.soil_moisture_sensor_01_temperature"],"2023-07-10T13:05:00+01:00", "2023-07-13T13:05:00+01:00")
    pprint.pprint(response)

