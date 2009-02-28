var URL_BASE = "/issue/";
var DEBUG = true;

$.ajaxSetup({
	'cache'		: false,
	'dataType'	: "json",
	'type'		: "GET"
});

function initializeJavascript(item) {
    item.find(".none-if-js").hide();

    item.find(".block-if-js").each( function () { this.style.display = "block"; } );
    item.find(".inline-if-js").each( function () { this.style.display = "inline"; } );
}

$(document).ready(function() {
        initializeJavascript($(document));

        $.each($(".errorl,.errorlist"), 
            function () { 
                this.addErr = function (err) {
                    $(this).append("<li>" + err + "</li>");
                };
                this.reset = function () {
                    $(this).empty();
                };
            } 
        );
    }
);

function appendError(list, msg) {
	var error = $('<li>' + msg + '</li>');
	list.empty().append(error);
	setTimeout( function () {
		error.fadeOut('slow', function () { 
			error.remove(); 
		});
	}, 5000);
}

var django_date_parser = {
	'id':		'django_date',
	'is':		function (s) {
					return false;
				},
	'format':	function (s) {
					s = s.replace(/\.|\bat\s+/g, "").replace(/\b(\w{2})$/, function (c) {
							return c.toUpperCase();
						});
					return $.tablesorter.formatFloat(new Date(s).getTime());
				},
	'type': "numeric"
};


/**
 * Creates the the html for rm link
 */
function rmCCLink(userid, username) {
    return '<a id="cc_' + userid + '" class="dropCC" title="Remove ' + username + 
        ' from CC" href="#">x</a>';
}


function debugLog(msg) {
    if (!DEBUG) { return; }

    if (typeof console != "undefined" && typeof console.log != "undefined") {
        console.log(msg);
    }
}
