import inspect
import functools
import importlib.util
import os
from docstring_parser import parse

# Map python types to JSON schema types
type_mapping = {
    "int": "integer",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "tuple": "array",
    "dict": "object",
    "None": "null",
}

def get_type_mapping(param_type):
    param_type = param_type.replace("<class '", '')
    param_type = param_type.replace("'>", '')
    return type_mapping.get(param_type, "string")

def get_params_dict(params, docstring):
    params_dict = {}
    try:
        # Parse the docstring to get parameter descriptions
        docstring_parsed = parse(docstring)
        param_descriptions = {p.arg_name: p.description for p in docstring_parsed.params}
    except Exception as e:
        print("Error parsing docstring:", e)
        param_descriptions = {}

    for k, v in params.items():
        annotation = str(v.annotation).split("[")
        try:
            param_type = annotation[0]
        except IndexError:
            param_type = "string"

        try:
            array_type = annotation[1].strip("]")
        except IndexError:
            array_type = "string"

        param_type = get_type_mapping(param_type)
        description = param_descriptions.get(k, k)  # Use the parameter name as a fallback

        params_dict[k] = {
            "type": param_type,
            "description": description,
        }

        if param_type == "array":
            if "," in array_type:
                array_types = array_type.split(", ")
                params_dict[k]["prefixItems"] = []
                for i, array_type in enumerate(array_types):
                    array_type = get_type_mapping(array_type)
                    params_dict[k]["prefixItems"].append({
                        "type": array_type,
                    })
            else:
                array_type = get_type_mapping(array_type)
                params_dict[k]["items"] = {
                    "type": array_type,
                }

    return params_dict

def openaifunc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Mark the function as an OpenAI function
    wrapper._is_openai_func = True
    return wrapper

class OpenAI_functions:
    def __init__(self, filename=None):
        if filename:
            self.func_list, self.func_mapping = self._func_list_from_file(filename)
            # Check if a description for the whole func_list exists at the module level
            self.func_description = self._func_description_from_file(filename)
            if not self.func_description:
                self.func_description = "\n".join([func["description"] for func in self.func_list])

    @classmethod
    def from_file(cls, filename):
        return cls(filename)

    def _func_list_from_file(self, filename):
        module_spec = importlib.util.spec_from_file_location(filename, filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        functions_info = []
        function_mapping = {}
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, '_is_openai_func'):
                params = inspect.signature(attr).parameters
                param_dict = get_params_dict(params, attr.__doc__ or "")
                func_info = {
                    "name": attr.__name__,
                    "description": inspect.cleandoc(attr.__doc__ or ""),
                    "parameters": {
                        "type": "object",
                        "properties": param_dict,
                        "required": list(param_dict.keys()),
                    },
                }
                functions_info.append(func_info)
                function_mapping[attr.__name__] = attr

        return functions_info, function_mapping

    def _func_description_from_file(self, filename):
        module_spec = importlib.util.spec_from_file_location(filename, filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return inspect.getdoc(module)

    def func_list(self):
        return self.func_list

    def func_mapping(self):
        return self.func_mapping

    def call_func(self, function_call):
        name = function_call["name"]
        arguments = function_call["arguments"]
        if name not in self.func_mapping:
            raise ValueError(f"Function {name} not found in mapping")

        try:
            arguments = eval(arguments)  # Convert the string to a dictionary
        except Exception as e:
            raise ValueError(f"Invalid arguments format: {e}")

        function = self.func_mapping[name]
        return function(**arguments)

class OpenAI_function_collection:
    def __init__(self):
        self.function_collections = []

    @classmethod
    def from_files(cls, *files):
        instance = cls()
        for file in files:
            instance.function_collections.append(OpenAI_functions.from_file(file))
        return instance

    @classmethod
    def from_folder(cls, folder_path):
        instance = cls()
        for filename in os.listdir(folder_path):
            if filename.endswith(".py"):
                instance.function_collections.append(OpenAI_functions.from_file(os.path.join(folder_path, filename)))
        return instance

    @property
    def func_description(self):
        return "\n".join([funcs.func_description for funcs in self.function_collections])
        
    @property
    def func_list(self):
        return [func for func_collection in self.function_collections for func in func_collection.func_list]
        
    def call_func(self, function_call):
        for funcs in self.function_collections:
            if function_call["name"] in funcs.func_mapping:
                return funcs.call_func(function_call)
        raise ValueError(f"Function {function_call['name']} not found in mapping")

    def func_mapping(self):
        mapping = {}
        for funcs in self.function_collections:
            mapping.update(funcs.func_mapping)
        return mapping
