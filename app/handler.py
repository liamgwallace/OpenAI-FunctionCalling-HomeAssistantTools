import json
import os
import pprint
import openai
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from dateutil.tz import tzlocal


class OpenAIHandler:
    def __init__(self, api_functions, function_definitions, system_role="", model="gpt-4-0613", temperature=0.2):
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
Use the user content and the function results to decide.
Always call a suitable function, NEVER ask the user for input. Make the best assumption based on the data you have
Only use the functions you have been provided with. Do not guess at the data needed for a function, try and see if you can search for what is needed using a function at your disposal
"""
#When you call a function you must first plan all the steps you will need to take to complete the user task in the notepad. 
#If you have been provided with an old notepad you will update this based on the result from the last function message.
#Keep a track of the successfull steps taken, the next one you are about to take and the planned tasks required to complete the user objective.
#Do not return the plan to the user, just the result.
#"""

    def send_message(self, messages):
        #print(f"\n\n############   messages   ##############")
        #pprint.pprint(messages)
        #print(f"############   messages   ##############\n")
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            functions=self.function_definitions,
        )
        #print(f"\nresponse:")
        #pprint.pprint(response)
        #print("")
        response = response["choices"][0]["message"]
        return response

    def process_function_call(self, response):
        function_name = None
        function_args = None
        notepad = None
        result = None

        try:
            if 'function_call' in response:
                function_call = response['function_call']
                function_name = function_call.get('name')

                # Ensure that arguments is a dictionary
                function_args_dict = function_call.get('arguments', {})
                if isinstance(function_args_dict, str):
                    function_args_dict = json.loads(function_args_dict)

                notepad = function_args_dict.pop('notepad', None)

                function_args_json = json.dumps(function_args_dict)
                function_args = json.loads(function_args_json)
                print(f"\n##########################")
                print("Notepad:")
                pprint.pprint(notepad)
                print(f"\nCalling function: {function_name}")
                print(f"Arguments: {function_args}")
                print("##########################")

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

        return function_name, result, notepad

    def send_response(self, query):
        # Format the datetime object as a string
        formatted_now = f" the current time is {datetime.now(tzlocal()).strftime('%Y-%m-%dT%H:%M:%S%z')}"
        messages_system = [
            {"role": "system", "content": f"{self.system_role}. {formatted_now}"},
            {"role": "user", "content": query}
        ]  
        messages = messages_system
        messages_functions=[]
        while True:
            response = self.send_message(messages)
            function_name, result, notepad = self.process_function_call(response)

            if result:
                function_message = {
                    "role": "function",
                    "name": function_name if function_name else "unknown",
                    "content": result,
                }
                messages_functions.append(function_message)
                
                if notepad:
                    notepad_message = {"role": "assistant", "content": f"To answer the users request I have made the following plan. I will update it as i get more information. I will store the updated plan in the function 'notepad' Plan:'{notepad}'"}
                    messages_functions.append(notepad_message)

                messages = messages_system + messages_functions
            else:
                return response["content"]
