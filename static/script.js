/**
 * Created by Rafaello on 2017-01-19.
 */

window.onload = function () {

    var showAllTasksBtn = document.getElementById("listOfAllTasks");
    showAllTasksBtn.addEventListener('click',listOfAllTasksFunction, false);

    var createNewTaskBtn = document.getElementById("addNewTask");
    createNewTaskBtn.addEventListener('click', createNewTaskFunction, false);


};

function listOfAllTasksFunction() {

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/tasks",
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })
}


function createNewTaskFunction() {


    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/createTask",
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })
}