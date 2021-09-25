from flask import Flask,session,render_template,request,redirect,url_for
import datetime
# from flask import url_for  # I will learn after that will use
# from flask import flash    # I will learn after that will use
import os
from hashlib import md5
from peewee import *

app = Flask(__name__)

db = SqliteDatabase('login.db')
def add_user(user):
    db.connect()
    user.save()
    db.close()
    return
@app.route("/signup",methods=['GET','POST'])
def signup():
    if  request.method == 'POST':
        testData = User(username='vanprokthp',password=md5(b'123').hexdigest(),fullname="Trọng Văn",active=True)
        add_user(testData)
        return redirect('/login')
    else:
        return render_template('signup.html')  
@app.route("/")  
@app.route("/index")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('home.html',login=True)    
@app.route("/login",methods=['GET','POST'])
def login():
    if not session.get('logged_in'):
        wrongpass=False
        if  request.method == 'POST':
            if request.form["submit_button"]=="login":
                username = request.form['username']
                password = request.form['password']
                login_user = User.select().where(User.username == username, User.password == md5(password.encode()).hexdigest())
                if login_user.exists():

                    session['logged_in'] = True
                    session['username'] = username
                    session['password'] = password
                    fullname=(User.get(User.username==username).fullname)
                    session["name"]=fullname
                    return redirect(url_for("index"))
                else:
                    return render_template('login.html',wrongpass=True)

            else: 
                if request.form["submit_button"]=="signup":
                    return redirect(url_for("signup"))
        else:
            return render_template('login.html')
    else:
        redirect(url_for("index"))

#@app.route("/template")
#def template():
#    return render_template('template.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

class User(Model):
    username = CharField(unique=True)
    fullname = CharField()
    password= CharField()
    active = BooleanField()
    created_at =DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

db.connect()

if not (User.table_exists() ):
    db.create_tables([User], safe=True)
    testData = User(username='trongvan',password=md5(b'123').hexdigest(),fullname="Bùi Trọng Văn",active=True)
    testData.save()
db.close()
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(port=1111,debug=True)
