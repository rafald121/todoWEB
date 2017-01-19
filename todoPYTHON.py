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
@app.route('/main', methods=['GET'])
def main():
    if 'token' in session:

        headers = {'token': session['token']}
        myRequest = Request("http://127.0.0.1:5000/notdone", headers=headers)

        try:
            responseJson = urlopen(myRequest)
            responseJsonData = json.load(responseJson)

            if responseJson.getcode()==200:
                undoneQuantity = responseJsonData['undone']
            else:
                responseJsonData = {"error": "response code is not 200"}

            return render_template("mainPage.html", login = session['login'], undoneQuantity=undoneQuantity)

        except HTTPError as e:
            print(e.code)
            print(e.message)
            return json.load(e)['error']

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

            # TODO redirect to todoList
            return redirect(url_for('main'))
        else:
            return render_template("logowanie.html", error = True, errorMessage = "sprawdzic jesli wyskoczy ten komunikat")

    except HTTPError as e:
        print e.code
        print e.reason
        # TODO sprawic, aby errorMessage zwracalo blad z API
        return render_template("logowanie.html", error=True, errorMessage=json.load(e)['error'])
        # return render_template("logowanie.html", error=myResponseDictionary['error'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/tasks", methods=['GET'])
def tasks():
    print("in tasks")
    print(session['token'])
    if 'token' in session:

        headers = {
            'token': session['token']
        }

        myRequest = Request("http://127.0.0.1:5000/tasks", headers=headers)
        myRequest.get_method = lambda: 'GET'

        try:
            myResponse = urlopen(myRequest)
            tasksData = json.load(myResponse)

            titleList = []
            detailsList = []

            for singleTask in tasksData:
                titleList.append(singleTask['title'])
                detailsList.append(singleTask['details'])

            print(titleList)
            print(detailsList)
        except HTTPError as e:
            print(e.code)
            print(e.message)
            return json.load(e)['error']

    else:
        return redirect(url_for('login'))

    # TODO RETURN RENDER TEMPLATE LIST OF MESEDŻ
    return redirect(url_for('main'))

@app.route("/allMessages")
def allMessages():

    print("przekierowano do allMessages")

    return "test"


if __name__ == '__main__':
    app.run(port=4999, debug=True)
