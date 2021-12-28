from flask import Flask, render_template, request, sessions, url_for, redirect, session, g, Response,redirect
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'supersecretkey'
def connection():
    conn = psycopg2.connect(
        host="localhost",
        database="eco",
        user="postgres",
        password="123"
    )
    print("hello",conn)
    return conn
connection()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        conn = connection()
        req=request.form
        username=str(req['username'])
        email=str(req['email'])
        password =str(req['password'])
        hased_password = generate_password_hash(
            password, method='sha256')
        cur = conn.cursor()

        cur.execute("SELECT * FROM {} WHERE {} = '{}';".format("userprofile", "username", username))

        # check if username is already taken or not
        user_object = cur.fetchall()
        if user_object:
            print("Username is taken")
            return "Username is already taken!"

        # Add User to DB
        cur.execute("INSERT INTO userprofile (email, password, username, usertype) VALUES (%s, %s, %s, %s);",
                    (email, hased_password, username, "admin"))

        print("User created")
        # commit changes to DB
        conn.commit()
        cur.close()
        conn.close()
        print("redirecting to sigin.html")



        return render_template('signin.html')
    return render_template('signup.html')

    
@app.route("/map", methods=['GET', 'POST'])
def map():
    return render_template('map.html')

@app.route('/signin', methods=['GET', 'POST'])

def signin():
    if request.method=='POST':
        conn = connection()
        req=request.form
        username=str(req['username'])
        password =str(req['password'])
        cur = conn.cursor()
        cur.execute("SELECT password, usertype FROM {} WHERE {} = '{}';".format(
            "userprofile", "username", username))
        user_object = cur.fetchall()
        print("data",user_object)
        session.pop('user', None)
        if len(user_object)==0:
            print("Wrong credentials")
            return "Wrong  username"

        elif check_password_hash(user_object[0][0], password) and user_object[0][1]=='admin':
            session['user'] = username
            print("user signed in")
            return render_template('map.html')
        elif check_password_hash(user_object[0][0], password) and user_object[0][1]=='user':
            session['user'] = username
            print("user signed in")
            return render_template('dashboard_map.html')
        else:
            print("Wrong credentials")
            return "Wrong  Password"

    return render_template('signin.html')   









if __name__ == '__main__':
    # For debugging while developing
    app.run(host='127.0.0.1', port=7000, debug=True)
