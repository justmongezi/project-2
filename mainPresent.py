# BACKEND CODE FOR E-Z CAR WASH SYSTEM (written by Mongezi Masango, Andre Potgieter and Thembisile Mdhluli)

# This is the backend code for the web system E-Z Car Wash. It is written in Python and one of its microframeworks,
# Flask, to use additional functionalities for the web and databases. This is the documentation. All parts
# of the code have comments detailing the function and current problems. Additional problems or code can be resolved
# in the HTML and CSS (good luck trying to resolve the CSS though LOL.) The comments were added on the 8th of June to
# help readers and other programmers with debugging and legibilitiy efforts.

# 3 July update:
# - Converted number in booking function that takes tuple to integer
# - Need to add a module for the Appointment booking function that attaches the PDF invoice to the email
# - Change the services pages to include R rand signs


import mysql.connector as mariadb
from flask import Flask, render_template, request, redirect, url_for, session 
import math
import re
import smtplib
from datetime import datetime

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
#import matplotlib.pyplot as plt

mariadb_connection = mariadb.connect(host="localhost", user="root", passwd="system", database="car_wash_db", buffered = True)

app = Flask(__name__)


# My secret key
app.secret_key = 'Mongezi123+'

# ____________________________________________________________________________
# CODE FOR SYSTEM FORM DOWNLOAD CONFIGURATION

# This FUNCTION will use the Python reportlab library to generate a downloadable PDF file with the relevant
# information for the caller.

# Current issues:
# 1. 
# 2. 

def generatePDF(full_name, message, docname):
    doc = SimpleDocTemplate(docname ,pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    logo = "logo.png"
    formatted_time = time.ctime()
    im = Image(logo, 2*inch, 2*inch)
    Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="12">%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = '<font size="12">%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))         
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = message
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size="12">Mongezi Masango</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
    #doc.save()


def generateAnalyticsPDF(full_name, message, docname):
    doc = SimpleDocTemplate(MEDIA_ROOT + "/Downloads/" + docname ,pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    logo = "logo.png"
    formatted_time = time.ctime()
    im = Image(logo, 2*inch, 2*inch)
    Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="12">%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = '<font size="12">%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))         
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = message
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size="12">Mongezi Masango</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)

# ____________________________________________________________________________
# CODE FOR SYSTEM SMTP CONFIGURATION

# This FUNCTION will use the SMTP Python library to send emails to users based on the 
# changes made to their information.

# Current issues:
# 1. 
# 2. 

def send_email(emailto, email_text):


    gmail_user = 'masangomsm'
    gmail_password = 'U2h^3D6q57Z'

    sent_from = gmail_user

    #Send request
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, emailto, email_text)
        server.close()

        return 'Email sent!'
    except Exception as e:
        return e

gmail_user = 'masangomsm'
gmail_password = 'U2h^3D6q57Z'


# ____________________________________________________________________________
# CODE FOR LOGGING INTO SYSTEM http://localhost:5000/systemDSO34BT/

# This part of the code OUGHT to take inputs from the login page, check them against existing database entries
# and take appropriate action. It will use the GET and POST requests of the Flask framework.
# UPDATE: The code will now also include lines to manipulate the SMTP Python library so that we can send emails to
# customers once they register or make a change to their profile. See the end of the function.

# Current issues:
# 1. Missing home page LOL
# 2. 


app.config["DEBUG"] = True
@app.route('/systemDSO34BT/', methods=['GET', 'POST'])
def login():
    #Output error message
    msg = ''
# Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mariadb_connection.cursor()#Dictionary = true
        if 'checkbox' in request.form:
            cursor.execute('SELECT * FROM administrator WHERE adNo = %s or adEmail = %s AND adPassword = %s', (username, username, password))
            administrator = cursor.fetchone()

            if administrator:
                session['loggedin'] = True
                session['id'] = administrator[0]
                session['name'] = administrator[1]
                session['email'] = administrator[3]
                # return the admin Home page here
                return redirect(url_for('adminDashboard'))
            else:
                msg = "Incorrect administrator details. Try again." 
        else:        
            cursor.execute('SELECT * FROM customer WHERE cUsername = %s AND cPassword = %s', (username, password,))
            #Fetch one record and return result
            customer = cursor.fetchone()

            # If customer exists in customer table in out database
            if customer:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = customer[0]
                session['username'] = customer[2]
                session['email'] = customer[4]
                session['name'] = customer[1]
                # Redirect to home page
                return redirect(url_for('home'))

            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
    return render_template('index.html', msg =msg)


