import sqlalchemy as sa
from source.db.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(sa.Integer, primary_key=True)
    nm_id = sa.Column(sa.BIGINT)

    def __str__(self):
        return str(self.nm_id)

    def __repr__(self):
        return str(self.nm_id)


class Screenshot(Base):
    __tablename__ = 'screenshots'

    id = sa.Column(sa.Integer, primary_key=True)
    nm_id = sa.Column(sa.BIGINT)
    screenshot_path = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime)

    def __str__(self):
        return str(self.nm_id)

    def __repr__(self):
        return str(self.nm_id)
