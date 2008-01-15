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

        $.each($(".compact_container"), function () {
            console.log("extending object");
            var item = $(this);
            $.extend(this, compactor);
            this.compactor.parent = this;
            $.extend(item.children('.compact_trigger')[0], { 'parent': this });
            item.children('.compact_trigger').click(function (e) {
                    console.log(this.parent);
                    this.parent.compactor.toggle();
                });
        });

    }
);

var compactor = {
    'compactor' : {
        'state'     : 1,
        'setState'  : function (g_state) {
            console.log("setting state to " + g_state);
            console.log("state is currently " + this.state);
            if (this.state == g_state)
                return;

            console.log("Will be doing it to these items:");
            console.log($(this.parent).children());

            if (g_state == 0) {     // compact everything
                // TODO
                $(this.parent).children('.compact').addClass('display_none');
                this.state = 0;
            } else {                // expand
                // TODO
                $(this.parent).children('.compact').removeClass('display_none');
                this.state = 1;
            }
        },
        'toggle'     : function () {
            this.setState(!this.state);
        }
    }
};
