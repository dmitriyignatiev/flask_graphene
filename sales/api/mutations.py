from flask import request
import os

import graphene

from sqlalchemy.exc import IntegrityError

from sales import models
from sales.models import User, Base, Deal, Customer, user_deal_table
from sales.models import db_session as db
from sales.db_session import db_session_

from graphene_file_upload.scalars import Upload

class User_test(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    deal_id = graphene.Int()

class CustomerInput(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    deal_id = graphene.Int()


class DealSchema(graphene.ObjectType):
    name = graphene.String()
    start_date = graphene.Date()
    stage_name = graphene.String()
    net_per_month = graphene.Float()
    gross_per_month = graphene.Float()
    user_id = graphene.Int()



class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User_test)

    def mutate(root, info, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')

        with db_session_() as db_session:
            user = User(email=email, name=name)
            db_session.add(user)
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
        with db_session_() as db_session:
            user  = db_session.query(User).filter(User.id == id).first()
            user.name = name
            user.email = email
        ok = True
        return UpdateUser(user=user, ok=ok)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.String()

    def mutate(self, info, id):
        with db_session_() as db_session:
            user = db_session.query(User).filter(User.id == id).first()
            if user:
                    db_session.delete(user)
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
    deal = graphene.Field(DealSchema)

    def mutate(self, info, **kwargs):
        deal = Deal(**kwargs)
        try:
            db.add(deal)
            db.commit()
            ok = 'done'
        except IntegrityError:
            db.rollback()
            ok = 'UPS'
        return CreateDeal(ok=ok, deal=deal)


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

UPLOAD_FOLDER = 'files'

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()


    file = Upload
    nameFile = graphene.String()

    @staticmethod
    def mutate(self, info, file,  **kwargs):
        files = request.files


        # do something with your file


        for key in request.files:
            file = request.files[key]
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))



        return UploadMutation(success=True)

class myMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_deal = CreateDeal.Field()
    update_deal = UpdateDeal.Field()
    delete_deal = DeleteDeal.Field()

    customer_create = CustomerCreate.Field()
    upload_file = UploadMutation.Field()


