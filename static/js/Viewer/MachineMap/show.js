var initialized = false;    // is page ready?

var timer = null;       // This is the interval timer
var last_call = 0;

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
 * Goes and updates machine stuff
 */
function updateMachines() {

    if (! initialized) {
        debugLog("Cannot run updates until initializeation");
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
                'last': last_call/1000
            },
            'error': function (xhr, txt, err) {
                // handle the error
                debugLog('error');
            },
            'success': function (json, txt) {
                debugLog("last call was: " +  last_call);
                last_call = Date.now();
                applyMachineUpdates(json);
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

        applyToMachine(item, data[ii]);
    }
}


function applyToMachine(item, data) {
    if (data.x) {
        item.css('left', data.x + 'px');
    }

    if (data.y) {
        item.css('top', data.y + 'px');
    }
    
    if (data.orient) {
        switchOrientation(item, data.orient);
    }

    if (data.state) {
        switchState(item, data.state);
    }

    if (data.size) {
        switchSize(item, data.size);
    }

}

function switchOrientation(item, orient) {
    if ($.inArray(orient, options.orientations) == -1) {
        debugLog("Unknown orientation, cannot set");
        return;
    }
    item.removeClass(options.orientations.join(" "));
    item.addClass(orient);
}

function switchState(item, state) {
    if (! options.states[state]) {
        debugLog("Given state is unknown");
        return;
    }
    
    var states = new Array();
    for (var state in options.states) {
        states.push(options.states[state]);
    }
    // first remove all the known states from this item
    item.removeClass(states.join(" "));
    item.addClass(options.states[state]);
}

function switchSize(item, size) {
    if ($.inArray(size, options.size) == -1) {
        debugLog("unknown size, cannot set");
        return;
    }
    item.removeClass(options.sizes.join(" "));
    item.addClass(size);
}
