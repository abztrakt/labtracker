$(document).ready(function () {
    //
});

var initialized = false;    // is page ready?

var timer = null;       // This is the interval timer

var options = {
    'timer':    5000,   // duration between updates
    'refresh':  0,      // should we just refresh the page instead of ajax?

    // Status is the mapping of what the server returns for status and what 
    // the class should be
    'status':   {}      // what status are available?
};

/**
 * Initialize
 *
 * Pass in a dictionary of options
 * Important ones include:
 *  'status' a mapping of what the server returns to what the class should be
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
    debugLog("Updating machines");

    if (options.refresh) {
        window.location.href = window.location.href;
    } else {
        // do ajax update
    }
}

/**
 * applyMachineUpdates
 *
 * Given a dictionary of machine info, go and find the machines to update
 */
function applyMachineUpdates(info) {
}

