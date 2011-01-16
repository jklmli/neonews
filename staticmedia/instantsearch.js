$(document).ready(function(){
	groups = $('li');
//Keyup fixes the issues of backspace
	$('input').keyup(function(){
		searchtext = $(this).val();
		$('li').remove();
		$('ul').after().html(groups);
		groupquery = $("li:contains("+searchtext+")");
		$('li').remove();
		$('ul').after().html(groupquery);
	});
});
