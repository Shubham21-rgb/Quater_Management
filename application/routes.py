from flask import current_app as app,jsonify,request,render_template,Response
from flask_security import auth_required, roles_required,current_user,login_user,roles_accepted
from application.database import db
from werkzeug.security import check_password_hash,generate_password_hash
import pandas as pd 
import io
import datetime
import uuid
#from .resources import roles_list
from .models import *
from sqlalchemy import cast,Float
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')
def roles_list(roles):
    role_list=[]
    for role in roles:
        role_list.append(role.name)
    return role_list

@app.route('/api/admin')
@auth_required('token')
@roles_required('admin')
def admin_home():
    return {
        "message":"admin logged in success"
    }
@app.route('/api/home')   
@auth_required('token')
@roles_accepted('admin')
def userhome():
    user=current_user
    if "admin" in  roles_list(user.roles):
        return jsonify({
        "id":user.id,
        "email":user.email,
        "password":user.password,
        "username":user.username,
        "roles":roles_list(user.roles) 
    })
###################################################
@app.route('/api/getvalofbill')   
@auth_required('token')
@roles_accepted('admin')
def adminqbill():
    transactions=[]
    trans_json=[]
    transactions=QuartersBilling.query.all()
    for transaction in transactions:
        this_trans={}
        this_trans["Sl_no"]=transaction.Sl_no
        this_trans["staff_code"]=transaction.staff_code
        this_trans["staff_name"]=transaction.staff_name
        this_trans["quarters_number"]=transaction.quarters_number  
        this_trans["licence_fee"]=transaction.licence_fee
        this_trans["Month"]=transaction.Month
        this_trans["meter_status"]=transaction.meter_status
        this_trans["initial_reading_1"]=transaction.initial_reading_1
        this_trans["final_reading_1"]=transaction.final_reading_1
        this_trans["difference_reading_1"]=transaction.difference_reading_1
        this_trans["meter_rent_1"]=transaction.meter_rent_1
        this_trans["electric_charge"]=transaction.electric_charge
        this_trans["common_initial_reading_2"]=transaction.common_initial_reading_2
        this_trans["common_final_reading_2"]=transaction.common_final_reading_2
        this_trans["difference_reading_2"]=transaction.difference_reading_2
        this_trans["common_meter_rent_2"]=transaction.common_meter_rent_2
        this_trans["common_electric_charge"]=transaction.common_electric_charge
        this_trans["total_electricity_charges"]=transaction.total_electricity_charges
        this_trans["water_charge"]=transaction.water_charge
        this_trans["coopt_electric_charge"]=transaction.coopt_electric_charge
        this_trans["grg_charge"]=transaction.grg_charge
        this_trans["other_charges"]=transaction.other_charges
        this_trans["net_amount"]=transaction.net_amount
        this_trans["remarks"]=transaction.remarks
        trans_json.append(this_trans)
    if trans_json:
        return jsonify(trans_json)
    return{
        "message":"Database is empty"
    },400



####################################
@app.route('/api/cregister',methods=['POST'])
def cregister():
    cred=request.get_json()
    if not cred["username"]:
        return{
            "message":"username is required please register again"
        }
    if not cred["email"]:
        return{
            "message":"email is required please register again"
        }
    if not cred["password"]:
        return{
            "message":"password is required please register again"
        } 
    
    if not app.security.datastore.find_user(username=cred["username"]):
        app.security.datastore.create_user(username=cred["username"],
                                                email=cred["email"],
                                                password=generate_password_hash(cred["password"]),
                                                roles=['user'])
        db.session.commit()
        return jsonify({
            "message":"User created succesfully"
        }),201
    return jsonify({   
        "message": "User already exsists"
    }),400


@app.route('/api/login',methods=['POST'])
def log34():
    body=request.get_json()
    email=body['email']
    password=body['password']
    if not email:
        return jsonify({
            "message":"Email is required"
        })
    if not password:
        return jsonify({
            "message":"password is required"
        })
    user=app.security.datastore.find_user(email=email)
    if user:
        if check_password_hash(user.password,password):
            login_user(user)
            return jsonify({
                "id":user.id,
                "email":user.email,
                "username":user.username,
                "auth-token":user.get_auth_token(),
                "roles":roles_list(user.roles)
            })
        else:
            return jsonify({
                "message":"Wrong credentials"
            })
    else:
        return jsonify({
            "message":"User does not exsist "
        })
    
