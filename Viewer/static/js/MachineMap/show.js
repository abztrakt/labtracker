var initialized = false;    // is page ready?
var zHelper= 0;
var timer = null;       // This is the interval timer
var last_call = Date.now()/1000;
var view = null;       //the map name
var timer1 =null
var options = {
    'view': view,          //the view name
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
    hideLists();
    $('.outerItem').bind('click', showInfo);
    $('.close').bind('click', closeList);
    zDex = 101+zHelper;
    $('.list').draggable({start: drag });
    initialized = true;
    view = options.view;
    timer = setInterval(updateMachines, options.timer);
    getAvailableInfo();
    timer1 = setInterval(getAvailableInfo, options.timer);
}

function getAvailableInfo() {
   $.ajax({
            'url':          '/views/MachineMap/' + view + '/availability',
            'type':         'GET',
            //'ifModified':   true,
            'dataType':     'json',
            'error': function (xhr, txt, err) {
                // handle the error
                debugLog('error');
            },
            'success': function (json, txt) {
                var spans = $('.available')
                for(var j=0; j<spans.length; j++) {
                    spans[j].innerHTML = json.available_machines;
                }
                $('#total')[0].innerHTML = json.total_machines;
                for (var i in json){
                    
                    if(i !="available_machines" && i != "total_machines") {
                        
                        if (json[i].total_count != 0) {
                            $('#'+json[i].safe_name)[0].innerHTML = json[i].count+'/';
                            $('#'+json[i].safe_name+'_total')[0].innerHTML = json[i].total_count;
                        }else {
                            $('#'+json[i].safe_name+'_info')[0].style.display = 'none';
                        }
                    }

                }
            }
        });
}

function closeList(event) {
    var id = event.currentTarget.parentNode.id;
    var list_id = '#'+id;
    $(list_id)[0].style.display = 'none';
}

function drag(event, ui) {
    ui.helper[0].style.zIndex= 101+zHelper;
    zHelper +=2;
}
function hideLists() {
    lists = $('.list');
    for( var i = 0; i< lists.length;i++) {
        lists[i].style.display = 'none';
    }
}

function showInfo(event) {
    var children=$(event.currentTarget).children();
    var id = children[0].getAttribute('value');
    var list_id='#list_'+id;
    var listItems = $('.list');
    style = $(list_id)[0].style.display;
    if (style == 'none') {
        $(list_id)[0].style.display = '';
        $(list_id)[0].style.zIndex = 100+zHelper;
        zHelper++;
    } else {
        $(list_id)[0].style.display = 'none'; 
    }
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
            'url':          '/views/MachineMap/' + view + '/',
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
                removeMachines(json.deletemachines);
            }
        });
    }
}

function removeMachines(machines) {
    for(var i in machines) {
        var machine_name = machines[i].name;
        var machine = $('#outer_'+machine_name);
    
        if (machine) {
            var list = $('#list_'+machine_name);
            machine.remove()
            list.remove()
        }
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
        var outer_id = "outer_" + data[ii].name;
        var outer_item= $('#' + outer_id);
        var list_id = "list_" + data[ii].name;
        if (item.size() == 0) {
            // have to create the item
            outer_item = newMachine(item_id, ii, outer_id, list_id, data[ii]);
            item = outer_item.children()
            // status will be wrong... mark as unusable?
            $('#map').append(outer_item);
        }

        applyToMachine(item, outer_item, data[ii]);
    }
}

function newMachine(id, pk, outer_id, list_id, data) {
    var mc = $('<div id="'+outer_id+'" class ="outerItem mapped"></div>');
    var inner_mc = $('<div id="' + id + '" class="item mapped" value="'+data.name+'"></div>');
    mc.append(inner_mc);
    var width = parseInt(data.x)+parseInt(data.width);
    var list = $('<div id="'+list_id+'" class="list" style="left: '+width+'px; top: '+parseInt(data.y)+'px; display: none; position: absolute;" value="'+data.name+'"></div>');
    var name= $('<li><a href="/machine/detailed/'+pk+'">'+data.name+'</a></li>');
    var mac1 = $('<li>MAC Address 1: "'+data.mac1+'"</li>');
    var mac2 = $('<li>MAC Address 2: "'+data.mac2+'"</li>');
    var ip = $('<li>IP Address: "'+data.ip+'"</li>');
    var wall_port = $('<li>Wall Port: "'+data.wall_port+'"</li>');
    var uw_tag = $('<li>UW Tag: "'+data.uw_tag+'"</li>');
    var man_u = $('<li>Manufacture Tag: "'+data.manu+'"</li>');
    var close_it= $('<img class="close" src="/static/img/Viewer/modmap/x.gif"/>');
    list.append(name).append(mac1).append(mac2).append(ip).append(wall_port).append(uw_tag).append(man_u).append(close_it);
    list.draggable({start: drag });
    mc.bind('click', showInfo);
    close_it.bind('click', closeList);
    $('#map').append(list);
    return mc;
}


function applyToMachine(item, outer_item, data) {
    var modified = false;
    var has_broken = outer_item.hasClass('broken');
    var broken = data.broken;
    var has_verified = outer_item.hasClass('verified');
    var verified = data.verified;
    if (broken != has_broken) {
        if (has_broken) {
            outer_item.removeClass('broken');
        }else {
            outer_item.addClass('broken');
        }
    }
    if (verified != has_verified) {
        if (has_verified) {
            outer_item.removeClass('verified');
            id = "#v_"+data.name;
            $(id).remove()
        }else {
            outer_item.addClass('verified');
            id ="v_" + data.name;
            var check = $('<div id="'+ id +'" class="check" style="top: 2px; left: 2px;" ></div>');
            var img = $("<img src='/static/img/Viewer/check.png'/>");
            check.append(img);
            outer_item.append(check)
        }

    }
    if (data.x) {
        var xpos = parseInt(data.x) + 'px';
        
        if (outer_item.css('left') != xpos) {
            outer_item.css('left', xpos);
            outer_item.data('modified', true);
        }
    }

    if (data.y) {
        var ypos = parseInt(data.y) + 'px';

        if (outer_item.css('top') != ypos) {
            outer_item.css('top', ypos);
            outer_item.data('modified', true);
        }
    }
    
    if (data.orient && switchClass(item, data.orient, options.orientations)) {
        item.data('modified', true);
    }
    if (data.orient && switchClass(outer_item, data.orient, options.orientations)) {
        outer_item.data('modified', true);
    }
    if (data.state && switchState(item, data.state)) {
        item.data('modified', true);
    }

    if (data.size && switchClass(item, data.size, options.sizes)) {
        item.data('modified', true);
    }
    if (data.size && switchClass(outer_item, data.size, options.sizes)) {
        outer_item.data('modified', true);
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
  
  
