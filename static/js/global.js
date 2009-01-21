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

        $.each($(".compact_container"), function () {
            var item = $(this);
            $.extend(this, compactor);
            this.compactor.parent = this;
            $.extend(item.children('.compact-trigger')[0], { 'parent': this });
            item.children('.compact-trigger').click(function (e) {
                    this.parent.compactor.toggle();
                });
        });

    }
);

var compactor = {
    'compactor' : {
        'state'     : 1,
        'setState'  : function (g_state) {
            if (this.state == g_state)
                return;

            if (g_state == 0) {     // compact everything
                // TODO
                $(this.parent).children('.compact').addClass('display-none');
                this.state = 0;
            } else {                // expand
                // TODO
                $(this.parent).children('.compact').removeClass('display-none');
                this.state = 1;
            }
        },
        'toggle'     : function () {
            this.setState(!this.state);
        }
    }
};

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
