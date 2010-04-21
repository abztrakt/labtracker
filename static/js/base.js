$(function () {
	$('#fast-search #search_term').focus(function (eve) {
		// highlight the inner text
		eve.target.select();
	});

	
    $('li.view-issues').hover(function(){
        $(this).addClass("hover");
        $('ul:first',this).css('visibility','visible');
    },function(){

        $(this).removeClass("hover");
        $('ul:first',this).css('visibility','hidden');
    });
});
