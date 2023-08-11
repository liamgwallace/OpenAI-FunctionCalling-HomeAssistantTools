from openai_decorator import OpenAI_functions, OpenAI_function_collection
from pprint import pprint

# Create an OpenAI_functions instance for math_funcs.py
math_functions = OpenAI_functions.from_file("tools/math_funcs.py")
print("\nmath_func_list:\n")
pprint(math_functions.func_list)
print("\nmath_func_mapping:")
pprint(math_functions.func_mapping)
print("\nmath_func_descriptions:")
print(math_functions.func_description)

# Create an OpenAI_functions instance for weather_funcs.py
weather_functions = OpenAI_functions.from_file("tools/weather_funcs.py")
print("\nweather_func_list:\n")
pprint(weather_functions.func_list)

# Create an OpenAI_function_collection instance from the tools folder
all_functions = OpenAI_function_collection.from_folder("tools")
print("\nall_func_list:")
pprint(all_functions.func_list)
print("\nall_func_descriptions:")
print(all_functions.func_description)
print("\nall_func_mapping:")
pprint(all_functions.func_mapping())

# Calling a function using math_functions
function_call_math = {
    "arguments": "{\n  \"a\": 3,\n  \"b\": 4\n}",
    "name": "sum"
}
result_math = math_functions.call_func(function_call_math)
print(f"\nThe result of {function_call_math['name']}(3, 4) is {result_math}")

# Calling a function using all_functions
function_call_all = {
    "arguments": "{\n  \"location\": \"New York\"\n}",
    "name": "curr_weather"
}
result_all = all_functions.call_func(function_call_all)
print(f"\nThe result of {function_call_all['name']}('New York') is {result_all}")
