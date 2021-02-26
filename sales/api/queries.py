import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
from rx import Observable
import random

from sales.api.mutations import myMutation

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


        def resolve_stageName(self, info):
            return 'hi'





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




class Query_(graphene.ObjectType):

    all_users = FilterableConnectionField(User, filters=UserFilter())
    #
    all_deals = FilterableConnectionField(Deal, filters=DealFilter())
    #
    all_customers=FilterableConnectionField(Customer, filters=CustomerFilter())













class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())

    random_int = graphene.Field(RandomType)

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_random_int(root, info):
        return Observable.interval(1000).map(lambda i: RandomType(seconds=i, random_int=random.randint(0, 500)))





schema = graphene.Schema(query=Query_,
                         mutation=myMutation,
                         subscription=Subscription
                         )