# ____________________________________________________________________________
# CODE FOR LOGGING OUT OF SYSTEM http://localhost:5000/systemDSO34BT/logout

# This part of the code will log a user out of the system.

# Current issues:
# 1. N/A, just connect to all pages under log out link.
# 2. 

@app.route('/systemDSO34BT/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# ____________________________________________________________________________
# CODE FOR REGISTERING INTO SYSTEM http://localhost:5000/systemDSO34BT/register

# This part of the code OUGHT to take inputs from the registration page, check them against existing database entries
# and take appropriate action. It will use the GET and POST requests of the Flask framework.

# Current issues:
# 1. None
# 2. 

@app.route('/systemDSO34BT/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "name, "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'name' in request.form and 'password' in request.form and 'password2' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
                # Check if account exists using MySQL        
        cursor = mariadb_connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE cUsername = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not name:
            msg = 'Please fill out the form!'
        elif password != password2:
            msg = "Oops, the passwords don't match. Try again."
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, %s, %s)', (name, username, password, email,))
            mariadb_connection.commit()
            msg = "You have successfully registered! Check your inbox, we've just sent you an email luv x."
            registerGood = """
                Hey there %s! We've received your registration. Your information is safely cocooned in our
                databases. Don't worry, we don't do anything malicious with your stuff. It just makes it easier
                to send you future promotions and fun stuff. And also to recover your account, since you'll forget
                your details sometime soon.

                We can't wait to send you promotions and fun things to look out for on our site, stay tuned.

                Best regards,

                Andre Potgieter
                Senior Executive, E-Z Car Wash Systems
            """
            send_email(email, registerGood)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    

# ____________________________________________________________________________
# CODE FOR ADMINISTRATORS REGISTERING INTO SYSTEM http://localhost:5000/systemDSO34BT/adminRegister

# This part of the code OUGHT to take inputs from the registration page, check them against existing database entries
# and take appropriate action. It will use the GET and POST requests of the Flask framework.

# Current issues:
# 1. None
# 2. 

@app.route('/systemDSO34BT/adminRegister', methods=['GET', 'POST'])
def registerAdmin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "name, "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'admEmail' in request.form and 'admPassword' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        admEmail = request.form['admEmail']
        admPassword = request.form['admPassword']
        
        # Check if account exists using MySQL        
        cursor = mariadb_connection.cursor()
        
        # Let's calculate the next administrator number and then rebuild the string with the new number
        # cursor.execute('SELECT MAX(SUBSTR(adNo, 3, 3)) FROM administrator')
        # maxAdNum = cursor.fetchone()
        # maxAdNum[0] += 1

        cursor.execute('SELECT * FROM administrator WHERE adEmail = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        
        cursor.execute('SELECT adPassword FROM administrator WHERE adEmail = %s OR adNo = %s', (admEmail, admEmail,))
        adminPass = cursor.fetchone()
        
        if not admEmail or not admPassword:
            msg = 'You need authorisation to open an administrator account.'
        elif not adminPass:
            msg = "Oops, that's not a valid administrator authenticator account. Try again."    
        elif admPassword != adminPass[0]:
            msg = "There's something wrong with the authentication details. Please try again."
        elif account:
            msg = 'An account with that email already exists. Please enter a different email or login here.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not password or not email or not name:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute("INSERT INTO administrator VALUES ('ad003', %s, %s, %s)", (name, password, email,))
            mariadb_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('adminRegister1.html', msg=msg)
    

# ____________________________________________________________________________
# CODE FOR SYSTEM HOMEPAGE http://localhost:5000/systemDSO34BT/home

# This part of the code manages information based on what is displayed on the home page.

# Current issues:
# 1. Missing home page LOL
# 2. 

@app.route('/systemDSO34BT/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', name=session['name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

# ____________________________________________________________________________
# CODE FOR SYSTEM ADMIN HOMEPAGE http://localhost:5000/systemDSO34BT/home

# This part of the code manages information based on what is displayed on the home page.

# Current issues:
# 1. Missing home page LOL
# 2. 

@app.route('/systemDSO34BT/adminDashboard')
def adminDashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('adminDashboard.html', name=session['name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# ____________________________________________________________________________
# CODE FOR SYSTEM SERVICES PAGE http://localhost:5000/systemDSO34BT/services

# This part of the code manages information based on what is displayed on the services page.

# Current issues:
# 1. 
# 2. 

@app.route('/systemDSO34BT/services')
def services():
    # Check if the user is logged in:
    if 'loggedin' in session:
        return render_template('services.html', username=session['username'])
    # User is not logged in, redirect them to login page
    return redirect(url_for('login'))


# ____________________________________________________________________________
# CODE FOR VIEWING/EDITING PROFILE http://localhost:5000/systemDSO34BT/profile

# This part of the code will let users view and edit their profile in accordance with
# the appropriate database tables. It will use the GET and POST requests of the Flask framework.

# Current issues:
# 1. Add edit profile section
# 2. 

@app.route('/systemDSO34BT/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        # Output message here for errors
        msg = ''
        # Check if "registration", "carmake", "bookdate" and "time" POST requests exist (user submitted form)
        if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form:
            # Create variables
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

                    
            cursor = mariadb_connection.cursor()

            if not name:
                name = session['name']
            elif not username:
                username = session['username']
            elif not email:
                email = session['email']
            elif not password:
                password = session['password']
            elif not name and not username and not email and not password:
                msg = 'Please fill out the form!'
            else:
                # Booking doesn't exist and the form data is valid, now insert new booking and vehicle into table
                cursor.execute("UPDATE customer SET cName = %s, cUsername = %s, email = %s, cPassword = %s WHERE cID = %s", (name, username, email, password, session['id']))
                mariadb_connection.commit()
                msg = 'Your profile has been edited.'
                editgood = """
                    Hey there! You've just made some changes to your profile. If you didn't do this, please inform us at
                    this email so we can help you secure your account.

                    Best regards,
                    Mongezi Masango
                """
                send_email(email, editgood)
                generatePDF(name, editgood, 'profile_change'+username)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out this form!'
        # Show registration form with message (if any)
        return render_template('profile.html', msg=msg, username=session['username'], name=session['name'], email=session['email'])
       # User is not loggedin redirect to login page
        
        return redirect(url_for('login'))   



# ____________________________________________________________________________
# CODE FOR BOOKING AN APPOINTMENT http://localhost:5000/systemDSO34BT/booking/

# This part of the code OUGHT to take inputs from the booking page and commit them to the vehicle and appointment
# tables, if they don't already exist. It will also use the GET and POST requests of the Flask framework.

# Current issues:
# 1. Code cannot get information from input boxes
#    RESOLVED - In the HTML, you need to specify the name attribute to the input tags.
# 2. Update how to get information from services box
# 3. Update tables to hold types of information


@app.route('/systemDSO34BT/booking', methods=['GET', 'POST'])
def booking():
    if 'loggedin' in session:
        # Output message here for errors
        msg = ''
        # Check if "registration", "carmake", "bookdate" and "time" POST requests exist (user submitted form)
        if request.method == 'POST' and 'registration' in request.form and 'carmake' in request.form and 'bookdate' in request.form and 'time' in request.form:
            # Create variables
            registration = request.form['registration']
            carmake = request.form['carmake']
            bookdate = request.form['bookdate']
            time = request.form['time']
            services = request.form['services']
            email = session['email']
            servicesNum = services[0:1]
            
            bookdatec = bookdate[6:]+ "-" + bookdate[:2] + "-" + bookdate[3:5] 
            # Check if booking already exists using MySQL        
            cursor = mariadb_connection.cursor()
 
            cursor.execute('SELECT MAX(aNo+2) FROM appointment')
            lastANo = cursor.fetchone()

            cursor.execute('SELECT MAX(vID+2) FROM vehicle')
            lastVID = cursor.fetchone()

            cursor.execute('SELECT * FROM vehicle WHERE vReg = %s', (registration,))
            registrationCheck = cursor.fetchone()

            # Validation check for time and date:
            cursor.execute('SELECT COUNT(aNo) FROM appointment WHERE aTime = %s AND aDate = %s', (time, bookdate,))
            booking = cursor.fetchone()
 
            # If booking exists show error and validation checks
            if booking>2:
                msg = 'Uh oh, that time is already taken! Try another time and/or date.'
            elif not registration or not carmake or not bookdate or not time:
                msg = 'Please fill out the form!'
            else:
                # Booking doesn't exist and the form data is valid, now insert new booking and vehicle into table
                if registrationCheck:
                    cursor.execute("INSERT INTO appointment VALUES (%s, %s, %s, %s)", (int(lastANo[0]), session['id'], bookdatec, time,))
                else:
                    cursor.execute('INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s) ', (int(lastVID[0]), carmake, session['id'], servicesNum, registration))
                    cursor.execute("INSERT INTO appointment VALUES (%s, %s, %s, %s)", (int(lastANo[0]), session['id'], bookdatec, time,))
                    mariadb_connection.commit()
                    msg = 'Your car is booked! See you soon. Check your email, we sent the details of your booking.'
                    bookinggood = """
                        Hey there! You've just made your booking for your %s on the %s at %s. We can't wait to see you there.
                        Your package is the %s, and you are liable for the charge stipulated. If you have any questions, don't
                        hesitate to email me at momasango1@gmail.com. Thanks a million, we're looking forward to seeing you soon!

                        Best regards,
                        Mongezi Masango
                    """, (carmake, bookdate, time, services)
                    send_email(email, bookinggood)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out this form!'
        # Show registration form with message (if any)
        return render_template('booking.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))   

# ____________________________________________________________________________
# CODE FOR BOOKING AN APPOINTMENT http://localhost:5000/systemDSO34BT/booking/

# This part of the code OUGHT to take inputs from the booking page and commit them to the vehicle and appointment
# tables, if they don't already exist. It will also use the GET and POST requests of the Flask framework.

# Current issues:
# 1. Code cannot get information from input boxes
#    RESOLVED - In the HTML, you need to specify the name attribute to the input tags.
# 2. Update how to get information from services box
# 3. Update tables to hold types of information


@app.route('/systemDSO34BT/adminBooking', methods=['GET', 'POST'])
def adminBooking():
    if 'loggedin' in session:
        # Output message here for errors
        msg = ''
        # Check if "registration", "carmake", "bookdate" and "time" POST requests exist (user submitted form)
        if request.method == 'POST' and 'registration' in request.form and 'carmake' in request.form and 'bookdate' in request.form and 'time' in request.form:
            # Create variables
            registration = request.form['registration']
            carmake = request.form['carmake']
            bookdate = request.form['bookdate']
            time = request.form['time']
            services = request.form['services']
            email = session['email']
            servicesNum = services[0:1]
            
            bookdatec = bookdate[6:]+ "-" + bookdate[:2] + "-" + bookdate[3:5] 
            # Check if booking already exists using MySQL        
            cursor = mariadb_connection.cursor()
 
            cursor.execute('SELECT MAX(aNo) + 1 FROM appointment')
            lastANo = cursor.fetchone()

            cursor.execute('SELECT MAX(vID) + 1 FROM vehicle')
            lastVID = cursor.fetchone()

            cursor.execute('SELECT * FROM vehicle WHERE vReg = %s', (registration,))
            registrationCheck = cursor.fetchone()

            # Validation check for time and date:
            cursor.execute('SELECT * FROM appointment WHERE aTime = %s AND aDate = %s', (time, bookdate,))
            booking = cursor.fetchone()
 
            # If booking exists show error and validation checks
            if booking:
                msg = 'Uh oh, that time is already taken! Try another time and/or date.'
            elif not registration or not carmake or not bookdate or not time:
                msg = 'Please fill out the form!'
            else:
                # Booking doesn't exist and the form data is valid, now insert new booking and vehicle into table
                if registrationCheck:
                    cursor.execute("INSERT INTO appointment VALUES (%s, %s, %s, %s)", (int(lastANo[0]), session['id'], bookdatec, time,))
                else:
                    cursor.execute('INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s) ', (int(lastVID[0]), carmake, session['id'], servicesNum, registration))
                    cursor.execute("INSERT INTO appointment VALUES (%s, %s, %s, %s)", (int(lastANo[0]), session['id'], bookdatec, time,))
                    mariadb_connection.commit()
                    msg = 'Your car is booked! See you soon. Check your email, we sent the details of your booking.'
                    bookinggood = """
                        Hey there! You've just made your booking for your %s on the %s at %s. We can't wait to see you there.
                        Your package is the %s, and you are liable for the charge stipulated below:
                        
                        USERNAME: %s
                        PACKAGE: %s
                        DATE: %s

                        If you have any questions, don't
                        hesitate to email me at momasango1@gmail.com. Thanks a million, we're looking forward to seeing you soon!

                        Best regards,
                        Mongezi Masango
                    """, (carmake, bookdate, time, services, username, services, bookdatec)
                    send_email(email, bookinggood)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out this form!'
        # Show registration form with message (if any)
        return render_template('adminBooking.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# ____________________________________________________________________________
# CODE FOR DOWNLOADING ADMINISTRATOR ANALYTICS http://localhost:5000/systemDSO34BT/booking/

# This part of the code OUGHT to take inputs from the booking page and commit them to the vehicle and appointment
# tables, if they don't already exist. It will also use the GET and POST requests of the Flask framework.

# Current issues:
# 1. Code cannot get information from input boxes
#    RESOLVED - In the HTML, you need to specify the name attribute to the input tags.
# 2. Update how to get information from services box
# 3. Update tables to hold types of information


@app.route('/systemDSO34BT/adminAnalytics1', methods=['GET', 'POST'])
def adminAnalytics1():
    if 'loggedin' in session:
        # Output message here for errors
        msg = ''        
        sqlAppointment = 'SELECT a.aNo, c.cName, c.cUsername, c.email, a.aDate, a.aTime FROM appointment a, customer c WHERE c.cID = a.cID ORDER BY 1 ASC;'
        cursor = mariadb_connection.cursor()
        cursor.execute(sqlAppointment)
        appointmentData = cursor.fetchall()

        cursor.execute("SELECT cID, cName, cUsername, email FROM customer")
        customerData = cursor.fetchall()

        cursor.execute("SELECT adNo, adName, adEmail FROM administrator")
        adminData = cursor.fetchall()

        now = datetime.now()
        current_time = now.strftime("%H%M%S")

        # Check if "registration", "carmake", "bookdate" and "time" POST requests exist (user submitted form)
        if request.method == 'POST' and 'option' in request.form:
            # Create variables
            optionChosen = request.form['option']
    
            doc = SimpleDocTemplate("adminAnalytics%s.pdf" % current_time,
            pagesize =letter)
            # container for the 'Flowable objects
            elements =[]
                    
            logo = "logo.png"
            formatted_time = time.ctime()
            im = Image(logo, 2*inch, 2*inch)
            elements.append(im)
            styles=getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            ptext = '<font size="12">%s</font>' % formatted_time
            elements.append(Paragraph(ptext, styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            if optionChosen == "All":
                
                appointmentHeadings = [[ '\t', 'Customer Name', 'Customer Username', 'Customer Email', 'Appointment Date', 'Time' ]]
                #s=Table(appointmentHeadings, 5*[1.65*inch], 1*[0.4*inch])
                #elements.append(s)
                t=Table(appointmentHeadings + appointmentData, 7*[1.65*inch], 10*[0.4*inch])
                #t.setStyle(TableStyle([('ALIGN', (1,1), (-2,-2), 'RIGHT'),
                # ('TEXTCOLOR', (1,1), (-2,-2), colors.black),
                # ]))

                elements.append(t)

                
                customerHeadings = [['CustomerID', 'Customer Name', 'Customer Username', 'Customer Email']]

                u=Table(customerHeadings + customerData, 4*[1.65*inch], 17*[0.4*inch])

                elements.append(u)

                adminHeadings = [['Administrator No', 'Administrator', 'Email']]

                v=Table(adminHeadings + adminData, 3*[1.65*inch], 4*[0.4*inch])

                elements.append(v)

                doc.build(elements) 
            elif optionChosen == "Appointment":
                appointmentHeadings = [[ '\t', 'Customer Name', 'Customer Username', 'Customer Email', 'Appointment Date', 'Time' ]]
                t=Table(appointmentHeadings + appointmentData, 7*[1.65*inch], 10*[0.4*inch])
                elements.append(t)
                doc.build(elements)

            elif optionChosen == "Customer":
                customerHeadings = [['CustomerID', 'Customer Name', 'Customer Username', 'Customer Email']]
                u=Table(customerHeadings + customerData, 4*[1.65*inch], 17*[0.4*inch])
                elements.append(u)
                doc.build(elements)

            elif optionChosen == "Administrator":
                adminHeadings = [['Administrator No', 'Administrator', 'Email']]
                v=Table(adminHeadings + adminData, 3*[1.65*inch], 4*[0.4*inch])
                elements.append(v)
                doc.build(elements)

            elif request.method == 'POST':
            # Form is empty... (no POST data)
                msg = 'Please choose an option before downloading.'
        # Show registration form with message (if any)
        return render_template('adminAnalytics1.html', msg=msg, output_data=appointmentData, outputCustData=customerData, outputAdminData=adminData)
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 

# Run the app
app.run()    
