// Close DatePicker modal when clicked on the second input box
$('#FromDatePicker').on('click', function() {
    $('#ToDatePicker').datepicker("hide");
});
$('#ToDatePicker').on('click', function() {
    $('#FromDatePicker').datepicker("hide");
});

// Close DatePicker after the date is selected
$('.datepicker').on('changeDate', function(ev) {
    $(this).datepicker('hide');
});

// Get the scroll size
function scroll_size() {
    var windowHeight = $(window).height();
    var otherHeight = 160.5;
    var tableHeight = windowHeight - otherHeight - 1;
    return tableHeight
}

// Get audits and apply them.
function apply_audits(data) {
    $.ajax({
        url: getBaseUrl() + 'audit_rows' + '/',
        type: "POST",
        data: data,
        dataType: "json",
        success: function(response) {
               for ( var i in response ) {
                    $("td[data-engineer='" + response[i].engg + "'][data-date='" + response[i].date + "']").addClass('td-blue')
               }
        }
    });
}

// Main function that calls all the above function to start create / load the table.
function load_table(method, data) {
    $.ajax({
        url: getBaseUrl() + 'get_rows' + '/',
        type: method,
        data: data,
        dataType: "json",
        success: function(response) {

            // Update dates
            $('#change_dates').html(response.from_date + '-' + response.to_date)
            $('input[name="FromDatePicker"]').val(response.from_date);
            $('input[name="ToDatePicker"]').val(response.to_date);

            // Remove any table if exists and generate a new one
            $('#roster-table').remove();
            var tableSkeletion = '<div id="roster-table"><table id="roster" class="table table-hover cell-border">' +
                '<thead class="">' +
                '<th></th>' +
                '</thead>' +
                '<tbody>' +
                '</tbody>' +
                '</table>'
            $('#roster-div').append(tableSkeletion);

            // Header
            $.each(response.headers, function(id, col){
                var headerTemplate = '<th style="cursor: pointer;">' + col.slice(0, 3) + "&nbsp;" + parseInt(col.slice(10, 12), 10) + "/" + parseInt(col.slice(13, 15), 10) + '</th>';
                $('#roster thead tr').append(headerTemplate);
            })

            // Rows
            $.each(response.users, function(id, user){

                td_prefix = '<tr><td>' + user + '</td>'
                td_value = ""
                for (var i in response.headers) {
                    var weekend = response.headers[i].slice(0, 3);
                    if (weekend == "Sat" || weekend == "Sun") {
                        td_value = td_value + '<td class="td-grey" data-engineer="'+ user +'" data-date="'+ response.headers[i].slice(5, 15) +'"></td>'
                    } else {
                        td_value = td_value + '<td data-engineer="'+ user +'" data-date="'+ response.headers[i].slice(5, 15) +'"></td>'
                    }

                }
                td_suffix = '</tr>'

                $('#roster tbody').append(td_prefix + td_value + td_suffix);

            })

            // Create DataTable
            $('#roster').DataTable({
                scrollX: true,
                scrollY: scroll_size(),
                paging: false,
                ordering: false,
                bInfo: false,
                searching: false,
                scrollCollapse: true,
                "columnDefs": [{
                    "width": 150,
                    "height": 1,
                    "targets": 0
                }],
                fixedColumns: true,
            });

            // Highlight the column with today's date
            $("td[data-date='" + response.today_date + "']").addClass('todays-heading-border');

            // Apply audits
            data = {
                "from_date": response.from_date,
                "to_date": response.to_date
            }
            apply_audits(data)

            // Enable click and drag functionality ...
            td_selected();
        }
    })

}


// Shuffle generator
var volunteer_state
function load_shuffle_rows(data) {
    $.ajax({
        url: getBaseUrl() + 'shuffle_rows' + '/',
        type: "POST",
        data: data,
        dataType: "json",
        success: function(response) {

            // If the reshuffle again button is clicked then reset the volunteer variable
            volunteer_state = ""

            // Removed shuffled rows if exists then remove
            if ( $("#shuffled_rows_table").length ) {
                 $("#shuffled_rows_table").remove()
            }

            // Show all the modifying rows to the user
            tableTemplate = '<table class="table table-hover" id="shuffled_rows_table">' +
                 '   <thead style="background: #283e4a;color: white;">'+
                 '       <tr>' +
                 '        <th><b>ID</b></th>' +
                 '        <th><b>Volunteer</b></th>' +
                 '        <th><b>Date</b></th>'+
                 '       </tr>'+
                 '  </thead>'+
                 '  <tbody></tbody>'+
                 '</table>'
            $('#shuffled_rows').append(tableTemplate)

            // Load to the table
            incrementor = 1
            $.each(response, function(date, user) {
                shuffle_tableTemplate =  '<tr>' +
                                                '<td>'+ incrementor +'</td>' +
                                                '<td>'+ user +'</td>' +
                                                '<td>'+ date +'</td>' +
                                           '</tr>'
                incrementor = incrementor + 1
                $('#shuffled_rows_table tbody').append(shuffle_tableTemplate)
            });

            // open shuffle modal
            if ($('#ShuffleModal').is(':hidden')) {
                $('#ShuffleModal').modal('show');
            }

            // Save the state, if user accept the shuffle.
            volunteer_state = response

        }

    });
}

