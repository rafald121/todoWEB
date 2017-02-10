
/**
 * Created by Rafaello on 2017-01-19.
 */

window.onload = function () {

     var createNewTaskBtn = document.getElementById("addNewTask");
    createNewTaskBtn.addEventListener('click', createNewTaskFunction, false);

    var showAllTasksBtn = document.getElementById("listOfAllTasks");
    showAllTasksBtn.addEventListener('click',listOfAllTasksFunction, false);

    var showDoneTasksBtn = document.getElementById("doneTasks");
    showDoneTasksBtn.addEventListener('click', listOfDoneTasksFunction, false);

    var showUndoneTasksBtn = document.getElementById("undoneTasks");
    showUndoneTasksBtn.addEventListener('click', listOfUndoneTasksFunction, false);

    $("#mainPane").on('click', ".task-link", goToTaskContentFunction);

    $(".leftPane").on('click', ".taskListByTag", getListByTagFunction);

    $("section").on('click', ".deleteButton", deleteTaskFunction);

    $("section").on('click', ".editButton", showEditTaskForm);

    $("#mainPane").on('click', "#newTaskConfirm", showListAfterAddTask);


};
function listOfUndoneTasksFunction() {

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/getListByTag/undone",
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })
}

function listOfDoneTasksFunction() {
    alert("done tasks clicked")

     $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/getListByTag/done",
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })
}

function showListAfterAddTask() {


    $.ajax({
        type:"POST",
        url:"http://127.0.0.1:4999/addTask",
        dataType: "text",
        success: function (response) {

            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;

        }
    })

}

// $('section').on('click', '.editNote', function () {
//
//     var taskID = jQuery(this).attr("id");
//     alert(taskID);
//     $.ajax({
//         type: "PUT",
//         url: "http://127.0.0.1:4999/clickEdit/" + taskID.toString(),
//         contentType: 'application/json',
//         data: JSON.stringify({
//             title: $('#taskContentTitle').val(),
//             details: $('#taskContentDetails').val(),
//             timeToDo: $('#taskContentTimeToDo').val(),
//             tag: $('#taskContentTag').val()
//         }).done(function (reply) {
//             $('section').html(reply)
//         })
//     })
//
// })

function showEditTaskForm() {

    var taskID = jQuery(this).attr("id");
    alert(taskID.toString());
    $.ajax({
        type: "PUT",
        url: "http://127.0.0.1:4999/editForm/" + taskID.toString(),
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })
}




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

function goToTaskContentFunction() {

    var taskID = $(this).attr("id");

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/taskContent/" + taskID.toString(),
        dataType: "text",

        success: function (response) {

            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response

        }
    })

}

function getListByTagFunction() {

    var tag = $(this).attr("id");

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:4999/getListByTag/" + tag.toString(),
        dataType: "text",

        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response

        }
    })
}

function deleteTaskFunction(){

    var taskID = $(this).attr("id");

    $.ajax({
        type: "DELETE",
        url: "http://127.0.0.1:4999/deleteTask/" + taskID.toString(),
        dataType: "text",

        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response

        }
    })
}

function editTaskFunction(){

    var taskID = $(this).attr("id");

    $.ajax({
        type: "PUT",
        url: "http://127.0.0.1:4999/editTask/" + taskID.toString(),
        dataType: "text",

        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response

        }
    })
}