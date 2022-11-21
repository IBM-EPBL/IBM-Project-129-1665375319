
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import json
import requests
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vlv61401;PWD=mo0lXoXdJD4sG9jL",'','')
print("Connected Successfully !")


app = Flask(__name__)

app.secret_key = 'Done ehhh'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/registerrec",methods = ['POST', 'GET'])
def registerrec():
    msg=''
    if request.method == 'POST':
        
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']

        sql = "SELECT * FROM register WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            return render_template('login.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO register VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, number)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, cpassword)
            ibm_db.execute(prep_stmt)
    
        return render_template('login.html', msg="Registered successfuly..login to continue")
#Login

@app.route("/loginrec", methods =['POST','GET'])
def loginrec():
    smsg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if((email and password) is not None ):
            sql = "SELECT * FROM register WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            prep_stmt = ibm_db.execute(stmt)
            dicto = ibm_db.fetch_assoc(stmt)
            while(dicto != False):
                res1 = dicto["EMAIL"]
                res2 = dicto['PASSWORD']
                res3 = dicto['NAME']
                res4 = dicto['NUMBER']

                if(res1 == email and res2 == password):
                    session['email'] = res1
                    session['pass'] = res2
                    session['name'] = res3
                    session['number'] = res4
                    return render_template('profile.html')
                else:
                    return render_template('login.html', smsg = 'Incorrect username / password !')
            else:
                return render_template('register.html', smsg = 'Not yet registered')
        else:   
            return render_template('login.html', smsg = 'Fill all the details')
    else:
        return render_template('login.html')
            

#contact

@app.route("/contactrec",methods = ['POST', 'GET'])
def contactrec():
    cmsg=''
    if request.method == 'POST':
        
        Name = request.form['name']
        MobileNumber = request.form['number']

        insert_sql = "INSERT INTO contact VALUES (?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, Name)
        ibm_db.bind_param(prep_stmt, 2, MobileNumber)
        ibm_db.execute(prep_stmt)
    
        return render_template('index.html', cmsg="We will contact you soon")

@app.route("/connectrec",methods = ['POST', 'GET'])
def connectrec():
    cnmsg=''
    if request.method == 'POST':
        
        CustomerName = request.form['CustomerName']
        MailID = request.form['MailID']
        ContactNumber = request.form['ContactNumber']
        ConvenientTime = request.form['ConvenientTime']
        CustomerMessage = request.form['CustomerMessage']
        insert_sql = "INSERT INTO connectwithus VALUES (?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, CustomerName)
        ibm_db.bind_param(prep_stmt, 2, MailID)
        ibm_db.bind_param(prep_stmt, 3, ContactNumber)
        ibm_db.bind_param(prep_stmt, 4, ConvenientTime)
        ibm_db.bind_param(prep_stmt, 5, CustomerMessage)
        ibm_db.execute(prep_stmt)
    
        return render_template('index.html', cnmsg="Lets Travel Together")


@app.route("/jobsrec",methods = ['POST', 'GET'])
def jobsrec():
    jmsg=''
    if request.method == 'POST':
        
        CandidateName = request.form['CandidateName']
        CompanyName = request.form['CompanyName']
        EmployeeRole = request.form['EmployeeRole']
        CandidateMail = request.form['CandidateMail']
        CandidateNumber = request.form['CandidateNumber']
        insert_sql = "INSERT INTO hirerform VALUES (?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, CandidateName)
        ibm_db.bind_param(prep_stmt, 2, CompanyName)
        ibm_db.bind_param(prep_stmt, 3, CandidateMail)
        ibm_db.bind_param(prep_stmt, 4, CandidateNumber)
        ibm_db.bind_param(prep_stmt, 5, EmployeeRole)
        ibm_db.execute(prep_stmt)
    
        return render_template('jobs.html', jmsg="We will contact you soon")



@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/exploreJobs', methods = ['GET', 'POST'])
def exploreJobs():
	url = "https://linkedin-jobs-search.p.rapidapi.com/"

	payload = {
		"search_terms": "python programmer",
		"location": "30301",
		"page": "1"
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "6ac028283fmshc8ee5a710f1e3c4p196a21jsnb05b95329620",
		"X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
	}

	response = requests.request("POST", url, json=payload, headers=headers)
	#print(response.text)
	job = json.loads(response.content)
	#print(job)
	#json_data = json.loads(job)
	return render_template('exploreJobs.html', jobs =job)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('email', None)
   session.pop('password', None)
   session.pop('name', None)
   session.pop('number', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)