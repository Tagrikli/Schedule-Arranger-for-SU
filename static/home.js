
var selected_courses = [];


$(document).ready(() => {


    $("#reset").click(elem=>{

        selected_courses = [];
        updateSelectedList();
        $("#results").empty();

    });


    $("#courses_select").on('change',(item)=>{

        let text = $("#courses_select option:selected").text();
        if (!selected_courses.includes(text))
            {
                selected_courses.push(text);
                updateSelectedList();
            }
        
    })

    $.ajax({
        url: "/api/v1/courseCodes", success: function (result) {
            
            result.codes.forEach(element => {
                $("#courses_select").append(`<option name=${element.replace(/\s+/g, '')}>${element}</option>`)
            });

        }
    });



});

function updateSelectedList(){

    $("#selected_courses").empty();

    selected_courses.forEach(item =>{

        let kiki = $(`<span>${item} </span>`); 
        $("#selected_courses").append(kiki);
        

    });

}

function requestMatch(){

    let text = selected_courses.join(";");
    console.log(text);

    $.ajax({
        url: `/api/v1/matchRequest/${text}&0`, success: function (res) {
            
            let konk = JSON.parse(res)
            konk.result.forEach(element => {
                $("#results").append(`<h3>${element.su.join(",")}</h3>`)
            });

        }
    });


}