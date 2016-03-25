from base.lib.testing import TestCase
from base.lib.exceptions import MutableException, ImmutableException


class TestExceptions(TestCase):
    def testMutableException(self):
        e = MutableException(123, "foo")
        self.assertIsInstance(e, Exception)
        self.assertEquals("Exception 123: foo", e.message)
        self.assertEquals("foo", e.get_description())
        self.assertEquals(123, e.get_code())

    def testImmutableException(self):
        e = ImmutableException()
        self.assertIsInstance(e, Exception)
        self.assertEquals("Exception 1000: Generic Error", e.message)
        self.assertEquals("Generic Error", e.get_description())
        self.assertEquals(1000, e.get_code())
