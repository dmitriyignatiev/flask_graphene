import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from sales.api.mutations import myMutation
# from sales.api.subscriptions import Subscription
from sales.models import (
                          User as UserModel,
                          Deal as DealModel,
                          Customer as CustomerModel,
                          )


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
        interfaces = (CustomNode_, )

class Deal(SQLAlchemyObjectType):
    class Meta:
        model = DealModel
        interfaces = (CustomNode_,)

class Customer(SQLAlchemyObjectType):
    class Meta:
        model=CustomerModel
        interfaces = (CustomNode_, )


class New(graphene.ObjectType):
    hi = graphene.String()

    def resolve_hi(self, info):
        return 'Say it'



import graphene
import graphene_sqlalchemy

from main import app
from sales.models import User


class Subscription(graphene.ObjectType):
    users = graphene_sqlalchemy.SQLAlchemyConnectionField(
        User,
        active=graphene.Boolean()
    )

    def resolve_users(self, args, context, info):
        with app.app_context():
            query = User.get_query(context)
            return query.filter_by(id=info.root_value.get('id'))

class Query_(graphene.ObjectType):

    all_users = FilterableConnectionField(User.connection,
                                          filters=UserFilter())

    all_deals = FilterableConnectionField(Deal.connection, filters=DealFilter(), sort=None)

    all_customers=FilterableConnectionField(Customer.connection, filters=CustomerFilter())

schema = graphene.Schema(query=Query_,
                         mutation=myMutation,
                         # subscription=Subscription
                         )