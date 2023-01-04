from dataclasses import dataclass

@dataclass
class Constants:
    ID_COURSE_OFFERING = "OFFERING-{}-{}"
    ID_COURSE_REGISTRATION = "REG-COURSE-{}-{}"

    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_COURSE_FULL = "COURSE_FULL_ERROR"

    FINAL_STATUS_CONFIRMED = "CONFIRMED"
    FINAL_STATUS_CANCELED = "COURSE_CANCELED"

    CANCEL_ACCEPTED = "CANCEL_ACCEPTED"
    CANCEL_REJECTED = "CANCEL_REJECTED"

    title = "title"
    instructor = "instructor"
    min_emp = "min_emp"
    max_emp = "max_emp"
    slots_left = "slots_left"
    date = "date"
    final_status = "final_status"
    alloted = "alloted"
    course_registered_ids = "course_registered_ids"
    
    course_id = "course_id"
    email_id = "email_id"
