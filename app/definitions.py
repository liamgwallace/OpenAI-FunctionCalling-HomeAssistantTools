function_definitions = [
    {
        "name": "get_todos",
        "description": "Get a list of todos, optionally filtered by their completion status",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "completed": {
                    "type": "boolean",
                    "description": "Whether to only return completed todos",
                },
            },
            "required": ["planning"],
        },
    },
    {
        "name": "create_todo",
        "description": "Create a new todo",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
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
            "required": ["todo","planning"],
        },
    },
    {
        "name": "update_todo",
        "description": "Update an existing todo",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
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
            "required": ["id", "todo", "planning"],
        },
    },
    {
        "name": "delete_todo",
        "description": "Delete an existing todo",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "id": {
                    "type": "integer",
                    "description": "The id of the todo to delete",
                },
            },
            "required": ["id", "planning"],
        },
    },
    {
        "name": "delete_all_todos",
        "description": "Delete all existing todos",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "ha_get_entity_history",
        "description": "Get the history of one or more entities on home assistant. Use this if you need to find information about the history or state changes for an item in the house",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "entity_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of entity IDs. If you dont know an entity ID use ha_get_filtered_entity_states_service function to find it"
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Start of the period (YYYY-MM-DDThh:mm:ssTZD)"
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "End of the period (YYYY-MM-DDThh:mm:ssTZD)"
                },
            },
            "required": ["entity_ids", "start_time", "end_time", "planning"]
        }
    },
    {
        "name": "ha_make_request",
        "description": "Makes a request to the home assistant endpoint with the provided method and data",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "method": {
                    "type": "string",
                    "description": "The HTTP method. Accepts 'GET' and 'POST'.",
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
GET,'/api/logbook/<timestamp>', Returns an array of logbook entries.
	<timestamp> (YYYY-MM-DDThh:mm:ssTZD) defines start of the period
GET,'/api/states/<entity_id>', Returns a state object for specified entity_id. Returns 404 if not found.
GET,'/api/error_log', Retrieve all errors logged during the current session of Home Assistant as a plaintext response.
POST,'/api/states/<entity_id>', Updates or creates a state. You can create any state that you want, it does not have to be backed by an entity in Home Assistant.
POST,'/api/services/<domain>/<service>', Calls a service within a specific domain. Will return when the service has been executed or after 10 seconds, whichever comes first.<domain> is equal to the first part of the 'entity_id' before the period
POST,'/api/template', Render a Home Assistant template
POST,'/api/config/core/check_config', Trigger a check of configuration.yaml. No additional data needs to be passed in with this request. Needs config integration enabled.
POST,'/api/intent/handle', Handle an intent.
If you dont know an <entity ID> or <domain> use ha_get_filtered_entity_states_service function to find it
                    """
                },
                "data": {
                    "type": ["object", "null"],
                    "description":"""
for:'/api/','/api/config','/api/events','/api/services','/api/states/<entity_id>','/api/error_log','/api/template','/api/config/core/check_config',
	'data' = ""
for:'/api/logbook/<timestamp>'
	'data' =
		Required:
			none
		Optional: 
			end_time=<timestamp> (YYYY-MM-DDThh:mm:ssTZD)(URL encoded, defaults to a day if omitted), 
			filter_entity_id=<entity_ids>, a comma-separated list,
for:'/api/states/<entity_id>'
	'data' = 
		Requiresd:
			a JSON object that has at least a state attribute e.g. data = {"state": "25", "attributes": {"unit_of_measurement": "°C"}}
POST,'/api/events/<event_type>', 
	'data' = 
		Optional:
			JSON object to be used as event_data. e.g. {"message": "Event download_file fired."}
POST,'/api/services/<domain>/<service>'
	'data' =
		Optional:
			JSON object to be used as service_data. Returns a list of states that have changed while the service was being executed. e.g. {"entity_id": "light.Ceiling"}
'/api/intent/handle',
	'data' =
		Required:
			a JSON object e.g.{ "name": "SetTimer", "data": { "seconds": "30" } }
If you dont know an <entity ID> or <domain> use ha_get_filtered_entity_states_service function to find it"""
                ,
                },
            },
            "required": ["method", "endpoint", "planning"],
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
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of all the steps you have taken so-far to complete the users request. use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the current step you are performing to complete the user task. use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "this is essential for this function to work. Make a detailed list of the planned next steps to complete the user task. use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "patterns": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of regex patterns to filter the entities. Default is None, which returns all entities."
                },
            },
            "required": ["planning"],
        },
    },
    {
        "name": "pw_get_weather_forecast",
        "description": "Get a weather forecast for a specific location from the Pirate Weather API, optionally filtered by forecast block(s)",
        "parameters": {
            "type": "object",
            "properties": {
                "planning": {
                    "type": "object",
                    "properties": {
                        "Complete_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of all the steps taken so far to complete the request. Use 'no-steps' if there are none"
                        },
                        "Current_step":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Current step being performed to complete the user task. Use 'no-steps' if there are none"
                        },
                        "Next_steps":{
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of the planned next steps to complete the user task. Use 'no-steps' if there are none"
                        },
                    },
                    "required": ["Complete_steps","Current_step", "Next_steps"],
                },
                "location": {
                    "type": "string",
                    "description": "Location for which the weather forecast is requested, e.g 'Cranleigh, Surrey, England'",
                },
                "forecast_type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optionall list of forecast blocks for which the weather forecast is requested. Can be 'currently', 'minutely' (returns next hour), 'hourly' (returns next 24 hours), 'daily' (returns next week), or 'alerts'. If not provided, data for all forecast blocks will be returned",
                }
            },
            "required": ["planning", "location", "forecast_type"],
        },
    }
]