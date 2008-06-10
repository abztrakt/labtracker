/**
 * @fileoverview
 *
 * View/modMachineMap.js
 *
 * @requires jQuery
 * @author Ziling Zhao
 * @version 0.2
 *
 * Holds javascript stuff for the modMachineMap view.
 */

/* extend draggable  */

/* Add 'flag', which basically enables people to query items to see if it is
 * in the process of being dragged
 */
$.ui.plugin.add('draggable', 'flag', {
	start: function (e, ui) { $(this).data('dragging.modmap', true); },
	stop: function (e, ui) { $(this).data('dragging.modmap', false); }
});

/**
 * modMap - 
 *
 * holds machine item related information and functions
 */
var modMap = {
	 // Default attributes
	'defaults': {
		'orientation':  null,
		'size':		 null,
		'mapped':	   false
	},
	'sizes': {},			// Acceptable sizes

	/**
	 * init
	 * Function used to initialize modMap with default settings
	 * @param {String} orientation - This is the default orientation, either 
	 *	  H or V (Horizontal or Vertical)
	 * @param {String} size - The default size for machines to have, must exist in sizes
	 * @param {Array} sizes - The list of sizes that machines can have
	 */
	'init': function (orientation, size, sizes) {
        var self = this;

		for (var size in sizes) {
			this.sizes[size] = sizes[size];
		}
		this.defaults.orientation = orientation;

		if (! this.validSize(size)) 
			throw "Given size does not exist in list of sizes does not exist";

		this.defaults.size = size;

		$(document).ready(function () {
			self.bindItems(self);
		});
	},

	/**
	 * Bind the machine items to their events
	 */
    'bindItems': function (self) {
        $('div#map').droppable({
                accept: "div.item",
                drop: function (ev, ui) {
                    var item = $(ui.draggable);

                    var item_off = item.offset();
                    var mapped_off = $(this).offset();

                    item.appendTo(this).
                        css({	'left':  item_off.left - mapped_off.left,
                                'top': item_off.top - mapped_off.top,
                                'position': 'absolute' }).
                        data('mapped.modmap', true).
                        data('dirty.modmap', true);
                }
            });

        $('div#unmapped').droppable({
                accept: "div.item",
                out: function (ev, ui) {
                    var item = $(ui.draggable);
                    item.removeClass('unmapped');
                    item.addClass('mapped');
                },
                over: function (ev, ui) {
                    var item = $(ui.draggable);
                    item.removeClass('mapped');
                    item.addClass('unmapped');
                },
                drop: function(ev, ui) {
                    self.unmapItem(ui.draggable);
                }
            }).children().droppable('disable');
	
		$('div.item')
			.draggable({ 
				'opacity': 0.5 ,
				'flag': true,
				'start': function (ev, ui) {
					var item = $(ui.draggable);
					// when beginning to drag, kill all 'infowraps' aka tooldiv
					$('div.tools').trigger('remove.modmap');
				}
			})
			.bind('mouseenter.modmap', function (event) {
				// make sure that this item is mapped first
				var item = $(this);

				modMap.updateInfoPane(modMap.getItemName(item));


				if (! item.data('mapped.modmap') || item.data('tools.modmap') 
						|| item.data('dragging.modmap')) {
					// do nothing
				} else {
					// remove all other tool divs
					$('div.tools').each(function () {
							$(this).trigger('remove.modmap');
						});

					modMap.drawToolDiv(this);
				}
			})
			.bind('mouseout.modmap', function (eve) {
				var item = $(eve.target);

				if (item.data('mapped.modmap')) {
				} else {
					modMap.updateInfoPane();
				}
			})
			.each( function () { 
				// figure out if they are mapped or not
				var item = $(this);

				var info = modMap.getMachineDict();
				info.mapped = item.parent().attr('id') == "map";

				if (info.mapped) {
					// Find the orientation
					info.orientation = item.hasClass('H') ? 'H' : 'V';

					for (var size in modMap.sizes) {
						if (item.hasClass(size)) {
							info.size = size;
							break;
						}
					}
				} 

				item.data('load.modmap', info).data('dirty.modmap', false)
					.data('orientation.modmap', info.orientation)
					.data('size.modmap', info.size).data('mapped.modmap', info.mapped)
					.addClass(info.size + " " + info.orientation)
			})
			.contextMenu('#itemcontextmenu', function (eve) {
				$('#itemcontextmenu').data('target', eve.target);
				$('div.tools').trigger('remove.modmap');
			})
		;

		$('#itemcontextmenu').children('li').bind('click.modmap', function (eve) {
			var menu = $('#itemcontextmenu');
			var item = $(menu.data('target'));
			menu.removeData('target');

			var target = $(eve.target);

			var size_span = target;

			if (! size_span.hasClass('sizename')) {
				size_span = size_span.find('span.sizename');
			}
			var target_size = size_span.text();

			item.removeClass(self.getItemSize(item, self));
			item.addClass(target_size);

			item.data('dirty.modmap', true)
			item.data('size.modmap', target_size);
		});
    },

	/**
	 * ready
	 * @returns True/False on whether or not init has happend and is acceptable
	 */
	'ready': function () {
		return this.defaults != null && this.defaults.size != null;
	},


	/**
	 * validSize
	 * @returns True/False on whehter or not the given size is valid
	 */
	'validSize': function (size) {
		return this.sizes[size] != null;
	},

	/**
	 * getSize
	 * Returns null if size does not exist
	 * @returns Dictionary with height and width for a given size
	 */
	'getSize': function (size) {
		if (!this.validSize(size)) return null;
		return this.sizes[size];
	},

	/**
	 * getItems - 
	 * Finds and returns all items
	 * @returns A jQuery object of all the items
	 */
	'getItems': function () {
		return $('div.item');
	},

	/**
	 * getMappedItems
	 * Finds and returns all items that have been mapped
	 * @returns A jQuery object of all the items
	 */
	'getMappedItems': function () {
		return $('div#map div.item');
	},
	
	/**
	 * getUnmappedItems
	 * Finds and returns all unmapped items
	 * @returns A jQuery object of all the items
	 */
	'getUnmappedItems': function () {
		return $('div#unmapped div.item');
	},

	/**
	 * getDirtyItems
	 * Finds and returns all dirty items
	 * @returns A jQuery object of all the items
	 */
	'getDirtyItems': function () {
		return $.grep(this.getItems(), function (item) {
				return $(item).data('dirty.modmap');
			});
	},

	/**
	 * getMachineDict, returns the dictionary holding attributes that all
	 * machine's should have
	 *
	 * @param {dict} options	Values to use as defaults
	 */
	'getMachineDict': function (options) {
		options = options || {};
		return {
			'mapped': options['mapped'] || this.defaults.mapped,
			'orientation': options['orientation'] || this.defaults.orientation,
			'size': options['size'] || this.defaults.size
		};
	},


	/**
	 * Draw the tool dive around the given item
	 * @param {object} item is the div to draw around
	 */
	'drawToolDiv': function (item) {
		var self = this;

		var item = $(item);
		
		// mark it early
		item.data('tools.modmap', true);
		item.addClass('selected');

		var pos = item.position();
		var padding = 20;

		// the div that will hold the list of tools
		// XXX is this needed?
		var tools = $("<div class='tools'></div>");
        
		// the actual ul of tools
		var tool_list = $("<ul class='struct'></ul>");


		// The rotation button
		var rotate = $("<img class='op rotatebtn' \
							src='/static/img/view/modmap/rotate.gif' />")
			 .bind('click.modmap', function (e) {
				 e.preventDefault();

				 item.toggleClass('H');
				 item.toggleClass('V');

				 // update the orientation
				 if (item.hasClass('H')) {
					 item.data('orientation.modmap', 'H');
				 } else {
					 item.data('orientation.modmap', 'V');
				 }

				 // mark data dirty for saving
				 item.data('dirty.modmap', true);

				 // redraw the tool div
				 tools.trigger('remove.modmap');
				 self.drawToolDiv(item[0]);
			 });
		tool_list.append(rotate);

		tools.data('removeable.modmap', true);

		// the unmap button
		var unmap = $("<img class='op unmap' \
							src='/static/img/view/modmap/x.gif' />")
			 .bind('click.modmap', function (e) {
				 e.preventDefault();
				 modMap.unmapItem(item[0]);
			 });
		tool_list.append(unmap);

		tool_list.children().wrap("<li></li>").end().appendTo(tools);


		// tell the tool div what item it is modifying
		tools.data('item.modmap', item)

			// tool div should be larger than the item it is wrapping
			.width(item.outerWidth() + padding * 2)
			.height(item.outerHeight() + padding * 2)

			// position the tool div so it is centered around the item
			// also, make it transparent when first adding
			.css({	'left': pos.left - padding + "px",
					'top': pos.top - padding + "px",
					'opacity': 0 })

			// on leaving the tool div area, remove it
			.bind('mouseleave.modmap', function (ev) {
				// make sure that the mouse is actually outside the tools box
				if (self.mouseOut(ev.pageX, ev.pageY, item)) {
					$(this).trigger('remove.modmap');
                    modMap.updateInfoPane();
				}
			})

			// clicking should also remove the tool div
			.bind('click.modmap', function (ev) { $(this).trigger('remove.modmap'); })

			.bind('remove.modmap', function (ev) { self.removeToolDiv($(ev.target)); })

			// add to the page, and fade it in
			.appendTo($('#map')).fadeTo("medium", 0.43);

	},

	/**
	 * Get the items size
	 */
	'getItemSize': function (item, self) {
		if (self == null) { self = this; }

		var item = $(item);

		for (var size in self.sizes) {
			if (item.hasClass(size)) {
				return size;
			}
		}

		return null;
	},

	/**
	 * See if the location is outside the boundaries of given item
	 */
	'mouseOut': function (x, y, item) {
		var offset = item.offset();
		return x < offset.left || y < offset.top
					|| x > offset.left + item.outerWidth()
					|| y > offset.top + item.outerHeight();
	},

	/**
	 * removeToolDiv
     *
	 * remove a tooldiv
	 * @param {jQuery} the jQuery object that holds one tooldiv
	 */
	'removeToolDiv': function (tooldiv) {
		if (!tooldiv.data('removeable.modmap')) { return; }
		if (tooldiv.size() < 1) { return; }

		tooldiv.each(function () {
			var item = $(this).data('item.modmap');
			item.data('tools.modmap', false);
			item.removeClass('selected');
		});

		tooldiv.unbind('.modmap');
		tooldiv.fadeOut("fast", 
			function () { 
				var tooldiv = $(this);
				tooldiv.remove(); 
			});

	},


	/**
	 * unmapItem
	 *
	 * Unmap an item, put it in the unmapped box
	 */
	'unmapItem': function (item) {
		var item = $(item);
		item.removeClass('mapped').addClass('unmapped')
			.appendTo($('div#unmapped').children('div#items'))
			.css({ 'left': '0px',
					'top': '0px',
					'position': 'relative'})
			.data('mapped.modmap', false)
			.data('dirty.modmap', true);
	},

    /**
     * getItemID
     *
     * From an item, get the item's real id (pk)
     */
    'getItemID': function (item) {
        var id = item.attr('id');
        return id.replace(/\[.*?\]$/, '');
    },

    /**
     * getItemName
     *
     * From an item, get the item's real name
     */
    'getItemName': function (item) {
        var id = item.attr('id');
        return id.match(/\[(.*?)\]$/)[1];
    },

    'updateInfoPane': function (name) {
        var infoPane = $('#infoPane');

        var machine_name = infoPane.find('#machineName');

        machine_name.text(name || "");
    }
};



