# termux_exiftool.py
# A custom wrapper for ExifTool to bypass the `preexec_fn` error on Termux.
# This module mimics the structure of the `pyexiftool` library for compatibility.

import subprocess
import json
import os
from typing import List, Union, Optional

class ExifToolHelper:
    """
    A Termux-compatible replacement for the pyexiftool.ExifToolHelper class.

    It does not keep a persistent exiftool process running, but instead
    calls the command-line tool for each operation. This avoids the
    `subprocess.SubprocessError: Exception occurred in preexec_fn` error
    that occurs on Termux due to permission restrictions with `os.setsid`.
    """

    def __init__(self, executable: str = "exiftool", encoding: str = "utf-8"):
        """
        Initializes the helper.

        Args:
            executable (str): The path to the exiftool executable.
                              Defaults to "exiftool", assuming it's in the system's PATH.
            encoding (str): The encoding to use for decoding output from exiftool.
        """
        self.executable = executable
        self.encoding = encoding
        self._check_executable()

    def _check_executable(self):
        """Verify that the exiftool executable is available."""
        try:
            subprocess.run(
                [self.executable, "-ver"],
                capture_output=True,
                check=True
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"The executable '{self.executable}' was not found. "
                "Please make sure ExifTool is installed and in your PATH. "
                "In Termux, you can install it with `pkg install exiftool`."
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"The executable '{self.executable}' returned an error: {e.stderr.decode(self.encoding, 'ignore')}"
            )

    def execute(self, *params: str, raw_bytes: bool = False) -> Union[str, bytes]:
        """
        Executes the exiftool command with the given parameters.

        This is a replacement for the original `execute` method.

        Args:
            *params: A sequence of string arguments to pass to exiftool.
            raw_bytes (bool): If True, the raw stdout is returned as a bytes
                              object. If False (default), it's decoded as a
                              string using the specified encoding.

        Returns:
            The stdout from the exiftool command as a string or bytes object.

        Raises:
            subprocess.CalledProcessError: If exiftool returns a non-zero exit code.
        """
        command = [self.executable, *params]
        
        # Prepare arguments for the subprocess call
        subprocess_args = {
            "capture_output": True,
            "check": True,
        }

        # Only add the 'encoding' argument if we want a decoded string.
        # If we want raw bytes, we omit it.
        if not raw_bytes:
            subprocess_args["encoding"] = self.encoding

        try:
            result = subprocess.run(command, **subprocess_args)
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Stderr will be bytes if raw_bytes=True, so we need to decode it
            # for the error message.
            stderr_decoded = ""
            if e.stderr:
                try:
                    stderr_decoded = e.stderr.decode(self.encoding, 'ignore')
                except AttributeError:
                    # It might already be a string
                    stderr_decoded = e.stderr
            
            error_message = (
                f"ExifTool command '{' '.join(command)}' failed with exit code {e.returncode}.\n"
                f"Stderr: {stderr_decoded}"
            )
            raise subprocess.CalledProcessError(
                e.returncode, e.cmd, output=e.stdout, stderr=stderr_decoded
            ) from e

    def get_metadata(self, files: Union[str, List[str]]) -> List[dict]:
        """
        Retrieves metadata for one or more files.

        This is a replacement for the original `get_metadata` method. It calls
        exiftool with the '-j' (JSON) and '-G' (Group names) flags.

        Args:
            files: A single file path (str) or a list of file paths (list[str]).

        Returns:
            A list of dictionaries, where each dictionary contains the
            metadata for a corresponding input file.
        """
        if isinstance(files, str):
            file_list = [files]
        elif isinstance(files, list):
            file_list = files
        else:
            raise TypeError("Input 'files' must be a string or a list of strings.")

        for f in file_list:
            if not os.path.exists(f):
                raise FileNotFoundError(f"The file '{f}' does not exist.")

        params = ["-j", "-G", *file_list]
        
        try:
            # Here we expect string output, so raw_bytes is False (default)
            json_output = self.execute(*params)
            if not json_output.strip():
                return []
            return json.loads(json_output)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to decode JSON from exiftool output: {e}\nOutput was: {json_output}") from e

    def __enter__(self):
        """Context manager entry. Returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit. Does nothing, as there's no persistent process."""
        pass