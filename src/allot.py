from src.constants import Constants


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
        course[Constants.final_status] = Constants.FINAL_STATUS_CANCELED
        if self.__min_slots_filled(course=course):
            course[Constants.final_status] = Constants.FINAL_STATUS_CONFIRMED
            course[Constants.alloted] = True
        self.courses[course_id] = course
        result = self.__format_allotments(course=course, course_id=course_id)
        return result