'''

#to update status to Accepted
@app.route('/api/accept/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof','admin')
def log27(id):
    servicerequest=Quater_List.query.get(id)
    servicerequest.status="Accepted"
    db.session.commit()
    return{
        "message":"Updated Succesfully"
    }

#to update status to Rejected
@app.route('/api/reject/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof','admin')
def log26(id):
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.status="Rejected"
    db.session.commit()
    user=servicerequest.bearer.username
    return{
        "message":"Updated Succesfully"
    }
#to Delete close/rejected Service
@app.route('/api/deleted/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof')
def log25(id):
    servicerequest=ServiceRequest.query.get(id)
    db.session.delete(servicerequest)
    db.session.commit()
    user=servicerequest.bearer.username
    return{
        "message":"Deleted Succesfully"
    }

#Pay part wroks as Completed Services
@app.route('/api/pay/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('user')
def log24(id):
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.status="Completed"
    db.session.commit()
    return{
        "message":"Paid Succesfully"
    }
#professional user used to change status to Completed
@app.route('/api/complete/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof','admin')
def log23(id):
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.status="Completed"
    db.session.commit()
    user=servicerequest.bearer.username
    return{
        "message":"Changed Succesfully"
    }
#professional user used to change status to Closed
@app.route('/api/close/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof','admin')
def log22(id):
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.status="Closed"
    db.session.commit()
    user=servicerequest.bearer.username
    return{
        "message":"Changed Succesfully"
    }
# user used to change cancel-Pending requets means to delete
@app.route('/api/cancel/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('user')
def log21(id):
    servicerequest=ServiceRequest.query.get(id)
    db.session.delete(servicerequest)
    db.session.commit()
    return{
        "message":"Closed-Service Permanently"
    }

# To Update the date Of Completion
@app.route('/api/tupdate/<int:id>',methods=['POST'])
@auth_required('token')
@roles_accepted('prof')
def log20(id):
    body=request.get_json()
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.Date_of_completion=body["time"]
    db.session.commit()
    return{
        "message":"Updated Succesfully"
    }

#To get professional Service
@app.route('/api/entry',methods=['POST'])
def log19():
    user=current_user
    prof=Service.query.filter_by(prof_id=user.id)
    tran=[]
    for role in prof:
        profess={}
        profess["ids"]=role.id
        tran.append(profess)
    if tran:
        return tran
    return{
        "message":"Unable to get"
    }

@app.route('/api/export')
def export_csv():
    user=current_user
    return jsonify({
    })










@app.route('/api/adelete/<int:id>',methods=['POST']) 
@auth_required('token')
@roles_accepted('admin')
def adelete(id):
    cus=ServiceRequest.query.get(id)
    if cus:
        db.session.delete(cus)
        db.session.commit()
        user=cus.bearer.username
        return{
            "message":"succesfully Restored"
        }
    else:
        return{
            "message":"Cannot restore"
        }

@app.route('/api/acomplete/<int:id>',methods=['POST']) 
@auth_required('token')
@roles_accepted('admin')
def acomplete(id):
    cus=ServiceRequest.query.get(id)
    if cus:
        cus.status="Completed"
        db.session.commit()
        user=cus.bearer.username
        return{
            "message":"succesfully Restored"
        }
    else:
        return{
            "message":"Cannot restore"
        }

@app.route('/api/aupdate/<int:id>',methods=['POST']) 
@auth_required('token')
@roles_accepted('admin')
def aupdate(id):
    body=request.get_json()
    servicerequest=ServiceRequest.query.get(id)
    servicerequest.Date_of_completion=body["time"]
    db.session.commit()
    return{
        "message":"Updated Succesfully"
    }

################################################  professional and customer profile works ########################
@app.route('/api/updateprof/<int:id>',methods=['POST']) 
@auth_required('token')
@roles_accepted('prof','user')
def profete(id):
    if 'prof' in roles_list(current_user.roles):
        body=request.get_json()
        ser=Professional.query.filter_by(user_id=id).all()
        for t in ser:
            t.description=body["description"]
            t.Service_type=body["service_type"]
            t.Experience=body["Experience"]
            t.Founder=body["Founder"]
            db.session.commit()
            return {
            "message":"Succesfully Updated"
            }
        return{
            'message':'cannot update'
        }
    else:
        body=request.get_json()
        ser=Customer.query.filter_by(user_id=id).all()
        for t in ser:
            t.contact_no=body["contact_no"]
            t.address=body["address"]
            db.session.commit()
            return {
            "message":"Succesfully Updated"
            }
        return{
            'message':'cannot update'
        }

@app.route('/api/profentryies')
@auth_required('token')
@roles_accepted('prof','user')
def rot():
    user=current_user
    d=[{"id":user.id}]
    return d
'''
######################### UPDATE/DELETE OF Service By Admin #########################
@app.route('/api/adminser',methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def adminser():
    prof=Quater_List.query.all()
    tran=[]
    for role in prof:
        profess={}
        profess["id"]=role.id
        profess["name"]=role.name 
        profess["Designation"]=role.Designation
        profess["Type_of_Quater"]=role.Type_of_Quater
        profess["Area"]=role.Area
        profess["Date_of_allotment"]=role.Date_of_allotment
        profess["Year_of_construction"]=role.Year_of_construction
        profess["Status"]=role.Status
        tran.append(profess)
    if tran:
        return tran
    return{
        "message":"Unable to get"
    }
@app.route('/downloadcsv',methods=['POST'])
def download_csv():
    data = request.get_json()
    csv_file_name = f"Report_{datetime.datetime.now().strftime('%f')}.csv"
    if not data:
        return "No data provided", 400

    # Convert received list of dicts to DataFrame
    df = pd.DataFrame(data)
    desired_order = ['name', 'Designation', 'Type_of_Quater', 'Area', 'Date_of_allotment','Date_Of_Vacation', 'Year_of_construction', 'Status']
    df = df[[col for col in desired_order if col in df.columns]]
    # Write DataFrame to a CSV string
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_file_name}"}
    )




