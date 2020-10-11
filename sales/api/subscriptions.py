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