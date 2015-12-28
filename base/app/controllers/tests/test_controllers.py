from base.lib.testing import ControllerTestCase
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from werkzeug.datastructures import ImmutableMultiDict
from flask.wrappers import Response
from flask import make_response, request, g
from base.app.models.api.exceptions import ApiInvalidAccessControlHeader
from base.app.controllers.validator import ArgumentValidator, FileValidator
from base.app.controllers import _get_response_from_result,\
    get_parameters_by_method, accepts_mimetypes,\
    _get_allowed_cross_origin_domain,\
    access_cross_origin_resource_sharing_header,\
    validate


class ControllersTestCase(ControllerTestCase):

    def test_validate_raises_proper_exception_when_missing_required_parameter(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar", "baf": "baf"}')
        self.app_request_context.push()

        @validate(ArgumentValidator(required_args=['foo', 'bar']))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        with self.assertRaises(BadRequest) as cm:
            dummyFunc()

        excp = cm.exception
        self.assertEquals(excp.description, "Required pamameter bar is missing.")

    # def test_validate_raises_proper_exception_when_missing_file_name(self):
    #     csv_file = Mock()
    #     self.app_request_context.pop()
    #     self.app_request_context = self.app.test_request_context(
    #         content_type="application/json",
    #         method="POST",
    #         data={'files': csv_file})
    #     self.app_request_context.push()

    #     @validate(FileValidator(file_name='transactions_csv'))
    #     def dummyFunc():
    #         return "foo", 201, {"header": "bar"}

    #     with self.assertRaises(BadRequest) as cm:
    #         dummyFunc()

    #     excp = cm.exception
    #     self.assertEquals(excp.description, "No file transactions_csv in request.")

    def test_accepts_mimetypes_decorator_raises_proper_exception_when_unsupported_type(self):
        @accepts_mimetypes(supported_types=["foo"])
        def dummyFunc():
            return "result"
        with self.assertRaises(UnsupportedMediaType):
            dummyFunc()

    def test_accepts_mimetypes_decorator(self):
        @accepts_mimetypes(supported_types=["foo", "application/json"])
        def dummyFunc():
            return "result"
        self.assertEquals("result", dummyFunc())

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
        response = _get_response_from_result(result)
        self.assertIsInstance(response, Response)
        self.assertEquals(response.response, ["foo"])
        self.assertEquals(response.status_code, 201)
        self.assertIn(response.headers["Origin"], "http://test.local")

    def test_get_reponse_from_result_when_reponse_object_provided(self):
        result = make_response("foo", 201, {"Origin": "http://test.local"})
        response = _get_response_from_result(result)
        self.assertIsInstance(response, Response)
        self.assertEquals(response.response, ["foo"])
        self.assertEquals(response.status_code, 201)
        self.assertIn(response.headers["Origin"], "http://test.local")

    def test_get_allowed_cross_origin_domain_when_valid_domain(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar"}',
            headers={"Origin": "http://test.local"})
        self.app_request_context.push()
        domain = _get_allowed_cross_origin_domain()
        self.assertEquals(domain, "http://test.local")
        self.assertEquals(g.allow_origin_domain, "http://test.local")

    def test_get_allowed_cross_origin_domain_when_invalid_domain(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar"}',
            headers={"Origin": "http://invalid"})
        self.app_request_context.push()
        with self.assertRaises(ApiInvalidAccessControlHeader):
            _get_allowed_cross_origin_domain()
        with self.assertRaises(AttributeError):
            self.assertIsNone(g.allow_origin_domain)

    def test_access_cross_origin_resource_sharing_header_when_valid_origin_on_request(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar"}',
            headers={"Origin": "http://test.local"})
        self.app_request_context.push()

        @access_cross_origin_resource_sharing_header
        def dummyFunc():
            return "foo", 201, {"header": "bar"}
        result = dummyFunc()
        self.assertEquals("http://test.local",
                          result.headers["Access-Control-Allow-Origin"])
        self.assertEquals(g.allow_origin_domain, "http://test.local")
        self.assertEquals(result.response, ["foo"])
        self.assertEquals(result.status_code, 201)

    def test_access_cross_origin_resource_sharing_header_when_options_request(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="OPTIONS",
            data='{"foo": "bar"}',
            headers={"Origin": "http://test.local"})
        self.app_request_context.push()

    def test_access_cross_origin_resource_sharing_header_when_options_request(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="OPTIONS",
            data='{"foo": "bar"}',
            headers={"Origin": "http://invalid"})
        self.app_request_context.push()
        with self.assertRaises(ApiInvalidAccessControlHeader):
            _get_allowed_cross_origin_domain()
        with self.assertRaises(AttributeError):
            self.assertIsNone(g.allow_origin_domain)
