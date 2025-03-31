from email.message import Message
from email.policy import default
from enum import unique
from os.path import split

from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
from flask_migrate import Migrate
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from werkzeug.security import check_password_hash

indexloc =r"C:\Users\jarod\PycharmProjects\Sportproject\.venv\Templates"
app = Flask(__name__, template_folder=indexloc)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app,db)

DayNumbers = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}


class TODO(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = True)
    dateCreated = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

class USER(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    account = relationship('ACCOUNTDATA', back_populates='login', uselist=False)
    planning = relationship('PDATA', back_populates='login')

    def __repr__(self):
        return '<Task %r>' % self.id

class ACCOUNTDATA(db.Model):
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    age = db.Column(db.String(120), nullable=True)
    place = db.Column(db.String(120), nullable=True)
    favorite_sport = db.Column(db.String(120), nullable=True)
    availableD = db.Column(db.String(120), nullable=True)
    availableT = db.Column(db.String(120), nullable=True)
    personality = db.Column(db.String(120), nullable=True)

    login_id = db.Column(Integer, ForeignKey('users.id') , unique = True)
    login = relationship('USER', back_populates='account',uselist=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class PDATA(db.Model):
    __tablename__ = "plan_data"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(255),nullable = False)
    day_created = db.Column(db.String(20))
    values = db.Column(db.String(255), nullable=False)

    login_id = db.Column(Integer, ForeignKey('users.id'))
    login = relationship('USER', back_populates='planning')


@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = TODO(content = taskContent)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an issue"
    else:
        if 'username' in session:
            return render_template("index.html", logged = True)
        else:
            return render_template("index.html", logged =False)

@app.route('/gotologin', methods = ['POST','GET'])
def gotologin():
    if request.method == "POST":
        return render_template('login.html', show = "login")
    else:
        return render_template('login.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = USER.query.filter_by(user_name=username).first()

        if user != None:
            if (user.password == password):
                session['username'] = username
                return redirect(url_for('index'))


        else:
            print(f"wrong")
            return render_template('login.html', loginError=True)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.json
        print(data)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if USER.query.filter_by(user_name = username).count() > 0:
            hey = jsonify(message="Deze gerbuikersnaam is al in gebruik")
            return hey
        elif USER.query.filter_by(email = email).count() > 0:
            return jsonify(message="Deze email is al in gebruik")

        else:
            newUser = USER(user_name=username,
                           password=password,
                           email=email)
            try:
                db.session.add(newUser)
                db.session.commit()
                jett = jsonify(message="")
                return jett
            except Exception as e:
                return f"{e}"

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop('username', None)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"{e}")

@app.route('/home', methods=['POST', 'GET'])
def gotohome():
    if request.method == "POST":
        return redirect(url_for('index'))
    else:
        return ""


@app.route('/showlogin', methods=['POST'])
def showlogin():
    # Get the number sent via AJAX (default is 0 if no number is provided)
    number = int(request.form['number'])

    # Check the number and return different content
    if number == 1:
        return 'show|loginForm|hide|RegisterForm'
    elif number == 2:
        return 'show|RegisterForm|hide|loginForm'

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user = USER.query.filter_by(user_name=username).first()

        if ACCOUNTDATA.query.filter_by(login_id=user.id).count() > 0:
            account = user.account
            days = account.availableD
            times = account.availableT
            splitdays = [item.strip() for item in days.split(",") if item]
            splittimes = [item.strip() for item in times.split(",") if item]
            combinedTimes = [(splittimes[i], splittimes[i+1]) for i in range(0, len(splittimes), 2)]

            myDict = dict(zip(splitdays,combinedTimes))
            print(splitdays)
            print(splittimes)
            print(myDict)

            return render_template("Dashboard.html",
                    logged=True,
                    account = account,
                    days = splitdays,
                    times = myDict)

        else:
            return render_template("Dashboard.html", logged=True, account = None)

    else:
        return redirect('/')

@app.route('/save_profile', methods=['GET', 'POST'])
def save_profile():
    if request.method == 'POST':
        username = session['username']
        user= USER.query.filter_by(user_name=username).first()
        name = request.form['profileNameL']
        age = request.form['profileAgeL']
        place = request.form['profilePlaceL']
        favorite_sport = request.form['profileSportL']
        daysList = request.form.getlist('days')
        days = ''
        timesList = request.form.getlist('times')
        times = ''
        for i in range(len(daysList)):
            day = daysList[i]
            dayN = DayNumbers[day]
            days += day + ','
            times += timesList[dayN*2] + ',' + timesList[dayN*2+1] + ','
        days = days[:-1]
        availableD = days
        availableT = times
        personality = request.form['profilePersonalityL']

        if ACCOUNTDATA.query.filter_by(login_id = user.id).count() > 0:
            account = user.account

            account.name=name
            account.age=age
            account.place=place
            account.favorite_sport=favorite_sport
            account.availableD = availableD
            account.availableT=availableT
            account.personality=personality
            account.login_id=user.id
            db.session.commit()
            return redirect('/profile')
        else:
            new_account = ACCOUNTDATA(name=name,
                                      age = age,
                                      place = place,
                                      favorite_sport = favorite_sport,
                                      availableT = availableT,
                                      availableD =availableD,
                                      personality = personality,
                                      login_id = user.id)
            db.session.add(new_account)
            db.session.commit()
            return redirect('/profile')
    else:
        return render_template('Dashboard.html')

@app.route('/planning', methods = ['GET', 'POST'])
def planning():
    if 'username' in session:
        username = session['username']
        user = USER.query.filter_by(user_name=username).first()
        try:
            if PDATA.query.filter_by(login_id=user.id).count() > 0:
                planning = db.session.query(PDATA).filter(PDATA.login_id == user.id).all()
                if len(planning) > 0:
                    dayList = []
                    for i in range(len(planning)):
                        day = planning[i].day
                        values = planning[i].values
                        value = str(values)
                        dayList.append((day, value))
                    print(dayList)
                    return render_template('planning.html', logged=True)
                else:
                    return render_template('planning.html', logged = True)
            else:
                return render_template('planning.html', logged = True)
        except Exception as e:
            print(e)
            return '{e}'
    else:
        return redirect('/')

@app.route('/savePlanning', methods = ['GET', 'POST'])
def savePlanning():
    if 'username' in session:
        username = session['username']
        user = USER.query.filter_by(user_name=username).first()
        values = request.form.get('vals')
        classes = request.form.get('classes')

        classSplit = classes.split(',')

        if PDATA.query.filter_by(login_id=user.id).count() > 0:
            planning = db.session.query(PDATA).filter(PDATA.login_id == user.id).first()
            for i in range(len(classSplit)):
                currentC = classSplit[i]
                if planning.query.filter_by(day=currentC).count() > 0:
                    current_plan = db.session.query(PDATA).filter(PDATA.day == currentC).first()
                    current_plan.values = values
                    db.session.commit()
                else:
                    new_plan = PDATA(day=currentC, login_id=user.id, values = values)
                    db.session.add(new_plan)
                    db.session.commit()
        else:
            for i in range(len(classSplit)):
                currentC = classSplit[i]
                new_plan = PDATA(day=currentC, login_id = user.id, values = values)
                db.session.add(new_plan)
                db.session.commit()

    return "Data saved successfully"

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if 'username' in session:
        username = session['username']
        user = USER.query.filter_by(user_name=username).first()
        searches = db.session.query(ACCOUNTDATA).filter(ACCOUNTDATA.id != user.id).limit(30).all()
        values = []
        for s in searches:
            values.append({"id": s.id,
                      "name": s.name,
                      "sport": s.favorite_sport,
                      "age": s.age,
                      "place": s.place,
                      "availableD": s.availableD,
                      "availableT": s.availableT,
                      "personality": s.personality})
        for i in values:
            print(i)
        return render_template('matching.html', logged = True, searches = values)
    else:
        return render_template('matching.html')

if __name__ == '__main__':
    app.run(debug=True)