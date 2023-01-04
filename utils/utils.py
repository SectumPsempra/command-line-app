from config import config
from utils import exceptions
import os
import datetime

def validate_args(args: list) -> None:
    err_message = (
        "File path not entered or extra arguments passed."
        f" Expected arguments are: {config.SUPPORTED_APP_ARGS}."
    )
    try:
        assert len(args) == len(config.SUPPORTED_APP_ARGS)
    except AssertionError:
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    except Exception as err:
        raise exceptions.INPUT_DATA_ERROR(message=err)

def validate_path(path: str) -> None:
    err_message = "File path is not valid or file doesn't exist"
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        file_path = os.path.join(base_dir, path)
        assert os.path.isfile(file_path)
        return file_path
    except AssertionError:
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    except Exception as err:
        raise exceptions.INPUT_DATA_ERROR(message=err)

def detect_command(line: str, separator: str=" ") -> list:
    args = line.split(sep=separator)
    return args

def _validate_add(args: list, command: str) -> None:
    if command != config.ADD:
        return
    err_message = ""
    try:
        _date, _min, _max = args[-3], args[-2], args[-1]
        err_message = "Minimum one enrollment must be done"
        assert _min >= 1
        err_message = "Max employees can not be less than min employees"
        assert _min <= _max
        err_message = "Date should be specified in ddmmyyyy format"
        assert len(_date) == 8
        _ = datetime.datetime(day=int(_date[:2]),
                                month=int(_date[2:4]),
                                year=int(_date[4:]))
    except AssertionError:
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    except Exception as err:
        raise exceptions.INPUT_DATA_ERROR(message=err)

def validate_command(args: list) -> list:
    try:
        cmd_name = args[0]
        updated_args = args[1:]
        cmd_metadata = config.COMMANDS_METADATA.get(cmd_name)
        err_message = (
            "Please specify a valid command and ensure its argument"
            " are in correct order. List of valid commands and the"
            f" parameters they support:\n{config.SUPPORTED_COMMANDS}"
        )
        assert cmd_metadata
        assert len(cmd_metadata) == len(updated_args)

        updated_args = [
            typ(val.strip()) if not isinstance(val, typ) else val.strip() \
                for typ, val in zip(cmd_metadata, updated_args)
        ]

        _validate_add(args=updated_args, command=cmd_name)
        return cmd_name, updated_args
    except AssertionError:
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    except Exception as err:
        raise err

def parse_file(arguments):
    validate_args(args=arguments)
    err_message = (
        "Input file should have valid content."
    )
    try:
        file_path = arguments[1]
        abs_file_path = validate_path(file_path)
        file_handle = open(abs_file_path, 'r')
        lines = file_handle.readlines()
        assert lines
        return lines
    except AssertionError:
        raise exceptions.INPUT_DATA_ERROR(message=err_message)

def print_output(result) -> None:
    res_type = {str: result, tuple: "\n".join(result), list: "\n".join(result)}
    print(res_type.get(type(result)))
