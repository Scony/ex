function renderLoadingGif () {
    $('#content').html('<div class="text-center"><img src="./gfx/loading.gif"></div>');
}

function renderPopular () {
    $.ajax({
	type: 'GET',
	url : server + '/commands/popular'
    }).done(function (data) {
	var list = ''
	var arr = JSON.parse(data)
	for (i in arr) {
	    list += '<li><a href="#" class="renderCommand" x-id="' + arr[i]['_id'] + '">'+ arr[i]['name'] + '</a></li>';
	}
	$('#commands').html(list);
	$('.renderCommand').click(function () {
	    renderCommand($(this).attr('x-id'));
	});
    });
    $.ajax({
	type: 'GET',
	url : server + '/examples/popular'
    }).done(function (data) {
	var list = ''
	var arr = JSON.parse(data)
	for (i in arr) {
	    list += '<li><a href="#" class="renderExample" x-id="' + arr[i]['_id'] + '">'+ arr[i]['example'] + '</a></li>';
	}
	$('#examples').html(list);
	$('.renderExample').click(function () {
	    renderExample($(this).attr('x-id'));
	});
    });
}

function renderCommands () {
    renderLoadingGif();
    $.ajax({
	type: 'GET',
	url : server + '/commands'
    }).done(function (data) {
	$('#content').html('');
	var arr = JSON.parse(data);
	var table = '<table class="table table-striped table-hover ">' +
	    '<thead>' +
	    '<tr>' +
	    '<th>Command</th>' +
	    '<th class="text-center">Actions</th>' +
	    '</tr>' +
	    '</thead>' +
	    '<tbody>';
	for(i in arr) {
	    table += '<tr>';
	    table += '<td><a href="#" class="renderCommand" x-id="' + arr[i]['_id'] + '">'+ arr[i]['name'] + '</a></td>';
	    table += '<td class="text-center"><button class="btn btn-danger btn-xs removeCommand" x-id="' + arr[i]['_id'] + '">X</button></td>';
	    table += '</tr>';
	}
	table += '</tbody>' +
	    '</table>';
	$('#content').html(table);
	$('.renderCommand').click(function () {
	    renderCommand($(this).attr('x-id'));
	});
	$('.removeCommand').click(function () {
	    $.ajax({
		type: 'DELETE',
		url : server + '/commands/' + $(this).attr('x-id')
	    }).fail(function (a,b,c) {
		renderCommands();
	    });
	});
	var well = '<hr>' +
	    '<div class="well">' + 
            '<h4>Add a command:</h4>' +
            '<div class="form-group">' +
            '<input type="text" id="cnamei" class="form-control" placeholder="Name">' +
            '</div>' +
            '<div class="form-group">' +
            '<textarea class="form-control" id="cdesci" rows="3" placeholder="Description"></textarea>' +
            '</div>' +
            '<button type="submit" id="caddb" class="btn btn-success">Add</button>' +
            '</div>';
	$('#content').append(well);
	$('#caddb').click(function () {
	    var cnamei = $('#cnamei').val();
	    var cdesci = $('#cdesci').val();
	    renderLoadingGif();
    	    $.ajax({
		type: 'POST',
		url : server + '/commands'
	    }).done(function (data, textStatus, request) {
    		$.ajax({
		    type: 'PUT',
		    url : server + request.getResponseHeader('Location'),
		    data : JSON.stringify({
		        name : cnamei,
		        description : cdesci
		    })
		}).done(function () {
		    renderCommands();
    		}).fail(function () {
    		    $.ajax({
			type: 'DELETE',
			url : server + request.getResponseHeader('Location')
		    });
		    renderError('Can not add given command');
		});
    	    }).fail(function (jqXHR, textStatus,errorThrown) {
		renderError('fail: '+textStatus+', '+errorThrown);
	    });
	});
    }).fail(function (jqXHR, textStatus,errorThrown) {
	renderError('fail: '+textStatus+', '+errorThrown);
    });
}

