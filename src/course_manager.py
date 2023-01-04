"""Course manager provides functionality to add a course, register
for a course, cancel registration, and allot a course to all registered
employees
"""
from src.constants import Constants


class Add:
    def __init__(self, courses={}, course_reg={}):
        """Instantiates this class

        Args:
            courses (dict): available courses.
            course_reg (dict): employee course registrations.
        """
        self.courses = courses
        self.course_reg = course_reg

    def __add_course(self, course_id: str, values: list) -> None:
        self.courses[course_id] = {
            Constants.title: values[0],
            Constants.instructor: values[1],
            Constants.min_emp: values[2],
            Constants.max_emp: values[3],
            Constants.slots_left: values[4],
            Constants.date: values[5],
            Constants.final_status: None,
            Constants.alloted: False,
            Constants.course_registered_ids: set()
        }

    def __set_id(self, values: list) -> str:
        return Constants.ID_COURSE_OFFERING.format(*values)

    def execute(self, title: str, instructor: str, date: str,
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

        Returns:
            dict: updated courses.
        """
        course_id = self.__set_id(values=[title, instructor])
        slots_left = max_emp
        self.__add_course(
            course_id=course_id,
            values=[title, instructor, min_emp, max_emp, slots_left, date]
        )
        return f'{course_id}'


class Register:
    def __init__(self, courses, course_reg):
        """Instantiates this class

        Args:
            courses (dict): available courses.
            course_reg (dict): employee course registrations.
        """
        self.courses = courses
        self.course_reg = course_reg

    def __register_course(self, registration_id: str, values: list) -> None:
        self.course_reg[registration_id] = {
            Constants.course_id: values[0],
            Constants.email_id: values[1]
        }

    def __set_id(self, values: list) -> str:
        return Constants.ID_COURSE_REGISTRATION.format(*values)

    def update(self, course, course_id, registration_id: str) -> dict:
        course[Constants.course_registered_ids].add(registration_id)
        course[Constants.slots_left] -= 1
        self.courses[course_id] = course

    def get_course(self, course_id: str) -> dict:
        return self.courses.get(course_id)

    def get_name(self, email_id: str, separator: str="@") -> str:
        return email_id.split(sep=separator)[0]

    def execute(self, email_id: str, course_id: str) -> None:
        """Register an employee for a course

        Args:
            email_id (str): email id of the employee.
            course_id (str): course id of the course for which employee
                wants to register.

        Returns:
            tuple: updated courses and employee registrations.
        """
        course = self.get_course(course_id)
        emp_name = self.get_name(email_id=email_id)
        course_name = course.get(Constants.title)
        course_registration_id = self.__set_id(
            values=[emp_name, course_name]
        )
        if course.get(Constants.slots_left):
            self.__register_course(
                registration_id=course_registration_id,
                values=[course_id, email_id]
            )
            self.update(
                course=course, course_id=course_id,
                registration_id=course_registration_id
            )
            return f'{course_registration_id} {Constants.STATUS_ACCEPTED}'
        else:
            return f'{Constants.STATUS_COURSE_FULL}'


class Allot:
    def __init__(self, courses, course_reg):
        """Instantiates this class

        Args:
            courses (dict): available courses.
            course_reg (dict): employee course registrations.
        """
        self.courses = courses
        self.course_reg = course_reg

    def __min_slots_filled(self, course: dict) -> bool:
        if course.get(Constants.max_emp) - \
            course.get(Constants.slots_left) < \
                course.get(Constants.min_emp):
                    return False
        return True

    def __format_allotments(self, course: dict, course_id: str) -> list:
        result = []
        registered_course_ids = sorted(course.get(
            Constants.course_registered_ids))
        for reg_id in registered_course_ids:
            email = self.course_reg.get(reg_id).get(Constants.email_id)
            result.append(f'{reg_id} {email} {course_id}'
                  f' {course.get(Constants.title)}'
                  f' {course.get(Constants.instructor)}'
                  f' {course.get(Constants.date)}'
                  f' {course.get(Constants.final_status)}')
        return result

    def get_course(self, course_id: str) -> dict:
        return self.courses.get(course_id)

    def execute(self, course_id: str) -> list:
        """Allot a course to all employees who registered for it

        Args:
            course_id (str): course id of the course for which employee
                wants to register.

        Returns:
            dict: updated courses.
        """
        course = self.get_course(course_id=course_id)
        if self.__min_slots_filled(course=course):
            course[Constants.final_status] = \
                Constants.FINAL_STATUS_CONFIRMED
            course[Constants.alloted] = True
        else:
            course[Constants.final_status] = \
                Constants.FINAL_STATUS_CANCELED
        self.courses[course_id] = course
        result = self.__format_allotments(course=course, course_id=course_id)
        return result


class Cancel:
    def __init__(self, courses, course_reg):
        """Instantiates this class

        Args:
            courses (dict): available courses.
            course_reg (dict): employee course registrations.
        """
        self.courses = courses
        self.course_reg = course_reg

    def update(self, course: dict, course_id: str,
                             registration_id: str):
        course.get(Constants.course_registered_ids).remove(registration_id)
        course[Constants.slots_left] += 1
        self.course_reg.pop(registration_id)
        self.courses[course_id] = course

    def get_course(self, course_id: str) -> dict:
        return self.courses.get(course_id)

    def execute(self, course_reg_id: str) -> None:
        """Cancel a registered course if it is not alloted

        Args:
            course_reg_id (str): registered course id.

        Returns:
            tuple: updated courses and employee registrations.
        """
        course_id = self.course_reg.get(course_reg_id).get(
            Constants.course_id
        )
        course = self.get_course(course_id=course_id)
        if course.get(Constants.alloted):
            return f'{course_reg_id} {Constants.CANCEL_REJECTED}'
        else:
            self.update(course=course,
                          course_id=course_id,
                          registration_id=course_reg_id)
            return f'{course_reg_id} {Constants.CANCEL_ACCEPTED}'
