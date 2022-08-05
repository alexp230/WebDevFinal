from __future__ import print_function
from ast import Delete, Pass
import email
from operator import mod
from tkinter import INSERT
from flask import Flask, render_template, request, flash, session, redirect, url_for
import random
import _sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, PrimaryKeyConstraint, Table, Column, Integer, String, ForeignKey, insert
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date

# List to keep track of emails and passwords in database
Emails = []
Passwords = []

total = 0
Sign_IN = True


# Stuff to start app, I guess? Was told by Internet to do this
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allitems.db'
app.config['SQLALCHEMY_BINDS'] = {
    'allusers': 'sqlite:///allusers.db',
    'allpurchases': 'sqlite:///allpurchases.db'
}

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '@#$%^&*('
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Class for items
class Item(db.Model):
    idITEM = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False,)

    # Helps with adding record to add to database
    def __init__(self, name, stock, barcode, price):
        self.name = name
        self.stock = stock
        self.barcode = barcode
        self.price = price

    # Allows us to print the database of Items in a rediable way === .toString()
    def __repr__ (self):
        return f'{self.barcode + ". " + self.name + ": ["+ self.stock + "] | $" + self.price}'

# Class for Users
class User(db.Model):
    __bind_key__ = 'allusers'
    idUSER = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    # Helps with adding record to add to database
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    # Allows us to print the database of Items in a rediable way === .toString()
    def __repr__ (self):
        return f'{self.firstname + " " + self.lastname + ": "+ self.email + " | " + self.password}'

class Manager_list(db.Model):
    __bind_key__ = 'allpurchases'
    M_idITEM = db.Column(db.Integer(), primary_key=True)
    M_name = db.Column(db.String(), nullable=False)
    M_stock = db.Column(db.Integer(), nullable=False)
    M_barcode = db.Column(db.String(), nullable=False)
    M_price = db.Column(db.Integer(), nullable=False,)

    # Helps with adding record to add to database
    def __init__(self, M_name, M_stock, M_barcode, M_price):
        self.M_name = M_name
        self.M_stock = M_stock
        self.M_barcode = M_barcode
        self.M_price = M_price

    # Allows us to print the database of Items in a rediable way === .toString()
    def __repr__ (self):
        return f'{self.M_barcode + ". " + self.M_name + ": ["+ self.M_stock + "] | $" + self.M_price}'

