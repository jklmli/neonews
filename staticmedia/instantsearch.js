$(document).ready(function(){
//USE KEYUP EVENTHANDLER INSTEAD!!!
	$('input').keypress(function(){
		searchtext = $(this).val();
		groups = $("a:contains("+searchtext+")");
		console.log(groups);
	});
});
