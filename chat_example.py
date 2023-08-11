from openai_decorator import OpenAI_functions, OpenAI_function_collection
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Example usage
math_functions = OpenAI_functions.from_file("tools/math_funcs.py")
weather_functions = OpenAI_functions.from_file("tools/weather_funcs.py")
all_functions = OpenAI_function_collection.from_folder("tools")

llm_math = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=math_functions.func_list)
llm_weather = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=weather_functions.func_list)
llm_all = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=all_functions.func_list)
llm = llm_all

user_prompt = [create_message("user", "{foo}")]
while True:
    user = input(f"\ninput?\n")
    llm.run(query=user)
    print(f"\nAI response: \n{llm.response_content}\n")
    print(f"\nFinish reason: '{llm.finish_reason}'")
    if llm.finish_reason == 'function_call':        
        print(f"\nAI function call: \n{llm.response_function}\n")
        function_call_result = all_functions.call_func(llm.response_function)
        print(f"\nFunction call result: \n{function_call_result}\n")
        # function_message = {
                    # "role": "function","name": function_name if function_name else "unknown",
                    # "content": f"function args: {json.dumps(function_args)}\nresponse:\n{result}",
                # }
        
        function_message = create_message('function', f"Function response: {function_call_result}")
        llm.add_messages(function_message)

    print(f"\nRunning tokens: {llm.running_tokens}")
    print(f"\nRunning cost:: {llm.running_cost}")