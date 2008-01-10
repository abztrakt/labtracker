var groups;

$(document).ready(function() {
    // initialization code
    reset();

    // attach hooks
    $('#id_it').change(function () { updateGroupList(this.value); } );
    $('#id_group').change(function () { updateItemList(this.value); } );
    $('#reset').click(function () { reset(); } );
	//$('div.tags li.tag').click( changeTagState );
	$('li.tag').click( changeTagState );
	
	$('#id_it').change();
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

/**
 * updateGroupList will fetch the groups for a given inventory type and append 
 * it to the id_item list
 * @param it_id         The id of the inventory type to fetch groups for, if null then show all
 *
 * FIXME what happens when group_id doesn't exist? how does getJSON react?
 */
function updateGroupList(it_id) {
    reset();

	// TODO need errorhandler
	$.ajax({
		"url"		: URL_BASE + "groups/",	
		"data"		: { "type": "json", "it_id": it_id },
		"success"	: function (data) {
				var id_group = $("#id_group");

				// Take the groups, construct option elements and append them 
				// to the group list
				$.each(data, 
					function (ii, val) { 
						id_group.append("<option value='" + val.id + "'>" + 
							val.name + "</option>");
					}
				);
				id_group[0].selectedIndex = 0;
				$('#id_group').change();
			}
	});
}

/**
 * updateItemList will fetch the items for a given group and append it to the id_item list
 * @param group_id      The id of the group to fetch items for, if null then show all
 *
 */
function updateItemList(group_id) {
    // reset only the itemList
    var id_item = $('#id_item')[0];
    id_item.selectedIndex = 0;
    id_item.options.length = 1;

	// TODO need errorhandler
	$.ajax({
		"url"		: URL_BASE + "items/",
		"data"		: { "type": "json", "group_id" : group_id },
		"success"	: function (data) {
				// for each of the items, append to the list
				var id_item = $('#id_item');
				$.each(data,
					function (ii, val) {
						id_item.append("<option value='" + ii + "'>" + 
							val.name + "</option>");
					}
				);
				id_item[0].selectedIndex = 0;
			}
	});
}

function changeTagState(e) {
	item = $(e.target);
	tag_m = /\s*tagged\s*/;
	it_class = item.attr('class')

	item.unbind('click');
	item.remove();

	// if has class tagged, put back into untagged area
	if (it_class && it_class.match(tag_m)) {
		$('#untagged ul').append(item);
		$('#id_problem_type').children(':contains('+item.text()+')').attr('selected', '');
	} else {
		$('#tagged ul').append(item);
		$('#id_problem_type').children(':contains('+item.text()+')').attr('selected', 'selected');
	}
	item.toggleClass('tagged');
	item.click( changeTagState );
}
