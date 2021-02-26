from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

engine = create_engine('postgresql://postgres:postgres@db:5432/sales', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

user_deal_table = Table('user_deal', Base.metadata,
    Column('customers_id', Integer, ForeignKey('customers.id')),
    Column('deals_id', Integer, ForeignKey('deals.id'))
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    deals = relationship('Deal')
    customers=relationship('Customer')


class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_date = Column(Date)
    stage_name = Column(String)
    net_per_month = Column(Float)
    gross_per_month = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    customer = relationship('Customer',
                            secondary=user_deal_table,
                            # back_populates='deals'
                            )


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    deal = relationship('Deal',
                          secondary=user_deal_table,
                          # back_populates='customers'
                        )





