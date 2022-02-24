import re
from flask import Flask, render_template, request, redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
import requests
import time

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

# em=""
# pa=""

class ContactUs(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(20), nullable=False)
    lname=db.Column(db.String(20), nullable=False)
    gender=db.Column(db.String(7), nullable=False)
    phone=db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(20), nullable=False)
    feedb=db.Column(db.String(500), nullable=False)

class registration(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(20), nullable=False)
    lname=db.Column(db.String(20), nullable=False)
    gender=db.Column(db.String(7), nullable=False)
    phone=db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(20), nullable=False)
    
class weather(db.Model):
    sno=db.Column(db.Integer, primary_key=True) 
    Email=db.Column(db.String(50), nullable=False)
    City=db.Column(db.String(20), nullable=False)
    Longitude=db.Column(db.String(20), nullable=False)
    Latitude=db.Column(db.String(20), nullable=False)
    Weather=db.Column(db.String(20), nullable=False)
    Temperature=db.Column(db.String(20), nullable=False)
    Feels_Like=db.Column(db.String(20), nullable=False)
    Pressure=db.Column(db.String(20), nullable=False)
    Humidity=db.Column(db.String(20), nullable=False)
    Wind=db.Column(db.String(20), nullable=False)
    Time=db.Column(db.String(20), nullable=False)


@app.route("/",methods=["GET","POST"])
def login():
    # global em,pa
    if 'email' in session:
        flash("You are already login","success")
        return render_template('home.html',se=session['logo'])

    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        lo=registration.query.all()
        for i in lo:
            if email==i.email and password==i.password:
                # em=i.email
                # pa=i.password
                session['email']=email
                session['logo']=(i.fname[0:1]+i.lname[0:1]).upper()
                break
        
        # if em=="" and pa="":
        if 'email' in session:
            return redirect("/home")
        else:
            flash("Invalid Email or Password Or you may have not signed up!!","warning")
            return redirect("/")

    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():

    if 'email' in session:
        flash("You are already login","success")
        return render_template('home.html',se=session['logo'])


    if request.method=="POST":
        fname=request.form['fname']
        lname=request.form['lname']
        gender=request.form['gender']
        phone=request.form['phone']
        email=request.form['email']
        password=request.form['password']
        
        if fname=="" or lname=="" or len(phone)!=10 or email=="" or password=="":
            flash("Please fill all the feilds and phone number should be of 10 digits","warning")
            redirect("/signup")
        else:
            log=registration(fname=fname,lname=lname,gender=gender,phone=phone,email=email,password=password)
            db.session.add(log)
            db.session.commit()
            flash("Successfully Sign Up","success")
            return redirect("/")
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    # global em,pa
    # em=""
    # pa=""
    session.pop('email')
    session.pop('logo')
    return redirect("/")

@app.route("/home")
def hello_world():
    # if em !="" and pa !="":
    if 'email' in session:
        return render_template("home.html",se=session['logo'])
    else:
        return redirect("/")

@app.route("/currentwea",methods=['GET','POST'])
def currentwea():
    # if em !="" and pa !="":
    if 'email' in session:
        if request.method=='POST':
            c=request.form['city']
            if c=="":
                return render_template("currentwea.html",l={'0':0},se=session['logo'])
            else:
               url="https://api.openweathermap.org/data/2.5/weather?appid=850789bc308ec795c19f9f4df7ed367d&q="+c
               
               d=requests.get(url).json()
               l=dict(d)
               print(l)
               if l['cod']!='404':
                    t=time.strftime('%H:%M:%S', time.gmtime(l['dt']-l['timezone']))
                    l['dth']=t

                    we=weather(Email=session['email'],City=l['name'],Longitude=l['coord']['lon'],Latitude=l['coord']['lon'],Weather=l['weather'][0]['main'],Temperature=(l['main']['temp']-273.15),Feels_Like=(l['main']['feels_like']-273.15),Pressure=l['main']['pressure'],Humidity=l['main']['humidity'],Wind=l['wind']['speed'],Time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    db.session.add(we)
                    db.session.commit()

               return render_template("currentwea.html",l=l,se=session['logo'])

        return render_template("currentwea.html",l={'0':0},se=session['logo'])
    else:
        return redirect("/")

@app.route("/AboutUs")
def about():
    # if em !="" and pa !="":
    if 'email' in session:
        return render_template("about.html",se=session['logo'])
    else:
        return redirect("/")

@app.route("/ContactUs",methods=["GET","POST"])
def contact():
    # if em !="" and pa !=""4
    if 'email' in session:
        if request.method=="POST":
            fname=request.form['fname']
            lname=request.form['lname']
            gender=request.form['gender']
            phone=request.form['phone']
            email=request.form['email']
            feedb=request.form['feedb']
            if fname=="" or lname=="" or len(phone)!=10 or email=="" or feedb=="":
                flash("Please fill all the feilds and phone number should be of 10 digits","warning")
                redirect("/ContactUs")
            else:
                con=ContactUs(fname=fname,lname=lname,gender=gender,phone=phone,email=email,feedb=feedb)
                db.session.add(con)
                db.session.commit()
                flash("Your feedback is successfully ","success")
                return redirect("/ContactUs")
        
        lo=registration.query.filter_by(email=session['email']).first()
        return render_template("contact.html",lo=lo,se=session['logo'])
 
    else:
        return redirect("/")
    
    
@app.route("/history")
def history():
    # if em !="" and pa !="":
    if 'email' in session:
        allfeed=weather.query.filter_by(Email=session['email']).all()
        return render_template("history.html",allfeed=allfeed,se=session['logo'])
    else:
        return redirect("/")

@app.route("/deletehistory/<int:sno>")
def deletehistory(sno):
    # if em !="" and pa !="":   
    if 'email' in session:
        feed=weather.query.filter_by(Email=session['email'],sno=sno).first()
        db.session.delete(feed)
        db.session.commit()
        flash("History is successfully deleted","success")
        return redirect('/history')
    else:
        return redirect("/")


@app.route("/delete/<int:sno>")
def delete(sno):
    # if em !="" and pa !="":   
    if 'email' in session:
        con=ContactUs.query.filter_by(sno=sno).first()
        db.session.delete(con)
        db.session.commit()
        flash("Your feedback is successfully deleted","success")
        return redirect('/history')
    else:
        return redirect("/")
    
@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    # if em !="" and pa !="":    
    if 'email' in session:
        if request.method=='POST':
            fname=request.form['fname']
            lname=request.form['lname']
            gender=request.form['gender']
            phone=request.form['phone']
            email=request.form['email']
            feedb=request.form['feedb']
            if fname=="" or lname=="" or len(phone)!=10 or email=="" or feedb=="":
                flash("Please fill all the feilds and phone number should be of 10 digits","warning")
                redirect("/update/sno")
            else:
                con=ContactUs.query.filter_by(sno=sno).first()
                con.fname=fname
                con.lname=lname
                con.gender=gender
                con.phone=phone
                con.email=email
                con.feedb=feedb

                db.session.add(con)
                db.session.commit()
                flash("Your feedback is successfully updated","success")

                return redirect('/history')

        con=ContactUs.query.filter_by(sno=sno).first()
        return render_template('update.html',feed=con,se=session['logo'])
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)