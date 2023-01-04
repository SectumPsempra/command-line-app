class CourseManager:
    """Course manager provides functionality to add a course, register
    for a course, cancel registration, and allot a course to all registered
    employees
    """
    ID_COURSE_OFFERING = "OFFERING-{}-{}"
    ID_COURSE_REGISTRATION = "REG-COURSE-{}-{}"

    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_COURSE_FULL = "COURSE_FULL_ERROR"
    # STATUS_COURSE_CANCEL = "COURSE_CANCELED"

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

    def __init__(self):
        """constructor of CourseManager class. Initializes class and keeps
        track of employees registered for courses.
        """
        self.courses = {}
        self.course_reg = {}

    def __add_course(self, course_id: str, values: list) -> None:
        self.courses[course_id] = {
            CourseManager.title: values[0],
            CourseManager.instructor: values[1],
            CourseManager.min_emp: values[2],
            CourseManager.max_emp: values[3],
            CourseManager.slots_left: values[4],
            CourseManager.date: values[5],
            CourseManager.final_status: None,
            CourseManager.alloted: False,
            CourseManager.course_registered_ids: set()
        }

    def add(self, title: str, instructor: str, date: str,
            min_emp: int, max_emp: int) -> None:
        """Adds a new course to courses data

        Args:
            title (str): title of the course.
            instructor (str): instructor who will teach the course.
            date (str): offering date of the course.
            min_emp (int): minimum number of employees that should enroll in
                this course.
            max_emp (int): maximum number of employees that can enroll in
                this course.
            courses (dict): All the information of a course by course offering
                id.

        Returns:
            dict: updated courses.
        """
        course_id = CourseManager.ID_COURSE_OFFERING.format(
            title, instructor
        )
        slots_left = max_emp
        self.__add_course(
            course_id=course_id,
            values=[title, instructor, min_emp, max_emp, slots_left, date]
        )
        return f'{course_id}'

    def __add_registered_course(self, registration_id: str,
                                values: list) -> None:
        self.course_reg[registration_id] = {
            CourseManager.course_id: values[0],
            CourseManager.email_id: values[1]
        }

    def __set_registration_id(self, values: list) -> str:
        return CourseManager.ID_COURSE_REGISTRATION.format(*values)

    def __get_name(self, email_id, separator="@"):
        return email_id.split(sep=separator)[0]

    def __get_course(self, course_id: str) -> dict:
        return self.courses.get(course_id)

    def __update_post_registrations(self, course, course_id,
                                    registration_id: str) -> dict:
        course[CourseManager.course_registered_ids].add(registration_id)
        course[CourseManager.slots_left] -= 1
        self.courses[course_id] = course

    def register(self, email_id: str, course_id: str) -> None:
        """Register an employee for a course

        Args:
            email_id (str): email id of the employee.
            course_id (str): course id of the course for which employee
                wants to register.
            courses (dict): available courses.
            course_reg (dict): employee course registrations.

        Returns:
            tuple: updated courses and employee registrations.
        """
        course = self.__get_course(course_id)
        emp_name = self.__get_name(email_id=email_id)
        course_name = course.get(CourseManager.title)
        course_registration_id = self.__set_registration_id(
            values=[emp_name, course_name]
        )
        if course.get(CourseManager.slots_left):
            self.__add_registered_course(
                registration_id=course_registration_id,
                values=[course_id, email_id]
            )
            self.__update_post_registrations(
                course=course, course_id=course_id,
                registration_id=course_registration_id
            )
            return f'{course_registration_id} {CourseManager.STATUS_ACCEPTED}'
        else:
            return f'{CourseManager.STATUS_COURSE_FULL}'

    def __min_slots_filled(self, course: dict) -> bool:
        if course.get(CourseManager.max_emp) - \
            course.get(CourseManager.slots_left) < \
                course.get(CourseManager.min_emp):
                    return False
        return True

    def __format_allotments(self, course: dict, course_id: str) -> list:
        result = []
        registered_course_ids = sorted(course.get(
            CourseManager.course_registered_ids))
        for reg_id in registered_course_ids:
            email = self.course_reg.get(reg_id).get(CourseManager.email_id)
            result.append(f'{reg_id} {email} {course_id}'
                  f' {course.get(CourseManager.title)}'
                  f' {course.get(CourseManager.instructor)}'
                  f' {course.get(CourseManager.date)}'
                  f' {course.get(CourseManager.final_status)}')
        return result

    def allot(self, course_id: str) -> list:
        """Allot a course to all employees who registered for it

        Args:
            course_id (str): course id of the course for which employee
                wants to register.
            courses (dict): available courses.
            course_reg (dict): employee course registrations.

        Returns:
            dict: updated courses.
        """
        course = self.__get_course(course_id=course_id)
        if self.__min_slots_filled(course=course):
            course[CourseManager.final_status] = \
                CourseManager.FINAL_STATUS_CONFIRMED
            course[CourseManager.alloted] = True
        else:
            course[CourseManager.final_status] = \
                CourseManager.FINAL_STATUS_CANCELED
        self.courses[course_id] = course
        result = self.__format_allotments(course=course, course_id=course_id)
        return result

    def __update_post_cancel(self, course: dict, course_id: str,
                             registration_id: str):
        course.get(CourseManager.course_registered_ids).remove(registration_id)
        course[CourseManager.slots_left] += 1
        self.course_reg.pop(registration_id)
        self.courses[course_id] = course

    def cancel(self, course_reg_id: str) -> None:
        """Cancel a registered course if it is not alloted

        Args:
            course_reg_id (str): registered course id.
            courses (dict): available courses.
            course_reg (dict): employee course registrations.

        Returns:
            tuple: updated courses and employee registrations.
        """
        course_id = self.course_reg.get(course_reg_id).get(
            CourseManager.course_id
        )
        course = self.__get_course(course_id=course_id)
        if course.get(CourseManager.alloted):
            return f'{course_reg_id} {CourseManager.CANCEL_REJECTED}'
        else:
            self.__update_post_cancel(course=course,
                                      course_id=course_id,
                                      registration_id=course_reg_id)
            return f'{course_reg_id} {CourseManager.CANCEL_ACCEPTED}'
