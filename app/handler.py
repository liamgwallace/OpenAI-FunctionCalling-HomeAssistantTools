import json
import os
import pprint
import openai
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from dateutil.tz import tzlocal
#gpt-3.5-turbo-0613
#gpt-4-0613

class OpenAIHandler:
    def __init__(self, api_functions, function_definitions, system_role="", model="gpt-3.5-turbo-0613", temperature=0.2):
        load_dotenv(find_dotenv())
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        self.api_functions = api_functions
        self.function_definitions = function_definitions
        self.model = model
        self.temperature = temperature
        self.system_role = """
You are professional level decision making assistant.
You have access to a variety of functions that can help the user. 
You must choose the next function to call in order to help the user where possible. 
Refer to the original plan, the updated plan and any results from function calls you have made to decide the next action.
Make your best attempt to call a function where possible. Only respond to the user if you cannot solve the task or have solved the task.
Only use the functions you have been provided with. Do not guess at the data needed for a function, try and see if you can search for what is needed using a function at your disposal.
When using the function make it is important to use the 
Do not return the plan to the user, just the result
"""
#When you call a function you must first plan all the steps you will need to take to complete the user task in the planning. 
#If you have been provided with an old planning you will update this based on the result from the last function message.
#Keep a track of the successfull steps taken, the next one you are about to take and the planned tasks required to complete the user objective.
#.
#"""

    def send_message(self, messages):
        print(f"\n\n############   messages to llm   ##############")
        pprint.pprint(messages)
        # pprint.pprint(self.function_definitions)
        print(f"############   end   ##############\n")
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            functions=self.function_definitions,
        )
        print(f"\n\n############   response from llm   ##############")
        pprint.pprint(response)
        print(f"############   end   ##############\n")
        response = response["choices"][0]["message"]
        return response

    def process_function_call(self, response):
        function_name = None
        function_args = None
        planning = None
        result = None
     
        try:
            if 'function_call' in response:
                print("DEBUG:function call found")
                function_call = response['function_call']
                function_name = function_call.get('name')                
                # Ensure that arguments is a dictionary
                function_args_dict = function_call.get('arguments', {})
                if isinstance(function_args_dict, str):
                    function_args_dict = json.loads(function_args_dict)
                #Strip the planning off of the function call resoponse
                planning = function_args_dict.pop('planning', None)
                print(f"\n\n############   planning   ##############")
                pprint.pprint(planning)
                print(f"############   end   ##############\n")
                function_args_json = json.dumps(function_args_dict)
                function_args = json.loads(function_args_json)
                print(f"\n\n############   Found function   ##############")
                print(f"function_name: {function_name}")
                print(f"Arguments: {function_args}")
                print(f"############   end   ##############\n")

        except json.JSONDecodeError as e:
            result = f"Error decoding JSON: {e}"
            print(result)

        except Exception as e:
            result = f"Unexpected error: {e}"
            print(result)

        if function_name and not result:
            api_function = self.api_functions.get(function_name)
            if api_function:
                try:
                    result = str(api_function(**function_args))
                except Exception as e:
                    result = f"Error calling function '{function_name}': {e}"
                    print(result)
            else:
                result = f"Function '{function_name}' not found"
                print(result)

        return function_args, function_name, result, planning

    def send_response(self, query):
        # Format the datetime object as a string
        user = "This house belongs to Liam Wallace and Jenny Wallace"
        location = "Your location is Cranleigh, Surrey, UK"
        formatted_now = f" the current time is {datetime.now(tzlocal()).strftime('%Y-%m-%dT%H:%M:%S%z')}"
        plan_prompt=f"Let's devise a step-by-step plan to address the user query '{query}'. When outlining each step, provide a succinct description. If you can foresee the need for any functions or parameters, mention them explicitly. If unsure, use placeholders. The sole output should be the plan, nothing more. Please note, do not make any function call during this step. Represent the plan in the following format: {{'Complete_steps': [<leave this field blank for now>, <list completed steps once complete>], 'Current_step': [<leave this field blank for now>], 'Next_steps': [<all steps should be listed here>, <etc.>]}} DO NOT CALL A FUNCTION. Just return a response to the user"
        
        #create a detailed plan to solve the user request
        messages_plan_create = [{"role": "user", "content": f"{plan_prompt}. {formatted_now}. {location}. {user}"}]
        messages_first_plan = [self.send_message(messages_plan_create)]
        messages_first_plan[0]['content'] = f"To answer the users query, this is the original plan:\n{messages_first_plan[0]['content']}"
        print(f"\n\n############   Plan   ##############")
        print(f"query: {query}")
        #pprint.pprint(messages_first_plan[0].to_dict())
        pprint.pprint(messages_first_plan)
        print(f"############   end   ##############\n")
        
        #setup the messages for the loop
        messages_curr_plan = []
        messages_functions=[]
        messages_system = [{"role": "system", "content": f"{self.system_role}. {formatted_now}. {location}. {user}"}]
        messages_user = [{"role": "user", "content": query}]
        while True:
            messages = messages_system + messages_user + messages_first_plan + messages_curr_plan + messages_functions
            response = self.send_message(messages)
            function_args, function_name, result, planning = self.process_function_call(response)
            if result:
                function_message = {
                    "role": "function",
                    "name": function_name if function_name else "unknown",
                    "content": f"function args: {json.dumps(function_args)}\nresponse:\n{result}",
                }
                messages_functions.append(function_message)
                #messages_curr_plan = [{"role": "assistant", "content": f"To answer the users request I have made the following plan. It needs to be updated based on the results from the function and used if i make another function call in the 'planning' field\nPlan:'{planning}'"}]
            else:
                return response["content"]
