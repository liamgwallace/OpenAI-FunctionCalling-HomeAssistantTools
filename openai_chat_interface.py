from openai_decorator import OpenAI_functions, OpenAI_function_collection
from pprint import pprint
import copy
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def calculate_cost(model_name, token_count, currency):
    model_data = {
        "gpt-4": {"usd": 0.045, "gbp": 0.045 * 0.79},
        "gpt-4-0613": {"usd": 0.045, "gbp": 0.045 * 0.79},
        "gpt-4-32k": {"usd": 0.090, "gbp": 0.090 * 0.79},
        "gpt-4-32k-0613": {"usd": 0.090, "gbp": 0.090 * 0.79},
        "gpt-3.5-turbo": {"usd": 0.00175, "gbp": 0.00175 * 0.79},
        "gpt-3.5-turbo-16k": {"usd": 0.00350, "gbp": 0.00350 * 0.79},
        "gpt-3.5-turbo-0613": {"usd": 0.00175, "gbp": 0.00175 * 0.79},
        "gpt-3.5-turbo-16k-0613": {"usd": 0.00350, "gbp": 0.00350 * 0.79}
    }
    
    model_currency_data = model_data.get(model_name.lower())
    if not model_currency_data:
        return "Invalid model name"
    
    cost = model_currency_data[currency.lower()] * (token_count / 1000)
    return cost

def create_message(role, content, name=None, function_call=None):
    message = {
        "role": role,
        "content": content
    }
    if name:
        message["name"] = name
    if function_call:
        message["function_call"] = function_call
    return message

class OpenAI_LLM:
    def __init__(self, api_key=None, model="gpt-3.5-turbo", temperature=1.0, system_message='You are a helpful assistant. Answer the user query', user_message='{query}', functions=None, function_call=None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")  # Load from .env file if not provided
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.system_message = create_message('system', system_message)
        self.user_message = create_message('user', user_message)
        self.functions = functions if functions else []
        self.function_call = function_call if function_call else "auto"
        self.memory = []
        self.choices = None
        self.response = None  # Initialize the response attribute
        self.running_tokens = 0
        self.running_cost = 0

    def add_messages(self, messages):
        self.memory.extend(messages)

    def clear_messages(self):
        self.memory = []

    def run(self, messages=None, functions=None, function_call=None, **kwargs):
        if messages is None:
            messages = [copy.deepcopy(self.user_message)]
        tmp_messages = copy.deepcopy(messages)
        processed_messages = []  # Store processed messages
        for message in tmp_messages:
            if kwargs:
                try:
                    message['content'] = message['content'].format(**kwargs)
                except KeyError as e:
                    print(f"KeyError: Keyword '{e.args[0]}' not provided. Message content: {message['content']}")
            processed_messages.append(message)

        self.memory.extend(processed_messages)
        combined_messages = [self.system_message] + self.memory

        kwargs_dict = {
            "model": self.model,
            "messages": combined_messages,
            "temperature": self.temperature
        }
        functions_to_use = functions if functions is not None else self.functions
        if functions_to_use is not None:
            kwargs_dict["functions"] = functions_to_use
            function_call_to_use = function_call if function_call is not None else self.function_call
            if function_call_to_use is not None:
                kwargs_dict["function_call"] = function_call_to_use
        try:
            response = openai.ChatCompletion.create(**kwargs_dict)
            if response.choices and response.choices[0].message:
                self.choices = response.choices[0]
                self.response = response  # Store the whole response
                used_tokens = response['usage']['total_tokens']
                self.running_tokens += used_tokens
                self.running_cost += calculate_cost(self.model, used_tokens, "gbp")
        except openai.error.OpenAIError as e:
            print("OpenAIError:", e)
            
    @property
    def response_content(self):
        if self.choices:
            return self.choices['message']['content']
        else:
            return "No response available"

    @property
    def response_function(self):
        if self.choices and 'function_call' in self.choices['message']:
            return self.choices['message']['function_call']
        else:
            return "No function available"

    @property
    def finish_reason(self):
        if self.choices:
            return self.choices['finish_reason']
        else:
            return "No finish reason available"