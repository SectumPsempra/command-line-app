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
