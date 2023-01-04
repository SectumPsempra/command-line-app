from src.constants import Constants

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
        if not course.get(Constants.alloted):
            self.update(course=course,
                          course_id=course_id,
                          registration_id=course_reg_id)
            return f'{course_reg_id} {Constants.CANCEL_ACCEPTED}'
        return f'{course_reg_id} {Constants.CANCEL_REJECTED}'
