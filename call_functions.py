from google import genai
from google.genai.types import FunctionCallOrDict

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)


def call_function(function_call: genai.FunctionCall, verbose=False):

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function = function_call.name or ""
    if function not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}

    function_result = function_map[function](**args)
    return genai.types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function,
                response=function_result,
            )
        ],
    )
