import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from sales.models import (
    User as UserModel,
    Deal as DealModel,
    Customer as CustomerModel,
)

import pika


class CustomNode_(graphene.Node):
    class Meta:
        name = 'Node'

    id = graphene.Int()


class UserFilter(FilterSet):
    is_admin = graphene.Boolean()

    class Meta:
        model = UserModel
        fields = {
            'name': ['eq', 'ne', 'in', 'ilike'],
            'id': ['eq', 'ne', 'in', 'ilike'],
            'is_active': [...],  # shortcut!
        }


class CustomerFilter(FilterSet):
    is_admin = graphene.Boolean()

    class Meta:
        model = CustomerModel
        fields = {
            'name': ['eq', 'ne', 'in', 'ilike'],
            'id': ['eq', 'ne', 'in', 'ilike'],
            'is_active': [...],  # shortcut!
        }


class DealFilter(FilterSet):
    is_admin = graphene.Boolean()

    class Meta:
        model = DealModel
        fields = {
            'name': ['eq', 'ne', 'in', 'ilike'],
            'id': ['eq', 'ne', 'in', 'ilike'],
            'is_active': [...],  # shortcut!
        }


class User(SQLAlchemyObjectType):


    class Meta:
        model = UserModel
        interfaces = (CustomNode_,)


class Deal(SQLAlchemyObjectType):


    class Meta:
        model = DealModel
        interfaces = (CustomNode_,)


class Customer(SQLAlchemyObjectType):


    class Meta:
        model = CustomerModel
        interfaces = (CustomNode_,)


class New(graphene.ObjectType):
    hi = graphene.String()

    def resolve_hi(self, info):
        return 'Say it'


class Query(graphene.ObjectType):
    all_users = SQLAlchemyConnectionField(User, filters=UserFilter())


    all_deals = FilterableConnectionField(Deal, filters=DealFilter(), sort=None)

    all_customers = FilterableConnectionField(Customer, filters=CustomerFilter())


