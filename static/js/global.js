var URL_BASE = "/issue/";

$.ajaxSetup({
	'cache'		: false,
	'dataType'	: "json",
	'type'		: "GET"
});

$(document).ready(function() {
        $.each($(".none_if_js"), function () { this.style.display = "none"; } );
        $.each($(".block_if_js"), function () { this.style.display = "block"; } );
        $.each($(".inline_if_js"), function () { this.style.display = "inline"; } );
        $.each($(".errorl"), 
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
