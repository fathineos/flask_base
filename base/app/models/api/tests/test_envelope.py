from base.lib.testing import TestCase
from base.app.models.api.envelope import Envelope
from base.app.models.api.exceptions import ApiValidationException


class TestEnvelope(TestCase):
    def testAppendGetErrors(self):
        envelope = Envelope()
        envelope.append_error(111, "foo")
        errors = envelope.get_errors()
        self.assertIsInstance(errors, list)
        self.assertEquals([{"message": "foo", "code": 111}], errors)

    def testAppendMoreErrors(self):
        envelope = Envelope()
        envelope.append_error(111, "foo")
        envelope.append_error(222, "bar")
        errors = envelope.get_errors()
        expected_errors = [{"message": "foo", "code": 111},
                          {"message": "bar", "code": 222}]
        self.assertListEqual(expected_errors, errors)

    def testSetGetCode(self):
        envelope = Envelope()
        envelope.set_code(111)
        self.assertEquals(111, envelope.get_code())

    def testSetCodeRaisesException(self):
        envelope = Envelope()
        from base.app.models.api.exceptions import InvalidEnvelopeParamException
        with self.assertRaises(InvalidEnvelopeParamException):
            envelope.set_code("invalid_param_type")

    def testSetGetResults(self):
        envelope = Envelope()
        envelope.set_results(["foo", "bar"])
        self.assertEquals(["foo", "bar"], envelope.get_results())

    def testSetGetMessage(self):
        envelope = Envelope()
        envelope.set_message("foo")
        self.assertEquals("foo", envelope.get_message())

    def testSetGetMessageRaisesExceptionWhenMessageNotString(self):
        envelope = Envelope()
        from base.app.models.api.exceptions import InvalidEnvelopeParamException
        with self.assertRaises(InvalidEnvelopeParamException):
            envelope.set_message(["func_not_expects_list"])

    def testToDictRaisesExceptionWhenNotValid(self):
        envelope = Envelope()
        from mock import Mock
        envelope._is_valid = Mock(return_value=False)

        from base.app.models.api.exceptions import InvalidEnvelopeException
        with self.assertRaises(InvalidEnvelopeException):
            envelope.to_dict()

    def testToDictReturnProperEnvelope(self):
        envelope = Envelope()
        envelope.set_code(111)
        envelope.set_message("test_message")
        envelope.set_results(["foo", "bar"])
        from mock import Mock
        envelope._is_valid = Mock(return_value=True)
        expected_envelope_result = {"results": ["foo", "bar"],
                                    "message": "test_message",
                                    "code": "111",
                                    "errors": []}
        self.assertEquals(expected_envelope_result, envelope.to_dict())

    def testSetErrorFromExceptionAppendsErrorFromAnException(self):
        envelope = Envelope()
        api_validation_exc = ApiValidationException()
        envelope.set_error_from_exception(api_validation_exc)

        self.assertEquals([{"code": api_validation_exc.code, "message": api_validation_exc.description}], envelope.get_errors())
