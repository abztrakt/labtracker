var start = 0;
var groups;
var list_mac = new Array(); 
$(document).ready(function() {
	// initialization code
	// reset();
	
	$("#id_problem_type").asmSelect({
		'removeLabel': 'X',
		'listClass': 'asmList prob-types',
		'listItemClass': 'asmListItem prob-types-item'
	});
    var passed_item=$('#passed_item')[0].innerHTML;
    var items = $('#id_item');
	var groups = $('#id_group');
	
    // attach hooks
	$('#id_it').change(function (e, cb) { 
        loadExtra(this.value); 
        updateGroupList(this.value, cb); }
        
    );
	groups.change(function (e, cb) { updateItem(this.value, cb); } );
    items.change(itemChange);
    $('#reset').click(function () { reset(); } );
    $('#create_issue').submit(submitIssue);

	// on initialize, we need to see if things are already set in it/group/item
	var values = {
		'item': items[0].selectedIndex > 0 ? items[0].value : null,
		'group': groups[0].selectedIndex > 0 ? groups[0].value : null
	};
	$('#id_it').trigger('change', function () {
		if (values.group !== null) {
			groups.children("option[value="+values.group+"]").attr('selected', 'selected');
			updateItem(groups[0].value, function () {
				items.children("option[value="+values.item+"]").attr('selected', 'selected');
                items.change();
			});
		}
        

	});

	// when a user is added to the cc list
	// bind the enter key to hit addCC
    $('#machineTxt').bind('autocompleteselect', function(event, ui){
        event.preventDefault();
        var user = ui.item.value;
        $('#machineTxt')[0].value= user;
        // check to see if user exists in the select 
        var option = $('#id_item').children('option:contains("'+user+'")');

        if (option.length == 1) {
            
            // Select the user in the cc list
            option.attr('selected', 'selected');
            $('#macText')[0].innerHTML= 'You have selected the Machine: '+ option[0].innerHTML;
            $("#relatedList").load("/issue/partial/" + option[0].value + "/");
        } else {
            $('#macText')[0].innerHTML = "Could not select the chosen Machine";
        }
        
    });
    
});

function auto() {
    var mac_nodes = $('#id_item').children();
    for (var i = 1; i <mac_nodes.length;i++) {
        list_mac.push(mac_nodes[i].innerHTML);
    }
    $('#machineTxt').autocomplete({
        source: list_mac 
    });
    var passed_item=$('#passed_item')[0].innerHTML;
    var items = $('#id_item');
    var br= $('<br></br>');
    for (i=0;i<items.children().length; i++) {
        if (items.children()[i].innerHTML==passed_item) {
            items.children()[i].selected='True';
            $('#macText')[0].innerHTML= 'You have selected the Machine: '+ items.children()[i].innerHTML;
            $('#macText').append(br);
            var warning = $("<img id='warning' style='float: left;' src='/static/img/icons/warning.png' />");
            $('#macText').append(warning);
            if ($('#query')[0].innerHTML=='True') {
                $('#macText')[0].innerHTML+= 'We guessed this based on your URL,<br />if we were wrong please correct us!';
            } else {
                $('#macText')[0].innerHTML+= 'We guessed this based on your IP Address,<br />if we were wrong please correct us!';
            }
            $('#machineTxt')[0].value= items.children()[i].innerHTML;
        }
    }

}

function machineAutoComplete() {
    list_mac = [];
    var mac_nodes = $('#id_item').children();
    for (var i = 1; i <mac_nodes.length;i++) {
        list_mac.push(mac_nodes[i].innerHTML);
    }
    $('#machineTxt').autocomplete("option", "source", list_mac);
}

/**
 * reset will go and kill all the extra items in both the group and item lists after
 * setting the selectedIndex to 0
 */
function reset() {
	$('#id_group, #id_item, #id_assignee').each(function () { 
		this.selectedIndex = 0;
		this.options.length = 1;
	});
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
function updateItem(group_id, cb) {
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
				//update group list
                var id_item = $('#id_item');
				id_item[0].options.length = 1;
				data.items = data.items.sort( function (a, b) {
                        return (a[1] > b[1]) ? 1 : -1;
                    }
                );
				$.each(data.items, function (ii, val) {
						id_item.append(["<option value='", val[0], "'>",
							val[1], "</option>"].join(""));
					}
				);
				id_item[0].selectedIndex = 0;
                $('#machineTxt')[0].value=''; 
				$('#macText')[0].innerHTML= 'You have no Machine selected';
                if (cb) { cb(); }
			    if (start == 0) {
                    auto();
                    start = 1;
                }else {
                    machineAutoComplete();
                }
                
            }
	});
}

/**
 * Validates the create issue form
 * @returns true if validates, false otherwise
 */
function validateForm(form) {
    var req = $.map(form.find('.required'), function (item) {
                return "#" + $(item).attr('for');
            });

    var validated = true;
    for (var ii in req) {
        var field = $(req[ii]);
        if ($.trim(field[0].value) === "") { 
            validated = false;
            appendError(field.next("ul.errorlist"), "This field is required.");
        }
    }

    return validated;
}

/**
 * Submit form handler
 */
function submitIssue(eve) {
    if (!validateForm($(eve.target))) {
        eve.preventDefault();
    }
}

/**
 * Do things when item selected is changed
 */
function itemChange(eve) {
    var list = $(eve.target);
    var value = list[0].value;

    }
