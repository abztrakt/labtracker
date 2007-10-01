$(document).ready( function () {
    //$('form#search div#query_add > input.query_add').bind('click', addQueryItem);
    $('form#search div#query_add > input.query_add').bind('click', addQueryItem);
})

/**
 * addQueryItem(event)
 * Takes an event on submit and prevents normal submission of form
 * Instead, takes current from input and does an ajax call to get a search field
 * that is appended to the query form
 */
function addQueryItem(event) {
    event.preventDefault();

    // find the item being added
    form = $('form#search');
    field = $(form).find("select#id_fields")[0].value;

    $.ajax({
        "url": URL_BASE + "search/field/" + encodeURIComponent(field) + "/",
        "data": {},
        'error': function (req, err, e) {
                console.log('failed to add item');
            },
        "dataType": "json",
        "success": function (data) {
                var ql = $('#query_list');

                var num = ql.children().length

                // create the form element and append to the form

                var field = $(data.field);
                field.map(function () {
                    var items = $(this).find('select, input');

                    var name = $(this).attr('name');
                    $(this).attr('name', num + "_" + name);

                    for (var ii = 0; ii < items.length; ++ii) {
                        var item = items[ii];
                        item.name = num + "_" + item.name;
                    }
                });
                field.filter('ul').attr('class','struct inline');

                var li = $('<li></li>') //.attr('class', 'q_' + name)
                    .append("<label>" + data.label + "</label>")
                    .append(field).appendTo(ql);

                $('<a href="#">[ - ]</a>').click(removeSearchItem)
                    .appendTo(li);

                // TODO need to disable some of the fields if single use

            },
    });
}

/**
 * removeSearchItem
 * Prevents default event,a nd then removes parent
 */
function removeSearchItem(event) {
    event.preventDefault();
    btn = event.target;

    // now we have to renumber everything under this item everything
    li = $(btn).parent();

    reg = /^(\d+)(_\w+?(?:_mode)?)$/;
    cur = li.next('li');
    while (cur != null && cur.length > 0) {
        items = cur.find('select, input');

        for (var ii = 0; ii < items.length; ++ii) {
            item = items[ii];
            matches = item.name.match(reg);

            item.name = (--matches[1]) + matches[2];
        }
        cur = cur.next('li');
        count++;
    }

    li.remove();
}

/**
 * genModeSelect(modes)
 * Gets a modes and generates a select list out of them
 * returns the select jquery obj
 */
function genModeSelect(modes) {
    select = $("<select name='mode'></select>");
    for (var ii = 0; ii < modes.length; ++ii) {
        select.append("<option value='" + modes[ii].value + "'>" 
                + modes[ii].name + "</option>");
    }
    return select;
}
