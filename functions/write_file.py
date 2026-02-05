import os

from google import genai
from typing_extensions import Required

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Path to the file to write or truncate overwrite, relative to the working directory.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
