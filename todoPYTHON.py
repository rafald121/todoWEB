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
        return redirect(url_for("login"))

# pobiera ile niezrobionych i wyswietla glowny panel
@app.route('/main')
def main():
    undoneQuantity = None

    token = session['token']
    requestData = {'token': token}
    requestHeaders = {"Content-Type": "application/json"}

    myRequest = Request("http://127.0.0.1:5000/notdone", data=requestData, headers=requestHeaders)

    try:
        responseJson = urlopen(myRequest)
        responseJsonData = json.load(responseJson)

        if responseJson.getcode() == 200:
            undoneQuantity = responseJsonData['undone']

            return render_template("mainPage.html", login = session['login'], undoneQuantity=undoneQuantity)
        else:
            return responseJsonData['error']
    except HTTPError as e:
        print(e.code)
        print(e.message)
        # TODO dodac w mainPage miejsce na komunikaty o np. niepoprawnym wczytaniu          niewykonanych zadań
        # return render_template("mainPage.html")
        return responseJsonData['error']

@app.route('/login')
def login():
    if 'token' in session:
        return redirect(url_for("main"))
    else:
        return render_template("logowanie.html")


# TODO co zmieni gdy usune POST albo GET
@app.route('/checkLogin', methods=['POST', 'GET'])
def checkLogin():

    myResponseDictionary = None
    # TODO error that is returning when login or password is valid

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
            return redirect(url_for('main'))
        else:
            return render_template("logowanie.html", error = True, errorMessage = "sprawdzic jesli wyskoczy ten komunikat")

    except HTTPError as e:
        print e.code
        print e.reason
        # TODO sprawic, aby errorMessage zwracalo blad z API
        return render_template("logowanie.html", error=True, errorMessage="blad logowania")
        # return render_template("logowanie.html", error=myResponseDictionary['error'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/allMessages")
def allMessages():
    print("przekierowano do allMessages")

    return "test"


if __name__ == '__main__':
    app.run(port=4999, debug=True)
