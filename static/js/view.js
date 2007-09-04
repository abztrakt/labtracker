$(document).ready(function() {
        $("form#update_cc")[0].style.display = "none";
        $("#cc_list")[0].style.display = "block";

        $("a.dropCC").bind("click", dropCC); 
    }
);

/**
 * Takes an event, stops the default action, and then drops the given cc user from the
 * list, and then removes that from the list
 *
 * @param event     The event that triggered dropCC
 */
function dropCC(event) {
    event.preventDefault();
    item = event.target;

    user_id = item.id.match(/^cc_(\d+)$/)[1];

    $.ajax({
        'datatype':'json',
        'url': "modIssue/",
        'type': 'POST',
        'data': { 
                'action': 'dropcc',
                'user': user_id, 
            },
        'error': function (req, err, e) {
                // TODO will need to append some error messages somewhere
            },
        'success': function (data) {
                // delete the object
                $(item).parent().remove()
            },
    });
}
