// Show modifying rows.
$('#edit_button').on('click', function(){
    // Disable all the error message if its turned on
    $('#avail_missing').css('display', 'none')
    $('#comment_missing').css('display', 'none')

    // Removed modifying rows exists then remove
    if ( $("#modifying_rows_table").length ) {
         $("#modifying_rows_table").remove()
    }

    // Show all the modifying rows to the user
    tableTemplate = '<table class="table table-hover" id="modifying_rows_table">' +
                    '   <thead style="background: #283e4a;color: white;">'+
                    '       <tr>' +
                    '        <th><b>ID</b></th>' +
                    '        <th><b>Engineer</b></th>' +
                    '        <th><b>Date</b></th>'+
                    '        <th><b>Action</b></th>'+
                    '       </tr>'+
                    '</thead>'+
                    '<tbody></tbody>'+
                    '</table>'
    $('#modifying_rows').append(tableTemplate)
    incrementor = 1
    $.each(all_selected, function(id, select) {
        modifying_rows = select.split("|")
        var modifying_engineer = modifying_rows[0];
        var modifying_mdate = modifying_rows[1];
        modifying_tableTemplate =  '<tr>' +
                                        '<td>'+ incrementor +'</td>' +
                                        '<td>'+ modifying_engineer +'</td>' +
                                        '<td>'+ modifying_mdate +'</td>' +
                                        '<td><i onclick="remove_edit_row(this, \''+ modifying_engineer +'\',\''+ modifying_mdate +'\')" class="fa fa-close a-pointer" aria-hidden="true"></i></td>' +
                                   '</tr>'
        incrementor = incrementor + 1
        $('#modifying_rows_table tbody').append(modifying_tableTemplate)
    });
})


// Remove rows from the edit window
function remove_edit_row(this_row, engineer, date) {

    // Select the engineer from the array and the parent tr
    selected_cell = engineer + '|' + date
    var idx = $.inArray(selected_cell, all_selected);
    var parent_td = $(this_row).parent().parent()

    // Remove them from the specified list and remove the selection class
    $("td[data-date='" + date + "'][data-engineer='" + engineer + "']").removeClass('select')
    parent_td.remove();
    all_selected.splice(idx, 1);

    // If user removes the last entry on the edit cell,
    // then close the modal and the button
    if ($(all_selected).length == 0) {
          $('#EditCellModal').modal('hide')
          td_selected_class()
    }

}

// Obtain all the cells with the selected class and return their values.
function form_values() {
    var selectedIDs = []
    $.each(all_selected, function(id, select){
        selector = select.split("|")
        var engineer = selector[0];
        var mdate = selector[1];
        attr = {
            "engineer": engineer,
            "date": mdate,
        }
        selectedIDs.push(attr);
    })
    return {
        "key": selectedIDs,
    }
}

// Update database
function update_database(this_id, data) {
    $.ajax({
        url: getBaseUrl() + 'update_rows' + '/',
        type: "POST",
        data: data,
        success: function(response) {
            if (response == 'success') {

                // Close the edit cell modal
                $('#EditCellModal').modal('hide');

                // Send success information
                $('#success-icon').html('<i class="fa fa-check" aria-hidden="true"></i>')
                $('#success_title').html("SUCCESS")
                $('#success_message').html("The requested changes or modification has been successfully committed to the database...")
                $('#success_modal').modal();

                // Get the modified rows and repaint it
                data = JSON.parse(data)
                $.each(data.key, function(id, value) {
                    if (this_id == "yes") {
                        $("td[data-engineer='" + value.engineer + "'][data-date='" + value.date + "']").addClass('td-blue')
                    } else {
                        $("td[data-engineer='" + value.engineer + "'][data-date='" + value.date + "']").removeClass('td-blue')
                    }

                })

                // Deselect the cells
                td_selected_class();

                // After a second turn of the success notification
                setTimeout(function() {
                    $('#success_modal').modal('hide');
                }, 2000)

            } else {
                $('#success_modal').modal('hide')
                $('#error_message').html("Error received from the database (error below), please contact Roster Admins....")
                $('#suberror_message').html(response)
                $('#error_modal').modal();
            }
        },
        error: function() {
            $('#success_modal').modal('hide')
            $('#error_message').html("Cannot connect to the database or failure to send ajax request, please try again or contact Roster Admins....")
            $('#error_modal').modal();
        }
    });

}

// Edit Yes
$('#edit_yes').on('click', function() {
    var data = form_values();
    data['what_to_do'] = "update"
    data = JSON.stringify(data)
    update_database("yes", data)
});

// Edit No
$('#edit_no').on('click', function() {
    var data = form_values();
    data['what_to_do'] = "delete"
    data = JSON.stringify(data)
    update_database("no", data)
});