$(document).ready(function () {


	$('a#save').bind('click.modmap', function (ev) {
			ev.preventDefault();

			// prevent all dragging until after we are done here
			modMap.getItems().draggable('disable');

			var params = { 'save': 1 };
			
			// get list of unmapped items from the dirty_items
			var dirty_items = modMap.getDirtyItems();
			var unmapped = new Array(), mapped = new Array();

			$.each(dirty_items, function () {
					var item = $(this);
					if (item.data('mapped.modmap')) {
						mapped.push(this);
					} else if (item.data('load.modmap').mapped) {
						unmapped.push(this);
					} else {
						// original was not mapped and current is not mapped,
						// not dirty
						item.data('dirty.modmap', false);
					}
				});

			if (unmapped.length > 0) {
				params['unmap'] = $.map(unmapped, 
						function (item) { return modMap.getItemID($(item)); });
			}

			if (mapped.length > 0) {
                params['map'] = $.map(mapped, 
                    function (item) { 
                        // in addition, for each of these items, we will
                        // need to set the param's for the attributes
                        var item = $(item);
                        var id = modMap.getItemID(item);

                        var prefix = 'map[' + id + ']';
                        params[prefix + '[x]'] = item.css('left').replace(/\D/g,"");
                        params[prefix + '[y]'] = item.css('top').replace(/\D/g,"");
                        params[prefix + '[size]'] = item.data('size.modmap');
                        params[prefix + '[orient]'] = item.data('orientation.modmap');

                        return id;
                    }
                );
			}

			// only do this if both unmapped and mapped hold items

			if (mapped.length + unmapped.length > 0) {
				$.ajax({
					'url': location.href.replace(/\?.*$/,""),
					'cache': false,
					'dataType': 'json',
					'type': 'GET',
					'data': params,
					'complete': function () {
							modMap.getItems().draggable('enable');
						},
                    'failure': function (xhr, text, err) {
				        // TODO failure handler
                    },
					'success': function (json) {
							// TODO set the load settings for the items
							$.each(dirty_items, function () {
									var item = $(this);
									item.data('dirty.modmap', false);
									if (item.data('mapped.modmap')) {
										item.data('load.modmap').mapped = true;
									} else {
										item.data('load.modmap').mapped = false;
									}
								});
						}
				});
			} else {
				modMap.getItems().draggable('enable');
			}

		});

});