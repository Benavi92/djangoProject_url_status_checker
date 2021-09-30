console.log("test msg")

let to_not_update = [] // ids
let interval = 1500


function update_table_body(info) {
    let main_table = document.querySelector("#main_table")
    console.log(info)
    for (data_row of info.to_update){
        row = main_table.querySelector(`#row_${data_row.pk}`)
        col_status_code = row.querySelector(".col_status_code")
        col_status_code.innerHTML = data_row.status_code
        if (data_row.status_code != 200){
            row.style.background = "red"
        }
    }
};

function request_to_server(e){
    console.log(to_not_update)
        $.ajax({
            type: "POST",
            url: '/check_all/',
            data: JSON.stringify({to_not_update: to_not_update}),
            dataType: "json",
            success: function (response) {
                update_table_body(response)
                setTimeout(request_to_server, interval)
            }
        });

};


function change_status(num){
    if (to_not_update.includes(num)) {
        button = document.querySelector(`#button_${num}`)
        button.textContent = "Pause"
        let index = to_not_update.indexOf(num)
        if (index > -1){
            to_not_update.splice(index, 1)
        }
    }
    else {
        button = document.querySelector(`#button_${num}`)
        button.textContent = "Start"
        to_not_update.push(num)
    }

}

$(document).ready(function(){
    setTimeout(request_to_server, interval);

});