from src import register, add, cancel, allot
from utils import utils
from utils import exceptions
from config import config
import sys

def main():    
    file_content = utils.parse_file(arguments=sys.argv)
    operations = {
        config.ADD: add.Add,
        config.REGISTER: register.Register,
        config.ALLOT: allot.Allot,
        config.CANCEL: cancel.Cancel
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

if __name__ == "__main__":
    main()
