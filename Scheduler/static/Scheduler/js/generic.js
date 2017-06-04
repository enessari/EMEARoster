// global variable since its used by edit cell and others to know what was selected
var all_selected = []

// What happens when td is clicked and dragged.
function td_selected() {

    $(function() {
        // Initialize the mouse click.
        var isMouseDown = false,
            isHighlighted;

        // When user click and overs around the roster cell.
        $("#roster td")
            .mousedown(function() {
                // If Fab button is disabled, enable it
                if ($('#floating-action-button').hasClass('action_button_disabled')) {
                    $('#floating-action-button').removeClass('action_button_disabled').addClass('bounce')
                }

                // Mouse click is enabled
                isMouseDown = true;

                // Add select class, if its already their then remove the class
                $(this).toggleClass("select");

                // Note down the selected cell.
                selected_cell = $(this).attr('data-engineer') + '|' + $(this).attr('data-date')
                var idx = $.inArray(selected_cell, all_selected);

                // If we never collected it then lets collect it....
                if (idx == -1) {
                    all_selected.push(selected_cell);
                } else { // else lets remove it, if its a second click on the same cell..
                    all_selected.splice(idx, 1);
                }
                isHighlighted = $(this).hasClass("select");

                // Remove the FAB bounce effect after 1.5 seconds
                setTimeout(function() {
                    $('#floating-action-button').removeClass('bounce');
                }, 1500)
                return false; // prevent text selection
            })
            .mouseover(function() {
                // Now when the user over with the mouse..
                if (isMouseDown) {

                    // Add select class, if its already their then remove the class
                    $(this).toggleClass("select", isHighlighted);

                    // Note down the selected cell..
                    selected_cell = $(this).attr('data-engineer') + '|' + $(this).attr('data-date')
                    var idx = $.inArray(selected_cell, all_selected);

                    // If we never collected it then lets collect it, if the cell has a select class.
                    if (idx == -1) {
                        if ($(this).hasClass("select")) {
                            all_selected.push(selected_cell);
                        }
                    } else { // else lets remove it, if its a second click on the same cell and no select cell found.
                        if (!$(this).hasClass("select")) {
                            all_selected.splice(idx, 1);
                        }
                    }
                }
            });

        $(document)
            .mouseup(function() {
                isMouseDown = false;
                // If everything is un-highlighted then remove FAB button.
                if ($(all_selected).length == 0) {
                    td_deselect();
                }
            });
    })

};


// Defining the play when the engineer name is clicked.
function td_deselect(engineer = '', highlight = false) {

    // Disable FAB button if the total td selected is only zero not otherwise.
    if ($(all_selected).length == 0) {
        $('#floating-action-button').addClass('action_button_disabled');
    }

    if (highlight) {
        // If the top eng is the one that is connected, then reduce the bottom border size
        if (engineer == connected_user) {
            $("td[data-engineer='" + connected_user + "']").addClass('connected-user-bottom-border')
        } else { // else remove the class
            $("td[data-engineer='" + connected_user + "']").removeClass('connected-user-bottom-border')
        }

        // Creating top highlight border in current row and bottom highlight border in the next row
        var top_eng_td = $("td[data-engineer='" + engineer + "']");

        // If there is already the cell is highlighted
        if (top_eng_td.hasClass('td-highlight-top')) {

            prev_class_td = top_eng_td.closest('tr').prev().children('td').attr('class')

            // If the cell is closer to the connected user, then remove the class called connected-user-border
            // from the variable so that the if condition matches...
            if (prev_class_td != null   ) {
                if (prev_class_td.indexOf('connected-user-border ') != -1) {
                    prev_class_td = prev_class_td.replace('connected-user-border ', '')
                }
            }
            prev_eng_td = top_eng_td.closest('tr').prev().children('td').attr('data-engineer')

            // Lets check if the previous engineer already has the cell highlighted
            // Yes the are highlighted
            if (prev_class_td == 'td-highlight-top') {

                // Then remove the top cell class and place the class on the bottom
                $("td[data-engineer='" + prev_eng_td + "']").removeClass('td-highlight-top');
                var bottom_eng_name = top_eng_td.parent().next('tr').find("td:first").attr('data-engineer');

                // Don't add any css to the highlighed connected engg row.
                if (bottom_eng_name != connected_user){
                    $("td[data-engineer='" + bottom_eng_name + "']").addClass('td-highlight-top');
                }
            } // No they the top one is not highlighted, user want to deselect it
            else {
                $("td.td-highlight-top").removeClass('td-highlight-top').removeClass('connected-user-bottom-border');
            }
        } // If its a first call
        else {
            // highlight the cell
            $("td.td-highlight-top").removeClass('td-highlight-top');
            top_eng_td.addClass('td-highlight-top');
            var bottom_eng_name = top_eng_td.parent().next('tr').find("td:first").attr('data-engineer');
            var bottom_eng_td = $("td[data-engineer='" + bottom_eng_name + "']")

            // Don't add any type of css to the connected user highlighed cell
            if (bottom_eng_name != connected_user) {
                bottom_eng_td.addClass('td-highlight-top');
            }
        }
    }
}


// If called it will deselect all the cell and close up the action button
function td_selected_class() {

    // Remove all the cell selection..
    $.each(all_selected, function(id, select) {
        selector = select.split("|")
        var engineer = selector[0];
        var mdate = selector[1];
        $("td[data-date='" + mdate + "'][data-engineer='" + engineer + "']").removeClass('select')
    });

    // Reset all the selected value
    all_selected = []

    // Remove FAB button
    $('#floating-action-button').addClass('action_button_disabled');
}


// Action button workplay
$('.fab').on('click', function() {
    $(this).toggleClass('open');
    $('.option').toggleClass('open');
    $('.close').toggleClass('open');
})