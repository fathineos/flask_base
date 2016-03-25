from base.lib.testing import TestCase
# from werkzeug.exceptions import InternalServerError
from base.exception_handler import exception_handler
from base.app.models.api.exceptions import ApiRequestValidationException


class ExceptionHandlerTestCase(TestCase):

    def test_check_and_set_default_error_code_and_description_sets_defaults_when_attributes_do_not_exist(self):
        error = Exception("dummy exception")
        actual_response = exception_handler(error)

        self.assertEquals("500 INTERNAL SERVER ERROR", actual_response.status)
        self.assertIn("\"message\": \"dummy exception\"", actual_response.data)
        self.assertIn("\"code\": 1000", actual_response.data)

    def test_error_handler_properly_sets_http_code_when_validation_exception(self):
        error = ApiRequestValidationException()
        actual_response = exception_handler(error)

        self.assertEquals("400 BAD REQUEST", actual_response.status)
        self.assertIn("\"message\": \"Request Validation Error\"", actual_response.data)
        self.assertIn("\"code\": 1200", actual_response.data)
