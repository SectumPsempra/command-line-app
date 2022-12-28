from src.course_manager import CourseManager
import utils
import exceptions
import config
import sys

def main():
    try:
        file_content = utils.parse_file(arguments=sys.argv)
        course_mgr = CourseManager()
        fn = {
            config.ADD: course_mgr.add,
            config.REGISTER: course_mgr.register,
            config.ALLOT: course_mgr.allot,
            config.CANCEL: course_mgr.cancel
        }
        for line in file_content:
            cmd_args = utils.detect_command(line)
            try:
                command, params = utils.validate_command(cmd_args)
            except exceptions.INPUT_DATA_ERROR:
                print("INPUT_DATA_ERROR")
                continue
            fn[command](*params)            
    except Exception as err:
        raise err

if __name__ == "__main__":
    main()
