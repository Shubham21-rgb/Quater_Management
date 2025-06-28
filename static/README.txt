Set Up Virtual Environment (if not copied)
Open Command Prompt or PowerShell inside the project directory:
cd D:\FlaskProjects\myapp
python -m venv .venv
Then activate it:
.venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
python app.py
IDS CREATED:admin1@admin.com
admin2@admin.com
admin3@admin.com
admin4@admin.com
admin5@admin.com
admin6@admin.com
Password:Nit@1234
install wkhtmltox-0.12.6-1.msvc2015-win64 this for pdf
Check for the advance firewall--->Inbound Rules Flask port 5000 entry 
Open:
1.Control Pannel--->System and Security---->windows defender firewall----->On the left sidebar, click "Advanced settings"--->inbound rules-->continue from 2
2.In the right pane, click "New Rule..."---->Choose "Port" and click Next---->Choose "TCP" Select "Specific local ports" and enter:5000--->Select "Allow the connection"
Click Next---->Leave all options (Domain, Private, Public) checked (or customize as needed).

Click Next

Name the Rule

Give it a name like: Flask Port 5000

Optionally, add a description.

Click Finish
#########################################################
##### Changing the Drive from C to D in CMD
D:
D:\>cd Quater_Management
D:\Quater_Management>python --version
D:\Quater_Management>.venv\Scripts\activate
(.venv) D:\Quater_Management>python app.py