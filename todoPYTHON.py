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

            if responseJson.getcode() == 200:
                undoneQuantity = responseJsonData['undone']
            else:
                responseJsonData = {"error": "response code is not 200"}

            return render_template("mainPage.html", login=session['login'], undoneQuantity=undoneQuantity)

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
            return render_template("logowanie.html", error=True, errorMessage="sprawdzic jesli wyskoczy ten komunikat")

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


# WYSWIETLA FORMULARZ DO TWORZENIA NOWEGO ZADANIA
@app.route("/createTask")
def createTask():
    if 'token' in session:
        return render_template("newTask.html")
    else:
        return redirect(url_for('login'))


# DODAJE NOWE ZADANIE DO API
@app.route("/addTask", methods=['POST'])
def addTask():
    print("addTask1")
    if request.form['tag'] != "":
        tag = request.form['tag']
    else:
        tag = "other"

    print("addTask2")

    title = request.form['newTaskTitle']
    details = request.form['newTaskDetails']
    timeToDo = request.form['newTaskTimeToDo']
    print(title, details, timeToDo)
    if (timeToDo == ""):
        print ("CO JEST!!!!")
    if title == "" or details == "" or timeToDo == "":
        print("ktores z pol jest puste!!!")
        return "MUSISZ UZUPELNIC POLA "

    data = {
        "title": title,
        "details": details,
        "timeToDo": timeToDo,
        "tag": tag
    }

    print(data)
    dataJson = json.dumps(data)
    print("tag: ")
    print(data['tag'])

    headers = {
        "token": session['token'],
        "Content-Type": "application/json"
    }

    myRequest = Request("http://127.0.0.1:5000/tasks", headers=headers, data=dataJson)
    myRequest.get_method = lambda: "POST"
    try:
        print("1")
        myResponse = urlopen(myRequest)
        print("2")
        myResponseData = json.load(myResponse)
        # TODO dopisac warunek if info = OK \/
        print("3")
        if myResponse.getcode() == 201:
            print("udalo sie dodac zadanie")
            print(myResponseData)
            return redirect(url_for('main'))
        else:
            return myResponseData['error']

    except HTTPError as e:
        print(e.code)
        print(e.message)
        return json.load(e)['error']


def getListOfTasks():
    if 'token' in session:

        headers = {
            'token': session['token']
        }

        myRequest = Request("http://127.0.0.1:5000/tasks", headers=headers)
        myRequest.get_method = lambda: 'GET'

        try:
            myResponse = urlopen(myRequest)
            tasksData = json.load(myResponse)

            listOfTask = tasksData
            print (listOfTask)

            return listOfTask

        except HTTPError as e:
            print(e.code)
            print(e.message)
            return json.load(e)

    else:
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
            print("1111bug error: ")
            print (myResponse.getcode())
            tasksData = json.load(myResponse)
            print("2222bug error: ")
            print (myResponse.getcode())
            listOfTask = tasksData
            print (listOfTask)

            return render_template("taskList.html", taskList=listOfTask)

        except HTTPError as e:
            print("code ")
            print(e.code)

            print("message ")
            print(e.message)
            print("haloookurde")
            return json.load(e)['error']

    else:
        return redirect(url_for('login'))


@app.route("/taskContent/" + "<id>", methods=['GET'])
def taskContent(id):
    print("1")
    if 'token' in session:

        task = getTask(id)
        if task is None:
            return "nie pobrano zadania z funkcji getTask(id)"
        else:
            print("pobrano zadania z funkcji getTask(id) i renderuje task_content")

            return render_template("taskContent.html", task=task)

    else:
        return redirect(url_for("login"))


def getTask(id):
    headers = {
        "token": session['token'],
        "Content-Type": "application/json"
    }

    myRequest = Request("http://127.0.0.1:5000/tasks/" + str(id), headers=headers)
    myRequest.get_method = lambda: 'GET'
    try:
        print("response?")
        response = urlopen(myRequest)
        print("response!")
        responseData = json.load(response)

        if response.getcode() == 200:
            task = responseData
            print(task)
            return task
        else:
            return "kod odpowiediz inny niż 200"
    except HTTPError as e:
        print(e.code)
        print(e.message)
        return json.load(e)['error']



