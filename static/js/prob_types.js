// @deprecated 
$(document).ready(function () {
	$('li.tag').click( tag_changeTagState );

    // Extend the li.tag objects with some power
    $('li.tag').each( function () {
        $.extend(this, {
			'state'         : 0,    // 0 is untagged, 1 is tagged
			'setState'      : function (g_state) {
				if (g_state == this.state) { return; }	// already set

				var item = $(this);
				item.unbind('click');
				item.remove();

				var box;
				var select = $('#id_problem_type')
					.children(':contains('+item.text()+')');

				if (g_state) {      // switch on
					this.state = 1;
					box = $('#tagged ul');
					select.attr('selected', 'selected');
				} else {            // switch off
					box = $('#untagged ul');
					this.state = 0;
					select.attr('selected', '');
				}
				box.append(item);
				item.toggleClass('tagged');
				item.click( tag_changeTagState );
			},
			'toggleState'   : function () {
				this.setState(!this.state);
			},
			'getState'      : function () {
				return this.state;
			}
		});
    });

    // sync
    $.each($('#id_problem_type').children('[selected]'), function () {
        var item = $(this);
        $('li#prob_tag_'+this.value)[0].setState(1);
    });
});

function tag_changeTagState(e) { e.target.toggleState(); }

