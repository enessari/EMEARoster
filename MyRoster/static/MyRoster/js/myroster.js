
// Main function that calls all the above function to start create / load the table.
function load_myroster() {
    $.ajax({
        url: getBaseUrl() + 'myroster_rows' + '/',
        type: "GET",
        success: function(response) {

            if (response.length == 0 ) {
                $('#myroster-table').remove();
                var tableSkeletion = '<div id="myroster-table"><table id="myroster" class="">' +
                    '<tbody>' +
                    '<td> You are not scheduled for any week this year </td>'
                    '</tbody>' +
                    '</table>'
                $('#myroster-div').append(tableSkeletion);
            } else {
                // Remove any table if exists and generate a new one
                $('#myroster-table').remove();
                var tableSkeletion = '<div id="myroster-table"><table id="myroster" class="table table-hover cell-border">' +
                    '<thead class="">' +
                    '<th>ID</th>' +
                    '<th>Scheduled Dates</th>' +
                    '</thead>' +
                    '<tbody>' +
                    '</tbody>' +
                    '</table>'
                $('#myroster-div').append(tableSkeletion);

                // Rows
                var rowTemplate
                var increment = 1
                $.each(response, function(id, date){
                    rowTemplate = '<tr><td>'+ increment + '</td>' + '<td>'+ date + '</td></tr>'
                    $('#myroster tbody').append(rowTemplate);
                    increment = increment + 1
                })
            }
        }
    })

}

$('#myroster_link').on('click', function(){
    load_myroster()
    $('#MyRosterModal').modal('show')
})