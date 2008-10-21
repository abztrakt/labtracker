var initialized = false;    // is page ready?

var timer = null;       // This is the interval timer
var last_call = Date.now()/1000;

var options = {
    'timer':    5000,   // duration between updates
    'refresh':  0,      // should we just refresh the page instead of ajax?

    'sizes': [],
    'orientations': ['H', 'V'],

    // States is the mapping of what the server returns for states and what 
    // the class should be
    'states':   {}      // what states are available
};

/**
 * Initialize
 *
 * Pass in a dictionary of options
 */
function init(opts) {
    $.extend(options, opts);

    initialized = true;
    timer = setInterval(updateMachines, options.timer);
}

/**
 * updateMachines
 *
 * Updates machine status on the map 
 */
function updateMachines() {

    if (! initialized) {
        debugLog("Cannot run updates until initialization");
        return;
    }

    if (options.refresh) {
        window.location.href = window.location.href;
    } else {
        // do ajax update
        $.ajax({
            'url':          '/views/MachineMap/CRC_Map/',
            'type':         'GET',
            //'ifModified':   true,
            'dataType':     'json',
            'data': {
                'last': last_call
            },
            'error': function (xhr, txt, err) {
                // handle the error
                debugLog('error');
            },
            'success': function (json, txt) {
                last_call = json.time;
                applyMachineUpdates(json.machines);
            }
        });
    }
}

/**
 * applyMachineUpdates
 *
 * Given a dictionary of machine info, go and find the machines to update
 */
function applyMachineUpdates(data) {
    for (var ii in data) {
        var item_id = ii + "_" + data[ii].name;
        var item = $('#' + item_id);

        if (item.size() == 0) {
            // have to create the item
            item = newMachine(item_id, data[ii]);

            // status will be wrong... mark as unusable?
            $('#map').append(item);
            data[ii].state = "broken";
        }

        applyToMachine(item, data[ii]);
    }
}

function newMachine(id, data) {
    var mc = $('<div id="' + id + '" class="item mapped"></div>');
    return mc;
}


function applyToMachine(item, data) {
    var modified = false;
    if (data.x) {
        var xpos = parseInt(data.x) + 'px';
        
        if (item.css('left') != xpos) {
            item.css('left', xpos);
            item.data('modified', true);
        }
    }

    if (data.y) {
        var ypos = parseInt(data.y) + 'px';

        if (item.css('top') != ypos) {
            item.css('top', ypos);
            item.data('modified', true);
        }
    }
    
    if (data.orient && switchClass(item, data.orient, options.orientations)) {
        item.data('modified', true);
    }

    if (data.state && switchState(item, data.state)) {
        item.data('modified', true);
    }

    if (data.size && switchClass(item, data.size, options.sizes)) {
        item.data('modified', true);
    }
}

/**
 * Switch a given items class
 * @param item {jQuery}  item which to apply it on
 * @param cl {String} the target class
 * @param classes {Array} the list of classes to swap out
 *
 * Takes a look at the item and removes all classes from the list of classes
 * given and adds the target class to the item
 */
function switchClass(item, cl, classes) {
    if (classes.length == 0) { return; }
    if (item.hasClass(cl)) { return false; }

    if ($.inArray(cl, classes) == -1 ) {
        return;
    }

    item.removeClass(classes.join(" "));
    item.addClass(cl);
    return true;
}

/**
 * switchState
 */
function switchState(item, state) {
    if (! options.states[state]) {
        debugLog("Given state is unknown");
        return;
    }

    var states = new Array();
    for (var st in options.states) {
        states.push(options.states[st]);
    }

    return switchClass(item, options.states[state], states);
}

