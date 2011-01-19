$(document).ready(function(){
	resultMap = {};
	initList = $('li');
	resultMap[''] = initList;
	$('input').keyup(function(){
		searchtext = $(this).val();
		if(resultMap[searchtext]==undefined)
		{
			$('li').remove();
			$('ul').after().html(resultMap['']);
			query = $("li:contains("+searchtext+")");
			$('li').remove();
			$('ul').after().html(query);
			resultMap[searchtext] = query;
		}
		else
		{
			$('li').remove();
			$('ul').after().html(resultMap[searchtext]);
		}
	});
});

/*

$(document).ready(function(){
	initList = $('li');
	$('input').keyup(function(){
		searchtext = $(this).val();
		$('li').remove();
		$('ul').after().html(initList);
		query = $("li:contains("+searchtext+")");
		$('li').remove();
		$('ul').after().html(query);
	});
});
*/