function renderExamples () {
    renderLoadingGif();
    $.ajax({
	type: 'GET',
	url : server + '/examples'
    }).done(function (data) {
	$('#content').html('');
	var arr = JSON.parse(data);
	var table = '<table class="table table-striped table-hover ">' +
	    '<thead>' +
	    '<tr>' +
	    '<th>Example</th>' +
	    '<th class="text-center">Actions</th>' +
	    '</tr>' +
	    '</thead>' +
	    '<tbody>';
	for(i in arr) {
	    table += '<tr>';
	    table += '<td><a href="#" class="renderExample" x-id="' + arr[i]['_id'] + '">'+ arr[i]['example'] + '</a></td>';
	    table += '<td class="text-center"><button class="btn btn-danger btn-xs removeExample" x-id="' + arr[i]['_id'] + '">X</button></td>';
	    table += '</tr>';
	}
	table += '</tbody>' +
	    '</table>';
	$('#content').html(table);
	$('.renderExample').click(function () {
	    renderExample($(this).attr('x-id'));
	});
	$('.removeExample').click(function () {
	    $.ajax({
		type: 'DELETE',
		url : server + '/examples/' + $(this).attr('x-id')
	    }).fail(function (a,b,c) {
		renderExamples();
	    });
	});
	var well = '<hr>' +
	    '<div class="well">' + 
            '<h4>Add an example:</h4>' +
            '<div class="form-group">' +
            '<input type="text" id="examplei" class="form-control" placeholder="Example">' +
            '</div>' +
            '<div class="form-group">' +
            '<textarea class="form-control" id="edesci" rows="3" placeholder="Description"></textarea>' +
            '</div>' +
            '<button type="submit" id="eaddb" class="btn btn-success">Add</button>' +
            '</div>';
	$('#content').append(well);
	$('#eaddb').click(function () {
	    var cnamei = $('#examplei').val();
	    var cdesci = $('#edesci').val();
	    renderLoadingGif();
    	    $.ajax({
		type: 'POST',
		url : server + '/examples'
	    }).done(function (data, textStatus, request) {
    		$.ajax({
		    type: 'PUT',
		    url : server + request.getResponseHeader('Location'),
		    data : JSON.stringify({
		        example : cnamei,
		        description : cdesci
		    })
		}).done(function () {
		    // renderDialog('Success','Example has been added');
		    renderExamples();
    		}).fail(function (jqXHR, textStatus,errorThrown) {
		    renderError('fail: '+textStatus+', '+errorThrown);
		});
    	    }).fail(function (jqXHR, textStatus,errorThrown) {
		renderError('fail: '+textStatus+', '+errorThrown);
	    });
	});
    }).fail(function (jqXHR, textStatus,errorThrown) {
	renderError('fail: '+textStatus+', '+errorThrown);
    });
}

function renderCommand (id) {
    renderLoadingGif();
    $.ajax({
	type: 'GET',
	url : server + '/commands/' + id
    }).done(function (data) {
	var command = JSON.parse(data);
	$.ajax({
	    type: 'GET',
	    url : server + '/commands/' + id + '/examples'
	}).done(function (data) {
	    var examples = JSON.parse(data);
	    var jumbo = '<div class="jumbotron">' +
		'<h2>' + command['name'] + '</h2>' +
		'<p>' + command['description'] + '</p>' +
		'</div>';
	    var table = '<table class="table table-striped table-hover ">' +
		'<thead>' +
		'<tr>' +
		'<th>Example</th>' +
		'<th class="text-center">Score</th>' +
		'<th class="text-center">Actions</th>' +
		'</tr>' +
		'</thead>' +
		'<tbody>';
	    for(i in examples) {
		table += '<tr>';
		table += '<td><a href="#" class="renderExample" x-id="' + examples[i]['_id'] + '">'+ examples[i]['example'] + '</a></td>';
		table += '<td class="text-center">' + examples[i]['score'] + '</td>';
		table += '<td class="text-center">';
		table += '<button class="btn btn-primary btn-xs upVote" x-id="' + examples[i]['_id'] + '">+</button> ';
		table += '<button class="btn btn-primary btn-xs downVote" x-id="' + examples[i]['_id'] + '">-</button> ';
		table += '<button class="btn btn-danger btn-xs removeExample" x-id="' + examples[i]['_id'] + '">X</button>';
		table += '</td>';
		table += '</tr>';
	    }
	    table += '</tbody>' +
		'</table>';
	    $('#content').html(jumbo + table);
	    $('.renderExample').click(function () {
		renderExample($(this).attr('x-id'));
	    });
	    $('.upVote').click(function () {
		$.ajax({
		    type: 'POST',
		    url : server + '/examples/' + $(this).attr('x-id') + '/upvotes'
		}).done(function () {
		    renderCommand(id);
		});
	    });
	    $('.downVote').click(function () {
		$.ajax({
		    type: 'POST',
		    url : server + '/examples/' + $(this).attr('x-id') + '/downvotes'
		}).done(function () {
		    renderCommand(id);
		});
	    });
	    $('.removeExample').click(function () {
		$.ajax({
		    type: 'DELETE',
		    url : server + '/commands/' + id + '/examples/' + $(this).attr('x-id')
		}).fail(function () {
		    renderCommand(id);
		});
	    });
	});
    }).fail(function () {
	renderError('Given command does not exist');
    });
}

