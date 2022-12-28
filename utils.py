import config
import exceptions
import os
import datetime

def validate_args(args: list) -> None:
    if len(args) != len(config.SUPPORTED_APP_ARGS):
        err_message = (
            "File path not entered or extra arguments passed."
            f" Expected arguments are: {config.SUPPORTED_APP_ARGS}."
        )
        raise exceptions.INPUT_DATA_ERROR(message=err_message)

def validate_path(path: str) -> None:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, path)
    if not os.path.isfile(file_path):
        err_message = "File path is not valid or file doesn't exist"
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    return file_path

def detect_command(line: str, separator: str=" ") -> list:
    args = line.split(sep=separator)
    return args

def validate_command(args: list) -> list:
    cmd_name = args[0]
    updated_args = args[1:]
    cmd_metadata = config.COMMANDS_METADATA.get(cmd_name)
    if not cmd_metadata or len(cmd_metadata) != len(updated_args):
        err_message = (
            "Please specify a valid command and ensure its argument"
            " are in correct order. List of valid commands and the"
            f" parameters they support:\n{config.SUPPORTED_COMMANDS}"
        )
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    for index in range(len(updated_args)):
        param_type = cmd_metadata[index]
        param_value = updated_args[index].strip()
        if not isinstance(param_value, param_type):
            updated_args[index] = param_type(param_value)
        else:
            updated_args[index] = param_value
    if cmd_name == config.ADD:
        _date, _min, _max = updated_args[-3], updated_args[-2], \
            updated_args[-1]
        if _min < 1:
            raise exceptions.INPUT_DATA_ERROR(
                message="Minimum one enrollment must be done"
            )
        if _min > _max:
            raise exceptions.INPUT_DATA_ERROR(
                message="Max employees can not be less than min employees"
            )
        if len(_date) != 8:
            raise exceptions.INPUT_DATA_ERROR(
                message="Date should be specified in ddmmyyyy format"
            )
        try:
            datetime.datetime(day=int(_date[:2]),
                              month=int(_date[2:4]),
                              year=int(_date[4:]))
        except Exception as err:
            raise exceptions.INPUT_DATA_ERROR(
                message=err
            )
    return cmd_name, updated_args

def parse_file(arguments):
    validate_args(args=arguments)
    file_path = arguments[1]
    abs_file_path = validate_path(file_path)
    file_handle = open(abs_file_path, 'r')
    lines = file_handle.readlines()
    if not lines:
        err_message = (
            "Input file should have valid content."
        )
        raise exceptions.INPUT_DATA_ERROR(message=err_message)
    return lines
