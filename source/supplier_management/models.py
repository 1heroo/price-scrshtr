import sqlalchemy as sa
from sqlalchemy.orm import relationship

from source.db.db import Base


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    seller_id = sa.Column(sa.Integer)

    is_active = sa.Column(sa.Boolean)

    products = relationship('Product', back_populates='supplier')

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(sa.Integer, primary_key=True)
    nm_id = sa.Column(sa.BIGINT)
    salePriceU = sa.Column(sa.Integer)
    priceU = sa.Column(sa.Integer)

    clientSale = sa.Column(sa.Integer)
    basicSale = sa.Column(sa.Integer)

    rrc = sa.Column(sa.Integer)

    supplier_id = sa.Column(sa.Integer, sa.ForeignKey('suppliers.id'))
    supplier = relationship('Supplier', back_populates='products')

    def __str__(self):
        return str(self.nm_id)

    def __repr__(self):
        return str(self.nm_id)
