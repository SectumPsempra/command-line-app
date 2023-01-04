# Valid commands
ADD = "ADD-COURSE-OFFERING"
REGISTER = "REGISTER"
ALLOT = "ALLOT"
CANCEL = "CANCEL"

# data types of arguments different commands support
COMMANDS_METADATA = {
    ADD: (str, str, str, int, int),
    REGISTER: (str, str),
    ALLOT: (str,),
    CANCEL: (str,)
}

# commands and expected parameters
SUPPORTED_COMMANDS = (
    "ADD-COURSE-OFFERING <course-name> <instructor>"
    " <date-in-ddmmyyyy> <minEmployees> <maxEmployees>\n"
    "REGISTER <email-id> <course-offering-id>\n"
    "ALLOT-COURSE <course-offering-id>\n"
    "CANCEL <course-registration-id>\n"
)

# arguments supported while starting the app from command line
SUPPORTED_APP_ARGS = ("module name", "file path")
