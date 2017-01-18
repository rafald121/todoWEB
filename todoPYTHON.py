# -*- coding: utf-8 -*-
from urllib2 import HTTPError, Request, urlopen
from flask import Flask, session, render_template, redirect, request, json
from flask import url_for

app = Flask(__name__)
app.secret_key = "fwgjebhuih4"

@app.route('/')
def hello_world():
    if 'token' in session:
        return redirect(url_for("main"))
    else:
        return redirect(url_for("loginPage"))

# pobiera ile niezrobionych
@app.route('/main')
def main():

    return "main"

@app.route('/login')
def loginPage():
    if 'token' in session:
        return redirect(url_for("main"))
    else:
        return render_template("logowanie.html")


# TODO czemu nie dziala gdy daje metode POST
# @app.route('/checkLogin')
@app.route('/checkLogin', methods=['POST', 'GET'])
def checkLogin():

    login = request.form['login']
    password = request.form['password']

    data = {
        "login": login,
        "password": password
    }

    headers = {
        'Content-Type': 'application/json'
    }

    jsonData = json.dumps(data)

    myRequest = Request("http://127.0.0.1:5000/login", data=jsonData, headers=headers)
    # TODO co to daje \/
    # myRequest.get_method = lambda: 'POST'

    try:
        myResponse = urlopen(myRequest)
        myResponseDictionary = json.load(myResponse)

        if myResponseDictionary['info'] == 'OK' and myResponse.getcode() == 200:
            session['token'] = myResponseDictionary['token']
            session['login'] = login
            session['id'] = myResponseDictionary['userID']
            print("token: ")
            print(session['token'])
            print("login:")
            print(session['login'])
            print("id:")
            print(session['id'])

            # redirect to todoList
            return redirect(url_for('allMessages'))
        else:
            print myResponseDictionary['error']
            # redirect to login again
    except HTTPError as e:
        print e.code
        print e.reason
        return render_template("logowanie.html")
               # return render_template("logowanie.html", error=myResponseDictionary['error'])

        # return e.read()


@app.route("/allMessages")
def allMessages():
    print("przekierowano do allMessages")

    return "test"


if __name__ == '__main__':
    app.run(port=4999, debug=True)
