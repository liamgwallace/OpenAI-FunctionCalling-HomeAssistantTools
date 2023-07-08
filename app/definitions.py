function_definitions = [
    {
        "name": "get_todos",
        "description": "Get a list of todos, optionally filtered by their completion status",
        "parameters": {
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Whether to only return completed todos",
                },
            },
            "required": [],
        },
    },
    {
        "name": "create_todo",
        "description": "Create a new todo",
        "parameters": {
            "type": "object",
            "properties": {
                "todo": {
                    "type": "object",
                    "description": "The new todo to be created",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "The id of the todo",
                        },
                        "task": {
                            "type": "string",
                            "description": "The task of the todo",
                        },
                        "is_completed": {
                            "type": "boolean",
                            "description": "Whether the task is completed",
                            "default": False,
                        },
                    },
                    "required": ["task"],
                },
            },
            "required": ["todo"],
        },
    },
    {
        "name": "update_todo",
        "description": "Update an existing todo",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The id of the todo to update",
                },
                "todo": {
                    "type": "object",
                    "description": "The updated todo",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The updated task of the todo",
                        },
                        "is_completed": {
                            "type": "boolean",
                            "description": "The updated completion status of the task",
                        },
                    },
                    "required": ["task"],
                },
            },
            "required": ["id", "todo"],
        },
    },
    {
        "name": "delete_todo",
        "description": "Delete an existing todo",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The id of the todo to delete",
                },
            },
            "required": ["id"],
        },
    },
    {
        "name": "delete_all_todos",
        "description": "Delete all existing todos",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "ha_make_request",
        "description": "Makes a request to the home assistant endpoint with the provided method and data",
        "parameters": {
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "description": "The HTTP method. Allowed methods are 'GET' and 'POST'.",
                },
                "endpoint": {
                    "type": "string",
                    "description": """
The API endpoint examples are.
method to use,endpoint details, description
GET,'/api/', Returns a message if the API is up and running.
GET,'/api/config', Returns the current configuration as JSON.
GET,'/api/events', Returns an array of event objects. Each event object contains event name and listener count.
GET,'/api/services', Returns an array of service objects. Each object contains the domain and which services it contains.
GET,'/api/history/period/<timestamp>', Returns an array of state changes in the past. Each object contains further details for the entities. filter_entity_id=<entity_ids> is required and filters one or more entities', comma separated. The <timestamp> (YYYY-MM-DDThh:mm:ssTZD) is optional and defaults to 1 day before the time of the request
GET,'/api/logbook/<timestamp>', Returns an array of logbook entries. The <timestamp> (YYYY-MM-DDThh:mm:ssTZD) is optional. entity=<entity_id> to filter on one entity.'/api/states', Returns an array of state objects. Each state has the following attributes: entity_id, state, last_changed and attributes.
GET,'/api/states/<entity_id>', Returns a state object for specified entity_id. Returns 404 if not found.
GET,'/api/error_log', Retrieve all errors logged during the current session of Home Assistant as a plaintext response.
GET,'/api/camera_proxy/<camera entity_id>', Returns the data (image) from the specified camera entity_id.'/api/calendars', Returns the list of calendar entities.
GET,'/api/calendars/<calendar entity_id>', Returns the list of calendar events for the specified calendar entity_id between the start and end times (exclusive).
POST,'/api/states/<entity_id>', Updates or creates a state. You can create any state that you want, it does not have to be backed by an entity in Home Assistant.Expects a JSON object that has at least a state attribute:
POST,'/api/events/<event_type>', Fires an event with event_type.You can pass an optional JSON object to be used as event_data.
POST,'/api/services/<domain>/<service>', Calls a service within a specific domain. Will return when the service has been executed or after 10 seconds, whichever comes first.You can pass an optional JSON object to be used as service_data.<domain> is equal to the first part of the 'entity_id'
POST,'/api/template', Render a Home Assistant template
POST,'/api/config/core/check_config', Trigger a check of configuration.yaml. No additional data needs to be passed in with this request. Needs config integration enabled.
POST,'/api/intent/handle', Handle an intent.
                    """
                },
                "data": {
                    "type": ["object", "null"],
                    "description": "The data to be sent with the request. Default is None.",
                },
            },
            "required": ["method", "endpoint"],
        },
    },
    {
        "name": "ha_get_filtered_entity_states_service",
        "description": """
Gets a list of entity_id, entity_name, entity_state from the Home Assistant endpoint included also is the <domain> and <service> for the returned entities, optionaly filters the list based on a list of regex patterns.
This is handy to find a short list to extract the name and state of an entity to allow you to use it in a POST request later.
cover your bases with the REGEX to include as many permutations as possible.
e.g. In this house lights, switch, led and lamps are used interchangably, so a filter for living room lights could be [r'\bliving\b', r'\broom\b', r'\blight\b', r'\bled\b', r'\blamp\b']"""
        ,
        "parameters": {
            "type": "object",
            "properties": {
                "patterns": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of regex patterns to filter the entities. Default is None, which returns all entities."
                },
            },
            "required": [],
        },
    }
]
