import os
import subprocess

from google import genai

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in the specified file path if it exists and is within the permitted working directory",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="File path to run python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                description="Arguments to pass to the Python file (argv)",
                items=genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            ),
        },
    ),
)


def run_python_file(working_directory: str, file_path: str, args=None) -> str:
    try:
        # early termination if not a python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        completeprocess = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        stdout, stderr, returncode = (
            completeprocess.stdout,
            completeprocess.stderr,
            completeprocess.returncode,
        )

        result = ""

        if returncode != 0:
            result += f"Process exited with code {returncode}\n"

        if stdout:
            result += f"\nSTDOUT: {stdout}"

        if stderr:
            result += f"\nSTDERR: {stderr}"

        if not stdout and not stderr:
            result += "No output produced"

        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
