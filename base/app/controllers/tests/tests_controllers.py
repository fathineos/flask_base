from base.lib.testing import ControllerTestCase


class ControllersTestCase(ControllerTestCase):
    def test_accepts_mimetypes_decorator_raises_proper_exception_when_unsupported_type(self):
        from base.app.controllers import accepts_mimetypes

        @accepts_mimetypes(supported_types=["foo"])
        def dummyFunc():
            return "result"
        from werkzeug.exceptions import UnsupportedMediaType
        with self.assertRaises(UnsupportedMediaType):
            dummyFunc()

    def test_accepts_mimetypes_decorator(self):
        from base.app.controllers import accepts_mimetypes

        @accepts_mimetypes(supported_types=["foo", "application/json"])
        def dummyFunc():
            return "result"
        self.assertEquals("result", dummyFunc())

    def test_jsonify_reponse_object(self):
        from base.app.controllers import jsonify_reponse_object

        class Obj(object):
            def to_dict(self):
                return {"foo": "bar"}

        @jsonify_reponse_object
        def dummyFunc():
            return Obj()
        self.assertTrue("foo" in dummyFunc()[0].data)

    def test_jsonify_reponse_object_raises_exception_when_result_object_doesnt_support_to_dict(self):
        from base.app.controllers import jsonify_reponse_object

        @jsonify_reponse_object
        def dummyFunc():
            return object()
        with self.assertRaises(AttributeError):
            dummyFunc()

    def test_jsonify_reponse_object_when_result_is_tuple(self):
        from base.app.controllers import jsonify_reponse_object

        class Obj(object):
            def to_dict(self):
                return {"foo": "bar"}

        @jsonify_reponse_object
        def dummyFunc():
            return Obj(), 404
        response, status_code = dummyFunc()
        self.assertTrue("foo" in response.data)
        self.assertEquals(status_code, 404)

    def test_set_http_code(self):
        from base.app.controllers import set_http_code

        @set_http_code(201)
        def dummyFunc():
            return "created"

        self.assertEquals(("created", 201), dummyFunc())

    def test_set_http_code_when_code_set(self):
        from base.app.controllers import set_http_code

        @set_http_code(200)
        def dummyFunc():
            return "created", 404

        self.assertEquals(("created", 404), dummyFunc())

    def test_get_parameters_by_method_when_method_is_get(self):
        from flask import request
        r = request
        from werkzeug.datastructures import ImmutableMultiDict
        r.args = ImmutableMultiDict({"foo": "bar"})

        from base.app.controllers import get_parameters_by_method
        params = get_parameters_by_method(r)
        self.assertEquals("bar", params["foo"])

    def test_get_parameters_by_method_when_method_is_post(self):
        self.app_request_context.pop()
        self.app_request_context = self.app.test_request_context(
            content_type="application/json", method="POST",
            data='{"foo": "bar"}')
        self.app_request_context.push()

        from flask import request
        r = request

        from base.app.controllers import get_parameters_by_method
        params = get_parameters_by_method(r)
        self.assertEquals("bar", params["foo"])