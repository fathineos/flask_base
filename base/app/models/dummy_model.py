"""
Simple example database model
"""

from base.lib.abstract_sql_model import AbstractSqlModel
from base.factory import DB


class DummyModel(AbstractSqlModel):
    __tablename__ = 'dummy_model'

    id = DB.Column(DB.Integer, primary_key=True)
    dummy_column = DB.Column(DB.String(10))

    def __init__(self, dummy_column):
        self.dummy_column = dummy_column
