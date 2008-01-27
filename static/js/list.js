$(document).ready(function () {
	//$.tablesorter.defaults.widgets = ['zebra'];
	$.tablesorter.addParser(django_date_parser);
		
	$('#issue_results').tablesorter({
			'headers':	{
				8:	{ 'sorter': 'django_date' },
				9:	{ 'sorter': 'django_date' }
			}
		});
});
