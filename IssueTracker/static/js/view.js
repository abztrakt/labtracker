$(document).ready(function() {
	$("a.dropCC").bind("click", dropCC); 
	$("#ccForm").bind("submit", addCC); 
	$("#addCC").bind("click", addCC); 

	$("#id_problem_type").asmSelect({
		'removeLabel': 'X',
		'listClass': 'asmList prob-types',
		'listItemClass': 'asmListItem prob-types-item'
	});
});


/**
 * Takes an event, stops the default action, and then drops the given cc user from the
 * list, and then removes that from the list
 *
 * @param event	 The event that triggered dropCC
 */
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

/**
 * Takes an event, stops default action. Request sent to create a new CC 
 * relation, if succesful, will append item to CC list on user side, otherwise
 * appends some errors to local errorl.
 *
 * @param event	 The event that triggered addCC
 */
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

	console.log("in addCC");

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