@app.route('/downloadbillcsv',methods=['POST'])
def download_csv1():
    data = request.get_json()
    csv_file_name = f"Quaterbill_{datetime.datetime.now().strftime('%f')}.csv"
    if not data:
        return "No data provided", 400

    # Convert received list of dicts to DataFrame
    df = pd.DataFrame(data)
    desired_order = ["Sl_no","staff_code","staff_name","quarters_number","licence_fee","Month","meter_status","initial_reading_1","final_reading_1","difference_reading_1","meter_rent_1","electric_charge","common_initial_reading_2","common_final_reading_2","difference_reading_2","common_meter_rent_2","common_electric_charge","total_electricity_charges","water_charge","coopt_electric_charge","grg_charge","other_charges","net_amount","remarks"]
    df = df[[col for col in desired_order if col in df.columns]]
    # Write DataFrame to a CSV string
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_file_name}"}
    )


####################################### Entery of New Billing Details #####################################

@app.route('/api/entrybillnew',methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def entrybill():
    body=request.get_json()
    if body:
        if body['meter_rent_1']==None:
            body['meter_rent_1']='0.25'
        if body['common_initial_reading_2']==None:
            body['common_initial_reading_2']='0'
        if body['common_final_reading_2']==None:
            body['common_final_reading_2']='0'
        if body['common_meter_rent_2']==None:
            body['common_meter_rent_2']='0'
        if body['unit2']==None:
            body['unit2']=0
        #if body['initial_reading_1'] and body['final_reading_1']:
        diff_read_1=float(body['final_reading_1'])-float(body['initial_reading_1'])
        #if body['initial_reading_1'] and body['final_reading_1'] and body['unit1']:
        elec_charge=round((float(body['unit1'])*diff_read_1)+float((body['meter_rent_1'])),2)
        #if body['common_initial_reading_2'] and body['common_final_reading_2']:
        diff_read_2=float(body['common_final_reading_2'])-float(body['common_initial_reading_2'])
        #if body['common_initial_reading_2'] and body['common_final_reading_2'] and body['unit2']:
        elec_charge_2 = round(float(body['unit2']) * diff_read_2 + float(body['common_meter_rent_2']),2)
        #if elec_charge and elec_charge_2:
        total_bill=elec_charge+elec_charge_2
        #if total_bill and body['licence_fee'] and body['water_charge'] and body['coopt_electric_charge'] and body['grg_charge'] and body['other_charges']:
        final_bill_amt=float(body['licence_fee'])+total_bill+float(body['water_charge'])+float(body['coopt_electric_charge'])+float(body['grg_charge'])+float(body['other_charges'])


        bill=QuartersBilling(staff_code=body['staff_code'],
                             staff_name=body['staff_name'],
                             quarters_number=body['quarters_number'],
                             licence_fee=body['licence_fee'],
                             Month=body['join_month_year'],
                             meter_status=body['meter_status'],
                             initial_reading_1=body['initial_reading_1'],
                             final_reading_1=body['final_reading_1'],
                             difference_reading_1=diff_read_1,
                             meter_rent_1=body['meter_rent_1'],
                             electric_charge=elec_charge,
                             common_initial_reading_2=body['common_initial_reading_2'],
                             common_final_reading_2=body['common_final_reading_2'],
                             difference_reading_2=diff_read_2,
                             common_meter_rent_2=body['common_meter_rent_2'],
                             common_electric_charge=elec_charge_2,
                             total_electricity_charges=total_bill,
                             water_charge=body['water_charge'],
                             coopt_electric_charge=body['coopt_electric_charge'],
                             grg_charge=body['grg_charge'],
                             other_charges=body['other_charges'],
                             net_amount=final_bill_amt,
                             remarks=body['remarks'])
        db.session.add(bill)
        db.session.commit()
        return{   
            "message":"Success"
        }
    else:
        return{
                "message":"error"
        }


@app.route('/api/genval',methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def genval():
    body=request.get_json()
    ser=QuartersBilling.query.filter_by(staff_code=body['staff_code']).all()
    tran=[]
    for r in ser:
        val={}
        val['staff_name']=r.staff_name 
        val['quarters_number']=r.quarters_number
        val['licence_fee']=r.licence_fee 
        val['initial_reading_1']=r.initial_reading_1 
        val['final_reading_1']=r.final_reading_1 
        val['meter_rent_1']=r.meter_rent_1 
        val['common_initial_reading_2']=r.common_initial_reading_2 
        val['common_final_reading_2']=r.common_final_reading_2
        val['water_charge']=r.water_charge 
        val['coopt_electric_charge']=r.coopt_electric_charge 
        val['grg_charge']=r.grg_charge 
        val['other_charges']=r.other_charges 
        val['remarks']=r.remarks 
        val['meter_status']=r.meter_status
        val['common_meter_rent_2']=r.common_meter_rent_2

        tran.append(val)
    if tran:
        return tran
    else:
        return{
            'message':"No Data"
        }








'''
############################## Admin/Professional to create Service ##########################
@app.route('/api/adcreate',methods=['POST'])
@auth_required('token')
@roles_accepted('admin','prof')
def createserwer():
    if 'prof' in roles_list(current_user.roles):
            body=request.get_json()
            try:
                Service_create=Service(id=body['id'],
                                    Service_name=body['service_name'],
                                    Time_required=body['Time_required'],
                                    Description=body['Description'],
                                    amount=body['amount'],
                                    prof_id=current_user.id
                                    )
                db.session.add(Service_create)
                db.session.commit()
                return{
                    "message":"Service Created Succesfully Generated"
                } 
            except:
                return{
                "message":"Service feilds are missiing"
                }
    elif 'admin' in roles_list(current_user.roles):
        body=request.get_json()
        try:
            Service_create=Service(id=body['id'],
                                    Service_name=body['service_name'],
                                    Time_required=body['Time_required'],
                                    Description=body['Description'],
                                    amount=body['amount'],
                                    prof_id=body['prof_id']
                                    )
            db.session.add(Service_create)
            db.session.commit()
            return{
                    "message":"Service Created Succesfully Generated"
                } 
        except:
            return{
                "message":"Service feilds are missiing or exsists"
                }

############################### Customer Ratings #################################
@app.route('/api/cusrate/<int:ids>',methods=['POST'])
@auth_required('token')
@roles_accepted('user')
def cusserrate(ids):
    body=request.get_json()
    ser = ServiceRequest.query.get(ids)
    try:
        d=ser.id
        s2=Ratings(id=d,
                    review=body['review'],
                    remarks='to_be_updated_by_the_company'

        )
        db.session.add(s2)
        db.session.commit()
        return{
                "message":"Rating Created Succesfully Generated"
            } 
    except:
        return{
            "message":"Rating feilds are missiing or exsists"
            }

#################################### Admin Ratings Management ###############
@app.route('/api/rateadmin/<int:ids>',methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def rateadmin123(ids):
    body=request.get_json()
    ser=Ratings.query.get(ids)
    ser.remarks=body['remark']
    db.session.commit()
    return{
        "message":"Succesfully responded"
    }

######################### 
@app.route('/api/mail')
def send_reports():
    return {
    }'''

############## Search FUnctionalities for Admin #############
@app.route('/api/adminsearchin',methods=['POST'])
def adminsearchin():
    body=request.get_json()   
    tran=[]
    if body['filter']=='name':
        ser = Quater_List.query.filter(Quater_List.name.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)

    elif body['filter']=='dg':
        ser = Quater_List.query.filter(Quater_List.Designation.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)
    elif body['filter']=='qt':
        ser = Quater_List.query.filter(Quater_List.Type_of_Quater.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)
    elif body['filter']=='area':
        ser = Quater_List.query.filter(Quater_List.Area.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)
    elif body['filter']=='doa':
        ser = Quater_List.query.filter(Quater_List.Date_of_allotment.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)
    elif body['filter']=='yoc':
        ser = Quater_List.query.filter(Quater_List.Year_of_construction.ilike(f"{body['search']}%")).all()
        for role in ser:
            profess={}
            profess["id"]=role.id
            profess["name"]=role.name 
            profess["Designation"]=role.Designation
            profess["Type_of_Quater"]=role.Type_of_Quater
            profess["Area"]=role.Area
            profess["Date_of_allotment"]=role.Date_of_allotment
            profess["Date_Of_Vacation"]=role.Date_Of_Vacation
            profess["Year_of_construction"]=role.Year_of_construction
            profess["Status"]=role.Status
            tran.append(profess)

    if tran:
        return tran
    else:
        return{
            "message":"No Data"
        }
from sqlalchemy import or_,and_
@app.route('/api/morefilt', methods=['POST'])
def fooil():
    body=request.get_json()   
    tran=[]
    f = 0
    for i in body:
        val = body.get(i)

    # Treat 'Open this select menu' as empty
        if val == 'Open this select menu':
            body[i] = ''  # Optional: reset it to empty string

    # Count if the field is not empty after that
        if body.get(i):
            f += 1

    if f==2:
        if body['filter1']:
            if body['filter1']=='name':
                ser = Quater_List.query.filter(Quater_List.name.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)

            elif body['filter1']=='Designation':
                ser = Quater_List.query.filter(Quater_List.Designation.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter1']=='Type_of_Quater':
                ser = Quater_List.query.filter(Quater_List.Type_of_Quater.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter1']=='Area':
                ser = Quater_List.query.filter(Quater_List.Area.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter1']=='Date_of_allotment':
                ser = Quater_List.query.filter(Quater_List.Date_of_allotment.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter1']=='Year_of_construction':
                ser = Quater_List.query.filter(Quater_List.Year_of_construction.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
        elif body['filter2']:
            if body['filter2']=='name':
                ser = Quater_List.query.filter(Quater_List.name.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)

            elif body['filter2']=='Designation':
                ser = Quater_List.query.filter(Quater_List.Designation.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter2']=='Type_of_Quater':
                ser = Quater_List.query.filter(Quater_List.Type_of_Quater.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter2']=='Area':
                ser = Quater_List.query.filter(Quater_List.Area.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter2']=='Date_of_allotment':
                ser = Quater_List.query.filter(Quater_List.Date_of_allotment.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            elif body['filter2']=='Year_of_construction':
                ser = Quater_List.query.filter(Quater_List.Year_of_construction.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)
            if tran:
                return tran
            else:
                return{
                "message":"No Data"
                }
    elif f==4:
        if body['filter1'] and body['filter2'] and body['search1'] and body['search2']:
            if body['filter1'] and body['filter2']:
                ser = Quater_List.query.filter(
                    and_(
            getattr(Quater_List, body['filter1']).ilike(f"{body['search1']}%"),
            getattr(Quater_List, body['filter2']).ilike(f"{body['search2']}%")
                    )
                ).all()
                for role in ser:
                    profess={}
                    profess["id"]=role.id
                    profess["name"]=role.name 
                    profess["Designation"]=role.Designation
                    profess["Type_of_Quater"]=role.Type_of_Quater
                    profess["Area"]=role.Area
                    profess["Date_of_allotment"]=role.Date_of_allotment
                    profess["Date_Of_Vacation"]=role.Date_Of_Vacation
                    profess["Year_of_construction"]=role.Year_of_construction
                    profess["Status"]=role.Status
                    tran.append(profess)

            if tran:
                return tran
            else:
                return{
                "message":"No Data"
                }
    if tran:
        return tran
    else:
        return{
            "message":"No Data"
            }

################################### New filters for billing search

@app.route('/api/billsearchfil', methods=['POST'])
def fooillll2():
    body=request.get_json()   
    tran=[]
    f = 0
    for i in body:
        val = body.get(i)

    # Treat 'Open this select menu' as empty
        if val == 'Open this select menu':
            body[i] = ''  # Optional: reset it to empty string

    # Count if the field is not empty after that
        if body.get(i):
            f += 1

    if f==2:
        if body['filter1']:
            if body['filter1']=='staff_code':
                ser = QuartersBilling.query.filter(QuartersBilling.staff_code.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)

            elif body['filter1']=='staff_name':
                ser = QuartersBilling.query.filter(QuartersBilling.staff_name.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
            elif body['filter1']=='quarters_number':
                ser = QuartersBilling.query.filter(QuartersBilling.quarters_number.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
            elif body['filter1']=='Month':
                ser = QuartersBilling.query.filter(QuartersBilling.Month.ilike(f"{body['search1']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
        elif body['filter2']:
            if body['filter2']=='staff_code':
                ser = QuartersBilling.query.filter(QuartersBilling.staff_code.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)

            elif body['filter2']=='staff_name':
                ser = QuartersBilling.query.filter(QuartersBilling.staff_name.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
            elif body['filter2']=='quarters_number':
                ser = QuartersBilling.query.filter(QuartersBilling.quarters_number.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
            elif body['filter2']=='Month':
                ser = QuartersBilling.query.filter(QuartersBilling.Month.ilike(f"{body['search2']}%")).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)
            if tran:
                return tran
            else:
                return{
                "message":"No Data"
                }
    elif f==4:
        if body['filter1'] and body['filter2'] and body['search1'] and body['search2']:
            if body['filter1'] and body['filter2']:
                ser = QuartersBilling.query.filter(
                    and_(
            getattr(QuartersBilling, body['filter1']).ilike(f"{body['search1']}%"),
            getattr(QuartersBilling, body['filter2']).ilike(f"{body['search2']}%")
                    )
                ).all()
                for role in ser:
                    profess={}
                    profess["Sl_no"]=role.Sl_no
                    profess["staff_code"]=role.staff_code 
                    profess["staff_name"]=role.staff_name
                    profess["quarters_number"]=role.quarters_number
                    profess["licence_fee"]=role.licence_fee
                    profess["Month"]=role.Month
                    profess["meter_status"]=role.meter_status
                    profess["initial_reading_1"]=role.initial_reading_1
                    profess["final_reading_1"]=role.final_reading_1
                    profess["difference_reading_1"]=role.difference_reading_1
                    profess["meter_rent_1"]=role.meter_rent_1
                    profess["electric_charge"]=role.electric_charge
                    profess["common_initial_reading_2"]=role.common_initial_reading_2
                    profess["common_final_reading_2"]=role.common_final_reading_2
                    profess["difference_reading_2"]=role.difference_reading_2
                    profess["common_meter_rent_2"]=role.common_meter_rent_2
                    profess["common_electric_charge"]=role.common_electric_charge
                    profess["total_electricity_charges"]=role.total_electricity_charges
                    profess["water_charge"]=role.water_charge
                    profess["coopt_electric_charge"]=role.coopt_electric_charge
                    profess["grg_charge"]=role.grg_charge
                    profess["other_charges"]=role.other_charges
                    profess["net_amount"]=role.net_amount
                    profess["remarks"]=role.remarks

                    tran.append(profess)

            if tran:
                return tran
            else:
                return{
                "message":"No Data"
                }
    if tran:
        return tran
    else:
        return{
            "message":"No Data"
            }
    

@app.route('/api/newallotment',methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def entrybillse():
    body=request.get_json()
    if body:
        t=Quater_List(name=body['name'],
                  Designation=body['Designation'],
                  Type_of_Quater=body['Type_of_Quater'],
                  Area=body['Area'],
                  Date_of_allotment=body['Date_of_allotment'],
                  Year_of_construction=body['Year_of_construction'])
        db.session.add(t)
        db.session.commit()
        return{   
                "message":"Request Created Succesfully Generated"
            } 
    else:
        return{
                "message":"Cannot add Service Already exists"
            }

'''
######################### Admin And User Summary ##################
@app.route('/api/persummary')
@auth_required('token')
@roles_accepted('admin','user')
def adminsummary():
    if 'admin' in roles_list(current_user.roles):
        sql1=ServiceRequest.query.all()
        c=0
        for j in sql1:
            if 'Closed' in j.status:
                c=c+1
        d=0
        for j in sql1:
            if 'Rejected' in j.status:
                d=d+1
        e=0
        for j in sql1:
            if 'Accepted' in j.status:
                e=e+1
        f=0
        for j in sql1:
            if 'Pending' in j.status:
                f=f+1
        g=0
        for j in sql1:
            if 'Completed' in j.status:
                g=g+1
        mv=c+d+e+f+g
        ac=(c/mv)*100    
        ad=(d/mv)*100
        ae=(e/mv)*100    
        af=(f/mv)*100    
        ag=(g/mv)*100
        labels = ['Closed Services', 'Pending Services', 'Accepted Services', 'Completed Services','Rejected Services']
        sizes = [ac,af,ae,ag,ad]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','red']
        explode = (0, 0.1, 0, 0,0)  
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.title('Summary')
        image_path = 'static/pie_chart1.png'
        plt.savefig(image_path)
        plt.close()
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.bar(labels,sizes, color='skyblue')
        ax.set_xlabel('labels',fontsize=14)
        ax.set_ylabel('size',fontsize=14)
        ax.set_title('Services_Records',fontsize=18)
        image_path1 = 'static/bar_chart1.png'
        plt.savefig(image_path1)
        plt.close()
        return {"image_path":image_path,"image_path1":image_path1}
    elif 'user' in roles_list(current_user.roles):
        id=current_user.id
        sql1=ServiceRequest.query.filter_by(customer_id=id).all()
        c=0
        for j in sql1:
            if 'Closed' in j.status:
                c=c+1
        d=0
        for j in sql1:
            if 'Rejected' in j.status:
                d=d+1
        e=0
        for j in sql1:
            if 'Accepted' in j.status:
                e=e+1
        f=0
        for j in sql1:
            if 'Pending' in j.status:
                f=f+1
        g=0
        for j in sql1:
            if 'Completed' in j.status:
                g=g+1
        mv=c+d+e+f+g
        ac=(c/mv)*100    
        ad=(d/mv)*100
        ae=(e/mv)*100    
        af=(f/mv)*100    
        ag=(g/mv)*100
        labels = ['Closed Services', 'Pending Services', 'Accepted Services', 'Completed Services','Rejected Services']
        sizes = [ac,af,ae,ag,ad]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','red']
        explode = (0, 0.1, 0, 0,0)  
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.title('Summary')
        image_path = 'static/pie_chart1.png'
        plt.savefig(image_path)
        plt.close()
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.bar(labels,sizes, color='skyblue')
        ax.set_xlabel('labels',fontsize=14)
        ax.set_ylabel('size',fontsize=14)
        ax.set_title('Services_Records',fontsize=18)
        image_path1 = 'static/bar_chart1.png'
        plt.savefig(image_path1)
        plt.close()
        return {"image_path":image_path,"image_path1":image_path1}'''     