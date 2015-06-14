from base.lib.testing import TestCase


class TestExceptions(TestCase):
    def testApiException(self):
        from base.app.models.api.exceptions import ApiException
        e = ApiException()
        self.assertIsInstance(e, Exception)
        self.assertEquals((1000, "Generic Api Error"), e.args)
        self.assertEquals("Generic Api Error", e.description)
        self.assertEquals(1000, e.code)

    def testInvalidEnvelopeException(self):
        from base.app.models.api.exceptions import InvalidEnvelopeException
        e = InvalidEnvelopeException()
        self.assertIsInstance(e, Exception)
        self.assertEquals((1100, "Invalid Envelope: General Error"), e.args)
        self.assertEquals("Invalid Envelope: General Error", e.description)
        self.assertEquals(1100, e.code)