// Delete scheduler from selected range
function delete_picked_dates(data) {
    $.ajax({
        url: getBaseUrl() + 'delete_date_rows' + '/',
        type: "POST",
        data: data,
        dataType: "json",
        success: function(response) {
               for ( var i in response ) {
                    $("td[data-engineer='" + response[i].engg + "'][data-date='" + response[i].date + "']").removeClass('td-blue')
               }
        }
    });
}

// Time difference calculator
function getDateDiff(date1, date2, interval) {
    var second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24,
        week = day * 7;
    date1 = new Date(date1).getTime();
    date2 = (date2 == 'now') ? new Date().getTime() : new Date(date2).getTime();
    var timediff = date2 - date1;
    if (isNaN(timediff)) return NaN;
    switch (interval) {
        case "years":
            return date2.getFullYear() - date1.getFullYear();
        case "months":
            return ((date2.getFullYear() * 12 + date2.getMonth()) - (date1.getFullYear() * 12 + date1.getMonth()));
        case "weeks":
            return Math.floor(timediff / week);
        case "days":
            return Math.floor(timediff / day);
        case "hours":
            return Math.floor(timediff / hour);
        case "minutes":
            return Math.floor(timediff / minute);
        case "seconds":
            return Math.floor(timediff / second);
        default:
            return undefined;
    }
}

// New dates loader
function load_new_dates(new_from_date, new_end_date) {
    var date_diff = getDateDiff(new_from_date, new_end_date, 'days');
    if ($('#ChangeDateModal').is(':visible')) {
        $('#ChangeDateModal').modal('hide');
    }
    if (date_diff < 0) {
        $('#error_message').html("From date is greater that to date, please correct it and try again...");
        $('#error_modal').modal();
    } else if (date_diff > 730) {
        $('#error_message').html("Roster has a cap of two years, please narrow your search to two years(730 days)...");
        $('#error_modal').modal();
    } else if (date_diff < 20) {
        $('#error_message').html("Roster needs a minimum of 20 days to display the data properly, please choose dates with 20 days difference");
        $('#error_modal').modal();
    } else {
        td_selected_class()
        return {
            "from_date": new_from_date,
            "to_date": new_end_date,
        }
    }
}


// Datepicker date selector
function data_picked(bywhom) {
    var from_date = $('input[name="FromDatePicker"]').val();
    var to_date = $('input[name="ToDatePicker"]').val();
    data = load_new_dates(from_date, to_date)
    if (typeof data != 'undefined') {
        if (bywhom == "change_dates") {
            load_table("POST", data);
        } else if ( bywhom == "shuffle") {
            global_data = data
            load_shuffle_rows(data)
        } else if ( bywhom == "delete") {
            global_data = data
            delete_picked_dates(data)
        }
    }

}

// When Shuffle again button is clicked.
$('#shuffle_again').on('click', function() {
    data_picked("shuffle")
});


// Repaint Grid
function repaint_grid(data) {
    $.each(data, function(date, engg) {
        $("td[data-engineer='" + engg + "'][data-date='" + date + "']").addClass('td-blue')
    })
}

// When shuffle save state is clicked.
$('#shuffle_save').on('click', function() {
    $.ajax({
        url: getBaseUrl() + 'shuffle_save' + '/',
        type: "POST",
        data: volunteer_state,
        success: function(response) {
            if (response == 'success') {
                repaint_grid(volunteer_state)
            }
        }
    });
});

// When Shuffle button is clicked.
$('#shuffle_dates').on('click', function() {
    $('#search_dates').html('<i class="fa fa-random icon-placement" aria-hidden="true"></i>Shuffle')
    $('#search_dates').attr('onclick','data_picked("shuffle")');
    $('#ChangeDateModal').modal('show')
});

// When Date button is clicked
$('#change_dates').on('click', function() {
    $('#search_dates').html('<i class="fa fa-refresh icon-placement" aria-hidden="true"></i>Reload');
    $('#search_dates').attr('onclick','data_picked("change_dates")');
    $('#ChangeDateModal').modal('show')
});

// When delete button is clicked.
$('#delete_dates').on('click', function() {
    $('#search_dates').html('<i class="fa fa-eraser icon-placement" aria-hidden="true"></i>Delete')
    $('#search_dates').attr('onclick','data_picked("delete")');
    $('#ChangeDateModal').modal('show')
});
