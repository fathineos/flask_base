from base.factory import DB


class AbstractSqlModel(DB.Model):
    __abstract__ = True

    def save(self):
        DB.session.add(self)
        DB.session.commit()

    def remove(self):
        DB.session.delete(self)
        DB.session.commit()
