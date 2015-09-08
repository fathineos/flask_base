from base.lib.testing import TestCase
from base.exception_handler import \
    check_and_set_default_error_code_and_description
from base.exception_handler import error_handler
from base.app.models.api.exceptions import ApiException


class ExceptionHandlerTestCase(TestCase):

    def test_check_and_set_default_error_code_and_description_sets_defaults_when_attributes_do_not_exist(self):
        error = Exception()
        check_and_set_default_error_code_and_description(error)

        self.assertEquals(500, error.code)
        self.assertEquals('Fatal Error', error.description)

    def test_error_handler_properly_sets_http_code_when_validation_exception(self):
        error = ApiException()
        actual_response = error_handler(error)

        self.assertEquals("500 INTERNAL SERVER ERROR", actual_response.status)
        self.assertEquals('{"code": "None", "errors": [{"code": 1000, '
                          '"message": "Generic Api Error"}], "message": null, '
                          '"results": null}', actual_response.data)
