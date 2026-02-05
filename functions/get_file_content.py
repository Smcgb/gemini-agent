import os

from google import genai

# provided by tutorial
schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Get the first 10000 characters of a file in an approved directory",
    parameters=genai.types.Schema(
        required=["file_path"],
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(
    working_directory: str = ".", file_path: str = ".", max_chars: int = 10000
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(max_chars)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {max_chars} characters]'
                )

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

    return content
