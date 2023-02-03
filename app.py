from flask import Flask,render_template,request,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import (StringField,PasswordField,EmailField)
from wtforms.validators import InputRequired,Length,EqualTo,Email,ValidationError

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '23y2193721ejwqe'

p=[
    {"title":"Hello World",
    "content":"Lorem Ipsum"},
    {"title":"Hello World",
    "content":"Lorem Ipsum"},
    {"title":"Hello World",
    "content":"Lorem Ipsum"}    
]

users=[
    {'username':"One",
    "email":"abc@gmail.com",
    "password":"a"
    }
]

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=2,max=20)])
    email=EmailField('Email',validators=[InputRequired(),Email()])
    password=PasswordField('Password',validators=[InputRequired()])
    confirmpassword=PasswordField('ConfirmPassword',validators=[InputRequired(),EqualTo('password')])

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[InputRequired(),Email()])
    password=PasswordField('Password',validators=[InputRequired()])



def emailvalidation(form,field):
    valid=0
    for user in users:
        if(user.email==field and form.password ==user.password):
            valid=1
    
    if valid == 0 :
        raise ValidationError('Not found')



@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        p.append({"title":request.form['title'],
        "content":request.form['content']})
        return render_template('home.html',contents=p)
    return render_template('home.html',contents=p)


@app.route('/',methods=['GET','POST'])
def login():
    form=LoginForm()

    if request.method=='POST':
        valid=0
        for user in users:
            print(user['email'],request.form['email'])
            if user['email']==request.form['email'] and user['password']==request.form['password']:
                valid=1
    
        if valid == 0 :
            return render_template('login.html',form=form,error="Incorrect Username or Password")
        else :
            return redirect('/home')

    return render_template('login.html',form=form,error="")


@app.route('/register',methods=['GET','POST'])
def register():

    if request.method=='POST':
        users.append({
            "username":request.form['username'],
            "email":request.form['email'],
            "password":request.form['password'],
        })
        return redirect(url_for('home'))
    form=RegisterForm()
    return render_template('register.html',form=form)
    