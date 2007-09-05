var groups;

$(document).ready(function() {
    // initialization code
    reset();

    // attach hooks
    $('#id_it').change(function () { updateGroupList(this.value); } );
    $('#id_group').change(function () { updateItemList(this.value); } );
    $('#reset').click(function () { reset(); } );
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
 * @param it_id         The id of the inventory type to fetch groups for
 *
 * FIXME what happens when group_id doesn't exist? how does getJSON react?
 */
function updateGroupList(it_id) {
    reset();
    if (it_id == "") return;
    // var id_group = $("#id_group")[0]; # XXX
    $.getJSON(URL_BASE + "groups/" + it_id + "/",
        function (data) {
            var id_group = $("#id_group");

            // Take the groups, construct option elements and append them to the group
            // list
            $.each(data.groups, 
                function (ii, val) { 
                    console.log(ii);
                    console.log(val);
                    id_group.append("<option value='" + val.pk + "'>" + val.fields.name +
                        "</option>");
                }
            );
            id_group[0].selectedIndex = 0;
        }
    );
}

/**
 * updateItemList will fetch the items for a given group and append it to the id_item list
 * @param group_id      The id of the group to fetch items for
 *
 * FIXME what happens when group_id doesn't exist? how does getJSON react?
 */
function updateItemList(group_id) {
    // reset only the itemList
    var id_item = $('#id_item');
    id_item[0].selectedIndex = 0;
    id_item[0].options.length = 1;

    if (group_id == "") return;

    $.getJSON(URL_BASE + "items/" + group_id + "/",
        function (data) {
            // for each of the items, append to the list
            $.each(data.items,
                function (ii, val) {
                    id_item.append("<option value='" + val.pk + "'>" + val.fields.name +
                        "</option>");
                }
            );
            id_item[0].selectedIndex = 0;
        }
    );
}

