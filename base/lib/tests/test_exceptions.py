from base.lib.testing import TestCase
from base.lib.exceptions import MutableException, ImmutableException


class TestExceptions(TestCase):
    def testApiException(self):
        e = MutableException(123, "foo")
        self.assertIsInstance(e, Exception)
        self.assertEquals("Exception 123: foo", e.message)
        self.assertEquals("foo", e.description)
        self.assertEquals(123, e.code)


    def testImmutableException(self):
        e = ImmutableException()
        self.assertIsInstance(e, Exception)
        self.assertEquals("Exception 1000: Generic Error", e.message)
        self.assertEquals("Generic Error", e.description)
        self.assertEquals(1000, e.code)