# Initial sign up page
@app.route('/', methods=['GET', 'POST'])
def signup():
    
    global Sign_IN
    Sign_IN = False


    # loops through users in database, gets their email and password, adds them to a list
    # for user in User.query.all():
    #     flash(user.email)
    #     flash(user.password)
    #     Email = str(user.email)
    #     Password = str(user.password)
    #     if Email not in Emails:
    #         Emails.append(Email)
    #     if Password not in Passwords:
    #         Passwords.append(Password)

    # Gets the text inside textbox in signup page
    if request.method == 'POST':
        FirstName = request.form.get('FirstName')
        Email = request.form.get('email')
        LastName = request.form.get('LastName')
        Password = request.form.get('password')
        ConfirmPassword = request.form.get('Confirmpassword')

        # Allows us to add user to database
        AddPerson = True

        # Checks to see if a field is blank
        if FirstName == "":
            AddPerson = False
        if Email == "":
            AddPerson = False
        if LastName == "":
            AddPerson = False
        if Password == "":
            AddPerson == False
        if ConfirmPassword == "":
            AddPerson == False
    
        # Checks to see if password and confirmed password are equal
        if Password != ConfirmPassword:
            AddPerson == False
            flash("Passwords Do Not Match! Try Again!")
            Sign_IN = False
            return render_template('SignUp.html')

        # Checks to see if the entered email is already in use
        if (Email in Emails):
            AddPerson = False
            flash("Email is already in use")
            Sign_IN = False
            return render_template('SignUp.html')

        # If everything is good, add User to database
        if AddPerson == True:
            Emails.append(Email)
            Passwords.append(Password)
            record = User(FirstName, LastName, Email, Password)
            db.session.add(record)
            db.session.commit()
            Sign_IN = False
            return thankyou()

    return render_template('SignUp.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ""

    global Sign_IN
    if Sign_IN == False:
        msg = "Must Sign in first"

    if request.method == 'POST':
        # Gets text inside textbox in signin page
        email = request.form.get('email')
        password = request.form.get('password')
       
       # Allow us to sign in
        ISIn = True
        E = False
        P = False

        # Checks to see if entered email exists
        for user in User.query.all():
            if user.email == email:
                E = True
        if (E == False):
            ISIn = False
            msg = "Could not find user"
            return render_template('signin.html', msg = msg)
        
        # Checks to see if entered password exists (just realized it needs to be change)
        for user in User.query.all():
            if user.password == password:
                P = True
        if (P == False):
            ISIn = False
            msg = "Password does not match"
            return render_template('signin.html', msg = msg)

        # If everything is good, go to home page
        if (ISIn == True):

            if (email == "manager@gmail.com"):
                return  redirect(url_for("secretpage"))

            #Josh - Adding this to get email to display on user home page.
            session["logedin"]  = True
            session["email"] = email
            Sign_IN = True
            if Sign_IN == True:
                return redirect(url_for("home"))

    return render_template("signin.html", msg = msg)

# Josh - Creating method that adds each item selected from browse to the users cart. 
# Edits made by Alex
@app.route('/additem', methods = ['POST', 'GET'])
def additem():
    msg = ""
    itemName = ""
    itemID = ""
    amount = ""
    price = ""

    global Sign_IN
    if Sign_IN == False:
        return redirect(url_for("signin"))
        
    if request.method == 'POST':
            check_amount = request.form.get('amount')
            check_barcode = request.form.get("theitemID")

            if (len(check_barcode) != 4):
                msg = "Invalid Barcode! Please Try Again!"
                return render_template("browse.html", msg = msg, items=Item.query.all())

            if (int(check_amount) < 1):
                msg = "Invalid Quantity! Please Try Again!"
                return render_template("browse.html", msg = msg, items=Item.query.all())

            for i in Item.query.all():
                if (str(check_barcode) == i.barcode):
                    itemName = i.name
                    itemID = i.barcode
                    amount = check_amount
                    price = i.price

    try:
        # Josh - Connecting to database. 
        with sql.connect("useritems.db") as con:
            cur = con.cursor()
            # Josh - Executing command to insert item data into users cart.
            cur.execute("INSERT INTO items (itemName, itemID, amount, price) VALUES (?,?,?,?)",
            (itemName, itemID, amount, price) )
            # Josh - Commiting changes to database.
            con.commit()
            # Josh - Testing to see if successful.
            msg = "Successfully added item to cart"
    except:
        # Josh - Rolling back commits in case of failure.
        con.rollback()
        # Josh - Testing for failure.
        msg = "Something went wrong, Try Again."
    finally:
        return render_template("browse.html", msg = msg, items=Item.query.all())
    
# Josh - Creating table in useritems.db
con = sql.connect('useritems.db')
cur = con.cursor()
# # cur.execute("CREATE TABLE items (itemName TEXT, itemID TEXT, amount TEXT, price TEXT)")

# Josh - Setting up user home page.
@app.route('/home')
def home():
    msg = ""
    global total
    total = 0
    global Sign_IN
    if Sign_IN == False:
        return redirect(url_for("signin"))

    # Josh - Connecting to the database, and accessing the table rows.
    con = sql.connect('useritems.db')
    con.row_factory = sql.Row

    # Josh - Setting the cursor, and executing the command to get info from table in database.
    cur = con.cursor()
    cur.execute("select * from items")

    # Josh - Sets a variable equal to all the rows data.
    rows = cur.fetchall()

    # adds total to subtotal value in html
    for i in rows:
        if (i[2].isnumeric()):
            total = total + ((int(i[2])) * (int(i[3])))
            msg = msg  + " " + i[3]
    

    return render_template('home.html', rows = rows, msg = msg, total = total)

@app.route('/browse')
def browse():

    # items=Item.query.all()   sets the database equal to a variable and allows us to display info on browse.html
    return render_template('browse.html', items=Item.query.all())

# Josh - Creating a method to list all items that have been added to users cart.
@app.route('/checkout')
def checkout():
    global total
    msg = ""

    # Josh - Connecting to the database, and accessing the table rows.
    con = sql.connect('useritems.db')
    con.row_factory = sql.Row

    # Josh - Setting the cursor, and executing the sql comand to get info from table in database (Not Working Yet).
    cur = con.cursor()
    cur.execute("select * from items")

    # Josh - Sets a variable equal to all the rows data.
    rows = cur.fetchall()
    return render_template('checkout.html', rows = rows, msg = msg, total = total)

@app.route('/secretpage', methods = ['POST', 'GET'])
def secretpage():
    msg = ""

    # Gets the text inside textbox in secret page
    if request.method == 'POST':
        itemname = request.form.get('itemname')
        itemstock = request.form.get('itemstock')
        itemprice = request.form.get('itemprice')
        itemmodify = request.form.get('itemmodify')
        itemdelete = request.form.get('itemdelete')
        itemadd= request.form.get('itemadd')

        # Allows us to check which option the manager wants to change
        Modify = False
        Delete = False
        Add = False
        counter = 0

        # Checks to see if a field is blank
        if itemmodify != "":
            Modify = True
            counter = counter + 1
        if itemdelete != "":
            Delete = True
            counter = counter + 1
        if itemadd != "":
            Add = True
            counter = counter + 1

        # Checks to see if data in is multiple boxes if so, error message
        if (counter > 1):
            msg = "Cannot fill data in Modify, Delete, and/or And at the same time!"
            rows = Manager_list.query.all()
            return render_template('secretpage.html', msg = msg, rows = rows)

        # If only modify is true
        if Modify == True:
            if itemname == "":
                msg = "Please fill in all data"
                rows = Manager_list.query.all()
                return render_template('secretpage.html', msg = msg, rows = rows)
            if itemstock == "":
                msg = "Please fill in all data"
                rows = Manager_list.query.all()
                return render_template('secretpage.html', msg = msg, rows = rows)
            if itemprice == "":
                msg = "Please fill in all data"
                rows = Manager_list.query.all()
                return render_template('secretpage.html', msg = msg, rows = rows)

            # Checks to see if entered barcode is in database
            # If yes, change data of item at specific barcode based off of request.method
            for i in Item.query.all():
                if (str(itemmodify) == i.barcode):
                    i.name = itemname
                    i.stock = itemstock
                    i.price = itemprice
                    db.session.commit()
                    msg = i
                    rows = Manager_list.query.all()
                    return render_template('secretpage.html', msg = msg, rows = rows)

        # If only add is true
        elif (Add == True):
            if itemname == "":
                msg = "Please fill in all data"
                return render_template('secretpage.html', msg = msg)
            if itemstock == "":
                msg = "Please fill in all data"
                return render_template('secretpage.html', msg = msg)
            if itemprice == "":
                msg = "Please fill in all data"
                return render_template('secretpage.html', msg = msg)

            # Checks to see if entered barcode is in database
            # If no, adds data of item based off of request.method
            # If yes, error message
            for i in Item.query.all():
                if (str(itemadd) == i.barcode): 
                    msg = "Barcode is already in use"
                    return render_template('secretpage.html', msg = msg)
            record = Item(itemname, itemstock, itemadd, itemprice)
            msg = record
            db.session.add(record)
            db.session.commit()
            rows = Manager_list.query.all()
            return render_template('secretpage.html', msg = msg, rows = rows)

        # If only delete is true
        elif (Delete == True):
           # Checks to see if entered barcode is in database
           # If yes, deletes the item based off barcode
           # If no, error message
            for i in Item.query.all():
                    if (str(itemdelete) == i.barcode): 
                        db.session.delete(i)
                        db.session.commit()
                        msg = "Delete has gone through"
                        rows = Manager_list.query.all()
                        return render_template('secretpage.html', msg = msg, rows = rows)
            msg = "Cannot find item based off of inputted barcode"
            rows = Manager_list.query.all()
            return render_template('secretpage.html', msg = msg, rows = rows)

    rows = Manager_list.query.all()
    
    return render_template('secretpage.html', msg = msg, rows = rows)

# Josh - Deleting the entire table upon pruchase.
@app.route('/specialthanks')
def specialthanks():
    msg = ""

    M_I = ""
    M_S = ""
    
    M_B = ""
    M_P = ""
    

    try:

        # Josh - Connecting to the database.
        with sql.connect("useritems.db") as con:

            con.row_factory = sql.Row

            # Josh - Setting the cursor, and executing the sql comand to get info from table in database (Not Working Yet).
            cur = con.cursor()
            cur.execute("select * from items")

            rows = cur.fetchall()

            for i in rows:
                M_I = i[0]
                M_B = i[1]
                M_S = i[2]
                M_S = int(M_S)
                M_P = i[3]
                M_P = int(M_P)

                record = Manager_list(M_I, M_S, M_B, M_P)
                db.session.add(record)
                db.session.commit()

                for j in Item.query.all():
                    if j.barcode == M_B:
                        j.stock = int(j.stock)
                        M_S = int(M_S)
                        j.stock = j.stock - M_S
                        db.session.commit()



            # Josh - Executing command to delete all data from table 'items'.
            cur.execute("DELETE FROM items")
            # Committing changes to table.
            con.commit()

            # Josh - Testing to see if successful.
            msg = "Thank you for your purchase!"
    except:
        # Josh - Rolling back commit in case of failure.
        con.rollback()
        # Josh - Testing for failure.
        msg = "Something went wrong, Try Again."
    finally:
        return render_template("specialthanks.html", msg = msg)

if __name__ == '__main__':
    app.run(debug = True)