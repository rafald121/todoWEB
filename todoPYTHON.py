# -*- coding: utf-8 -*-
from urllib2 import HTTPError, Request, urlopen
from flask import Flask, session, render_template, redirect, request, json
from flask import url_for

app = Flask(__name__)
app.secret_key="fwgjebhuih4"

# TODO czemu nie dziala gdy daje metode POST
@app.route('/')
def hello_world():
    print("3")

    login = 'rafal'
    password = 'rafal'

    data = {
        "login": login,
        "password": password
    }

    headers = {
        'Content-Type': 'application/json'
    }

    print("5")
    jsonData = json.dumps(data)
    print("jsonData: " + jsonData)

    url = "http://127.0.0.1:5000/login"
    print("url: " + url)
    myRequest = Request(url, data=jsonData, headers=headers)
    # TODO co to daje \/
    # myRequest.get_method = lambda: 'POST'

    try:
        print("a tutaj")
        myResponse = urlopen(myRequest)

        print("a tutaj1")
        myResponseDictionary = json.load(myResponse)
        session['token'] = myResponseDictionary['token']
        session['user_name'] = login

        print ("mój token to : ")
        print session['token']

        return redirect(url_for('allMessages'))

    except HTTPError as e:
        print e.code
        print e.reason
        return e.read()


@app.route("/allMessages")
def allMessages():

    print("przekierowano do allMessages")
    return "test"


if __name__ == '__main__':
    app.run(port=4999, debug=True)
