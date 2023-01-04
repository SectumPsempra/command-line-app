from src.constants import Constants


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
        return f'{Constants.STATUS_COURSE_FULL}'