@app.route("/updateTask/" + "<id>", methods=['PUT'])
def updateTask(id):
    print("przekierowuje?")
    if 'token' in session:
        print("hmm?")

        task = getTask(id)

        print task
        # headers = {
        #     'Content-Type': 'application/json',
        #     'token': session['token']
        # }

        # return render_template("updateTask.html", tasks=)


    else:
        return redirect(url_for("login"))


# @app.route("/updateTask/" + "<id>", methods=['PUT'])
# def updateTask(id):
#     print("dziala editask nr:. " + str(id))
#     if 'token' in session:
#
#         # data = json.loads(request.data)
#
#         data = request.data
#
#         # values = {
#         #     'title': data['title'],
#         #     'details': data['details'],
#         #     'timeToDo': data['timeToDo'],
#         #     'tag': data['tag']
#         # }
#         # taskToEdit =
#
#         print data
#
#         headers = {
#             "token": session['token'],
#             "Content-Type": "application/json"
#         }
#
#         myRequest = Request("http://127.0.0.1:5000/tasks/" + str(id), headers=headers)
#         myRequest.get_method = lambda: 'PUT'
#         print ("http://127.0.0.1:5000/tasks/" + str(id))
#
#         try:
#             myResponse = urlopen(myRequest)
#             print("111")
#             myResponseData = json.load(myResponse)
#             print("222")
#             listOfTask = myResponseData
#             print listOfTask
#             print(myResponse.getcode())
#             if myResponse.getcode() == 200:
#                 print "po ifie"
#                 return render_template("taskList.html", taskList=listOfTask)
#             else:
#                 return "ZLY KOD GETCODE"
#         except HTTPError as e:
#             print(e.code)
#             print(e.message)
#             return json.load(e)['error']
#     else:
#         return redirect(url_for("login"))


@app.route("/deleteTask/" + "<id>", methods=['DELETE'])
def deleteTask(id):
    print("tukej")
    if 'token' in session:

        headers = {
            "token": session['token'],
            "Content-Type": "application/json"
        }

        myRequest = Request("http://127.0.0.1:5000/tasks/" + str(id), headers=headers)
        myRequest.get_method = lambda: 'DELETE'
        print ("http://127.0.0.1:5000/tasks/" + str(id))

        try:
            myResponse = urlopen(myRequest)
            print("111")
            myResponseData = json.load(myResponse)
            print("222")
            deletedTask = myResponseData

            if myResponse.getcode() == 200:
                print(myResponse.getcode())

                listOfTask = getListOfTasks()
                return render_template("taskList.html", taskList=listOfTask)
            else:
                return "ZLY KOD GETCODE"
        except HTTPError as e:
            print(e.code)
            print(e.message)
            return json.load(e)['error']


    else:
        return redirect(url_for("login"))


@app.route("/getListByTag/" + "<tag>", methods=['GET'])
def getListByTag(tag):
    if 'token' in session:

        headers = {
            "token": session['token'],
            "Content-Type": "application/json"
        }

        myRequest = Request("http://127.0.0.1:5000/tasks/" + str(tag), headers=headers)
        myRequest.get_method = lambda: 'GET'
        print ("http://127.0.0.1:5000/tasks/" + str(tag))

        try:
            myResponse = urlopen(myRequest)
            print "nie dziala"
            myResponseData = json.load(myResponse)
            print("myresponsedata")
            print(myResponseData)

            if myResponse.getcode() == 200:
                return render_template("taskList.html", taskList=myResponseData)
            else:
                return myResponseData['error']
        except HTTPError as e:
            print(e.code)
            print(e.message)
            return json.load(e)['error']


    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(port=4999, debug=True)