function renderExample (id) {
    renderLoadingGif();
    $.ajax({
	type: 'GET',
	url : server + '/examples/' + id
    }).done(function (data) {
	var example = JSON.parse(data);
	$.ajax({
	    type: 'GET',
	    url : server + '/examples/' + id + '/commands'
	}).done(function (data) {
	    var commands = JSON.parse(data);
	    var jumbo = '<div class="jumbotron">' +
		'<h2>' + example['example'] + '</h2>' +
		'<p>' + example['description'] + '</p>' +
		'</div>';
	    var table = '<table class="table table-striped table-hover ">' +
		'<thead>' +
		'<tr>' +
		'<th>Related command</th>' +
		'<th class="text-center">Actions</th>' +
		'</tr>' +
		'</thead>' +
		'<tbody>';
	    for(i in commands) {
		table += '<tr>';
		table += '<td><a href="#" class="renderCommand" x-id="' + commands[i]['_id'] + '">'+ commands[i]['name'] + '</a></td>';
		table += '<td class="text-center"><button class="btn btn-danger btn-xs removeCommand" x-id="' + commands[i]['_id'] + '">X</button></td>';
		table += '</tr>';
	    }
	    table += '</tbody>' +
		'</table>';
	    var well = '<hr>' +
		'<div class="well">' + 
		'<h4>Add relation:</h4>' +
		'<div class="form-group">' +
		'<input type="text" id="rcnamei" class="form-control" placeholder="Command name">' +
		'</div>' +
		'<button type="submit" id="raddb" class="btn btn-success">Add</button>' +
		'</div>';
	    $('#content').html(jumbo + table + well);
	    $('#raddb').click(function () {
		var rcnamei = $('#rcnamei').val();
		renderLoadingGif();
    		$.ajax({
		    type: 'POST',
		    url : server + '/examples/' + id + '/commands',
		    data : JSON.stringify({
		        command : rcnamei
		    })
		}).done(function () {
		    renderExample(id);
    		}).fail(function (jqXHR, textStatus,errorThrown) {
		    renderError('Given command does not exist');
		});
	    });
	    $('.renderCommand').click(function () {
		renderCommand($(this).attr('x-id'));
	    });
	    $('.removeCommand').click(function () {
		$.ajax({
		    type: 'DELETE',
		    url : server + '/examples/' + id + '/commands/' + $(this).attr('x-id')
		}).fail(function () {
		    renderExample(id);
		});
	    });
	});
    }).fail(function () {
	renderError('Can\'t fetch example');
    });
}

function renderDialog (title,message) {
    bootbox.dialog({
	message: message,
	title: title,
	buttons: {
	    main: {
		label: "OK",
		className: "btn-primary",
	    }
	}
    });
}

function renderError(message) {
    var error = '<div class="alert alert-danger text-center">' +
	'<h3>' + message + '</h3>' +
	'</div>';
    $('#content').html(error);
}