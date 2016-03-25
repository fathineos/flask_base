from base.lib.testing import ControllerTestCase
from werkzeug.datastructures import ImmutableMultiDict
from flask.wrappers import Response
from flask import make_response, request
from base.app.models.api import get_response_from_result,\
    get_parameters_by_method


class ControllersTestCase(ControllerTestCase):

    def test_get_parameters_by_method_when_method_is_get(self):
        r = request
        r.args = ImmutableMultiDict({"foo": "bar"})

        params = get_parameters_by_method()
        self.assertEquals("bar", params["foo"])

    def test_get_parameters_by_method_when_method_is_post(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar"}')
        self.app_request_context.push()

        params = get_parameters_by_method()
        self.assertEquals("bar", params["foo"])

    def test_get_response_from_result_when_tuple_provided(self):
        result = ("foo", 201, {"Origin": "http://test.local"})
        response = get_response_from_result(result)
        self.assertIsInstance(response, Response)
        self.assertEquals(response.response, ["foo"])
        self.assertEquals(response.status_code, 201)
        self.assertIn(response.headers["Origin"], "http://test.local")

    def test_get_reponse_from_result_when_reponse_object_provided(self):
        result = make_response("foo", 201, {"Origin": "http://test.local"})
        response = get_response_from_result(result)
        self.assertIsInstance(response, Response)
        self.assertEquals(response.response, ["foo"])
        self.assertEquals(response.status_code, 201)
        self.assertIn(response.headers["Origin"], "http://test.local")
