import graphene
from sqlalchemy.exc import IntegrityError

from sales import models
from sales.models import User, Base, Deal, Customer, user_deal_table
from sales.models import db_session as db

class User_test(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    deal_id = graphene.Int()

class CustomerInput(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    deal_id = graphene.Int()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User_test)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        try:
            user = User(email=email, name=name)
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            print('user exist')
        ok = True
        return CreateUser(user=user, ok=ok)


class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        id = graphene.Int()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User_test)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        id= kwargs.get('id')
        try:
            user = db.query(User).filter(User.id == id).first()
            if user:
                user.name = name
                user.email = email
                db.commit()
        except IntegrityError:
            db.rollback()
            print('user exist')
        ok = True
        return UpdateUser(user=user, ok=ok)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.String()

    def mutate(self, info, id):
        user = db.query(User).filter(User.id == id).first()
        if user:
                db.delete(user)
                db.commit()
                ok = 'User was delete successfully'
        else:
                ok = 'User do not exist'
        return UpdateUser(ok=ok)


class CreateDeal(graphene.Mutation):
    class Arguments:
        name=graphene.String()
        start_date=graphene.Date()
        stage_name=graphene.String()
        net_per_month=graphene.Float()
        gross_per_month = graphene.Float()
        user_id = graphene.Int()

    ok = graphene.String()

    def mutate(self, info, **kwargs):
        deal = Deal(**kwargs)
        try:
            db.add(deal)
            db.commit()
            ok = 'done'
        except IntegrityError:
            db.rollback()
            ok = 'UPS'
        return CreateDeal(ok=ok)


class UpdateDeal(graphene.Mutation):
    class Arguments:
        name=graphene.String()
        start_date=graphene.Date()
        stage_name=graphene.String()
        net_per_month=graphene.Float()
        gross_per_month = graphene.Float()
        user_id = graphene.Int()
        id = graphene.Int()

    ok = graphene.String()

    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        try:
            deal = db.query(Deal).filter(Deal.id == id).update({**kwargs})
            db.commit()
            ok = 'done'
        except IntegrityError:
            db.rollback()
            ok = 'UPS'
        return UpdateDeal(ok=ok)


class DeleteDeal(graphene.Mutation):
    class Arguments:
        id=graphene.Int()

    ok = graphene.String()

    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        try:
            deal = db.query(Deal).filter(Deal.id == id).first()
            db.delete(deal)
            db.commit()
            ok = 'done'
        except IntegrityError:
            db.rollback()
            ok = 'UPS'
        return DeleteDeal(ok=ok)


class CustomerCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        deal_id = graphene.Int()

    ok = graphene.Boolean()
    customer = graphene.Field(lambda: CustomerInput)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        # email = kwargs.get('email')
        deal_id = kwargs.get('deal_id')

        try:
            customer = Customer(name=name)
            db.add(customer)
            deal = db.query(Deal).filter_by(id=deal_id).first()
            customer.deal.append(deal)
            db.commit()
        except IntegrityError:
            db.rollback()
            print('customer exist')
        ok = True
        return CustomerCreate(customer=customer, ok=ok)



class myMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_deal = CreateDeal.Field()
    update_deal = UpdateDeal.Field()
    delete_deal = DeleteDeal.Field()

    customer_create = CustomerCreate.Field()


