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

/**
 * Enables passing of a CSRF Token in AJAX posts
 */
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
