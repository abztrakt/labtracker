$(function () {
	$('#fast-search #search_term').focus(function (eve) {
		// highlight the inner text
		eve.target.select();
	});

	$('#nav').droppy();
});
