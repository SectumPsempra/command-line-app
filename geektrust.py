from src import course_manager
from utils import utils
from utils import exceptions
from config import config
import sys

def main():
    try:
        file_content = utils.parse_file(arguments=sys.argv)
        operations = {
            config.ADD: course_manager.Add,
            config.REGISTER: course_manager.Register,
            config.ALLOT: course_manager.Allot,
            config.CANCEL: course_manager.Cancel
        }
        courses, course_registrations = {}, {}
        for line in file_content:
            cmd_args = utils.detect_command(line)
            try:
                command, params = utils.validate_command(cmd_args)
            except exceptions.INPUT_DATA_ERROR:
                print("INPUT_DATA_ERROR")
                continue
            object = operations[command](courses, course_registrations)
            result = object.execute(*params)
            utils.print_output(result=result)
            courses, course_registrations = object.courses, object.course_reg
    except Exception as err:
        raise err

if __name__ == "__main__":
    main()
