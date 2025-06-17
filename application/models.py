from .database import db
from flask_security import UserMixin,RoleMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    fs_uniquifier=db.Column(db.String,unique=True,nullable=False)
    roles=db.relationship('Role',secondary='roles_users',backref="bearer")
    active=db.Column(db.Boolean,nullable=False)
class Role(db.Model,RoleMixin):
     id=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.String,nullable=False,unique=True)
     description=db.Column(db.String,nullable=False)
class RolesUsers(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     user_id=db.Column(db.Integer,db.ForeignKey('user.username'))
     role_id=db.Column(db.Integer,db.ForeignKey('role.name'))
class Quater_List(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False,unique=False)
    Designation=db.Column(db.String,nullable=False,unique=False)
    Type_of_Quater=db.Column(db.String,nullable=False,unique=False)
    Area=db.Column(db.String,nullable=False,unique=False)
    Date_of_allotment=db.Column(db.String,nullable=False,unique=False)
    Year_of_construction=db.Column(db.String,nullable=False,unique=False)
    Date_Of_Vacation=db.Column(db.String,nullable=True,unique=False,default='Yet_to_be_updated')
    Remarks=db.Column(db.String,nullable=False,unique=False,default='Yet_to_be_updated')

class QuartersBilling(db.Model):
    __tablename__ = 'quarters_billing'
    Sl_no=db.Column(db.Integer,autoincrement=True,primary_key=True)
    staff_code = db.Column(db.String(50))
    staff_name = db.Column(db.String(100))
    quarters_number = db.Column(db.String(50))
    licence_fee = db.Column(db.Float)
    Month=db.Column(db.String(30))
    meter_status = db.Column(db.String(20),default='Working')

    # First meter
    initial_reading_1 = db.Column(db.Float)
    final_reading_1 = db.Column(db.Float)
    difference_reading_1=db.Column(db.Float,nullable=True)
    meter_rent_1 = db.Column(db.Float,default=0.25)


    
    electric_charge=db.Column(db.Float)

    # Second meter
    common_initial_reading_2 = db.Column(db.Float,default=0.0)
    common_final_reading_2 = db.Column(db.Float,default=0.0)

    difference_reading_2=db.Column(db.Float,nullable=True)
    common_meter_rent_2 = db.Column(db.Float,default=0.0)
    common_electric_charge=db.Column(db.Float,nullable=True)
    total_electricity_charges=db.Column(db.Float,nullable=True)
    
    water_charge = db.Column(db.Float)
    coopt_electric_charge = db.Column(db.Float)
    grg_charge = db.Column(db.Float)
    other_charges = db.Column(db.Float)
    net_amount = db.Column(db.Float,nullable=True)
    remarks=db.Column(db.String(30))