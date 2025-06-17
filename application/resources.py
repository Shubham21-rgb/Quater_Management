from flask_restful import Api, Resource, reqparse
from .models import *
from flask import jsonify
from flask_security import auth_required,roles_required,roles_accepted,current_user
import datetime
api=Api()

def roles_list(roles):
    role_list=[]
    for role in roles:
        role_list.append(role.name)
    return role_list



parser=reqparse.RequestParser()
class TransApi(Resource):
    @auth_required('token')  
    @roles_accepted('admin')
    def get(self):
        transactions=[]
        trans_json=[]

        transactions=Quater_List.query.all()
        for transaction in transactions:
            this_trans={}
            this_trans["id"]=transaction.id
            this_trans["name"]=transaction.name
            this_trans["Designation"]=transaction.Designation
            this_trans["Type_of_Quater"]=transaction.Type_of_Quater  
            this_trans["Area"]=transaction.Area
            this_trans["Date_of_allotment"]=transaction.Date_of_allotment
            this_trans["Date_Of_Vacation"]=transaction.Date_Of_Vacation
            this_trans["Year_of_construction"]=transaction.Year_of_construction
            this_trans["Remarks"]=transaction.Remarks
            trans_json.append(this_trans)
        if trans_json:
            return jsonify(trans_json)
        return{
            "message":"Database is empty"
        },400
    @auth_required('token')
    @roles_accepted('user')
    def post(self,trans_id):
        if 'user' in roles_list(current_user.roles):
            parser.add_argument('amount', type=str, required=True)
            args= parser.parse_args()
            try:
                servreq=Quater_List(customer_id=current_user.id,
                                        Date_of_Request=datetime.datetime.now(),
                                        Date_of_completion="to_be_updated",
                                        amount=args['amount'],
                                        status="Pending",
                                        service_id=trans_id)
                db.session.add(servreq)
                db.session.commit()
                return{   
                "message":"Request Created Succesfully Generated"
                } 
                
            except:
                return{
                    "message":"Cannot add Service Already exists"
                }
    @auth_required('token')
    @roles_accepted('admin')
    def put(self,trans_id):
            
        parser.add_argument('name', type=str)
        parser.add_argument('Date_of_allotment', type=str)
        parser.add_argument('Type_of_Quater', type=str)
        parser.add_argument('Designation',type=str)
        parser.add_argument('Area', type=str)
        parser.add_argument('Year_of_construction', type=str)
        parser.add_argument('Date_Of_Vacation', type=str)
        parser.add_argument('Remarks', type=str)
        service_request = Quater_List.query.filter_by(id=trans_id).first()
        args= parser.parse_args()
        for key, value in args.items():
            if value and value.strip() != "":
                setattr(service_request, key, value)
            else:
                print(f"{key} is empty, skipping update")
        db.session.commit()
        return{
                    "message":"Updated Sucessfully"
        }

    @auth_required('token')
    @roles_accepted('user','prof','admin')
    def delete(self,trans_id):

        t=Quater_List.query.get(trans_id)
        if t:
            db.session.delete(t)
            print('Success')
            db.session.commit()
            return{
                    "message":"Transaction deleted Succesfully"
            }
        else:
            return{
                    "message":"Deletion Failed"
            },400
        


api.add_resource(TransApi,'/api/get','/api/create/<int:trans_id>','/api/update/<int:trans_id>','/api/delete/<int:trans_id>')

class RemarksUpdateApi(Resource):
    @auth_required('token')
    @roles_accepted('admin')
    def put(self, trans_id):
        parser.add_argument('staff_name', type=str)
        parser.add_argument('staff_code', type=str)
        parser.add_argument('Month', type=str)
        parser.add_argument('quarters_number',type=str)
        parser.add_argument('meter_status', type=str)
        parser.add_argument('remarks', type=str)
        service_request = QuartersBilling.query.filter_by(Sl_no=trans_id).first()
        args= parser.parse_args()
        for key, value in args.items():
            if value and value.strip() != "":
                setattr(service_request, key, value)
            else:
                print(f"{key} is empty, skipping update")
        db.session.commit()
        return{
                    "message":"Updated Sucessfully"
        }
    @auth_required('token')
    @roles_accepted('admin')
    def delete(self, trans_id):
        ne=QuartersBilling.query.get(trans_id)
        if ne:
            db.session.delete(ne)
            db.session.commit()
            return{
                    "message":"Transaction deleted Succesfully"
                }
        else:
            return{
                 "message":"Deletion Failed"
            },400


api.add_resource(RemarksUpdateApi, '/api/update_bill/<int:trans_id>','/api/delete_bill/<int:trans_id>')
