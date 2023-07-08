import requests

from .ha_api_funcs import get_filtered_entity_states_service, make_request # Import the functions from the 'ha_api_funcs.py' file


def get_todos(completed=None):
    params = {"completed": completed} if completed is not None else None
    response = requests.get(
        "https://fastapilangchain-1-w0858112.deta.app/todos", params=params
    )
    return response.json()


def create_todo(todo):
    response = requests.post(
        "https://fastapilangchain-1-w0858112.deta.app/todos", json=todo
    )
    return response.json()


def update_todo(id, todo):
    response = requests.put(
        f"https://fastapilangchain-1-w0858112.deta.app/todos/{id}", json=todo
    )
    return response.json()


def delete_todo(id):
    response = requests.delete(
        f"https://fastapilangchain-1-w0858112.deta.app/todos/{id}"
    )
    return response.status_code

# Function to call get_filtered_entity_states
def ha_get_filtered_entity_states_service(patterns=None):
    print(f"###\nFunction call: ha_get_filtered_entity_states_service \n###")
    return get_filtered_entity_states_service(patterns)

# Function to call make_request
def ha_make_request(method, endpoint, data=None):
    print(f"###\nFunction call: ha_make_request \n###")
    return make_request(method, endpoint, data)



api_functions = {
    "get_todos": get_todos,
    "create_todo": create_todo,
    "update_todo": update_todo,
    "delete_todo": delete_todo,
    "ha_get_filtered_entity_states_service": ha_get_filtered_entity_states_service,
    "ha_make_request": ha_make_request
}
