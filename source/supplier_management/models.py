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
    vendor_code = sa.Column(sa.String)
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


class Report(Base):
    __tablename__ = 'reports'

    id = sa.Column(sa.Integer, primary_key=True)
    product_title = sa.Column(sa.String)
    pnc = sa.Column(sa.String)
    supplier_name = sa.Column(sa.String)
    product_link = sa.Column(sa.String)
    brand = sa.Column(sa.String)
    city = sa.Column(sa.String)
    rrc = sa.Column(sa.Integer)
    company_price = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    time = sa.Column(sa.String)
    screen_link = sa.Column(sa.String)

    def to_dict(self) -> dict:
        return {
            'product_title': self.product_title,
            'pnc': self.pnc,
            'supplier_name': self.supplier_name,
            'product_link': self.product_link,
            'brand': self.brand,
            'city': self.city,
            'rrc': self.rrc,
            'company_price': self.company_price,
            'date': self.date.strftime('%m/%d/%Y'),
            'time': self.time,
            'screen_link': self.screen_link,
        }

    def __str__(self):
        return str(self.pnc)

    def __repr__(self):
        return str(self.pnc)
