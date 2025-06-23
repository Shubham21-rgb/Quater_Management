from flask import Flask  
from application.database import db
from application.models import *
from application.config import LocalDevelopmentConfig
from flask_security import Security,SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from application.resources import api

#here we will use the hash password for encrypting the password
from flask_security import hash_password
def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    datastore=SQLAlchemyUserDatastore(db,User,Role)  
    app.security=Security(app,datastore)
    app.app_context().push()
    return app
app=create_app()
with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name="admin",description="super user of app ")
    app.security.datastore.find_or_create_role(name="user",description="Customer user of app ")
    db.session.commit()
    if not app.security.datastore.find_user(email="admin1@admin.com"):
        app.security.datastore.create_user(username="Subrata Chakraborty",
                                           email="admin1@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    if not app.security.datastore.find_user(email="admin2@admin.com"):
        app.security.datastore.create_user(username="Ritwick Ghosh",
                                           email="admin2@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    if not app.security.datastore.find_user(email="admin3@admin.com"):
        app.security.datastore.create_user(username="A.K.Bhagat",
                                           email="admin3@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    if not app.security.datastore.find_user(email="admin4@admin.com"):
        app.security.datastore.create_user(username="User4",
                                           email="admin4@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    if not app.security.datastore.find_user(email="admin5@admin.com"):
        app.security.datastore.create_user(username="User5",
                                           email="admin5@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    if not app.security.datastore.find_user(email="admin6@admin.com"):
        app.security.datastore.create_user(username="User6",
                                           email="admin6@admin.com",
                                           password=generate_password_hash("Nit@1234"),
                                           roles=['admin'])
    db.session.commit()
from application.routes import *


'''
df = pd.read_csv("InsBill.csv")
df = df[df['Staff Code'].notna()]


for _, row in df.iterrows():
    
    record = QuartersBilling(
        Sl_no=row['Sl. No.'],
        staff_code = row['Staff Code'],
        staff_name = row['Staff Name'],
        quarters_number = row['Quarters Number '],
        licence_fee = row['Licence fee'],
        Month=row['Month'],
        meter_status = row['Meter Status'],

        # First meter
        initial_reading_1 = row['Initial Reading'],
        final_reading_1 = row['Final Reading'],
        meter_rent_1 = row['Meter Rent'],

        # Second meter
        common_initial_reading_2  = row['Common Initial Reading'],
        common_final_reading_2  = row['Common Final Reading'],
        common_meter_rent_2  = row['Common Meter Rent'],
        difference_reading_1=row['Difference of Reading'],
        electric_charge=row['Electric Charge'],
        difference_reading_2=row['Common meter Difference of Reading'],
        common_electric_charge=row['Common Electric Charge'],
        total_electricity_charges=row['TOTAL ELECTRICITY CHARGES '],
        net_amount=row['Net Amount (2+14+15+16+17+18)'],
        water_charge = row['WATER CHARGE'],
        coopt_electric_charge = row['CO-OPT. ELECT. CHARGE'],
        grg_charge = row['GRG. CHRG. '],
        other_charges = row['Others/ charges'],
        remarks=row['Remarks']
    )

    db.session.add(record)

db.session.commit()

df2= pd.read_csv("NITquater12.csv")
for _, row in df2.iterrows():
    r=Quater_List(
        id=row['Sl.No'],
        name=row['Name'],
        Designation=row['Designation'],
        Type_of_Quater=row['Type of quarter'],
        Area=row['Area'],
        Date_of_allotment=row['Date of allotment'],
        Year_of_construction=row['Year of const'],
        Status=row['Status']
    )
    db.session.add(r)
db.session.commit()'''
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)