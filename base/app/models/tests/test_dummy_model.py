from base.lib.testing import TestCase


class TestDummyModel(TestCase):
    def setUp(self):
        super(TestDummyModel, self).setUp()
        from base.app.models.dummy_model import DummyModel
        from base.factory import DB
        DB.create_all()

    def tearDown(self):
        super(TestDummyModel, self).tearDown()
        from base.app.models.dummy_model import DummyModel
        from base.factory import DB
        DB.drop_all()

    def testSaveStoresProperRowInDatabase(self):
        from base.app.models.dummy_model import DummyModel
        from base.factory import DB
        user = DummyModel(dummy_column="foo")
        DummyModel.save(user)
        rows = DB.session.query(DummyModel).all()
        self.assertEqual("foo", rows[0].dummy_column)
        DummyModel.remove(user)
