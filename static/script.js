/**
 * Created by Rafaello on 2017-01-19.
 */

window.onload = function () {

    var showAllTasksBtn = document.getElementById("listOfAllTasks");
    showAllNewMessagesBtn.addEventListener('click',listOfAllTasksFunction, false);

};

function listOfAllTasksFunction() {

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/listOfUsers",
        dataType: "text",
        success: function (response) {
            var currSection = document.getElementById("mainPane");
            currSection.innerHTML = response;
        }
    })

}