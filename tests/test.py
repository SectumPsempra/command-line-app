import unittest
from src.course_manager import Add, Register, Allot, Cancel
from src.constants import Constants
from utils import exceptions
from utils import utils


class TestApp(unittest.TestCase):
    def test_add(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        courses.execute("Advanced Physics 2", "Stephen Hawking", "120223", 1, 1)
        expected_output = sorted([
            "OFFERING-Advanced Physics-Stephen Hawking",
            "OFFERING-Advanced Physics 2-Stephen Hawking"
        ])
        output = sorted(list(courses.courses.keys()))
        self.assertEqual(expected_output, output)

    def test_add_course_full(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 1)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        email_id = "test@email.com"
        courses = Register(courses.courses, courses.course_reg)
        courses.execute(email_id=email_id, course_id=course_id)
        email_id = "test2@email.com"
        courses.execute(email_id=email_id, course_id=course_id)
        expected_slots_left = 0
        self.assertEqual(expected_slots_left,
                         courses.courses.get(course_id).get("slots_left"))

    def test_register(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        email_id = "test@email.com"
        courses = Register(courses.courses, courses.course_reg)
        courses.execute(email_id=email_id, course_id=course_id)
        expected_course_reg_dict = {
            "REG-COURSE-test-Advanced Physics": {
                "course_id": course_id,
                "email_id": email_id
            }
        }
        self.assertEqual(expected_course_reg_dict, courses.course_reg)
        slots_left = 1
        self.assertEqual(slots_left,
                         courses.courses.get(course_id).get("slots_left"))

    def test_allot_cancel(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        courses = Allot(courses.courses, courses.course_reg)
        courses.execute(course_id=course_id)
        expected_final_status = Constants.FINAL_STATUS_CANCELED
        self.assertEqual(expected_final_status,
                         courses.courses.get(course_id).get("final_status"))
        
    def test_allot_confirm(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        email_id = "test@email.com"
        courses = Register(courses.courses, courses.course_reg)
        courses.execute(email_id=email_id, course_id=course_id)
        courses = Allot(courses.courses, courses.course_reg)
        courses.execute(course_id=course_id)
        expected_allotment_status = True
        self.assertEqual(expected_allotment_status,
                         courses.courses.get(course_id).get("alloted"))

    def test_cancel_accepted(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        email_id = "test@email.com"
        courses = Register(courses.courses, courses.course_reg)
        courses.execute(email_id=email_id, course_id=course_id)
        course_reg_id = "REG-COURSE-test-Advanced Physics"
        courses = Cancel(courses.courses, courses.course_reg)
        courses.execute(course_reg_id=course_reg_id)
        expected_course_reg = {}
        self.assertEqual(expected_course_reg, courses.course_reg)
        slots_left = 2
        self.assertEqual(slots_left,
                         courses.courses.get(course_id).get("slots_left"))

    def test_cancel_rejected(self):
        courses = Add()
        courses.execute("Advanced Physics", "Stephen Hawking", "120123", 1, 2)
        course_id = "OFFERING-Advanced Physics-Stephen Hawking"
        email_id = "test@email.com"
        courses = Register(courses.courses, courses.course_reg)
        courses.execute(email_id=email_id, course_id=course_id)
        courses = Allot(courses.courses, courses.course_reg)
        courses.execute(course_id=course_id)
        course_reg_id = "REG-COURSE-test-Advanced Physics"
        courses = Cancel(courses.courses, courses.course_reg)
        courses.execute(course_reg_id=course_reg_id)
        expected_slots_left = 1
        self.assertEqual(expected_slots_left,
                         courses.courses.get(course_id).get("slots_left"))

    def test_utils_validate_command_invalid(self):
        try:
            utils.validate_command([
                "ADD-COURSE-OFFERING", "DATASCIENCE", "BOB",
                "05262022", "1", "3"
            ])
        except Exception as err:
            self.assertIsInstance(err, exceptions.INPUT_DATA_ERROR)
        else:
            assert False

    def test_utils_validate_command_valid(self):
        output_cmd_name, output_args = utils.validate_command([
            "ADD-COURSE-OFFERING", "DATASCIENCE", "BOB",
            "05062022", "1", "3\n"
        ])
        expected_cmd_name = "ADD-COURSE-OFFERING"
        expected_args = ["DATASCIENCE", "BOB", "05062022", 1, 3]
        self.assertEqual(output_cmd_name, expected_cmd_name)
        self.assertEqual(output_args, expected_args)

    def test_utils_validate_args(self):
        arg_list = ["sample_input/input2.txt"]
        try:
            validate_args = utils.validate_args(arg_list)
        except Exception as err:
            self.assertIsInstance(err, exceptions.INPUT_DATA_ERROR)
        else:
            assert False

    def test_utils_validate_path_fail(self):
        try:
            abs_path = utils.validate_path("sample_input/wrong_file.txt")
        except Exception as err:
            self.assertIsInstance(err, exceptions.INPUT_DATA_ERROR)
        else:
            assert False

    def test_utils_validate_path_success(self):
        try:
            abs_path = utils.validate_path("sample_input/input1.txt")
        except Exception as err:
            assert False
        else:
            self.assertIsInstance(abs_path, str)

    def test_utils_detect_command(self):
        args = utils.detect_command(("ADD-COURSE-OFFERING DATASCIENCE BOB"
                             " 05062022 1 3\n"))
        self.assertIsInstance(args, list)
        self.assertEqual(len(args), 6)

    def test_validate_command_wrong_cmd(self):
        try:
            output_cmd_name, output_args = utils.validate_command([
                "ADD-COURSE-OFFERINGS", "DATASCIENCE", "BOB",
                "05062022", "1", "3\n"
            ])
        except Exception as err:
            self.assertIsInstance(err, exceptions.INPUT_DATA_ERROR)
        else:
            assert False

    def test_validate_command_invalid_min_max(self):
        try:
            output_cmd_name, output_args = utils.validate_command([
                "ADD-COURSE-OFFERINGS", "DATASCIENCE", "BOB",
                "05062022", "0", "-1\n"
            ])
        except Exception as err:
            self.assertIsInstance(err, exceptions.INPUT_DATA_ERROR)
        else:
            assert False

if __name__ == "__main__":
    unittest.main()
