$(document).ready(function() {
        $("a.dropCC").bind("click", dropCC); 
        $("form#addCC").bind("submit", addCC); 
        $('#problem_type_clicker')[0].compactor.setState(0);
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

    errorl = $('div#cc_box > div.block_if_js > ul.errorl')[0];

    $.ajax({
        'url': "modIssue/",
        'data': { 
                'action'    : 'dropcc',
                'user'      : user_id, 
                'js'        : 1
            },
        'error': function (req, err, e) {
                errorl.addErr("Was unable to remove user from CC list.");
            },
        'success': function (data) {
                // delete the object
                $(item).parent().remove()
                reloadHistory();
            },
    });
}

/**
 * Takes an event, stops default action. Request sent to create a new CC relation, if
 * succesful, will append item to CC list on user side, otherwise appends some errors to
 * local errorl.
 *
 * @param event     The event that triggered addCC
 */
function addCC(event) {
    event.preventDefault();
    btn = event.target;
    user = $("input#addCC_user")[0].value;
    
    findRes = $("ul#cc_list > li > span").filter( 
        function () { return this.innerHTML == user; } );


    errorl = $('div#cc_box > div.block_if_js > ul.errorl')[0];

    if (findRes.length > 0) {
        errorl.addErr("User already in CC list");
        return false;
    }

    $.ajax({
        'url':'modIssue/',
        'data': {
                'action'    : 'addcc',
                'user'      : user,
                'js'        : 1
            },
        'error': function (req, err, e) {
                errorl.addErr("'" + user + "' could not be added to CC list. Please make sure '" + user + "' exists.");
            },
        'success': function (data) {
                reloadCcList();

                // reload the history
                reloadHistory();
            },
    });
}

// TODO updateHistory, only retrieve stuff we don't have
function updateHistory(last) {
}

/**
 * Reloads the history, deletes everything in the history_box and requests a new one from
 * server
 */
function reloadHistory() {
    $('#history_box').empty();
    $.ajax({
        'url'       : 'fetch/',
        'dataType'  : 'text',
        'data'      : {
                'format'    : 'html',
                'req'       : 'history'
            },
        'success'   : function (text) {
                $('#history_box').append(text);
            }
    });
}

/**
 * Reload the CC list, removes everything and request a new box from server
 */
function reloadCcList() {
    $('#cc_box').empty();
    $.ajax({
        'url'       : 'fetch/',
        'dataType'  : 'text',
        'data'      : {
                'req'       : 'cclist'
            },
        'success'   : function (text) {
                var cc_box = $('#cc_box').html(text);
                initializeJavascript(cc_box);
                $('.dropCC').bind('click', dropCC);
            }
    });
}