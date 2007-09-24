$(document).ready( function () {
    console.log('ready');
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
    console.log('in addquery');
    event.preventDefault();

    // find the item being added
    form = $('form#search');
    field = $(form).find("select#id_fields")[0].value;
    console.log('in addquery');

    $.ajax({
        "url": URL_BASE + "search/field/" + encodeURIComponent(field) + "/",
        "data": {},
        'error': function (req, err, e) {
                //console.log('failed to add item');
            },
        "dataType": "json",
        "success": function (data) {
                ql = $('#query_list');

                // create the form element and append to the form
                modes = genModeSelect(data.modes);

                //console.log(data);
                //console.log(modes);

                field = $(data.field);
                name = field.attr('name');

                li = $('<li></li>').attr('class', 'q_' + name)
                    .append(data.label).append(modes)
                    .append(field).appendTo(ql);

                $('<a href="#">[ - ]</a>').click(removeSearchItem)
                    .appendTo(li);

                // TODO need to disable some of the fields if single use

            },
    });
}

/**
 # removeSearchItem
 * Prevents default event,a nd then removes parent
 */
function removeSearchItem(event) {
    event.preventDefault();
    btn = event.target;
    $(btn).parent().remove();
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
