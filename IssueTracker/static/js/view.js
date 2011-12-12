$(document).ready(function() {
	$("a.dropCC").bind("click", dropCC); 
	$("#ccForm").bind("submit", addCC); 
	$("#addCC").bind("click", addCC); 
    var list_cc = new Array();
    var cc_nodes = $('#id_cc').children();
    for (var i = 0; i <cc_nodes.length;i++) {
        list_cc.push(cc_nodes[i].innerHTML);
    }
    $('#addCC_user').autocomplete({
        source: list_cc
    });
    option =$('#machineLink');
    issueNum = $('#issueNumber');
    $("#relatedList").load("/issue/" + issueNum[0].innerHTML + "/partial/" + option[0].innerHTML+ "/");
	$("#id_problem_type").asmSelect({
		'removeLabel': 'X',
		'listClass': 'asmList prob-types',
		'listItemClass': 'asmListItem prob-types-item'
	});
});

function addUserToCCList(id, username) {
	var btn = $(rmCCLink(id, username)).bind("click", dropCC);
	var li = $("<li></li>").append(btn).append(" ").append("<span>" + 
			username + "</span>");
	$("ul#cc_list").append(li);
}


/**
 * Takes an event, stops the default action, and then drops the given cc user from the
 * list, and then removes that from the list
 *
 * @param event	 The event that triggered dropCC
function dropCC(event) {
	event.preventDefault();
	item = event.target;

	user_id = item.id.match(/^cc_(\d+)$/)[1];

	errorl = $('div#cc_box > div.block-if-js > ul.errorl')[0];

	$.ajax({
		'url': "modIssue/",
		'type': "POST",
		'data': { 
				'action'	: 'dropcc',
				'user'	  : user_id
			},
		'error': function (req, err, e) {
				errorl.addErr("Was unable to remove user from CC list.");
			},
		'success': function (data) {
				// delete the object
				$(item).parent().remove()
				reloadHistory();
			}
	});
}
*/
/**
 * Takes an event, stops the default action, and then drops the given cc user from the
 * list, and then unselects from the cc box
 *
 * @param event	 The event that triggered dropCC
 */
function dropCC(event) {
	event.preventDefault();
	var item = event.target;

	var user_id = item.id.match(/^cc_(\d+)$/)[1];

	// remove from the list
	$(item).parent().remove();

	// remove from the select
	$('#id_cc').children('option[value='+user_id+']').removeAttr('selected');
}


function addCC(event) {
	event.preventDefault();
	var btn = event.target;

	var input = $("input#addCC_user")
	var user = input[0].value;
	var js_block = $(btn).parent().parent();

	// make sure this user is not bogus
	var errorl = js_block.children('.errorlist')[0];
	var cclist = js_block.children('#cc_list');

	// before doing ajax, check to see if user is already in the list
	findRes = cclist.children().children('span:contains("'+user+'")');

	if (findRes.length > 0) {
		return false;
	}

	// check to see if user exists in the select 
	var option = $('#id_cc').children('option:contains("'+user+'")');

	if (option.length == 1) {
		var id = option.attr('value');
		addUserToCCList(id, user);
		input[0].value = "";

		// Select the user in the cc list
		$('#id_cc').children('option[value='+id+']').attr('selected','selected');
	} else {
		errorl.addErr("Could not add user to CC list, does user exist?");
	}
}


/**
 * Takes an event, stops default action. Request sent to create a new CC 
 * relation, if succesful, will append item to CC list on user side, otherwise
 * appends some errors to local errorl.
 *
 * @param event	 The event that triggered addCC
function addCC(event) {
	event.preventDefault();
	btn = event.target;
	user = $("input#addCC_user")[0].value;
	
	findRes = $("ul#cc_list > li > span").filter( 
		function () { return this.innerHTML == user; } );


	errorl = $('div#cc_box > div.block-if-js > ul.errorl')[0];

	if (findRes.length > 0) {
		errorl.addErr("User already in CC list");
		return false;
	}

    //	console.log("in addCC");

	$.ajax({
		'url':'modIssue/',
		'type': 'POST',
		'data': {
				'action'	: 'addcc',
				'user'	  : user
			},
		'error': function (req, err, e) {
				errorl.addErr("'" + user + 
					"' could not be added to CC list. Please make sure '" + 
					user + "' exists.");
			},
		'success': function (data) {
				reloadCCList();

				// reload the history
				reloadHistory();
			}
	});
}
*/
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
		'url'	   : 'fetch/',
		'dataType'  : 'text',
		'data'	  : {
				'format'	: 'html',
				'req'	   : 'history'
			},
		'success'   : function (text) {
				$('#history_box').append(text);
			}
	});
}

/**
 * Reload the CC list, removes everything and request a new box from server
 */
function reloadCCList() {
	$('#cc_box').empty();
	$.ajax({
		'url'	   : 'fetch/',
		'dataType'  : 'text',
		'data'	  : {
				'req'	   : 'cclist'
			},
		'success'   : function (text) {
				var cc_box = $('#cc_box').html(text);
				initializeJavascript(cc_box);
				$('.dropCC').bind('click', dropCC);
			}
	});
}
