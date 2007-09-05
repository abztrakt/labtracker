$(document).ready(function() {
        $("a.dropCC").bind("click", dropCC); 
        $("form#addCC").bind("submit", addCC); 
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
    errorl.reset();

    $.ajax({
        'dataType':'json',
        'url': "modIssue/",
        'type': 'POST',
        'data': { 
                'action': 'dropcc',
                'user': user_id, 
            },
        'error': function (req, err, e) {
                // TODO will need to append some error messages somewhere
                errorl.addErr("Was unable to remove user from CC list.");
            },
        'success': function (data) {
                // delete the object
                $(item).parent().remove()
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
    errorl.reset();
    if (findRes.length > 0) {
        console.log("Found dupes, will not submit");
        errorl.addErr("User already in CC list");
        return false;
    }
    console.log(findRes.length);
    console.log("in addCC");

    $.ajax({
        'dataType':'json',
        'url':'modIssue/',
        'type': 'POST',
        'data': {
                'action': 'addcc',
                'user': user,
            },
        'error': function (req, err, e) {
                errorl.addErr("Could not add user to CC list, does user exist?");
            },
        'success': function (data) {
                var btn = $(rmCCLink(data['userid'], data.username)).bind("click", dropCC);
                var li = $("<li></li>").append(btn).append(" ").append("<span>" + 
                    data['username'] + "</span>");
                $("ul#cc_list").append(li);
            },
    });
}

/**
 * Creates the the html for rm link
 */
function rmCCLink(userid, username) {
    return '<a id="cc_' + userid + '" class="dropCC" title="Remove ' + username + 
        ' from CC" href="#">x</a>';
}
