from graphene.types import Int
from graphene_sqlalchemy.converter import convert_sqlalchemy_type
from sqlalchemy import PickleType


@convert_sqlalchemy_type.register(PickleType)
def convert_column_to_string(type, column, registry=None):
    return Int
