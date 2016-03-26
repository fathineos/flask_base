from flask import g
from StringIO import StringIO
from io import BytesIO
from sys import getsizeof
from werkzeug.exceptions import UnsupportedMediaType
from base.lib.exceptions import MutableException
from base.lib.testing import ControllerTestCase
from base.app.models.api.validators import accepts_mimetypes,\
    validate_request, ParamsValidator, _get_allowed_cross_origin_domain,\
    access_cross_origin_resource_sharing_validator, FileValidator,\
    FileTooBigValidator
from base.app.models.api.exceptions import ApiInvalidAccessControlHeader


class TestParamsValidators(ControllerTestCase):

    def test_params_validator_raises_proper_exception_when_missing_required_parameter(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "1", "baf": "2"}')
        self.app_request_context.push()

        @validate_request(ParamsValidator(required_params=['foo', 'bar']))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        with self.assertRaises(MutableException):
            dummyFunc()

    def test_params_validator(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "1", "bar": "2"}')
        self.app_request_context.push()

        @validate_request(ParamsValidator(required_params=['foo', 'bar']))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        self.assertIsNotNone(dummyFunc())

    def test_validate_request_raises_proper_exception_when_missing_file_name(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST")
        self.app_request_context.push()

        @validate_request(FileValidator(file_name='transactions_csv'))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        with self.assertRaises(MutableException) as cm:
            dummyFunc()

        excp = cm.exception
        self.assertEquals(excp.get_description(), "File transactions_csv Missing")

    def test_file_validator(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="multipart/form-data",
            method="POST",
            data={'transactions_csv': (StringIO('test'), 'transactions_csv')})
        self.app_request_context.push()

        @validate_request(FileValidator(file_name='transactions_csv'))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        self.assertIsNotNone(dummyFunc())

    def test_file_too_big_validator_raises_proper_exception(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="multipart/form-data",
            method="POST",
            data={'transactions_csv': (StringIO('this is longer than 10'), 'transactions_csv')})
        self.app_request_context.push()
        size_limit = getsizeof(BytesIO(""))

        @validate_request(FileTooBigValidator(
            file_name='transactions_csv', size_limit=size_limit))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        with self.assertRaises(MutableException) as cm:
            dummyFunc()

        excp = cm.exception
        self.assertEquals(excp.get_description(), "File larger than {} bytes".format(size_limit))

    def test_file_too_big_validator(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="multipart/form-data",
            method="POST",
            data={'transactions_csv': (StringIO('short'), 'transactions_csv')})
        self.app_request_context.push()

        @validate_request(FileTooBigValidator(
            file_name='transactions_csv', size_limit=1000))
        def dummyFunc():
            return "foo", 201, {"header": "bar"}

        self.assertIsNotNone(dummyFunc())


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

    def test_access_cross_origin_resource_sharing_validator_when_valid_origin_on_request(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="POST",
            data='{"foo": "bar"}',
            headers={"Origin": "http://test.local"})
        self.app_request_context.push()

        @access_cross_origin_resource_sharing_validator
        def dummyFunc():
            return "foo", 201, {"header": "bar"}
        result = dummyFunc()
        self.assertEquals("http://test.local",
                          result.headers["Access-Control-Allow-Origin"])
        self.assertEquals(g.allow_origin_domain, "http://test.local")
        self.assertEquals(result.response, ["foo"])
        self.assertEquals(result.status_code, 201)

    def test_access_cross_origin_resource_sharing_validator_when_options_request(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json",
            method="OPTIONS",
            data='{"foo": "bar"}',
            headers={"Origin": "http://test.local"})
        self.app_request_context.push()

    def test_access_cross_origin_resource_sharing_validator_when_invalid_options_request(self):
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
