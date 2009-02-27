var groups;

$(document).ready(function() {
	// initialization code
	// reset();
	
	$("#id_problem_type").asmSelect({
		'removeLabel': 'X',
		'listClass': 'asmList prob-types',
		'listItemClass': 'asmListItem prob-types-item'
	});

	var items = $('#id_item');
	var groups = $('#id_group');

	// attach hooks
	$('#id_it').change(function (e, cb) { loadExtra(this.value); updateGroupList(this.value, cb); } );
	groups.change(function (e, cb) { updateItemList(this.value, cb); } );
	$('#reset').click(function () { reset(); } );

	// on initialize, we need to see if things are already set in it/group/item
	var values = {
		'item': items[0].selectedIndex > 0 ? items[0].value : null,
		'group': groups[0].selectedIndex > 0 ? groups[0].value : null
	};

	$('#id_it').trigger('change', function () {
		if (values.group !== null) {
			groups.children("option[value="+values.group+"]").attr('selected', 'selected');
			updateItemList(groups[0].value, function () {
				items.children("option[value="+values.item+"]").attr('selected', 'selected');
			});
		}
	});

	// when a user is added to the cc list
	$('#addCC').bind('click', addCC);

	// bind the enter key to hit addCC
	$('#addCC_user').keypress(function (e) { if (e.which == 13) { addCC(e); } });

	loadCC();
});

/**
 * reset will go and kill all the extra items in both the group and item lists after
 * setting the selectedIndex to 0
 */
function reset() {
	$('#id_group, #id_item').each(function () { 
		this.selectedIndex = 0;
		this.options.length = 1;
	});
}

function appendError(list, msg) {
	var error = $('<li>' + msg + '</li>');
	list.empty().append(error);
	setTimeout( function () {
		error.fadeOut('slow', function () { 
			error.remove(); 
		});
	}, 5000);
}

/**
 * updateGroupList will fetch the groups for a given inventory type and append 
 * it to the id_item list
 * @param it_id		 The id of the inventory type to fetch groups for, if 
 *					null then show all
 *
 * FIXME what happens when group_id doesn't exist? how does getJSON react?
 */
function updateGroupList(it_id, cb) {
	reset();

	$.ajax({
		"url"		: URL_BASE + "groups/",	
		"data"		: { "type": "json", "it_id": it_id },
		"error"		: function (xhr, text, err) {
				appendError($('#group_block .errorlist'), 
					"Error occurred while retrieving groups: " + text);
			},
		"success"	: function (data) {
				var id_group = $("#id_group");

				// Take the groups, construct option elements and append them 
				// to the group list
				$.each(data, 
					function (ii, val) { 
						id_group.append("<option value='" + val.group_id + "'>" + 
							val.name + "</option>");
					}
				);
				id_group[0].selectedIndex = 0;
				$('#id_group').change();

				if (cb) { cb(); }
			}
	});
}

/**
 * Given an inventory id, load extra stuff for it
 * @param it_id		The id of the inventory type
 */
function loadExtra(it_id) {
	if (it_id <= 0) {
		$('div#invSpecific').empty();
		return;
	}

	$("div#invSpecific").load("/issue/invSpec/create/", { 'type': it_id });
}

/**
 * updateItemList will fetch the items for a given group and append it to the
 * id_item list
 * @param group_id	  The id of the group to fetch items for, if null then show all
 *
 */
function updateItemList(group_id, cb) {
	var id_item = $('#id_item')[0];
	id_item.selectedIndex = 0;
	id_item.options.length = 1;

	$.ajax({
		"url"		: URL_BASE + "items/",
		"data"		: { "type": "json", "group_id" : group_id },
		"error"		: function (xhr, text, err) {
				appendError($('#item_block .errorlist'), 
					"Error occurred while retrieving items: " + text);
			},
		"success"	: function (data) {
				// for each of the items, append to the list
				var id_item = $('#id_item');
				id_item[0].options.length = 1;
				var items = data.items;
				$.each(items, function (ii, val) {
						id_item.append("<option value='" + ii + "'>" + 
							val.name + "</option>");
					}
				);

				id_item[0].selectedIndex = 0;

				if (cb) { cb(); }
			}
	});
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


/**
 * Takes the selected indexes in the cc select and adds them to the list
 */
function loadCC() {
	$('#id_cc').children('option[selected]').each(function () {
			addUserToCCList(this.value, this.innerHTML);
		});
}

function addUserToCCList(id, username) {
	var btn = $(rmCCLink(id, username)).bind("click", dropCC);
	var li = $("<li></li>").append(btn).append(" ").append("<span>" + 
			username + "</span>");
	$("ul#cc_list").append(li);
}
