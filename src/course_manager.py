class CourseManager:
    """Course manager provides functionality to add a course, register
    for a course, cancel registration, and allot a course to all registered
    employees
    """
    ID_COURSE_OFFERING = "OFFERING-{}-{}"
    ID_COURSE_REGISTRATION = "REG-COURSE-{}-{}"

    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_COURSE_FULL = "COURSE_FULL_ERROR"
    STATUS_COURSE_CANCEL = "COURSE_CANCELED"

    FINAL_STATUS_CONFIRMED = "CONFIRMED"
    FINAL_STATUS_CANCELED = "CANCELED"

    CANCEL_ACCEPTED = "CANCEL_ACCEPTED"
    CANCEL_REJECTED = "CANCEL_REJECTED"

    def __init__(self):
        """constructor of CourseManager class. Initializes class and keeps
        track of employees registered for courses.
        """
        self.courses = {}
        self.course_reg = {}

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
        self.courses[course_id] = {
            "title": title,
            "instructor": instructor,
            "min_emp": min_emp,
            "max_emp": max_emp,
            "slots_left": max_emp,
            "date": date,
            "final_status": None,
            "alloted": False,
            "course_registered_ids": set()
        }
        print(course_id)

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
        course = self.courses.get(course_id)
        emp_name = email_id.split("@")[0]
        course_name = course.get("title")
        course_registration_id = CourseManager.ID_COURSE_REGISTRATION.format(
            emp_name, course_name)
        if course.get("slots_left") > 0:
            course["slots_left"] = course["slots_left"] - 1
            self.course_reg[course_registration_id] = {
                "course_id": course_id,
                "email_id": email_id
            }
            course["course_registered_ids"].add(course_registration_id)
            print(f"{course_registration_id} {CourseManager.STATUS_ACCEPTED}")
        else:
            print(CourseManager.STATUS_COURSE_FULL)
        self.courses[course_id] = course

    def allot(self, course_id: str) -> None:
        """Allot a course to all employees who registered for it

        Args:
            course_id (str): course id of the course for which employee
                wants to register.
            courses (dict): available courses.
            course_reg (dict): employee course registrations.

        Returns:
            dict: updated courses.
        """
        course = self.courses.get(course_id)
        if course.get("max_emp") - course.get("slots_left") < \
                course.get("min_emp"):
            course["final_status"] = CourseManager.FINAL_STATUS_CANCELED
        else:
            course["final_status"] = CourseManager.FINAL_STATUS_CONFIRMED
            course["alloted"] = True
        registered_course_ids = sorted(course.get("course_registered_ids"))
        for reg_id in registered_course_ids:
            email = self.course_reg.get(reg_id).get("email_id")
            print(f'{reg_id} {email} {course_id} {course.get("title")}'
                  f' {course.get("instructor")} {course.get("date")}'
                  f' {course.get("final_status")}')
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
        course_id = self.course_reg.get(course_reg_id).get("course_id")
        course = self.courses.get(course_id)
        if course.get("alloted"):
            print(f"{course_reg_id} {CourseManager.CANCEL_REJECTED}")
        else:
            course.get("course_registered_ids").remove(course_reg_id)
            course["slots_left"] += 1
            self.course_reg.pop(course_reg_id)
            print(f"{course_reg_id} {CourseManager.CANCEL_ACCEPTED}")
        self.courses[course_id] = course
